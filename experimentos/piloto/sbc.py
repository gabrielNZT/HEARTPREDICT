"""
Categoria de risco e metas segundo a Diretriz Brasileira de Dislipidemias e Prevenção da
Aterosclerose – 2025 (SBC), restritas ao escopo do piloto (D011): adultos de 30–79 anos,
sem DCV prévia, sem aterosclerose subclínica e sem diabetes.

Operacionalização (D010, revista em D026 após a banca):
1. escore arredondado a 0,1 ponto percentual (a mesma precisão exibida) → corte 5% / 20% (Tabela 4.1);
2. LDL-c 160–189 → no mínimo intermediário (seção 4.1: "sejam considerados de risco intermediário");
3. ≥ 1 agravante sobe uma categoria (Tabela 4.1: "risco intermediário, com presença de fator
   agravante" → alto; Figura 4.1: baixo → intermediário). Aplicado depois do passo 2 porque quem
   tem LDL-c 160–189 já "é considerado" intermediário;
4. LDL-c ≥ 190 ou Lp(a) > 180 mg/dL (> 390 nmol/L) → alto (Tabela 4.1; seção 4.3).
"""

ORDEM = ["baixo", "intermediário", "alto"]

# Tabela 5.1 (LDL-c e não-HDL-c em mg/dL; redução mínima de LDL-c)
METAS = {
    "baixo": {"ldl": "< 115", "nao_hdl": "< 145", "reducao_ldl": "≥ 30%"},
    "intermediário": {"ldl": "< 100", "nao_hdl": "< 130", "reducao_ldl": "≥ 30%"},
    "alto": {"ldl": "< 70", "nao_hdl": "< 100", "reducao_ldl": "≥ 50%"},
}

AGRAVANTES_PT = {
    "historia_familiar_prematura": "história familiar de doença cardiovascular prematura",
    "sindrome_metabolica": "síndrome metabólica",
    "doenca_inflamatoria_cronica": "doença inflamatória crônica",
    "transplante": "transplante de órgão",
    "fator_especifico_mulher": "fator de risco específico da mulher",
    "lpa_elevada": "lipoproteína(a) elevada",
    "pcr_us_elevada": "PCR ultrassensível elevada",
}
AGRAVANTES_VALIDOS = set(AGRAVANTES_PT)
AGRAVANTES_SO_MULHER = {"fator_especifico_mulher"}

# Critérios que classificam diretamente como alto (Tabela 4.1), além do LDL-c ≥ 190.
CRITERIOS_ALTO_PT = {"lpa_muito_elevada": "lipoproteína(a) acima de 180 mg/dL"}


class ForaDoEscopo(ValueError):
    pass


def categoria(risco_10a, paciente):
    """Retorna (categoria, regras_aplicadas)."""
    if paciente.get("diabetes"):
        raise ForaDoEscopo("Diabetes: a SBC 2025 usa as Tabelas 4.5–4.8, fora do escopo do piloto (D011).")
    regras = []
    pct = round(risco_10a * 100, 1)
    if pct < 5:
        cat = "baixo"
    elif pct < 20:
        cat = "intermediário"
    else:
        cat = "alto"
    regras.append("escore PREVENT %s%% → %s (Tabela 4.1)" % (("%.1f" % pct).replace(".", ","), cat))

    ldl = paciente.get("ldl")
    if ldl is not None and 160 <= ldl < 190 and cat == "baixo":
        regras.append("LDL-c %d entre 160 e 189 → intermediário (seção 4.1)" % ldl)
        cat = "intermediário"

    agravantes = [a for a in paciente.get("agravantes", []) if a in AGRAVANTES_VALIDOS]
    if agravantes and cat != "alto":
        nova = ORDEM[ORDEM.index(cat) + 1]
        regras.append("agravante(s): %s → de %s para %s (Tabela 4.1)" % (
            "; ".join(AGRAVANTES_PT[a] for a in agravantes), cat, nova))
        cat = nova

    if ldl is not None and ldl >= 190 and cat != "alto":
        regras.append("LDL-c %d ≥ 190 → alto (seção 4.1)" % ldl)
        cat = "alto"
    if "lpa_muito_elevada" in paciente.get("criterios_alto", []) and cat != "alto":
        regras.append("Lp(a) > 180 mg/dL → alto (Tabela 4.1)")
        cat = "alto"
    return cat, regras
