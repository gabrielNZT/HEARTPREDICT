"""
Varredura da API do gateway (banca, engenharia). NÃO faz parte do projeto.

Rodar a partir de backend-gateway/app (o gateway importa `avaliacao` por nome):
    cd backend-gateway/app
    <venv com fastapi 0.108>/bin/python -m unittest discover \
        -s ../../tcc/05-banca/anexos/engenharia -p "test_api_*.py" -v

Não chama LLM real: `llm.gerar` é substituído por dublês.
"""

import math
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "backend-gateway" / "app"))

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
import avaliacao  # noqa: E402

BASE = dict(idade=50, sexo="feminino", dcv_previa=False, diabetes=False, colesterol_total=240, hdl=55, pas=160,
            tfge=90, anti_hipertensivo=True, estatina=False, tabagismo=False)

FAIXAS = {"idade": (30, 79), "colesterol_total": (130, 320), "hdl": (20, 100), "pas": (90, 200), "tfge": (15, 140)}


class TestVarreduraDeFaixas(unittest.TestCase):
    """Limites inclusivos aceitos; valores imediatamente fora recusados com 422 'fora_da_faixa'."""

    def setUp(self):
        self.c = TestClient(main.app, raise_server_exceptions=False)

    def test_limites(self):
        falhas = []
        for campo, (lo, hi) in FAIXAS.items():
            passo = 1 if campo == "idade" else 0.01
            for valor, esperado in ((lo, 200), (hi, 200), (lo - passo, 422), (hi + passo, 422)):
                r = self.c.post("/api/avaliacao", json=dict(BASE, **{campo: valor}))
                if r.status_code != esperado:
                    falhas.append((campo, valor, r.status_code, r.text[:120]))
        self.assertEqual(falhas, [])


class TestContratoDaApi(unittest.TestCase):
    def setUp(self):
        self.c = TestClient(main.app, raise_server_exceptions=False)

    def post(self, **mudancas):
        corpo = dict(BASE)
        for k, v in mudancas.items():
            if v is ...:
                corpo.pop(k, None)
            else:
                corpo[k] = v
        return self.c.post("/api/avaliacao", json=corpo)

    # ---------- BUGS (o teste passa quando o bug está presente) ----------
    def test_BUG_creatinina_zero_gera_500(self):
        r = self.post(tfge=..., creatinina=0)
        self.assertEqual(r.status_code, 500)

    def test_BUG_creatinina_negativa_gera_500(self):
        r = self.post(tfge=..., creatinina=-1)
        self.assertEqual(r.status_code, 500)

    def test_BUG_agravante_feminino_aceito_para_homem(self):
        homem = dict(idade=35, sexo="masculino", colesterol_total=170, hdl=60, pas=115, anti_hipertensivo=False)
        sem = self.post(**homem).json()
        com = self.post(**homem, agravantes=["fator_especifico_mulher"]).json()
        self.assertEqual(sem["categoria"], "baixo")
        self.assertEqual(com["categoria"], "intermediário")
        self.assertIn("fator de risco específico da mulher", com["agravantes"])

    def test_BUG_agravante_desconhecido_descartado_em_silencio(self):
        r = self.post(agravantes=["historia_familiar_PREMATURA"])  # erro de digitação do cliente
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["agravantes"], [])

    def test_BUG_ldl_sem_validacao_de_faixa(self):
        for ldl in (-50, 0, 5000, 239):  # 239 com CT 240 e HDL 55 é fisicamente impossível
            r = self.post(ldl=ldl)
            self.assertEqual(r.status_code, 200, ldl)
        self.assertEqual(self.post(ldl=5000).json()["categoria"], "alto")

    def test_BUG_limite_exibido_5_0_categoria_baixo(self):
        r = self.post(idade=55, sexo="masculino", colesterol_total=256.0, hdl=44, pas=140,
                      anti_hipertensivo=False, tfge=95).json()
        self.assertEqual((r["risco_pct"], r["categoria"]), (5.0, "baixo"))
        self.assertIn("5,0% → baixo", r["regras_aplicadas"][0])

    def test_arredondamento_bancario_em_100_pessoas(self):
        # round() do Python arredonda 0,5 para o par: 2,5% → 2 pessoas; 3,5% → 4 pessoas.
        self.assertEqual((round(0.5), round(1.5), round(2.5), round(3.5)), (0, 2, 2, 4))

    # ---------- Comportamentos corretos ----------
    def test_virgula_decimal_recusada_pelo_pydantic(self):
        r = self.post(pas="130,5")
        self.assertEqual(r.status_code, 422)
        self.assertIsInstance(r.json()["detail"], list)  # formato diferente do {codigo, mensagens}

    def test_idade_decimal_recusada(self):
        self.assertEqual(self.post(idade=50.5).status_code, 422)

    def test_nan_recusado_como_fora_da_faixa(self):
        r = self.c.post("/api/avaliacao", content=b'{"idade":50,"sexo":"feminino","dcv_previa":false,'
                        b'"diabetes":false,"colesterol_total":NaN,"hdl":55,"pas":160,"tfge":90,'
                        b'"anti_hipertensivo":true,"estatina":false,"tabagismo":false}',
                        headers={"Content-Type": "application/json"})
        print("\n  [NaN colesterol_total] HTTP %d %s" % (r.status_code, r.text[:160]))

    def test_tfge_e_creatinina_juntas_tfge_prevalece(self):
        d = self.post(creatinina=5.0).json()
        self.assertEqual(d["origem_tfge"], "informada")


