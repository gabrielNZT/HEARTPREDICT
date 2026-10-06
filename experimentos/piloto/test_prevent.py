"""Testes da calculadora contra o caso publicado no artigo do PREVENT (Khan et al. 2024, Results)."""

import math
import unittest

import prevent

# Mulher de 50 anos, CT 240, HDL 55, sem estatina, PAS tratada 160, sem diabetes,
# não fumante, IMC 35, TFGe 90 → DCV total 5,4%, DCVA 3,6%, IC 2,5%; fumante: 9,3%, 6,0%, 4,7%.
CASO_PUBLICADO = {
    "idade": 50, "sexo": "feminino", "colesterol_total": 240, "hdl": 55, "pas": 160,
    "anti_hipertensivo": 1, "estatina": 0, "diabetes": 0, "tabagismo": 0, "imc": 35, "tfge": 90,
}


class TestCasoPublicado(unittest.TestCase):
    def _pct(self, p, desfecho):
        return round(prevent.risco(p, desfecho) * 100, 1)

    def test_nao_fumante(self):
        self.assertEqual(self._pct(CASO_PUBLICADO, "ascvd"), 3.6)
        self.assertEqual(self._pct(CASO_PUBLICADO, "total_cvd"), 5.4)
        self.assertEqual(self._pct(CASO_PUBLICADO, "heart_failure"), 2.5)

    def test_fumante(self):
        p = dict(CASO_PUBLICADO, tabagismo=1)
        self.assertEqual(self._pct(p, "ascvd"), 6.0)
        self.assertEqual(self._pct(p, "total_cvd"), 9.3)
        self.assertEqual(self._pct(p, "heart_failure"), 4.7)


class TestShapley(unittest.TestCase):
    def test_eficiencia(self):
        # Propriedade de eficiência: soma das atribuições = L(paciente) - L(referência).
        phi = prevent.shapley(CASO_PUBLICADO)
        L = prevent.log_odds(prevent._para_modelo(CASO_PUBLICADO), "feminino")
        ref = dict(prevent.REFERENCIA, imc=CASO_PUBLICADO["imc"])
        L0 = prevent.log_odds(ref, "feminino")
        self.assertTrue(math.isclose(sum(phi.values()), L - L0, abs_tol=1e-9))

    def test_imc_nao_altera_risco_de_dcva(self):
        a = prevent.risco(dict(CASO_PUBLICADO, imc=22))
        b = prevent.risco(dict(CASO_PUBLICADO, imc=39))
        self.assertAlmostEqual(a, b, places=12)

    def test_tabagismo_aumenta(self):
        phi = prevent.shapley(dict(CASO_PUBLICADO, tabagismo=1))
        self.assertGreater(phi["tabagismo"], 0)


class TestValidacao(unittest.TestCase):
    def test_recusa_dado_ausente(self):
        p = dict(CASO_PUBLICADO)
        del p["tfge"]
        with self.assertRaises(prevent.EntradaInvalida):
            prevent.risco(p)

    def test_recusa_fora_da_faixa(self):
        with self.assertRaises(prevent.EntradaInvalida):
            prevent.risco(dict(CASO_PUBLICADO, pas=220))


if __name__ == "__main__":
    unittest.main()
