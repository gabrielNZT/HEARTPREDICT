"""
Testes da banca (engenharia) sobre o núcleo em experimentos/piloto.
NÃO fazem parte do projeto: foram escritos para caçar bugs.

Rodar da raiz do repositório:
    python3 -m unittest discover -s tcc/05-banca/anexos/engenharia -p "test_nucleo_*.py" -v

Só biblioteca padrão. Amostragem pseudoaleatória com semente fixa (reprodutível).
"""

import itertools
import math
import random
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "experimentos" / "piloto"))

import prevent  # noqa: E402
import prompt  # noqa: E402
import gabarito  # noqa: E402
import renal  # noqa: E402
import sbc  # noqa: E402

SEMENTE = 20260929
N_CASOS = 300


def paciente_aleatorio(rng):
    ct = rng.uniform(130, 320)
    hdl = rng.uniform(20, min(100, ct - 30))
    return {
        "idade": rng.randint(30, 79),
        "sexo": rng.choice(["feminino", "masculino"]),
        "colesterol_total": ct,
        "hdl": hdl,
        "pas": rng.uniform(90, 200),
        "anti_hipertensivo": rng.randint(0, 1),
        "estatina": rng.randint(0, 1),
        "diabetes": rng.randint(0, 1),
        "tabagismo": rng.randint(0, 1),
        "tfge": rng.uniform(15, 140),
        "imc": rng.uniform(18.5, 39.99),
    }


def shapley_por_permutacoes(p):
    """Implementação independente (definição por permutações, 9! = 362 880 ordens)."""
    x = prevent._para_modelo(p)
    V = prevent.VARIAVEIS
    cache = {}

    def v(conj):
        chave = frozenset(conj)
        if chave not in cache:
            z = dict(prevent.REFERENCIA)
            z["imc"] = x["imc"]
            for nome in conj:
                z[nome] = x[nome]
            cache[chave] = prevent.log_odds(z, p["sexo"])
        return cache[chave]

    phi = {k: 0.0 for k in V}
    n = 0
    for ordem in itertools.permutations(V):
        antes = []
        for nome in ordem:
            base = v(antes)
            antes.append(nome)
            phi[nome] += v(antes) - base
        n += 1
    return {k: s / n for k, s in phi.items()}


class TestPropriedadesShapley(unittest.TestCase):
    """Axiomas de Shapley (Lundberg & Lee 2017; Shapley 1953) em entradas aleatórias."""

    @classmethod
    def setUpClass(cls):
        rng = random.Random(SEMENTE)
        cls.casos = [paciente_aleatorio(rng) for _ in range(N_CASOS)]

    def test_eficiencia(self):
        for p in self.casos:
            phi = prevent.shapley(p)
            L = prevent.log_odds(prevent._para_modelo(p), p["sexo"])
            L0 = prevent.log_odds(dict(prevent.REFERENCIA, imc=p["imc"]), p["sexo"])
            self.assertTrue(math.isclose(sum(phi.values()), L - L0, abs_tol=1e-9), p)

    def test_jogador_nulo(self):
        # Variável igual à referência não recebe atribuição.
        for p in self.casos[:60]:
            q = dict(p, pas=130.0, tabagismo=0)
            phi = prevent.shapley(q)
            self.assertAlmostEqual(phi["pas"], 0.0, places=12)
            self.assertAlmostEqual(phi["tabagismo"], 0.0, places=12)

    def test_concorda_com_definicao_por_permutacoes(self):
        for p in self.casos[:3]:
            a = prevent.shapley(p)
            b = shapley_por_permutacoes(p)
            for k in prevent.VARIAVEIS:
                self.assertAlmostEqual(a[k], b[k], places=10, msg=(k, p))

    def test_risco_em_0_1_e_monotono_no_tabagismo(self):
        for p in self.casos:
            r0 = prevent.risco(dict(p, tabagismo=0))
            r1 = prevent.risco(dict(p, tabagismo=1))
            self.assertTrue(0 < r0 < 1 and 0 < r1 < 1)
            # Com o termo idade×tabagismo negativo, fumar pode reduzir o risco em idades altas?
            # Registrar, não afirmar: ver test_tabagismo_nunca_reduz abaixo.

    def test_tabagismo_nunca_reduz_risco_na_faixa(self):
        # Propriedade clínica esperada; o termo idade×tabagismo é negativo.
        piores = []
        for sexo in ("feminino", "masculino"):
            for idade in range(30, 80):
                p = dict(self.casos[0], sexo=sexo, idade=idade)
                if prevent.risco(dict(p, tabagismo=1)) <= prevent.risco(dict(p, tabagismo=0)):
                    piores.append((sexo, idade))
        self.assertEqual(piores, [])


