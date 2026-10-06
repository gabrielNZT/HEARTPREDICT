"""
Calculo de poder ILUSTRATIVO para o desfecho principal de H2 (explicacao "totalmente fiel",
comparacao pareada C-ferramenta x C-verificador na mesma vinheta, teste de McNemar).

Modelo dos cenarios (parametros plausiveis, NAO estimados -- o piloto ainda nao rodou):
  pA = proporcao de vinhetas NAO totalmente fieis em C-ferramenta
  r  = fracao dessas falhas que o verificador detecta E o ciclo corrige  (depende de B1/B6)
  q  = fracao das vinhetas fieis em C-ferramenta que ficam infieis em C-verificador
       (erro novo introduzido na reescrita, ou bloqueio contado como falha, ou variacao estocastica)
  p10 = pA * r        (falha em A, fiel em B)   -- pares discordantes a favor do verificador
  p01 = (1 - pA) * q  (fiel em A, falha em B)
Formula: Connor (1987), Biometrics 43:207-211 (aproximacao normal para McNemar).
Conferencia por simulacao Monte Carlo com o teste mid-p (Fagerland et al., 2013).

Tambem calcula:
  (b) curva operacional da regra de decisao do piloto (limiar 10%, 24 vinhetas x 3 repeticoes),
      com e sem correlacao intra-vinheta (beta-binomial);
  (c) vies da taxa do piloto por enriquecimento de armadilhas;
  (d) n para H3 (evento raro: atribuir risco a raca/etnia);
  (e) carga de anotacao do nucleo;
  (f) precisao do kappa com n anotado.
Uso: <venv>/bin/python v2_poder_mcnemar.py  (numpy, scipy, matplotlib)
"""
import math
from pathlib import Path

import numpy as np
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

AQUI = Path(__file__).parent
RNG = np.random.default_rng(20260929)


def n_connor(p10, p01, alpha=0.05, poder=0.80):
    psi = p10 + p01
    d = p10 - p01
    if d <= 0:
        return float("inf")
    za = stats.norm.ppf(1 - alpha / 2)
    zb = stats.norm.ppf(poder)
    return math.ceil((za * math.sqrt(psi) + zb * math.sqrt(psi - d * d)) ** 2 / (d * d))


def midp_mcnemar(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = 2 * stats.binom.cdf(k, n, 0.5) - stats.binom.pmf(k, n, 0.5)
    return min(1.0, p)


def poder_sim(n, p10, p01, alpha=0.05, reps=4000):
    probs = [p10, p01, 1 - p10 - p01]
    x = RNG.multinomial(n, probs, size=reps)
    ok = sum(midp_mcnemar(b, c) < alpha for b, c, _ in x)
    return ok / reps


linhas = []
print("=" * 90)
print("(a) n de VINHETAS (pares) para McNemar, poder 80%")
print("    alpha=0,05 (1 contraste) | alpha=0,025 (Bonferroni: 1 contraste x 2 LLMs) | alpha=0,0083 (3 pares x 2 LLMs)")
print("%-5s %-5s %-5s %-6s %-6s | %8s %8s %8s | poder simulado (mid-p, alpha=0,025) no n Bonferroni" % (
    "pA", "r", "q", "p10", "p01", "a=.05", "a=.025", "a=.0083"))
cenarios = []
for pA in (0.10, 0.20, 0.30, 0.50):
    for r in (0.3, 0.5, 0.8):
        for q in (0.01, 0.03, 0.05):
            p10, p01 = pA * r, (1 - pA) * q
            n1 = n_connor(p10, p01, 0.05)
            n2 = n_connor(p10, p01, 0.025)
            n3 = n_connor(p10, p01, 0.05 / 6)
            cenarios.append((pA, r, q, p10, p01, n1, n2, n3))
for pA, r, q, p10, p01, n1, n2, n3 in cenarios:
    sim = ""
    if n2 != float("inf") and n2 <= 3000 and q in (0.01, 0.03) and r in (0.5, 0.8):
        sim = "%.2f" % poder_sim(n2, p10, p01, 0.025)
    fmt = lambda n: ("%8d" % n) if n != float("inf") else "     inf"
    print("%-5.2f %-5.1f %-5.2f %-6.3f %-6.3f | %s %s %s | %s" % (pA, r, q, p10, p01, fmt(n1), fmt(n2), fmt(n3), sim))

# Figura 1: n (alpha=0,025) x pA, para r in {0.3,0.5,0.8}, q=0,03
fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=150)
cores = {0.3: "#2a78d6", 0.5: "#eb6834", 0.8: "#1baf7a"}
pAs = np.linspace(0.06, 0.6, 60)
for r in (0.3, 0.5, 0.8):
    ns = [n_connor(p * r, (1 - p) * 0.03, 0.025) for p in pAs]
    ns = [n if n != float("inf") else np.nan for n in ns]
    ax.plot(pAs * 100, ns, color=cores[r], lw=2, label="verificador corrige %d%% das falhas" % (r * 100))
    ax.annotate("r = %.1f" % r, xy=(pAs[-1] * 100, ns[-1]), xytext=(4, 0), textcoords="offset points",
                color="#52514e", fontsize=8, va="center")
