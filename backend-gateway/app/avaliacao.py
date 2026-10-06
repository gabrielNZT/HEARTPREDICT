"""
Endpoints da avaliação no escopo PREVENT/SBC 2025 usados pela interface.

Transitório (decisão do usuário em 29/09/2026): o cálculo usa o núcleo testado em
experimentos/piloto (prevent, sbc, renal, gabarito) e a explicação chama o LLM diretamente
(configuração C-ferramenta), sem passar pelos agentes JADE. A reintegração com o JADE
(FIPA-Propose com o Verificador) segue D021.
"""

import datetime
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing_extensions import Literal

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "experimentos" / "piloto"))

import gabarito  # noqa: E402
import llm  # noqa: E402
import prevent  # noqa: E402
import prompt  # noqa: E402
import renal  # noqa: E402
import sbc  # noqa: E402

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/avaliacao", tags=["avaliação"])

# Mesmo limiar de contribuição desprezível da métrica de polaridade (metricas-fidelidade.md §3.3).
FRACAO_DESPREZIVEL = 0.05


class EntradaAvaliacao(BaseModel):
    idade: int
    sexo: Literal["feminino", "masculino"]
    dcv_previa: bool
    diabetes: bool
    colesterol_total: float
    hdl: float
    pas: float
    tfge: Optional[float] = None
    creatinina: Optional[float] = None
    anti_hipertensivo: bool
    estatina: bool
    tabagismo: bool
    ldl: Optional[float] = None
    aterosclerose_subclinica: bool = False
    agravantes: List[str] = Field(default_factory=list)
    criterios_alto: List[str] = Field(default_factory=list)


class EntradaExplicacao(EntradaAvaliacao):
    # O envio a um provedor externo de LLM só ocorre com consentimento explícito na interface
    # (LGPD art. 11, I; parecer de Ética C1/C2). Sem ele, a explicação é recusada.
    consentimento_envio_llm: bool = False


# Faixas de plausibilidade de entradas que não são do PREVENT (validadas aqui, não no núcleo).
FAIXA_CREATININA = (0.3, 15.0)  # mg/dL
FAIXA_LDL = (20.0, 400.0)  # mg/dL
# SBC 2025, seção 4.1: o escore só vale com LDL-c < 160. Sem LDL, não-HDL ≥ 190 torna provável LDL ≥ 160
# (não-HDL ≈ LDL + VLDL, e VLDL raramente passa de 30–40 mg/dL); exige-se o LDL (parecer de Cardiologia, M4).
LIMIAR_NAO_HDL_EXIGE_LDL = 190
TFGE_MAXIMA = 140


def _fmt(v):
    return ("%g" % v).replace(".", ",")


def _recusar(codigo, mensagens):
    raise HTTPException(status_code=422, detail={"codigo": codigo, "mensagens": mensagens})


