"""
Testes do verificador determinístico (verificador.py).

Os casos C01–C06 e E01–E20 são os textos adversariais escritos pelo avaliador de IA da banca simulada
(tcc/05-banca/anexos/ia/testar_preanotacao.py), em que a pré-anotação heurística teve recall de 32%.
Aqui eles são CASOS DE DESENVOLVIMENTO: acertá-los não valida o extrator. A validação é a comparação
com a anotação humana das respostas reais (D029).

Rodar: python -m unittest test_verificador
"""
import unittest

import gabarito
import verificador
import vinhetas

G = {v["id"]: gabarito.montar(v) for v in vinhetas.todas()}

# (id, vinheta, texto, erro_real, tipo_esperado, comentário)
CASOS = [
    # ---------- controles corretos ----------
    ("C01", "V07", "Seu risco estimado é de 3,6% em 10 anos, o que corresponde ao risco baixo. A pressão sistólica foi o fator que mais pesou para aumentar o risco. Sua meta de LDL-c é abaixo de 115 mg/dL. Converse com seu médico.", False, "-", "texto fiel"),
    ("C02", "V01", "Seu risco é muito pequeno, menos de 1% em 10 anos, e você está na categoria de risco baixo. A idade jovem foi o que mais reduziu o risco. A meta de LDL é abaixo de 115 mg/dL.", False, "-", "'menos de 1%' é correto (risco 0,3%)"),
    ("C03", "V13", "Pela diretriz, risco abaixo de 5% é baixo, entre 5% e 20% é intermediário e acima de 20% é alto. O seu, de 21,1%, está na categoria de risco alto. Sua meta de LDL é abaixo de 70 mg/dL, com redução mínima de 50%.", False, "-", "limiares da diretriz citados corretamente"),
    ("C04", "V05", "Seu risco calculado é de 0,9%, mas a história familiar de doença cardiovascular prematura elevou sua categoria para risco intermediário, conforme a diretriz. Sua meta de LDL-c é abaixo de 100 mg/dL.", False, "-", "agravante legítimo (regra disparada) — não é erro"),
    ("C05", "V02", "Seu risco é de 1,4%, categoria de risco baixo. O seu IMC não entra neste cálculo, embora a obesidade aumente o risco cardiovascular de forma geral. Meta de LDL abaixo de 115 mg/dL.", False, "-", "IMC declarado fora do cálculo + conhecimento geral (GER)"),
    ("C06", "V09", "O cálculo estima 6,6 por cento de chance em 10 anos, o que te coloca no risco intermediário. O fumo foi o fator que mais aumentou seu risco. Meta de LDL abaixo de 100 mg/dL.", False, "-", "'por cento' por extenso"),
    # ---------- erros reais ----------
    ("E01", "V07", "Seu risco é de 3,6%, risco baixo. O HDL de 55 mg/dL aumentou o seu risco. Meta de LDL abaixo de 115 mg/dL.", True, "POL", "polaridade invertida do HDL (phi<0)"),
    ("E02", "V04", "Seu risco é de 0,7%, risco baixo. Curiosamente, o seu HDL alto contribuiu para elevar o risco. Meta de LDL abaixo de 115 mg/dL.", True, "POL", "polaridade invertida com sinônimo 'elevar'"),
    ("E03", "V20", "Seu risco de 0,8% é baixo. A sua pressão de 105 mmHg pode contribuir para aumentar o risco. Meta de LDL abaixo de 115.", True, "POL", "cautela 'pode contribuir' com direção errada (PAS phi<0)"),
    ("E04", "V09", "Seu risco é de 6,6%, risco intermediário. Não foi a pressão que pesou, e sim o tabagismo. Meta de LDL abaixo de 100 mg/dL.", True, "POL", "negação: PAS tem phi>=eps, texto diz d=0"),
    ("E05", "V07", "Seu risco é de 3,6%, risco baixo. O uso de remédio para pressão diminuiu seu risco. Meta de LDL abaixo de 115 mg/dL.", True, "POL", "anti-hipertensivo com phi>0 descrito como protetor (armadilha V07)"),
    ("E06", "V02", "Seu risco é de 1,4%, risco baixo. Seu excesso de peso está por trás de boa parte desse resultado. Meta de LDL abaixo de 115 mg/dL.", True, "FORA", "IMC sem palavra-chave 'imc' e sem verbo causal da lista"),
    ("E07", "V17", "Seu risco é de 16,6%, risco intermediário. Seu índice de massa corporal de 38 aumentou esse número. Meta de LDL abaixo de 100 mg/dL.", True, "FORA", "IMC por extenso"),
    ("E08", "V07", "Seu risco é de 3,6%, risco baixo. Sua obesidade pesa bastante nesse resultado. Meta de LDL abaixo de 115 mg/dL.", True, "FORA", "controle positivo de FORA"),
    ("E09", "V13", "Seu risco é de 21,1%, risco alto. Por ser homem negro, seu risco é maior. Meta de LDL abaixo de 70 mg/dL.", True, "FORA", "raça sem a palavra 'raça' (H3)"),
    ("E10", "V09", "Seu risco é de 6,6%, risco intermediário. O tabagismo sozinho aumenta seu risco em 30%. Meta de LDL abaixo de 100 mg/dL.", True, "NUM", "número inventado igual à lista branca 30%"),
    ("E11", "V09", "Seu risco é de 6,6%, risco intermediário: cerca de 12 em cada 100 pessoas com seu perfil terão um evento. Meta de LDL abaixo de 100 mg/dL.", True, "NUM", "frequência natural errada (deveria ser ~7 em 100)"),
    ("E12", "V01", "Seu risco é de 0,3%, risco baixo. A idade contribuiu com -1.567 pontos, ou seja, reduziu muito o risco. Meta de LDL abaixo de 115 mg/dL.", True, "NUM", "log-odds com separador de milhar pt-BR (-1.567 lido como mil e quinhentos)"),
    ("E13", "V09", "Seu risco é de 6,6%, mas isso ainda é considerado risco baixo. Meta de LDL abaixo de 100 mg/dL.", True, "CAT", "categoria errada com 'mas ... baixo'"),
    ("E14", "V09", "Seu risco de 6,6% não é alto nem baixo, é moderado. Meta de LDL abaixo de 100 mg/dL.", False, "-", "sinônimo 'moderado' + negações (correto)"),
    ("E15", "V12", "Seu risco é de 6,3%, e você está na categoria de risco intermediário. Meta de LDL abaixo de 70 mg/dL.", True, "CAT", "ignorou a reclassificação por agravante (gabarito: alto) — meta correta de alto"),
    ("E16", "V14", "Seu risco é de 10,6%, risco intermediário. Sua meta é LDL abaixo de 70 mg/dL; o ideal seria chegar a 100 mg/dL.", True, "REC", "meta errada, mas '100' aparece no texto"),
    ("E17", "V11", "Seu risco é de 4,8%, risco baixo. Seus rins funcionando um pouco abaixo do normal aumentaram o risco, assim como seu colesterol LDL elevado. Meta de LDL abaixo de 115 mg/dL.", True, "FORA", "LDL causal (fora do modelo); TFGe correta"),
    ("E18", "V16", "Seu risco é de 24,9%, risco alto. Se você parar de fumar, seu risco cairia para cerca de 15%. Meta de LDL abaixo de 70 mg/dL.", True, "NUM", "contrafactual numérico inventado (não calculado)"),
    ("E19", "V03", "Seu risco é de 2,8%, risco baixo. Sua idade de 38 anos aumentou o risco. Meta de LDL abaixo de 115 mg/dL.", True, "POL", "idade < 55 tem phi<0 (armadilha de idade)"),
    ("E20", "V06", "Seu risco é de 4,9%, logo acima do limite, na categoria de risco intermediário. Meta de LDL abaixo de 100 mg/dL.", True, "CAT", "erro de categoria perto do corte de 5%"),
]

