"""Verificações clínicas independentes (parecer de cardiologia). Não altera o projeto; só lê os módulos."""
import json, math, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "experimentos" / "piloto"))
import prevent, sbc, renal, vinhetas, gabarito

C = json.loads((RAIZ / "experimentos/piloto/coeficientes_prevent_base_10a.json").read_text())

def risco_indep(idade, sexo, ct, hdl, pas, trat, est, dm, fumo, tfge):
    """Reimplementação independente, escrita a partir da Tabela S12 (forma) sem usar prevent._termos."""
    m = 38.67
    nh = (ct - hdl) / m - 3.5
    h = (hdl / m - 1.3) / 0.3
    a = (idade - 55) / 10
    s1 = (min(pas, 110) - 110) / 20
    s2 = (max(pas, 110) - 130) / 20
    e1 = (min(tfge, 60) - 60) / -15
    e2 = (max(tfge, 60) - 90) / -15
    b = C[("female_" if sexo == "f" else "male_") + "ascvd"]
    x = [a, nh, h, s1, s2, dm, fumo, 0, 0, e1, e2, trat, est, trat*s2, est*nh,
         a*nh, a*h, a*s2, a*dm, a*fumo, 0, a*e1, 1]
    L = sum(bi*xi for bi, xi in zip(b, x))
    return 100 / (1 + math.exp(-L))

print("== 1. Caso publicado (Khan 2024) e reimplementação independente ==")
print("F50 CT240 HDL55 PAS160 trat, não fumante: %.2f%% (publicado 3,6%%)" % risco_indep(50,"f",240,55,160,1,0,0,0,90))
print("idem fumante: %.2f%% (publicado 6,0%%)" % risco_indep(50,"f",240,55,160,1,0,0,1,90))

print("\n== 2. Vinhetas: projeto x reimplementação ==")
maxdif = 0
for v in vinhetas.todas():
    p = v["paciente"]
    r1 = prevent.risco(p)*100
    r2 = risco_indep(p["idade"], "f" if p["sexo"]=="feminino" else "m", p["colesterol_total"], p["hdl"], p["pas"],
                     p["anti_hipertensivo"], p["estatina"], p["diabetes"], p["tabagismo"], p["tfge"])
    maxdif = max(maxdif, abs(r1-r2))
    g = gabarito.montar(v)
    print("%s %-45s risco=%5.2f%% cat=%-13s regras=%s" % (v["id"], v["objetivo"][:45], r1, g["categoria"], " | ".join(g["regras_aplicadas"][1:]) or "-"))
print("maior diferença absoluta projeto x independente: %.2e pontos percentuais" % maxdif)

print("\n== 3. Sinal da atribuição da ESTATINA (varredura) ==")
base = dict(idade=55, sexo="masculino", colesterol_total=200, hdl=45, pas=130, anti_hipertensivo=0,
            estatina=1, diabetes=0, tabagismo=0, tfge=90, agravantes=[])
for sexo in ("feminino","masculino"):
    for idade in (40, 55, 70):
        linha = []
        for ct in (160, 200, 240, 280, 320):
            p = dict(base, sexo=sexo, idade=idade, colesterol_total=ct)
            phi = prevent.shapley(p)["estatina"]
            linha.append("CT%d(nHDL%d):%+.3f" % (ct, ct-45, phi))
        print(sexo, idade, " ".join(linha))

print("\n== 4. Sinal da atribuição do ANTI-HIPERTENSIVO ==")
for sexo in ("feminino","masculino"):
    for pas in (110, 120, 130, 150, 180):
        p = dict(base, sexo=sexo, estatina=0, anti_hipertensivo=1, pas=pas)
        print(sexo, "PAS", pas, "phi_anti=%+.3f" % prevent.shapley(p)["anti_hipertensivo"], "phi_pas=%+.3f" % prevent.shapley(p)["pas"])

print("\n== 5. Efeito do tratamento dentro do modelo (mesma PAS/não-HDL, com x sem remédio) ==")
for sexo in ("feminino","masculino"):
    p0 = dict(base, sexo=sexo, estatina=0, colesterol_total=240, pas=140)
    print(sexo, "sem remédio %.2f%%; com anti-HAS %.2f%%; com estatina %.2f%%" % (
        prevent.risco(p0)*100, prevent.risco(dict(p0, anti_hipertensivo=1))*100, prevent.risco(dict(p0, estatina=1))*100))

