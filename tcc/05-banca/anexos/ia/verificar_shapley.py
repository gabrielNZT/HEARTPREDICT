"""
Verificação independente da função prevent.shapley (parecer da banca, IA/XAI).
Não modifica o projeto: importa experimentos/piloto em modo somente leitura.

Checagens:
 1. Eficiência: soma(phi) = L(x) - L(ref) nas 24 vinhetas.
 2. Implementação independente A: média sobre TODAS as 9! permutações (fórmula por ordens de chegada).
 3. Implementação independente B: forma fechada para modelo aditivo + interações de pares
    (phi_i = efeito principal_i + 1/2 * soma das interações que envolvem i).
 4. Implementação independente C: shap.KernelExplainer / shap.explainers.Exact com fundo = paciente de referência.
 5. Axiomas no algoritmo (jogo sintético via monkeypatch): simetria, jogador nulo, linearidade.
 6. Sensibilidade: escala de probabilidade; referência alternativa; atribuição alternativa das interações.
Uso: <python> verificar_shapley.py
"""
import itertools
import json
import math
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "experimentos" / "piloto"))
import numpy as np  # noqa: E402
import prevent  # noqa: E402
import vinhetas  # noqa: E402

VAR = prevent.VARIAVEIS
N = len(VAR)
VS = vinhetas.todas()
saida = {}


def L_de(z, sexo):
    return prevent.log_odds(z, sexo)


def ponto(p):
    return prevent._para_modelo(p)


def coal_val(x, sexo, S, ref=None, f=None):
    z = dict(ref or prevent.REFERENCIA)
    z["imc"] = x["imc"]
    for i in S:
        z[VAR[i]] = x[VAR[i]]
    return (f or L_de)(z, sexo)


# ---------- 1 e 2: eficiência e permutações ----------
def shapley_permutacoes(x, sexo, ref=None, f=None):
    cache = {}

    def v(S):
        k = frozenset(S)
        if k not in cache:
            cache[k] = coal_val(x, sexo, k, ref, f)
        return cache[k]
    phi = np.zeros(N)
    nperm = 0
    for perm in itertools.permutations(range(N)):
        S = set()
        prev = v(S)
        for i in perm:
            S.add(i)
            cur = v(S)
            phi[i] += cur - prev
            prev = cur
        nperm += 1
    return dict(zip(VAR, phi / nperm))


# ---------- 3: forma fechada ----------
def shapley_fechado(x, sexo):
    ref = dict(prevent.REFERENCIA, imc=x["imc"])
    c = prevent._coluna(sexo, "ascvd")
    tx = prevent._termos(dict(ref, **{k: x[k] for k in VAR}))
    # termos individuais em cada variável (valor centrado)
    t = {}
    z = dict(ref)
    for k in VAR:
        zz = dict(ref)
        zz[k] = x[k]
        t[k] = prevent._termos(zz)
    nomes = prevent._COEF["termos"]
    idx = {n: i for i, n in enumerate(nomes)}
    phi = {k: 0.0 for k in VAR}
    # efeitos principais: termo i depende de uma variável
    main = {"idade": ["idade"], "nao_hdl": ["nao_hdl"], "hdl": ["hdl"], "pas": ["pas_lt_110", "pas_gte_110"],
            "diabetes": ["diabetes"], "tabagismo": ["tabagismo"], "tfge": ["tfge_lt_60", "tfge_gte_60"],
            "anti_hipertensivo": ["anti_hipertensivo"], "estatina": ["estatina"]}
    for k, termos in main.items():
        for n in termos:
            phi[k] += c[idx[n]] * tx[idx[n]]
    pares = {"anti_hipertensivo_x_pas_gte_110": ("anti_hipertensivo", "pas"),
             "estatina_x_nao_hdl": ("estatina", "nao_hdl"), "idade_x_nao_hdl": ("idade", "nao_hdl"),
             "idade_x_hdl": ("idade", "hdl"), "idade_x_pas_gte_110": ("idade", "pas"),
             "idade_x_diabetes": ("idade", "diabetes"), "idade_x_tabagismo": ("idade", "tabagismo"),
             "idade_x_tfge_lt_60": ("idade", "tfge")}
    for n, (a, b) in pares.items():
        val = c[idx[n]] * tx[idx[n]]
        phi[a] += val / 2
        phi[b] += val / 2
    # idade x IMC>=30: coeficiente 0 no modelo DCVA (conferido abaixo)
    assert c[idx["idade_x_imc_gte_30"]] == 0.0
    return phi, {n: c[idx[n]] * tx[idx[n]] for n in pares}