ax.axhline(24, color="#52514e", lw=1, ls=":")
ax.text(11, 25, "24 vinhetas (piloto)", fontsize=8, color="#52514e", va="bottom", ha="left")
ax.set_yscale("log")
ax.set_xlabel("Vinhetas NÃO totalmente fiéis em C-ferramenta (pA, %)", color="#0b0b0b")
ax.set_ylabel("Vinhetas necessárias (log)", color="#0b0b0b")
ax.set_title("McNemar, poder 80%, α = 0,025 (2 LLMs), q = 3% de erros novos", fontsize=10, color="#0b0b0b", loc="left")
ax.grid(True, which="major", color="#e5e4df", lw=0.6)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=8)
ax.set_facecolor("#fcfcfb")
fig.patch.set_facecolor("#fcfcfb")
fig.tight_layout()
fig.savefig(AQUI / "fig1_n_mcnemar.png")

print()
print("=" * 90)
print("(b) Curva operacional da regra do piloto: P('SEGUE') = P(taxa por resposta >= 10%)")
print("    24 vinhetas x 3 repeticoes = 72 respostas; ICC = correlacao intra-vinheta (beta-binomial)")


def p_segue(p, icc, reps=20000, nv=24, m=3, limiar=0.10):
    if icc == 0:
        k = RNG.binomial(nv * m, p, size=reps)
    else:
        a = p * (1 - icc) / icc
        b = (1 - p) * (1 - icc) / icc
        pv = RNG.beta(a, b, size=(reps, nv))
        k = RNG.binomial(m, pv).sum(axis=1)
    return np.mean(k / (nv * m) >= limiar - 1e-12)


ps = [0.03, 0.05, 0.075, 0.10, 0.125, 0.15, 0.20, 0.25]
print("%-8s %10s %10s %10s" % ("p real", "ICC=0", "ICC=0,3", "ICC=0,6"))
curvas = {}
for icc in (0, 0.3, 0.6):
    curvas[icc] = [p_segue(p, icc) for p in ps]
for i, p in enumerate(ps):
    print("%-8.3f %10.2f %10.2f %10.2f" % (p, curvas[0][i], curvas[0.3][i], curvas[0.6][i]))
n_eff = 72 / (1 + 2 * 0.3)
print("    n efetivo com ICC=0,3: 72/(1+(3-1)*0,3) = %.0f respostas" % n_eff)
lo, hi = stats.binom.interval(0.95, 72, 0.10)
print("    IC95% (Wilson) para 7/72: ", end="")
k, n = 7, 72
z = 1.96
c = (k / n + z * z / (2 * n)) / (1 + z * z / n)
h = z * math.sqrt(k / n * (1 - k / n) / n + z * z / (4 * n * n)) / (1 + z * z / n)
print("%.1f%% a %.1f%%" % (100 * (c - h), 100 * (c + h)))

fig, ax = plt.subplots(figsize=(7.2, 4.0), dpi=150)
for icc, cor in ((0, "#2a78d6"), (0.3, "#eb6834"), (0.6, "#1baf7a")):
    ax.plot(np.array(ps) * 100, curvas[icc], color=cor, lw=2, marker="o", ms=4, label="ICC intra-vinheta = %.1f" % icc)
