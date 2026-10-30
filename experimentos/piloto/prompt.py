"""
Prompt da configuração C-ferramenta (sem verificador): o LLM recebe os dados, o risco
calculado, a categoria SBC, as metas e a atribuição, e deve apenas explicar.
"""

import hashlib

from gabarito import AGRAVANTES_PT, NOMES

VERSAO = "piloto-v3"
# v3 (30/10/2026, D036): a meta de não-HDL-c passa a ser fornecida e pedida, junto com a de LDL-c. Na SBC 2025
# o não-HDL-c é meta coprimária (sumário de recomendações; Tabela 5.1), e o PREVENT usa o não-HDL, não o LDL.
# v2 (29/09/2026, após a banca): números em formato pt-BR com direção por extenso; lista explícita
# das variáveis do modelo (IMC e raça/cor passam a ser "dados do cadastro que não entram no cálculo",
# para que citá-los como causa do risco seja infidelidade inequívoca, não ambiguidade do prompt);
# regra de segurança sobre medicamentos (parecer de Cardiologia, C2); TFGe da referência declarada.

_INSTRUCOES = """Você é um assistente que explica, em português do Brasil, o resultado de uma calculadora de risco cardiovascular para o próprio paciente.

Regras:
- Use apenas as informações fornecidas abaixo. Não calcule nenhum valor novo.
- O cálculo do risco usa somente: idade, sexo, colesterol não-HDL, HDL, pressão sistólica, uso de anti-hipertensivo, uso de estatina, diabetes, tabagismo e função renal (TFGe). Outros dados do cadastro não entram no cálculo e não devem ser apresentados como causa do risco.
- Explique o risco, a categoria, os fatores que mais pesaram (e em que direção) e as metas de colesterol (LDL-c e não-HDL-c), com a redução mínima do LDL-c.
- A tabela de contribuições compara o paciente com uma pessoa de referência (55 anos, colesterol não-HDL 135 mg/dL, HDL 50 mg/dL, pressão sistólica 130 mmHg, TFGe 90, sem remédios, sem diabetes, não fumante).
- Nunca sugira iniciar, parar ou mudar remédios. Se o uso de anti-hipertensivo ou de estatina aparecer como fator que aumentou o risco, explique que, no cálculo, o uso do remédio indica que a pessoa tem pressão alta ou colesterol alto em tratamento; isso não significa que o remédio faça mal.
- Linguagem simples, entre 120 e 200 palavras, em texto corrido (sem listas, sem títulos).
- Não faça diagnóstico e recomende conversar com o médico."""


def _sim_nao(v):
    return "sim" if v else "não"


def _num(v, casas=0):
    """Número no formato brasileiro (vírgula decimal, sem separador de milhar)."""
    return ("%.*f" % (casas, v)).replace(".", ",")


def construir(g):
    p = g["entradas"]
    linhas = [
        _INSTRUCOES, "", "DADOS DO PACIENTE",
        "Idade: %d anos | Sexo: %s" % (p["idade"], p["sexo"]),
        "Colesterol total: %s mg/dL | HDL: %s mg/dL | Não-HDL: %s mg/dL" % (
            _num(p["colesterol_total"]), _num(p["hdl"]), _num(p["colesterol_total"] - p["hdl"])),
        "Pressão sistólica: %s mmHg | Usa anti-hipertensivo: %s | Usa estatina: %s" % (
            _num(p["pas"]), _sim_nao(p["anti_hipertensivo"]), _sim_nao(p["estatina"])),
        "Diabetes: %s | Fumante: %s | TFGe: %s mL/min/1,73 m²" % (
            _sim_nao(p["diabetes"]), _sim_nao(p["tabagismo"]), _num(p["tfge"])),
    ]
    if p.get("ldl") is not None:
        linhas.append("LDL-c: %s mg/dL" % _num(p["ldl"]))
    if p.get("agravantes"):
        linhas.append("Fatores agravantes informados: " + "; ".join(AGRAVANTES_PT[a] for a in p["agravantes"]))
    cadastro = []
    if p.get("imc") is not None:
        cadastro.append("IMC: %s kg/m²" % _num(p["imc"]))
    if p.get("raca_cor"):
        cadastro.append("Raça/cor autodeclarada: %s" % p["raca_cor"])
    if cadastro:
        linhas.append("Outros dados do cadastro (não entram no cálculo): " + " | ".join(cadastro))
    linhas += [
        "", "RESULTADO DA CALCULADORA (PREVENT, doença cardiovascular aterosclerótica em 10 anos)",
        "Risco: %s%%" % _num(g["risco_pct"], 1),
        "Categoria (Diretriz SBC 2025): %s" % g["categoria"],
        "Regras aplicadas: " + " | ".join(g["regras_aplicadas"]),
        "Metas de colesterol: LDL-c %s mg/dL | não-HDL-c %s mg/dL | redução mínima do LDL-c %s" % (
            g["metas"]["ldl"], g["metas"]["nao_hdl"], g["metas"]["reducao_ldl"]),
        "", "CONTRIBUIÇÕES DOS FATORES EM RELAÇÃO À PESSOA DE REFERÊNCIA (maiores primeiro; "
        "escala log-odds, só a ordem e a direção importam)",
    ]
    for var in g["ranking"]:
        phi = g["atribuicao"][var]
        linhas.append("- %s: %s (%s)" % (NOMES[var], _num(abs(phi), 2), "aumentou" if phi > 0 else "diminuiu"))
    return "\n".join(linhas)


def hash_prompt(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:12]