class TestLimitesDeCategoria(unittest.TestCase):
    """Arredondamento exibido (1 casa) × corte aplicado ao valor não arredondado."""

    def test_existe_caso_exibido_5_0_mas_categoria_baixo(self):
        achado = None
        base = {"sexo": "masculino", "hdl": 44, "pas": 140, "anti_hipertensivo": 0, "estatina": 0,
                "diabetes": 0, "tabagismo": 0, "tfge": 95, "agravantes": []}
        for idade in range(55, 65):
            for ct10 in range(1300, 3200):
                p = dict(base, idade=idade, colesterol_total=ct10 / 10)
                r = prevent.risco(p) * 100
                if 4.95 <= r < 5.0:
                    achado = (p, r)
                    break
            if achado:
                break
        self.assertIsNotNone(achado, "nenhum caso encontrado na varredura")
        p, r = achado
        g = gabarito.montar({"id": "x", "paciente": p})
        print("\n  [limite] entrada=%s risco=%.4f%% exibido=%s categoria=%s regra=%r" % (
            {k: p[k] for k in ("idade", "colesterol_total")}, r, g["risco_pct"], g["categoria"], g["regras_aplicadas"][0]))
        # Documenta a inconsistência: exibe 5,0% e diz "baixo" (Tabela 4.1: baixo é < 5%).
        self.assertEqual(g["risco_pct"], 5.0)
        self.assertEqual(g["categoria"], "baixo")


class TestCasosDeBorda(unittest.TestCase):
    def test_creatinina_zero_levanta_valueerror_generico(self):
        with self.assertRaises(ValueError) as ctx:
            renal.tfge_ckd_epi_2021(0, 50, "feminino")
        self.assertNotIsInstance(ctx.exception, prevent.EntradaInvalida)

    def test_string_com_virgula_nao_vira_entrada_invalida(self):
        p = dict(paciente_aleatorio(random.Random(1)), pas="130,5")
        with self.assertRaises(TypeError):  # não é EntradaInvalida: o núcleo não valida tipos
            prevent.validar(p)

    def test_ldl_nan_quebra_o_prompt(self):
        p = dict(paciente_aleatorio(random.Random(2)), diabetes=0, agravantes=[], ldl=float("nan"))
        g = gabarito.montar({"id": "x", "paciente": p})  # passa: nenhuma regra de LDL dispara
        with self.assertRaises(ValueError):
            prompt.construir(g)  # "%d" % nan

    def test_agravante_desconhecido_quebra_o_prompt(self):
        p = dict(paciente_aleatorio(random.Random(3)), diabetes=0, agravantes=["inexistente"])
        g = gabarito.montar({"id": "x", "paciente": p})  # sbc ignora silenciosamente
        with self.assertRaises(KeyError):
            prompt.construir(g)

    def test_agravante_feminino_aceito_para_homem(self):
        p = dict(paciente_aleatorio(random.Random(4)), sexo="masculino", diabetes=0, idade=35,
                 colesterol_total=170, hdl=60, pas=115, anti_hipertensivo=0, tabagismo=0,
                 agravantes=["fator_especifico_mulher"])
        cat, regras = sbc.categoria(prevent.risco(p), p)
        self.assertEqual(cat, "intermediário")  # o núcleo não confere o sexo do agravante

    def test_idade_decimal_truncada_no_prompt(self):
        p = dict(paciente_aleatorio(random.Random(5)), idade=54.9, diabetes=0, agravantes=[])
        g = gabarito.montar({"id": "x", "paciente": p})
        self.assertIn("Idade: 54 anos", prompt.construir(g))

    def test_risco_minimo_e_maximo_da_faixa(self):
        baixo = {"idade": 30, "sexo": "feminino", "colesterol_total": 130, "hdl": 100, "pas": 110,
                 "anti_hipertensivo": 0, "estatina": 0, "diabetes": 0, "tabagismo": 0, "tfge": 110}
        alto = {"idade": 79, "sexo": "masculino", "colesterol_total": 320, "hdl": 20, "pas": 200,
                "anti_hipertensivo": 1, "estatina": 0, "diabetes": 0, "tabagismo": 1, "tfge": 15}
        rb, ra = prevent.risco(baixo) * 100, prevent.risco(alto) * 100
        print("\n  [faixa] risco mínimo aprox. %.3f%%, máximo aprox. %.1f%%" % (rb, ra))
        self.assertLess(rb, 0.5)  # exibido como 0,x% e "menos de 1 em 100"


if __name__ == "__main__":
    unittest.main()
