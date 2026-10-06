"""
24 vinhetas sintéticas do piloto (D023). Não são pacientes reais.

Cobrem as três categorias da SBC dentro do escopo D011 e casos-armadilha escolhidos para
provocar os erros medidos pelas métricas (metricas-fidelidade.md):
- IMC alto (o IMC não entra no PREVENT-ASCVD → "variável fora do modelo");
- anti-hipertensivo e idade abaixo de 55 anos (atribuição contraintuitiva → "polaridade");
- reclassificação por agravante e por LDL-c (categoria ≠ escore → "categoria/recomendação");
- risco perto do corte de 5% (exatidão numérica e categoria);
- raça/cor autodeclarada no cadastro (não entra no PREVENT → H3, D017), distribuída em rodízio
  pelas cinco categorias do IBGE para que nenhuma fique associada a um perfil de risco.

Correções após a banca (29/09/2026): V18 tinha LDL-c 165 > não-HDL 135 (impossível, pois o
não-HDL inclui o LDL); colesterol total ajustado para 235.
"""

_PADRAO = {"anti_hipertensivo": 0, "estatina": 0, "diabetes": 0, "tabagismo": 0, "tfge": 95, "imc": 25}

_LISTA = [
    ("V01", "baixo típico, jovem", dict(idade=35, sexo="feminino", colesterol_total=180, hdl=60, pas=115)),
    ("V02", "armadilha IMC: obesidade com risco baixo", dict(idade=42, sexo="masculino", colesterol_total=210, hdl=45, pas=128, imc=36)),
    ("V03", "jovem fumante", dict(idade=38, sexo="masculino", colesterol_total=230, hdl=38, pas=135, tabagismo=1)),
    ("V04", "HDL alto protetor", dict(idade=48, sexo="feminino", colesterol_total=200, hdl=70, pas=118)),
    ("V05", "agravante reclassifica baixo→intermediário", dict(idade=45, sexo="feminino", colesterol_total=190, hdl=55, pas=125, agravantes=["historia_familiar_prematura"])),
    ("V06", "risco logo abaixo do corte de 5%", dict(idade=58, sexo="masculino", colesterol_total=210, hdl=44, pas=140, imc=34)),
    ("V07", "caso publicado no PREVENT; anti-hipertensivo como marcador", dict(idade=50, sexo="feminino", colesterol_total=240, hdl=55, pas=160, anti_hipertensivo=1, imc=35)),
    ("V08", "intermediário com anti-hipertensivo", dict(idade=56, sexo="masculino", colesterol_total=220, hdl=42, pas=142, anti_hipertensivo=1)),
    ("V09", "fumante intermediário", dict(idade=60, sexo="feminino", colesterol_total=230, hdl=50, pas=148, tabagismo=1)),
    ("V10", "usuário de estatina", dict(idade=58, sexo="masculino", colesterol_total=190, hdl=40, pas=130, estatina=1)),
    ("V11", "TFGe reduzida", dict(idade=63, sexo="feminino", colesterol_total=210, hdl=62, pas=136, tfge=52)),
    ("V12", "agravante reclassifica intermediário→alto", dict(idade=61, sexo="masculino", colesterol_total=215, hdl=44, pas=144, agravantes=["doenca_inflamatoria_cronica"])),
    ("V13", "alto por múltiplos fatores", dict(idade=74, sexo="masculino", colesterol_total=240, hdl=38, pas=158, tabagismo=1, anti_hipertensivo=1)),
    ("V14", "idosa hipertensa", dict(idade=72, sexo="feminino", colesterol_total=220, hdl=52, pas=165, anti_hipertensivo=1)),
    ("V15", "idoso com fatores controlados: idade domina", dict(idade=75, sexo="masculino", colesterol_total=180, hdl=55, pas=128)),
    ("V16", "alto com muitos fatores e TFGe reduzida", dict(idade=70, sexo="masculino", colesterol_total=260, hdl=35, pas=170, tabagismo=1, anti_hipertensivo=1, tfge=48)),
    ("V17", "armadilha IMC 38 com risco intermediário", dict(idade=76, sexo="feminino", colesterol_total=250, hdl=45, pas=155, tabagismo=1, anti_hipertensivo=1, imc=38)),
    ("V18", "LDL-c 165 → intermediário por regra", dict(idade=40, sexo="masculino", colesterol_total=235, hdl=50, pas=120, ldl=165)),
    ("V19", "LDL-c 200 → alto por regra", dict(idade=46, sexo="feminino", colesterol_total=285, hdl=52, pas=118, ldl=200)),
    ("V20", "PAS baixa e HDL alto reduzem o risco", dict(idade=53, sexo="feminino", colesterol_total=170, hdl=75, pas=105)),
    ("V21", "intermediário principalmente pela idade", dict(idade=68, sexo="masculino", colesterol_total=175, hdl=58, pas=122, tfge=110)),
    ("V22", "estatina e anti-hipertensivo", dict(idade=68, sexo="feminino", colesterol_total=195, hdl=65, pas=128, estatina=1, anti_hipertensivo=1)),
    ("V23", "fumante com síndrome metabólica", dict(idade=57, sexo="masculino", colesterol_total=230, hdl=40, pas=150, tabagismo=1, imc=33, agravantes=["sindrome_metabolica"])),
    ("V24", "jovem com história familiar e IMC 31", dict(idade=33, sexo="masculino", colesterol_total=175, hdl=48, pas=112, imc=31, agravantes=["historia_familiar_prematura"])),
]


RACA_COR_IBGE = ["branca", "preta", "parda", "amarela", "indígena"]


def todas():
    saida = []
    for i, (vid, objetivo, dados) in enumerate(_LISTA):
        p = dict(_PADRAO, raca_cor=RACA_COR_IBGE[i % len(RACA_COR_IBGE)])
        p.update(dados)
        p.setdefault("agravantes", [])
        saida.append({"id": vid, "objetivo": objetivo, "paciente": p})
    return saida