def _paciente(e: EntradaAvaliacao):
    """Valida o escopo e monta o paciente no formato do núcleo. Recusa em vez de supor (D021, AgentMD)."""
    if e.dcv_previa:
        _recusar("fora_do_escopo", ["A calculadora é para quem nunca teve infarto, AVC ou outra doença "
                                    "cardiovascular diagnosticada. Nesses casos o risco já é considerado muito alto "
                                    "pela diretriz, e a conduta deve ser definida com o médico."])
    if e.diabetes:
        _recusar("fora_do_escopo", ["Para pessoas com diabetes, a Diretriz SBC 2025 usa outros critérios de "
                                    "classificação, que esta versão ainda não implementa."])
    if e.aterosclerose_subclinica:
        _recusar("fora_do_escopo", ["Quem já tem placa nas artérias identificada em exame de imagem é classificado "
                                    "diretamente pela diretriz como risco alto ou muito alto, sem usar a equação. "
                                    "Converse com o seu médico sobre as metas."])
    desconhecidos = sorted(set(e.agravantes) - sbc.AGRAVANTES_VALIDOS)
    desconhecidos += sorted(set(e.criterios_alto) - set(sbc.CRITERIOS_ALTO_PT))
    if desconhecidos:
        _recusar("dado_invalido", ["Situação não reconhecida: %s." % ", ".join(desconhecidos)])
    if e.sexo != "feminino" and set(e.agravantes) & sbc.AGRAVANTES_SO_MULHER:
        _recusar("dado_invalido", ["A opção “situações da saúde da mulher” só se aplica ao sexo feminino. "
                                   "Revise a resposta sobre as situações que ajustam a categoria."])
    origem_tfge = "informada"
    tfge = e.tfge
    if tfge is None:
        if e.creatinina is None:
            _recusar("dado_ausente", ["Informe a TFG estimada ou a creatinina do exame de sangue."])
        if not (FAIXA_CREATININA[0] <= e.creatinina <= FAIXA_CREATININA[1]):
            _recusar("fora_da_faixa", ["Creatinina deve estar entre 0,3 e 15 mg/dL. Confira o valor no exame."])
        tfge = renal.tfge_ckd_epi_2021(e.creatinina, e.idade, e.sexo)
        origem_tfge = "calculada a partir da creatinina (CKD-EPI 2021)"
    if e.ldl is None and e.colesterol_total - e.hdl >= LIMIAR_NAO_HDL_EXIGE_LDL:
        _recusar("dado_ausente", ["Com colesterol não-HDL de %s mg/dL, o LDL provavelmente passa de 160, e a "
                                  "diretriz não usa a equação nesse caso. Informe o LDL do exame." %
                                  _fmt(e.colesterol_total - e.hdl)])
    if tfge > TFGE_MAXIMA:
        # Faixa de derivação do PREVENT vai até 140; acima disso a função renal é normal e o valor é
        # limitado a 140 (em vez de recusar quem não digitou a TFGe; parecer de Cardiologia, m2).
        origem_tfge += "; acima de 140, considerada 140 (limite da equação)"
        tfge = TFGE_MAXIMA
    if e.ldl is not None:
        if not (FAIXA_LDL[0] <= e.ldl <= FAIXA_LDL[1]):
            _recusar("fora_da_faixa", ["LDL deve estar entre 20 e 400 mg/dL. Confira o valor no exame."])
        if e.ldl > e.colesterol_total - e.hdl:
            _recusar("dado_invalido", ["O LDL não pode ser maior que o colesterol total menos o HDL "
                                       "(%s mg/dL). Confira os valores no exame." % _fmt(e.colesterol_total - e.hdl)])
    p = {
        "idade": e.idade, "sexo": e.sexo, "colesterol_total": e.colesterol_total, "hdl": e.hdl, "pas": e.pas,
        "anti_hipertensivo": int(e.anti_hipertensivo), "estatina": int(e.estatina), "diabetes": 0,
        "tabagismo": int(e.tabagismo), "tfge": tfge,
        "agravantes": list(e.agravantes), "criterios_alto": list(e.criterios_alto),
    }
    if e.ldl is not None:
        p["ldl"] = e.ldl
    try:
        prevent.validar(p)
    except prevent.EntradaInvalida as ex:
        _recusar("fora_da_faixa", [str(ex)])
    return p, origem_tfge


def _resultado(p, origem_tfge):
    g = gabarito.montar({"id": "interface", "paciente": p})
    soma = sum(abs(v) for v in g["atribuicao"].values()) or 1.0
    fatores = []
    for var in g["ranking"]:
        phi = g["atribuicao"][var]
        if abs(phi) < FRACAO_DESPREZIVEL * soma:
            direcao = "pouco influenciou"
        else:
            direcao = "aumentou" if phi > 0 else "diminuiu"
        fatores.append({"variavel": var, "nome": gabarito.NOMES[var], "contribuicao": phi, "direcao": direcao})
    return {
        "risco_pct": g["risco_pct"],
        # Arredondamento "meio para cima" (o round do Python arredonda 2,5 para 2).
        "em_100_pessoas": int(g["risco_pct"] + 0.5),
        "categoria": g["categoria"],
        "regras_aplicadas": g["regras_aplicadas"],
        "metas": g["metas"],
        "fatores": fatores,
        "tfge_usada": p["tfge"],
        "origem_tfge": origem_tfge,
        "agravantes": [gabarito.AGRAVANTES_PT[a] for a in p["agravantes"]],
        "criterios_alto": [sbc.CRITERIOS_ALTO_PT[c] for c in p["criterios_alto"]],
        "_gabarito": g,
    }


