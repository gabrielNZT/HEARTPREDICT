"""
TFGe pela equação CKD-EPI 2021 sem raça (Inker et al., N Engl J Med 2021), a mesma usada na derivação
do PREVENT (Khan et al. 2024, Methods). Constantes conferidas contra o pacote R preventr (calc_egfr).
"""


def tfge_ckd_epi_2021(creatinina_mg_dl, idade, sexo):
    if creatinina_mg_dl is None or creatinina_mg_dl <= 0:
        raise ValueError("creatinina deve ser maior que zero")
    feminino = sexo == "feminino"
    k = 0.7 if feminino else 0.9
    a1 = -0.241 if feminino else -0.302
    razao = creatinina_mg_dl / k
    valor = 142 * min(razao, 1) ** a1 * max(razao, 1) ** -1.2 * 0.9938 ** idade * (1.012 if feminino else 1)
    return round(valor)