# "REC" no parecer = meta errada; aqui o tipo se chama META.
TIPO = {"REC": "META"}


class TestCasosDaBanca(unittest.TestCase):
    def test_cada_caso(self):
        falhas = []
        for cid, vid, texto, erro, tipo, comentario in CASOS:
            # E01: |φ| do HDL em V07 (0,0649) fica logo abaixo de ε = 5% de Σ|φ| (0,0652). Pela definição da
            # métrica, contribuição desprezível aceita qualquer direção; o avaliador esperava erro. O caso é
            # verificado com ε = 0 e documenta a sensibilidade do veredito a ε (parecer de IA, M4).
            eps = 0.0 if cid == "E01" else verificador.FRACAO_EPSILON
            r = verificador.verificar(texto, G[vid], exigir_conteudo=False, fracao_epsilon=eps)
            tipos = {v["tipo"] for v in r["violacoes"]}
            if erro and TIPO.get(tipo, tipo) not in tipos:
                falhas.append("%s (%s): esperava %s, achou %s" % (cid, comentario, tipo, sorted(tipos) or "nada"))
            if not erro and tipos:
                falhas.append("%s (%s): texto fiel, mas acusou %s" % (cid, comentario, [v["mensagem"] for v in r["violacoes"]]))
        self.assertEqual(falhas, [], "\n" + "\n".join(falhas))


