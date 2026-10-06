"""
Verificacoes da banca (metodologia) sobre o piloto D023 -- SOMENTE LEITURA.

Importa os modulos de experimentos/piloto sem altera-los e verifica:
  1. propriedade de eficiencia do Shapley (soma phi = L(x) - L(ref));
  2. plausibilidade fisiologica das vinhetas (LDL-c <= nao-HDL-c);
  3. distribuicao de categorias e quantas vem do escore x de regras;
  4. quantas vinhetas sao "armadilha" pelos criterios declarados em vinhetas.py;
  5. formato decimal misto no prompt;
  6. se a regra de decisao de resumir.py usa a unidade de analise que ela declara.

Uso: python3 v1_verificar_piloto.py   (Python 3.8, sem dependencias)
"""
import csv
import io
import math
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
PILOTO = RAIZ / "experimentos" / "piloto"
sys.path.insert(0, str(PILOTO))

import gabarito  # noqa: E402
import prevent  # noqa: E402
import prompt  # noqa: E402
import vinhetas  # noqa: E402

print("=" * 72)
print("1) Eficiencia do Shapley: soma(phi) == L(x) - L(ref)")
maxdif = 0.0
for v in vinhetas.todas():
    p = v["paciente"]
    x = prevent._para_modelo(p)
    ref = dict(prevent.REFERENCIA)
    ref["imc"] = x["imc"]
    L = prevent.log_odds(x, p["sexo"])
    L0 = prevent.log_odds(ref, p["sexo"])
    s = sum(prevent.shapley(p).values())
    maxdif = max(maxdif, abs(s - (L - L0)))
print("   maior |soma(phi) - (L - L_ref)| nas 24 vinhetas = %.2e  -> %s" % (maxdif, "OK" if maxdif < 1e-9 else "FALHA"))

print("=" * 72)
print("2) Plausibilidade: LDL-c nao pode exceder nao-HDL-c (nao-HDL = LDL + VLDL)")
for v in vinhetas.todas():
    p = v["paciente"]
    if p.get("ldl") is not None:
        nhdl = p["colesterol_total"] - p["hdl"]
        st = "IMPOSSIVEL" if p["ldl"] > nhdl else "ok"
        print("   %s  CT=%d HDL=%d -> nao-HDL=%d ; LDL informado=%d  -> %s" % (
            v["id"], p["colesterol_total"], p["hdl"], nhdl, p["ldl"], st))

print("=" * 72)
print("3) Categorias e origem (escore puro x regra de agravante/LDL)")
cont = {}
por_regra = 0
riscos = []
for v in vinhetas.todas():
    g = gabarito.montar(v)
    cont[g["categoria"]] = cont.get(g["categoria"], 0) + 1
    riscos.append(g["risco_pct"])
    if len(g["regras_aplicadas"]) > 1:
        por_regra += 1
print("   categorias:", cont)
print("   vinhetas cuja categoria foi alterada por regra (agravante/LDL): %d/24" % por_regra)
print("   vinhetas com risco PREVENT >= 20%%: %d/24 ; < 5%%: %d/24" % (
    sum(r >= 20 for r in riscos), sum(r < 5 for r in riscos)))

print("=" * 72)
print("4) Vinhetas 'armadilha' segundo os criterios declarados em vinhetas.py (docstring)")
flags_total = 0
for v in vinhetas.todas():
    p = v["paciente"]
    g = gabarito.montar(v)
    f = []
    if p.get("imc", 25) >= 30:
        f.append("IMC>=30")
    if p.get("anti_hipertensivo"):
        f.append("anti-HAS")
    if p["idade"] < 55:
        f.append("idade<55")
    if p.get("agravantes") or p.get("ldl") is not None:
        f.append("reclassif.")
    if abs(g["risco_pct"] - 5) <= 0.5:
        f.append("perto de 5%")
    flags_total += bool(f)
    print("   %s %-50s %s" % (v["id"], v["objetivo"][:50], ",".join(f) or "-"))
print("   -> %d/24 vinhetas tem ao menos um gatilho de erro declarado" % flags_total)

print("=" * 72)
print("5) Formato decimal no prompt (virgula x ponto)")
txt = prompt.construir(gabarito.montar(vinhetas.todas()[0]))
virg = re.findall(r"\d+,\d+", txt)
pont = re.findall(r"-?\d+\.\d+", txt)
print("   numeros com virgula:", virg[:5], " | com ponto:", pont[:5])

print("=" * 72)
print("6) resumir.py: unidade declarada (vinheta) x unidade usada na regra (resposta)")
linhas = []
# 24 vinhetas x 3 repeticoes; 7 vinhetas com 1 erro em 3 repeticoes
for i in range(1, 25):
    for rep in (1, 2, 3):
        fiel = "N" if (i <= 7 and rep == 1) else "S"
        linhas.append({"modelo": "sim", "vinheta": "V%02d" % i, "H_totalmente_fiel(S/N)": fiel})
tmp = Path(tempfile.mkdtemp()) / "sim_anotacao.csv"
with tmp.open("w", encoding="utf-8-sig", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(linhas[0].keys()), delimiter=";")
    w.writeheader()
    w.writerows(linhas)
out = subprocess.run([sys.executable, str(PILOTO / "resumir.py"), str(tmp)], capture_output=True, text=True)
print("   cenario: 7 de 24 vinhetas (29%) com erro em 1 de 3 repeticoes")
for l in out.stdout.strip().splitlines():
    print("   " + l)
