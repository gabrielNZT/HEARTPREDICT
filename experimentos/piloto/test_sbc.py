"""Testes das regras da Diretriz SBC 2025 (sbc.py, D010/D026). Rodar: python -m unittest test_sbc"""
import unittest

import prompt
import sbc
import gabarito
import vinhetas


class TestCategoria(unittest.TestCase):
    def test_cortes_no_valor_exibido(self):
        # 4,951% é exibido como "5,0%": a categoria tem de ser a de 5,0% (parecer de Engenharia/IHC).
        self.assertEqual(sbc.categoria(0.04951, {})[0], "intermediário")
        self.assertEqual(sbc.categoria(0.04949, {})[0], "baixo")
        self.assertEqual(sbc.categoria(0.19951, {})[0], "alto")

    def test_ldl_160_189_com_agravante_vira_alto(self):
        # Seção 4.1: LDL-c 160–189 "considerado intermediário"; Tabela 4.1: intermediário + agravante → alto.
        cat, regras = sbc.categoria(0.02, {"ldl": 170, "agravantes": ["sindrome_metabolica"]})
        self.assertEqual(cat, "alto")
        self.assertEqual(len(regras), 3)

    def test_ldl_190_alto(self):
        self.assertEqual(sbc.categoria(0.01, {"ldl": 190})[0], "alto")

    def test_lpa_acima_de_180_alto(self):
        self.assertEqual(sbc.categoria(0.01, {"criterios_alto": ["lpa_muito_elevada"]})[0], "alto")

    def test_agravante_sobe_uma(self):
        self.assertEqual(sbc.categoria(0.01, {"agravantes": ["transplante"]})[0], "intermediário")
        self.assertEqual(sbc.categoria(0.10, {"agravantes": ["transplante"]})[0], "alto")


class TestVinhetasEPrompt(unittest.TestCase):
    def test_ldl_nunca_maior_que_nao_hdl(self):
        for v in vinhetas.todas():
            p = v["paciente"]
            if p.get("ldl") is not None:
                self.assertLessEqual(p["ldl"], p["colesterol_total"] - p["hdl"], v["id"])

    def test_prompt_sem_ponto_decimal(self):
        # Nenhum número com ponto decimal (em pt-BR "1.567" se lê como milhar; parecer de IA).
        import re
        for v in vinhetas.todas():
            texto = prompt.construir(gabarito.montar(v))
            self.assertIsNone(re.search(r"(?<!Tabela )(?<!seção )\b\d+\.\d", texto), v["id"])
            self.assertIn("não entram no cálculo", texto)


if __name__ == "__main__":
    unittest.main()