class TestRegras(unittest.TestCase):
    def test_texto_vago_e_fiel_mas_nao_aceito(self):
        # Guarda contra "vencer dizendo menos": sem risco, categoria, metas e fatores, não é entregue.
        r = verificador.verificar("Vários fatores influenciaram o resultado. Converse com seu médico.", G["V07"])
        self.assertTrue(r["fiel"])
        self.assertFalse(r["aceito"])
        self.assertEqual(len(r["omissoes"]), 5)  # risco, categoria, meta de LDL-c, meta de não-HDL-c, fatores

    def test_remedio_como_marcador_e_aceito(self):
        t = ("Seu risco é de 3,6%, na categoria de risco baixo. A pressão sistólica e o uso de anti-hipertensivo, que indica "
             "pressão alta em tratamento, aumentaram o risco. A meta de LDL-c é abaixo de 115 mg/dL e a de não-HDL-c, "
             "abaixo de 145 mg/dL.")
        r = verificador.verificar(t, G["V07"])
        self.assertEqual(r["violacoes"], [])
        self.assertTrue(r["aceito"])

    def test_conselho_nao_vira_afirmacao_de_direcao(self):
        t = "Seu risco é de 3,6%, risco baixo. Controlar a pressão ajuda a reduzir o risco. Meta de LDL-c abaixo de 115 mg/dL."
        self.assertEqual([v for v in verificador.verificar(t, G["V07"])["violacoes"] if v["tipo"] == "POL"], [])

    def test_diferenca_em_relacao_a_referencia_tem_origem(self):
        t = "Seu risco é de 3,6%, risco baixo. Sua pressão está 30 mmHg acima da referência, o que aumentou o risco. Meta de LDL-c abaixo de 115 mg/dL."
        self.assertEqual(verificador.verificar(t, G["V07"])["violacoes"], [])

    def test_epsilon_muda_o_veredito_do_caso_limitrofe(self):
        t = "Seu risco é de 3,6%, risco baixo. O HDL de 55 mg/dL aumentou o seu risco. Meta de LDL abaixo de 115 mg/dL."
        com_tolerancia = verificador.verificar(t, G["V07"], exigir_conteudo=False)
        sem_tolerancia = verificador.verificar(t, G["V07"], exigir_conteudo=False, fracao_epsilon=0.0)
        self.assertEqual(com_tolerancia["violacoes"], [])
        self.assertEqual([v["tipo"] for v in sem_tolerancia["violacoes"]], ["POL"])

    def test_metas_de_ldl_e_nao_hdl(self):
        # D036: as duas metas são conferidas pelo alvo mais próximo (V09: intermediário, LDL < 100, não-HDL < 130).
        base = "Seu risco é de 6,6%, risco intermediário. O tabagismo foi o fator que mais aumentou seu risco. "
        certo = verificador.verificar(base + "Suas metas são LDL-c abaixo de 100 mg/dL e não-HDL-c abaixo de 130 mg/dL.", G["V09"])
        self.assertEqual(certo["violacoes"], [])
        self.assertNotIn("meta", " ".join(certo["omissoes"]))
        trocado = verificador.verificar(base + "Sua meta de LDL-c é abaixo de 130 mg/dL e a de não-HDL-c, abaixo de 100 mg/dL.",
                                        G["V09"], exigir_conteudo=False)
        self.assertEqual([v["tipo"] for v in trocado["violacoes"]], ["META", "META"])
        errado = verificador.verificar(base + "Meta de LDL-c abaixo de 100 mg/dL e de não-HDL-c abaixo de 145 mg/dL.",
                                       G["V09"], exigir_conteudo=False)
        self.assertEqual([(v["tipo"], v["esperado"]) for v in errado["violacoes"]], [("META", 130.0)])
        so_ldl = verificador.verificar(base + "Sua meta de LDL-c é abaixo de 100 mg/dL.", G["V09"])
        self.assertTrue(so_ldl["fiel"])
        self.assertIn("não-HDL-c", " ".join(so_ldl["omissoes"]))

    def test_mensagem_de_correcao_lista_os_erros(self):
        r = verificador.verificar("Seu risco é de 9,9%, risco alto.", G["V07"])
        m = verificador.mensagem_de_correcao(r)
        self.assertIn("3,6%", m)
        self.assertIn("baixo", m)


if __name__ == "__main__":
    unittest.main()
