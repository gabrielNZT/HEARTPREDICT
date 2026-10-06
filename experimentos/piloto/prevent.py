"""
Cálculo do PREVENT (modelo base, 10 anos) e atribuição exata de Shapley por variável.

Forma da equação: risco = exp(L) / (1 + exp(L)), L = soma(beta * termo), com termos centrados
(Khan et al., Circulation 2024; Tabela S12). Coeficientes em coeficientes_prevent_base_10a.json
(fonte provisória: pacote R preventr — ver campo "_origem").

Decisões do TCC: D009 (modelo PREVENT-ASCVD 10 anos) e D012 (Shapley exato, escala log-odds,
referência = valores de centralização do modelo).
"""

import itertools
import json
import math
from pathlib import Path

MG_DL_POR_MMOL_L = 38.67  # conversão de colesterol (PREVENT, nota da Tabela 1)

_COEF = json.loads((Path(__file__).parent / "coeficientes_prevent_base_10a.json").read_text(encoding="utf-8"))

# Variáveis do paciente que entram no modelo (conjunto M das métricas; o IMC só afeta os modelos de IC).
VARIAVEIS = ["idade", "nao_hdl", "hdl", "pas", "anti_hipertensivo", "estatina", "diabetes", "tabagismo", "tfge"]

# Paciente de referência: valores de centralização do modelo (todos os termos centrados = 0).
REFERENCIA = {
    "idade": 55.0,
    "nao_hdl": 3.5 * MG_DL_POR_MMOL_L,
    "hdl": 1.3 * MG_DL_POR_MMOL_L,
    "pas": 130.0,
    "anti_hipertensivo": 0,
    "estatina": 0,
    "diabetes": 0,
    "tabagismo": 0,
    "tfge": 90.0,
    "imc": 25.0,
}

# Faixas usadas na derivação do PREVENT (Methods); fora delas o cálculo é recusado.
FAIXAS = {
    "idade": (30, 79),
    "colesterol_total": (130, 320),
    "hdl": (20, 100),
    "pas": (90, 200),
    "imc": (18.5, 39.99),
    "tfge": (15, 140),
}


_ROTULOS = {
    "idade": ("Idade", "anos"),
    "colesterol_total": ("Colesterol total", "mg/dL"),
    "hdl": ("HDL", "mg/dL"),
    "pas": ("Pressão sistólica", "mmHg"),
    "imc": ("IMC", "kg/m²"),
    "tfge": ("TFGe", "mL/min/1,73m²"),
}


def _fmt(v):
    return ("%g" % v).replace(".", ",")


class EntradaInvalida(ValueError):
    pass


def validar(p):
    obrigatorios = ["idade", "sexo", "colesterol_total", "hdl", "pas", "anti_hipertensivo",
                    "estatina", "diabetes", "tabagismo", "tfge"]
    faltando = [c for c in obrigatorios if p.get(c) is None]
    if faltando:
        raise EntradaInvalida("Dados ausentes: " + ", ".join(faltando))
    if p["sexo"] not in ("feminino", "masculino"):
        raise EntradaInvalida("sexo deve ser 'feminino' ou 'masculino'")
    for campo, (lo, hi) in FAIXAS.items():
        v = p.get(campo)
        if v is not None and not (lo <= v <= hi):
            nome, unidade = _ROTULOS[campo]
            raise EntradaInvalida("%s de %s %s está fora da faixa em que a equação foi desenvolvida (%s a %s %s)." % (
                nome, _fmt(v), unidade, _fmt(lo), _fmt(hi), unidade))


def _termos(x):
    """Termos centrados do modelo base de 10 anos (na ordem de _COEF['termos'])."""
    idade = (x["idade"] - 55) / 10
    nao_hdl = x["nao_hdl"] / MG_DL_POR_MMOL_L - 3.5
    hdl = (x["hdl"] / MG_DL_POR_MMOL_L - 1.3) / 0.3
    pas_lt = (min(x["pas"], 110) - 110) / 20
    pas_gte = (max(x["pas"], 110) - 130) / 20
    imc = x.get("imc", 25.0)
    imc_lt = (min(imc, 30) - 25) / 5
    imc_gte = (max(imc, 30) - 30) / 5
    tfge_lt = (min(x["tfge"], 60) - 60) / -15
    tfge_gte = (max(x["tfge"], 60) - 90) / -15
    dm, fumo, anti, est = x["diabetes"], x["tabagismo"], x["anti_hipertensivo"], x["estatina"]
    return [
        idade, nao_hdl, hdl, pas_lt, pas_gte, dm, fumo, imc_lt, imc_gte, tfge_lt, tfge_gte, anti, est,
        anti * pas_gte, est * nao_hdl,
        idade * nao_hdl, idade * hdl, idade * pas_gte, idade * dm, idade * fumo, idade * imc_gte, idade * tfge_lt,
        1.0,
    ]


def _coluna(sexo, desfecho):
    return _COEF[("female_" if sexo == "feminino" else "male_") + desfecho]


def log_odds(x, sexo, desfecho="ascvd"):
    return sum(b * t for b, t in zip(_coluna(sexo, desfecho), _termos(x)))


def _para_modelo(p):
    """Converte a entrada do paciente (mg/dL, 0/1) para as variáveis do modelo."""
    x = {k: p[k] for k in ("idade", "hdl", "pas", "tfge")}
    x["nao_hdl"] = p["colesterol_total"] - p["hdl"]
    for k in ("anti_hipertensivo", "estatina", "diabetes", "tabagismo"):
        x[k] = int(bool(p[k]))
    x["imc"] = p.get("imc", 25.0)
    return x


def risco(p, desfecho="ascvd"):
    """Risco em 10 anos (fração 0-1)."""
    validar(p)
    L = log_odds(_para_modelo(p), p["sexo"], desfecho)
    return 1 / (1 + math.exp(-L))


def shapley(p, desfecho="ascvd"):
    """Valores de Shapley exatos (log-odds) de cada variável em VARIAVEIS, com referência REFERENCIA."""
    validar(p)
    x = _para_modelo(p)
    n = len(VARIAVEIS)
    cache = {}

    def v(coalizao):
        if coalizao not in cache:
            z = dict(REFERENCIA)
            z["imc"] = x["imc"]  # o IMC não é variável de atribuição (coeficiente 0 no modelo de DCVA)
            for i in coalizao:
                z[VARIAVEIS[i]] = x[VARIAVEIS[i]]
            cache[coalizao] = log_odds(z, p["sexo"], desfecho)
        return cache[coalizao]

    fat = math.factorial
    phi = {}
    for i in range(n):
        outros = [j for j in range(n) if j != i]
        total = 0.0
        for k in range(len(outros) + 1):
            peso = fat(k) * fat(n - k - 1) / fat(n)
            for S in itertools.combinations(outros, k):
                total += peso * (v(tuple(sorted(S + (i,)))) - v(S))
        phi[VARIAVEIS[i]] = total
    return phi