res_eq = []
max_err_perm = max_err_fech = max_err_eff = 0.0
for vv in VS:
    p = vv["paciente"]
    x = ponto(p)
    phi = prevent.shapley(p)
    Lx = L_de(dict(x), p["sexo"])
    L0 = coal_val(x, p["sexo"], [])
    max_err_eff = max(max_err_eff, abs(sum(phi.values()) - (Lx - L0)))
    phip = shapley_permutacoes(x, p["sexo"])
    max_err_perm = max(max_err_perm, max(abs(phi[k] - phip[k]) for k in VAR))
    phif, _ = shapley_fechado(x, p["sexo"])
    max_err_fech = max(max_err_fech, max(abs(phi[k] - phif[k]) for k in VAR))
saida["eficiencia_max_erro"] = max_err_eff
saida["permutacoes_max_dif"] = max_err_perm
saida["forma_fechada_max_dif"] = max_err_fech

# ---------- 4: shap ----------
try:
    import shap
    feats = VAR

    def f_vec(X, sexo, imc):
        out = []
        for row in X:
            z = dict(zip(feats, row))
            z["imc"] = imc
            out.append(L_de(z, sexo))
        return np.array(out)
    max_err_shap = 0.0
    max_err_exact = 0.0
    for vv in VS:
        p = vv["paciente"]
        x = ponto(p)
        bg = np.array([[prevent.REFERENCIA[k] for k in feats]])
        xv = np.array([[x[k] for k in feats]])
        fn = lambda X, s=p["sexo"], m=x["imc"]: f_vec(X, s, m)
        ke = shap.KernelExplainer(fn, bg)
        sv = ke.shap_values(xv, nsamples=2 ** N + 10, silent=True)[0]
        phi = prevent.shapley(p)
        max_err_shap = max(max_err_shap, max(abs(phi[k] - sv[i]) for i, k in enumerate(feats)))
        ex = shap.explainers.Exact(fn, shap.maskers.Independent(bg, max_samples=1))
        se = ex(xv).values[0]
        max_err_exact = max(max_err_exact, max(abs(phi[k] - se[i]) for i, k in enumerate(feats)))
    saida["shap_versao"] = shap.__version__
    saida["shap_kernel_max_dif"] = max_err_shap
    saida["shap_exact_max_dif"] = max_err_exact
except Exception as e:  # pragma: no cover
    saida["shap_erro"] = repr(e)

# ---------- 5: axiomas no algoritmo (jogo sintético) ----------
orig = prevent.log_odds
try:
    # simetria: idade e pas entram de forma idêntica; jogador nulo: estatina não entra
    def jogo_sim(z, sexo, desfecho="ascvd"):
        a = 1.0 if z["idade"] != prevent.REFERENCIA["idade"] else 0.0
        b = 1.0 if z["pas"] != prevent.REFERENCIA["pas"] else 0.0
        c = 1.0 if z["hdl"] != prevent.REFERENCIA["hdl"] else 0.0
        return 3 * a + 3 * b + 2 * a * b + 5 * a * b * c + 0.7 * c
    prevent.log_odds = jogo_sim
    p = dict(VS[0]["paciente"], estatina=1)
    phi = prevent.shapley(p)
    saida["simetria_idade_vs_pas"] = (phi["idade"], phi["pas"])
    saida["jogador_nulo_estatina"] = phi["estatina"]
    saida["eficiencia_jogo_sintetico"] = (sum(phi.values()), 3 + 3 + 2 + 5 + 0.7)

    # linearidade: phi(g1+g2) = phi(g1)+phi(g2)
    def g1(z, s, d="ascvd"):
        return (z["idade"] - 55) * (z["pas"] - 130) / 100.0

    def g2(z, s, d="ascvd"):
        return (z["hdl"] - 50.271) ** 2 / 100.0 * (1 if z["tabagismo"] else 0.3)
    prevent.log_odds = g1
    a = prevent.shapley(p)
    prevent.log_odds = g2
    b = prevent.shapley(p)
    prevent.log_odds = lambda z, s, d="ascvd": g1(z, s) + g2(z, s)
    ab = prevent.shapley(p)
    saida["linearidade_max_dif"] = max(abs(ab[k] - a[k] - b[k]) for k in VAR)
finally:
    prevent.log_odds = orig

# ---------- 6: sensibilidade ----------
def eps_sign(phi, frac=0.05):
    s = sum(abs(v) for v in phi.values())
    return {k: (0 if abs(v) < frac * s else (1 if v > 0 else -1)) for k, v in phi.items()}


def rank(phi, k=3):
    return [a for a, b in sorted(phi.items(), key=lambda kv: -abs(kv[1])) if abs(b) > 1e-9][:k]