class TestExplicacao(unittest.TestCase):
    def setUp(self):
        self.c = TestClient(main.app, raise_server_exceptions=False)

    def test_sem_configuracao_503(self):
        with mock.patch.dict("os.environ", {}, clear=True), mock.patch.object(avaliacao.llm, "_ler_env"):
            r = self.c.post("/api/avaliacao/explicacao", json=BASE)
        self.assertEqual(r.status_code, 503)

    def test_BUG_ldl_nan_aceito_e_explicacao_falha_como_503(self):
        corpo = (b'{"idade":50,"sexo":"feminino","dcv_previa":false,"diabetes":false,"colesterol_total":240,'
                 b'"hdl":55,"pas":160,"tfge":90,"anti_hipertensivo":true,"estatina":false,"tabagismo":false,'
                 b'"ldl":NaN}')
        env = {"LLM_PROVEDOR": "groq", "LLM_MODELO": "x"}
        with mock.patch.dict("os.environ", env), mock.patch.object(avaliacao.llm, "gerar", return_value=("ok", {})):
            r1 = self.c.post("/api/avaliacao", content=corpo, headers={"Content-Type": "application/json"})
            r2 = self.c.post("/api/avaliacao/explicacao", content=corpo, headers={"Content-Type": "application/json"})
        print("\n  [ldl=NaN] /api/avaliacao HTTP %d; /explicacao HTTP %d %s" % (
            r1.status_code, r2.status_code, r2.json().get("detail")))
        self.assertEqual(r1.status_code, 200)  # NaN aceito no cálculo
        self.assertEqual(r2.status_code, 503)  # erro de programação (prompt) mascarado de "LLM indisponível"
        self.assertIn("NaN", r2.json()["detail"])

    def test_erro_de_rede_vira_503_com_mensagem_crua(self):
        env = {"LLM_PROVEDOR": "groq", "LLM_MODELO": "x"}
        falha = urllib.error.URLError("[Errno -2] Name or service not known")
        with mock.patch.dict("os.environ", env), mock.patch.object(avaliacao.llm, "gerar", side_effect=falha):
            r = self.c.post("/api/avaliacao/explicacao", json=BASE)
        self.assertEqual(r.status_code, 503)
        print("\n  [rede] detail=%r" % r.json()["detail"])

    def test_temperatura_fixa_no_codigo(self):
        env = {"LLM_PROVEDOR": "groq", "LLM_MODELO": "x"}
        with mock.patch.dict("os.environ", env), \
                mock.patch.object(avaliacao.llm, "gerar", return_value=("texto", {})) as g:
            self.c.post("/api/avaliacao/explicacao", json=BASE)
        self.assertEqual(g.call_args.kwargs["temperatura"], 0.7)


class TestEndpointAntigo(unittest.TestCase):
    """/predict: HTTPException interna é engolida pelo `except Exception` e vira 500."""

    def test_BUG_timeout_408_vira_500(self):
        class Resp:
            status_code = 200

        class ClienteFalso:
            def __init__(self, *a, **k):
                pass

            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                return False

            async def post(self, *a, **k):
                return Resp()

        async def sem_resposta(user_id, timeout=60):
            return None

        corpo = dict(user_id="u1", age=50, gender=1, height=165, weight=60.0, ap_hi=120, ap_lo=80,
                     cholesterol=1, gluc=1, smoke=0, alco=0, active=1)
        c = TestClient(main.app, raise_server_exceptions=False)
        with mock.patch.object(main.httpx, "AsyncClient", ClienteFalso), \
                mock.patch.object(main, "wait_for_explanation", sem_resposta):
            r = c.post("/predict", json=corpo)
        print("\n  [/predict timeout] HTTP %d %s" % (r.status_code, r.text[:120]))
        self.assertEqual(r.status_code, 500)

    def test_BUG_explicacao_pode_ser_injetada_sem_autenticacao(self):
        c = TestClient(main.app)
        main.pending_explanations["vitima"] = {"timestamp": None, "explanation": None}
        try:
            r = c.post("/explanation/vitima", json={"explanation": "{\"texto\": \"forjado\"}"})
            self.assertEqual(r.status_code, 200)
            self.assertEqual(main.pending_explanations["vitima"]["explanation"], "{\"texto\": \"forjado\"}")
            self.assertIn("vitima", c.get("/pending").json()["pending_explanations"])
        finally:
            main.pending_explanations.pop("vitima", None)


if __name__ == "__main__":
    unittest.main()