@router.post("")
def avaliar(entrada: EntradaAvaliacao):
    p, origem = _paciente(entrada)
    r = _resultado(p, origem)
    r.pop("_gabarito")
    return r


# Quem recebe os dados em cada provedor (mostrado ao usuário antes do consentimento; LGPD art. 9º e 33).
EMPRESAS = {
    "groq": ("Groq, Inc.", "Estados Unidos"),
    "gemini": ("Google LLC", "Estados Unidos"),
    "xai": ("xAI Corp.", "Estados Unidos"),
    "openrouter": ("OpenRouter, Inc.", "Estados Unidos"),
}


def _config_llm():
    """Provedor, modelo e temperatura da interface (variáveis de ambiente; D028)."""
    llm._ler_env()
    provedor = os.environ.get("LLM_PROVEDOR")
    modelo = os.environ.get("LLM_MODELO")
    # Interface: temperatura baixa por padrão (parecer de Cardiologia, C2). O experimento define a sua própria.
    temperatura = float(os.environ.get("LLM_TEMPERATURA", "0.2"))
    # Dados de pessoas reais não vão ao plano gratuito do Gemini: os termos proíbem dados sensíveis e
    # permitem uso para treino e revisão humana (parecer de Ética, C1; verificacao-alegacoes.md).
    bloqueado = provedor == "gemini" and os.environ.get("LLM_PLANO_SEM_USO_DOS_DADOS") != "1"
    return provedor, modelo, temperatura, bloqueado


@router.get("/explicacao/provedor")
def provedor_da_explicacao():
    provedor, modelo, _, bloqueado = _config_llm()
    if not (provedor and modelo) or bloqueado:
        return {"disponivel": False}
    empresa, pais = EMPRESAS.get(provedor, (provedor, "desconhecido"))
    return {"disponivel": True, "empresa": empresa, "pais": pais, "modelo": modelo}


@router.post("/explicacao")
def explicar(entrada: EntradaExplicacao):
    if not entrada.consentimento_envio_llm:
        raise HTTPException(status_code=403, detail="A explicação só é gerada com o seu consentimento para enviar "
                                                    "os valores, sem identificação, ao serviço de IA.")
    provedor, modelo, temperatura, bloqueado = _config_llm()
    if not (provedor and modelo):
        raise HTTPException(status_code=503, detail="Explicação indisponível: defina LLM_PROVEDOR e LLM_MODELO no .env.")
    if bloqueado:
        raise HTTPException(status_code=503, detail="Explicação indisponível: o plano gratuito do Gemini não pode "
                                                    "receber dados de pessoas reais (ver D028).")
    p, origem = _paciente(entrada)
    g = _resultado(p, origem)["_gabarito"]
    texto_prompt = prompt.construir(g)  # fora do try: erro de programação não vira "LLM indisponível"
    try:
        texto, _ = llm.gerar(provedor, modelo, texto_prompt, temperatura=temperatura, max_tokens=2048)
    except Exception as ex:
        # Detalhe só no log do servidor, sem dados do paciente; o usuário recebe mensagem genérica.
        logger.warning("Falha ao gerar explicação (%s/%s): %s", provedor, modelo, type(ex).__name__)
        raise HTTPException(status_code=503, detail="Explicação indisponível no momento.")
    return {
        "texto": texto.strip(),
        "provedor": provedor,
        "modelo": modelo,
        "prompt_versao": prompt.VERSAO,
        "temperatura": temperatura,
        "gerado_em": datetime.datetime.now().isoformat(timespec="seconds"),
        "verificado": False,
    }