print("\n== 6. CKD-EPI 2021 (Inker 2021) ==")
def ckd(cr, idade, fem):
    k = 0.7 if fem else 0.9; a = -0.241 if fem else -0.302
    return 142*min(cr/k,1)**a*max(cr/k,1)**-1.200*0.9938**idade*(1.012 if fem else 1)
for cr, idade, sexo in [(0.7,50,"feminino"),(0.9,50,"masculino"),(1.0,60,"feminino"),(1.2,60,"masculino"),(2.0,70,"masculino"),(0.5,30,"masculino"),(0.4,30,"feminino"),(0.3,30,"feminino"),(0.6,35,"masculino")]:
    t = renal.tfge_ckd_epi_2021(cr, idade, sexo)
    ok = "OK" if 15 <= t <= 140 else "RECUSADO pelo PREVENT (fora de 15-140)"
    print("Cr %.1f %d %s -> projeto %d | indep %.1f  %s" % (cr, idade, sexo, t, ckd(cr, idade, sexo=="feminino"), ok))

print("\n== 7. Arredondamento: frequência natural x categoria ==")
for pct in (4.5, 4.6, 4.9, 19.5, 19.9):
    cat = "baixo" if pct < 5 else "intermediário" if pct < 20 else "alto"
    print("risco %.1f%% -> em_100_pessoas=%d, categoria=%s" % (pct, round(pct), cat))

print("\n== 8. Regras SBC: casos de fronteira ==")
casos = [
    ("escore<5 + LDL 170 + agravante", 0.03, dict(ldl=170, agravantes=["historia_familiar_prematura"])),
    ("escore 10 + LDL 170", 0.10, dict(ldl=170)),
    ("escore<5 + Lp(a)>=50 (sem valor)", 0.03, dict(agravantes=["lpa_elevada"])),
    ("escore<5 + 3 agravantes", 0.02, dict(agravantes=["historia_familiar_prematura","sindrome_metabolica","pcr_us_elevada"])),
    ("escore<5, LDL não informado", 0.02, dict()),
    ("escore 12 + LDL 189,5", 0.12, dict(ldl=189.5)),
]
for nome, r, extra in casos:
    p = dict(dict(diabetes=0, agravantes=[]), **extra)
    print("%-40s -> %s  %s" % (nome, *sbc.categoria(r, p)))

print("\n== 9. Saída do endpoint (mesma lógica de backend-gateway/app/avaliacao.py::_resultado) para usuários de estatina ==")
sys.path.insert(0, str(RAIZ / "backend-gateway"))
try:
    from app import avaliacao
    exemplos = [
        ("M 62, estatina, CT 280 HDL 42 (não-HDL 238), PAS 128", dict(idade=62, sexo="masculino", colesterol_total=280, hdl=42, pas=128, anti_hipertensivo=0, estatina=1, diabetes=0, tabagismo=0, tfge=85, agravantes=[])),
        ("F 58, estatina+anti-HAS, CT 290 HDL 50, PAS 124", dict(idade=58, sexo="feminino", colesterol_total=290, hdl=50, pas=124, anti_hipertensivo=1, estatina=1, diabetes=0, tabagismo=0, tfge=90, agravantes=[])),
        ("F 45, anti-HAS, PAS 118 (bem controlada)", dict(idade=45, sexo="feminino", colesterol_total=190, hdl=55, pas=118, anti_hipertensivo=1, estatina=0, diabetes=0, tabagismo=0, tfge=95, agravantes=[])),
    ]
    for nome, p in exemplos:
        r = avaliacao._resultado(p, "informada")
        print(nome, "-> risco %.1f%%, cat %s" % (r["risco_pct"], r["categoria"]))
        for f_ in r["fatores"]:
            print("    %-28s %+.3f  %s" % (f_["nome"], f_["contribuicao"], f_["direcao"]))
except Exception as ex:
    print("gateway indisponível neste Python:", ex)