ax.axvline(10, color="#52514e", lw=1, ls=":")
ax.text(10.3, 0.05, "limiar 10%", fontsize=8, color="#52514e")
ax.set_xlabel("Taxa real de respostas com erro (%)", color="#0b0b0b")
ax.set_ylabel("P(regra diz 'SEGUE')", color="#0b0b0b")
ax.set_title("Regra do piloto D023: 24 vinhetas × 3 repetições", fontsize=10, color="#0b0b0b", loc="left")
ax.set_ylim(0, 1.02)
ax.grid(True, color="#e5e4df", lw=0.6)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(frameon=False, fontsize=8, loc="lower right")
ax.set_facecolor("#fcfcfb")
fig.patch.set_facecolor("#fcfcfb")
fig.tight_layout()
fig.savefig(AQUI / "fig2_regra_piloto.png")

print()
print("=" * 90)
print("(c) Vies por enriquecimento de armadilhas (20/24 vinhetas com gatilho declarado; ver v1)")
print("    taxa_piloto = 20/24*p_arm + 4/24*p_tip ; taxa_populacional = w*p_arm + (1-w)*p_tip")
for p_arm, p_tip in ((0.15, 0.03), (0.20, 0.05), (0.10, 0.02)):
    tp = 20 / 24 * p_arm + 4 / 24 * p_tip
    for w in (0.2, 0.4):
        tpop = w * p_arm + (1 - w) * p_tip
        print("    p_arm=%.2f p_tip=%.2f w=%.1f -> piloto %.1f%% x populacao %.1f%%  (regra: %s x %s)" % (
            p_arm, p_tip, w, 100 * tp, 100 * tpop, "SEGUE" if tp >= .1 else "AJUSTA", "SEGUE" if tpop >= .1 else "AJUSTA"))

print()
print("=" * 90)
print("(d) H3 -- evento raro (explicacao atribui risco a raca/etnia). p01 ~ 0 (verificador nao cria mencao)")
for pr in (0.01, 0.02, 0.05, 0.10):
    for r in (0.8, 1.0):
        print("    base %.0f%%, verificador remove %.0f%% -> n = %s pares (alpha=0,05)" % (
            100 * pr, 100 * r, n_connor(pr * r, 0.001, 0.05)))

print()
print("=" * 90)
print("(e) Carga do nucleo (D020): textos gerados e a anotar")
for nv in (100, 200, 300):
    textos = nv * 3 * 2 * 3  # vinhetas x configs x LLMs x repeticoes
    chamadas = nv * 2 * 3 * (1 + 1 + 2.5)  # isolado 1, ferramenta 1, verificador media 2,5
    print("    %d vinhetas: %d textos finais (3 configs x 2 LLMs x 3 reps); ~%d chamadas de API;"
          " com ~8 afirmacoes/texto = %d afirmacoes" % (nv, textos, chamadas, textos * 8))

print()
print("=" * 90)
print("(f) Precisao do kappa (2 anotadores, desfecho binario, prevalencia 20%, kappa real 0,70)")


def sim_kappa(n, prev=0.2, kappa=0.7, reps=4000):
    # modelo: cada anotador ve o verdadeiro rotulo e erra com prob e, simetrico
    # escolhe e tal que kappa esperado ~ alvo (busca simples)
    best = None
    for e in np.linspace(0.001, 0.3, 300):
        pa = prev * (1 - e) + (1 - prev) * e
        po = (prev * ((1 - e) ** 2 + e * e) + (1 - prev) * ((1 - e) ** 2 + e * e))
        pe = pa * pa + (1 - pa) * (1 - pa)
        k = (po - pe) / (1 - pe)
        if best is None or abs(k - kappa) < abs(best[1] - kappa):
            best = (e, k)
    e = best[0]
    ks = []
    for _ in range(reps):
        t = RNG.random(n) < prev
        a = np.where(RNG.random(n) < e, ~t, t)
        b = np.where(RNG.random(n) < e, ~t, t)
        po = np.mean(a == b)
        pa, pb = a.mean(), b.mean()
        pe = pa * pb + (1 - pa) * (1 - pb)
        ks.append((po - pe) / (1 - pe) if pe < 1 else np.nan)
    ks = np.array(ks)
    return np.nanpercentile(ks, 2.5), np.nanpercentile(ks, 97.5)


for n in (50, 100, 200):
    lo, hi = sim_kappa(n)
    print("    n=%d textos anotados em dobro -> 95%% dos kappas amostrais entre %.2f e %.2f" % (n, lo, hi))

print()
print("Figuras: fig1_n_mcnemar.png, fig2_regra_piloto.png")
