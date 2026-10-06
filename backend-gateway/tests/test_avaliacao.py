"""Testes de POST /api/avaliacao. Rodar a partir de backend-gateway/app: python -m unittest discover -s ../tests"""
import unittest

from fastapi.testclient import TestClient

import main

BASE = dict(idade=50, sexo="feminino", dcv_previa=False, diabetes=False, colesterol_total=240, hdl=55, pas=160,
            tfge=90, anti_hipertensivo=True, estatina=False, tabagismo=False)


class TestAvaliacao(unittest.TestCase):
    def setUp(self):
        self.c = TestClient(main.app)

    def test_caso_publicado_prevent(self):
        d = self.c.post("/api/avaliacao", json=BASE).json()
        self.assertEqual(d["risco_pct"], 3.6)  # Khan et al. 2024, Results
        self.assertEqual(d["categoria"], "baixo")

    def test_agravante_reclassifica(self):
        d = self.c.post("/api/avaliacao", json=dict(BASE, agravantes=["historia_familiar_prematura"])).json()
        self.assertEqual(d["categoria"], "intermediário")

    def test_recusa_fora_do_escopo(self):
        for campo in ("diabetes", "dcv_previa"):
            r = self.c.post("/api/avaliacao", json=dict(BASE, **{campo: True}))
            self.assertEqual(r.status_code, 422)
            self.assertEqual(r.json()["detail"]["codigo"], "fora_do_escopo")

    def test_recusa_dado_ausente(self):
        b = dict(BASE)
        del b["tfge"]
        r = self.c.post("/api/avaliacao", json=b)
        self.assertEqual(r.json()["detail"]["codigo"], "dado_ausente")

    def test_tfge_pela_creatinina(self):
        b = dict(BASE, creatinina=0.8)
        del b["tfge"]
        d = self.c.post("/api/avaliacao", json=b).json()
        self.assertEqual(d["tfge_usada"], 90)

    def test_recusa_fora_da_faixa(self):
        r = self.c.post("/api/avaliacao", json=dict(BASE, pas=230))
        self.assertEqual(r.json()["detail"]["codigo"], "fora_da_faixa")

    # Casos levantados pela banca (29/09/2026)
    def _codigo(self, **extra):
        r = self.c.post("/api/avaliacao", json=dict(BASE, **extra))
        self.assertEqual(r.status_code, 422, r.text)
        return r.json()["detail"]["codigo"]

    def test_creatinina_zero_ou_negativa_nao_quebra(self):
        b = dict(BASE)
        del b["tfge"]
        for c in (0, -1, 50):
            r = self.c.post("/api/avaliacao", json=dict(b, creatinina=c))
            self.assertEqual(r.status_code, 422, "creatinina=%s → %s" % (c, r.status_code))

    def test_ldl_validado_no_servidor(self):
        self.assertEqual(self._codigo(ldl=500), "fora_da_faixa")
        self.assertEqual(self._codigo(ldl=190), "dado_invalido")  # não-HDL = 185

    def test_agravante_desconhecido_e_recusado(self):
        self.assertEqual(self._codigo(agravantes=["inventado"]), "dado_invalido")

    def test_agravante_feminino_em_homem_e_recusado(self):
        self.assertEqual(self._codigo(sexo="masculino", agravantes=["fator_especifico_mulher"]), "dado_invalido")

    def test_aterosclerose_subclinica_fora_do_escopo(self):
        self.assertEqual(self._codigo(aterosclerose_subclinica=True), "fora_do_escopo")

    def test_lpa_acima_de_180_alto(self):
        d = self.c.post("/api/avaliacao", json=dict(BASE, criterios_alto=["lpa_muito_elevada"])).json()
        self.assertEqual(d["categoria"], "alto")

    def test_ldl_exigido_com_nao_hdl_alto(self):
        # CT 300, HDL 45 → não-HDL 255: sem LDL, recusa (SBC §4.1; parecer de Cardiologia, M4)
        self.assertEqual(self._codigo(colesterol_total=300, hdl=45), "dado_ausente")

    def test_tfge_calculada_acima_de_140_e_limitada(self):
        b = dict(BASE, idade=30, sexo="masculino", creatinina=0.5)
        del b["tfge"]
        d = self.c.post("/api/avaliacao", json=b).json()
        self.assertEqual(d["tfge_usada"], 140)
        self.assertIn("considerada 140", d["origem_tfge"])

    def test_explicacao_exige_consentimento(self):
        r = self.c.post("/api/avaliacao/explicacao", json=BASE)
        self.assertEqual(r.status_code, 403)

    def test_gemini_gratuito_bloqueado_para_dados_reais(self):
        import os
        antes = {k: os.environ.get(k) for k in ("LLM_PROVEDOR", "LLM_MODELO", "LLM_PLANO_SEM_USO_DOS_DADOS")}
        os.environ.update(LLM_PROVEDOR="gemini", LLM_MODELO="qualquer")
        os.environ.pop("LLM_PLANO_SEM_USO_DOS_DADOS", None)
        try:
            self.assertFalse(self.c.get("/api/avaliacao/explicacao/provedor").json()["disponivel"])
            r = self.c.post("/api/avaliacao/explicacao", json=dict(BASE, consentimento_envio_llm=True))
            self.assertEqual(r.status_code, 503)
            self.assertIn("gratuito", r.json()["detail"])
        finally:
            for k, v in antes.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v

    def test_fluxo_legado_desligado(self):
        self.assertEqual(self.c.post("/predict", json={}).status_code, 404)
        self.assertEqual(self.c.post("/explanation/x", json={"explanation": "{}"}).status_code, 404)

    def test_cors_nao_aceita_qualquer_origem(self):
        r = self.c.options("/api/avaliacao", headers={"Origin": "https://exemplo.invalid",
                                                      "Access-Control-Request-Method": "POST"})
        self.assertNotEqual(r.headers.get("access-control-allow-origin"), "*")
        self.assertNotEqual(r.headers.get("access-control-allow-origin"), "https://exemplo.invalid")


if __name__ == "__main__":
    unittest.main()