def prob(z, sexo, desfecho="ascvd"):
    return 1 / (1 + math.exp(-orig(z, sexo)))


# referência alternativa ilustrativa (aprox. de médias populacionais de adultos dos EUA 40-79a sem DCV; NÃO é o NHANES
# processado pelo projeto — serve só para mostrar a magnitude da dependência da referência)
REF_ALT = {"idade": 55.0, "nao_hdl": 145.0, "hdl": 52.0, "pas": 124.0, "anti_hipertensivo": 0.3,
           "estatina": 0.2, "diabetes": 0.1, "tabagismo": 0.15, "tfge": 90.0, "imc": 25.0}
# Observação: binárias com valor fracionário = "paciente médio" (baseline Shapley com média). Em log-odds,
# o modelo é linear nos termos binários, portanto isso é bem definido.

linhas = []
tot = {"prob_sinal": 0, "prob_top3": 0, "alt_sinal": 0, "alt_top3": 0, "inter_sinal": 0, "inter_top3": 0,
       "n_var_nz": 0}
for vv in VS:
    p = vv["paciente"]
    x = ponto(p)
    base = prevent.shapley(p)
    sb = eps_sign(base)
    # (a) escala de probabilidade (mesma referência)
    pp = shapley_permutacoes(x, p["sexo"], f=prob)
    sp = eps_sign(pp)
    # (b) referência alternativa
    pa = shapley_permutacoes(x, p["sexo"], ref=REF_ALT)
    sa = eps_sign(pa)
    # (c) interações com a idade atribuídas 100% ao fator (não à idade): alternativa "fator-cêntrica"
    phif, inter = shapley_fechado(x, p["sexo"])
    pi = dict(phif)
    for n, val in inter.items():
        if n.startswith("idade_x_"):
            outra = {"idade_x_nao_hdl": "nao_hdl", "idade_x_hdl": "hdl", "idade_x_pas_gte_110": "pas",
                     "idade_x_diabetes": "diabetes", "idade_x_tabagismo": "tabagismo",
                     "idade_x_tfge_lt_60": "tfge"}[n]
            pi["idade"] -= val / 2
            pi[outra] += val / 2
    si = eps_sign(pi)
    d = {"id": vv["id"], "risco_pct": round(prevent.risco(p) * 100, 1),
         "sinais_base": {k: sb[k] for k in VAR if sb[k] != 0},
         "flip_prob": [k for k in VAR if sb[k] != sp[k]],
         "flip_ref_alt": [k for k in VAR if sb[k] != sa[k]],
         "flip_interacao_ao_fator": [k for k in VAR if sb[k] != si[k]],
         "top3_base": rank(base), "top3_prob": rank(pp), "top3_ref_alt": rank(pa), "top3_inter": rank(pi),
         "phi_base": {k: round(v, 4) for k, v in base.items()},
         "phi_ref_alt": {k: round(v, 4) for k, v in pa.items()},
         "phi_inter_ao_fator": {k: round(v, 4) for k, v in pi.items()}}
    linhas.append(d)
    tot["prob_sinal"] += bool(d["flip_prob"])
    tot["alt_sinal"] += bool(d["flip_ref_alt"])
    tot["inter_sinal"] += bool(d["flip_interacao_ao_fator"])
    tot["prob_top3"] += d["top3_prob"] != d["top3_base"]
    tot["alt_top3"] += d["top3_ref_alt"] != d["top3_base"]
    tot["inter_top3"] += d["top3_inter"] != d["top3_base"]
saida["sensibilidade_resumo_(n_vinhetas_com_mudanca_de_24)"] = tot
saida["por_vinheta"] = linhas

# sensibilidade do limiar epsilon: nº de (vinheta, variável) cuja classe muda entre eps
for fr in (0.0, 0.02, 0.05, 0.10):
    n_desp = 0
    for vv in VS:
        phi = prevent.shapley(vv["paciente"])
        s = sum(abs(v) for v in phi.values())
        n_desp += sum(1 for v in phi.values() if abs(v) > 1e-12 and abs(v) < fr * s)
    saida["eps_%.2f_pares_variavel_desprezivel" % fr] = n_desp

out = Path(__file__).with_name("resultado_verificar_shapley.json")
out.write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
for k, v in saida.items():
    if k != "por_vinheta":
        print(k, "=", v)
for d in linhas:
    if d["flip_prob"] or d["flip_ref_alt"] or d["flip_interacao_ao_fator"]:
        print(d["id"], d["risco_pct"], "flip_prob", d["flip_prob"], "| flip_ref", d["flip_ref_alt"],
              "| flip_inter", d["flip_interacao_ao_fator"], "| top3", d["top3_base"], d["top3_ref_alt"])
