"""
Verificador determinístico de fidelidade (nível 1), independente do LLM explicador (D034).

Entrada: o texto da explicação e o pacote de referência do caso (gabarito.montar).
Saída: dicionário com `aceito`, a lista de `violacoes` (cada uma com tipo, trecho e uma mensagem
de correção), as `omissoes` de conteúdo obrigatório, as afirmações extraídas e a `cobertura`.

Definições: tcc/03-metodologia/metricas-fidelidade.md.
  POL   polaridade por variável (§3)        NUM   exatidão numérica (§4)
  FORA  variável fora do modelo (§5)        CAT   categoria de risco
  META  meta de LDL-c / não-HDL-c

Limites (declarar no texto do TCC):
- A extração é por regras (glossário + léxico). Ela erra com paráfrases que o léxico não cobre.
  Sensibilidade e especificidade têm de ser medidas contra a anotação humana (D029).
- Os 26 textos adversariais do parecer de IA foram usados como casos de desenvolvimento
  (test_verificador.py). Acertá-los não valida o extrator.
- O extrator usado na avaliação final tem de ser outro (brecha B1).
"""

import re
import unicodedata

import prevent

VERSAO = "verificador-v2"  # v2 (D036): meta de não-HDL-c conferida e exigida, como a de LDL-c
FRACAO_EPSILON = 0.05  # ε = 5% de Σ|φ| (metricas-fidelidade.md §3.3)

# ---------------------------------------------------------------- glossário (ordem = prioridade)
# Padrões mais específicos primeiro: cada trecho casado é mascarado e não casa de novo.
FORA_DO_MODELO = [
    ("IMC/peso", r"\bimc\b|indice de massa corp\w+|excesso de peso|sobrepeso|\bobes\w+|\bpeso\b"),
    ("raça/cor", r"\braca\b|\betnia\w*|cor da pele|\bnegr[oa]s?\b|\bpard[oa]s?\b|\bbranc[oa]s?\b|\bindigenas?\b"
                 r"|\bamarel[oa]s?\b|\bafrodescend\w+"),
    ("LDL", r"\bldl(-c)?\b|colesterol ruim"),
    ("história familiar", r"historia familiar|historico familiar|\bfamiliar(es)?\b|\bgenetic\w+|\bhereditar\w+"),
    ("triglicérides", r"\btriglic\w+"),
    ("lipoproteína(a)", r"lipoproteina ?\(a\)|\blp ?\(a\)"),
    ("PCR", r"\bpcr\b|proteina c reativa"),
    ("estilo de vida", r"\bsedentar\w+|\bdieta\b|\balimentac\w+|\bestresse\b|\balcool\b|atividade fisica|\bexercicio\w*"),
]
MODELO = [
    ("anti_hipertensivo", r"anti-?hipertensiv\w+|(remedio|medica\w+|comprimido)s? (para|de|da|pra) (a )?(pressao|hipertensao)"
                          r"|hipertensao (em tratamento|tratada)|tratamento (para|da|de) (a )?(pressao|hipertensao)"),
    ("estatina", r"\bestatinas?\b|(remedio|medica\w+)s? (para|de|do|pra) (o )?colesterol"),
    ("hdl", r"\bhdl(-c)?\b|colesterol bom"),
    ("nao_hdl", r"nao-?hdl(-c)?|colesterol total|\bcolesterol\b"),
    ("pas", r"pressao( arterial)?( sistolica)?|\bsistolica\b|\bhipertensao\b"),
    ("tabagismo", r"\btabag\w+|\bfum\w+|\bcigarr\w+"),
    ("tfge", r"\btfge?\b|funcao (renal|dos rins)|\brins\b|\brenal\b|filtracao"),
    ("diabetes", r"\bdiabet\w+"),
    ("idade", r"\bidade\b|mais jovem|mais velh\w+|\benvelhec\w+"),
]
NOMES = {
    "idade": "idade", "nao_hdl": "colesterol não-HDL", "hdl": "HDL", "pas": "pressão sistólica",
    "anti_hipertensivo": "uso de anti-hipertensivo", "estatina": "uso de estatina", "diabetes": "diabetes",
    "tabagismo": "tabagismo", "tfge": "função renal (TFGe)",
}

# ---------------------------------------------------------------- léxico de direção
MAIS = (r"\baument\w+|\belev(a|am|ou|aram|ar|ando|aria|e|em)\b|\bpior\w+|para cima|\bagrav(a|am|ou|aram|ar)\b"
        r"|risco (e|fica|ficou|seja|esta) (um pouco |muito |bem )?(maior|mais alto)|\bsob(e|em|iu|iram)\b"
        r"|\bdesfavor\w+|\bprejudic\w+|\bcontra voce\b")
MENOS = (r"\breduz\w*|\bredu(cao|ziu|ziram)\b|\bdiminu\w+|\bproteg\w+|\bprotetor\w*|\bprotec\w+|para baixo|\babaix\w+"
         r"|\batenu\w+|\bbenefic\w+|a seu favor|risco (e|fica|ficou|seja|esta) (um pouco |muito |bem )?(menor|mais baixo)"
         r"|\bfavorec\w+|\bfavorav\w+|\bajud\w+")
PESO = r"\bpes(a|am|ou|aram|ando)\b|\bcontribu\w+|\binfluenc\w+|\bimpact\w+|por tras|\bexplic(a|am|ou)\b|\bdetermin\w+"
CAUSA = MAIS + "|" + MENOS + "|" + PESO + r"|\bpor ser\b|\bpor causa\b|\bdevido\b|\bdeve-se\b|\bem razao\b|\bgracas\b"
NEGACAO = r"\bnao (foi|e|sao|foram|teve|tem|houve)\b|\bnao (pes|contribu|influenc|aument|reduz|diminu|alter)\w+|\bsem (efeito|influencia|impacto)\b|\bneutr[oa]\b|praticamente nao|quase nao|pouco (influenc|pes|contribu|alter)\w+"
# Trechos que não afirmam nada sobre o cálculo: conselho, condição hipotética, conhecimento geral.
NAO_AFIRMA = (r"\bcontrol\w+|\bmant(er|enha|endo|em)\b|\bpar(ar|e|ando) de\b|\bdeix(ar|e) de\b|\bse voce\b|\bcaso voce\b|\bcaso\b"
              r"|\bimportante\b|\brecomend\w+|\bconvers\w+|\bacompanh\w+|\bcuid\w+|\badot\w+|\bhabit\w+|estilo de vida"
              r"|\bprocur\w+|\bpode(ra|ria|m)? ajudar\b|\bcontinu\w+|\bmelhorar\b|\bevit\w+|\bbusc\w+|\bconsult\w+")
GERAL = r"de (forma|modo|maneira) geral|\bem geral\b|na populacao|\bgeralmente\b|\bcostuma\w*\b|de modo amplo"
EXCLUI = (r"nao (entra|entram|faz parte|fazem parte|e usad[oa]|sao usad[oa]s|foi considerad[oa]|foram considerad[oa]s"
          r"|e considerad[oa]|participa|participam|influenci\w+|pes\w+|cont\w+|interfer\w+|e levad[oa]|sao levad[oa]s)")
ALVO_CATEGORIA = r"\bcategoria\b|\bclassific\w+|\breclassific\w+|\bdiretriz\b|\bagravante\w*|\bmetas?\b|\bpassa (a|para)\b"

CATEGORIAS = {"baixo": "baixo", "baixa": "baixo", "intermediario": "intermediário", "intermediaria": "intermediário",
              "moderado": "intermediário", "moderada": "intermediário", "medio": "intermediário", "alto": "alto",
              "alta": "alto", "elevado": "alto"}
CAT_RE = (r"(?:risco|categoria)(?: de risco)?(?: cardiovascular)?(?: (?:e|foi|fica|esta|seja|como|considerado|considerada"
          r"|classificado|classificada|classifica-se|se classifica|ainda|de|na|no|em|um|uma|nivel|faixa)){0,5} "
          r"(baixo|baixa|intermediario|intermediaria|moderado|moderada|medio|alto|alta|elevado)\b")
NUMERO = r"(?<![\w,.])-?\d+(?:\.\d{3})*(?:,\d+)?(?![\w]|,\d)"
# Números que não precisam de origem no pacote de referência.
NUMEROS_LIVRES = {10.0, 100.0, 1000.0, 2025.0, 1.73}


def _sem_acento(t):
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[‐-―−]", "-", t).replace(" ", " ").replace(" ", " ").lower()


def _num(txt):
    """Número no formato brasileiro: '1.234,5' → 1234.5. Ponto com 3 dígitos é milhar."""
    return float(txt.replace(".", "").replace(",", "."))


def _trechos(texto):
    """Divide o texto em orações curtas. Devolve [(original, normalizado)]."""
    partes = re.split(r"(?<=[.!?;:])\s+|\s+(?:mas|porem|contudo|entretanto|enquanto|ja|por outro lado|em contrapartida"
                      r"|por sua vez|no entanto|embora|apesar de)\s+", texto.replace("\n", " "),
                      flags=re.IGNORECASE)
    # "3.6%" (decimal com ponto, 1 ou 2 casas) é lido como 3,6; ponto + 3 dígitos continua sendo milhar.
    return [(p.strip(), re.sub(r"(\d)\.(\d{1,2})(?!\d)", r"\1,\2", _sem_acento(p.strip())))
            for p in partes if p and p.strip()]


def _mencoes(norm, glossario):
    """Casamentos (variável, início, fim), mascarando cada trecho casado para os padrões seguintes."""
    achados, buf = [], list(norm)
    for var, padrao in glossario:
        for m in re.finditer(padrao, "".join(buf)):
            achados.append((var, m.start(), m.end()))
            for i in range(m.start(), m.end()):
                buf[i] = "#"
    return achados, "".join(buf)


def _direcao_mais_proxima(norm, pos):
    """
    Direção da pista mais próxima da posição: +1, -1 ou 'peso' (influencia, sem sinal).
    Uma direção explícita a até 60 caracteres vence a pista de peso: em "contribuiu para elevar",
    o que vale é "elevar".
    """
    def mais_proxima(pares):
        melhor = None
        for rotulo, padrao in pares:
            for m in re.finditer(padrao, norm):
                d = min(abs(m.start() - pos), abs(m.end() - pos))
                if melhor is None or d < melhor[0]:
                    melhor = (d, rotulo, m.group(0))
        return melhor

    explicita = mais_proxima(((1, MAIS), (-1, MENOS)))
    if explicita and explicita[0] <= 60:
        return explicita
    return mais_proxima((("peso", PESO),)) or explicita


def _fmt(v, casas=None):
    if casas is None:
        casas = 0 if float(v).is_integer() else 1
    return ("%.*f" % (casas, v)).replace(".", ",")


def _origens_numericas(g):
    """Valores que um número do texto pode legitimamente reproduzir (origem → valor)."""
    p = g["entradas"]
    nao_hdl = p["colesterol_total"] - p["hdl"]
    o = {
        "idade": p["idade"], "colesterol total": p["colesterol_total"], "HDL": p["hdl"], "não-HDL": nao_hdl,
        "pressão sistólica": p["pas"], "TFGe": p["tfge"],
        "idade de referência": 55, "não-HDL de referência": 135, "HDL de referência": 50,
        "pressão de referência": 130, "TFGe de referência": 90,
        "diferença de idade": abs(p["idade"] - 55), "diferença de não-HDL": abs(nao_hdl - 135),
        "diferença de HDL": abs(p["hdl"] - 50), "diferença de pressão": abs(p["pas"] - 130),
        "diferença de TFGe": abs(p["tfge"] - 90),
        "meta de LDL": _num(re.sub(r"[^\d,.]", "", g["metas"]["ldl"])),
        "meta de não-HDL": _num(re.sub(r"[^\d,.]", "", g["metas"]["nao_hdl"])),
        "redução mínima de LDL": _num(re.sub(r"[^\d,.]", "", g["metas"]["reducao_ldl"])),
        "corte 5%": 5, "corte 20%": 20, "LDL 160": 160, "LDL 189": 189, "LDL 190": 190, "LDL 145": 145,
    }
    if p.get("ldl") is not None:
        o["LDL"] = p["ldl"]
    if p.get("imc") is not None:
        o["IMC"] = p["imc"]
    for var, phi in g["atribuicao"].items():
        o["contribuição de " + var] = round(abs(phi), 2)
    return o


def _alvo_da_meta(antes, depois):
    """A qual meta o número se refere: a menção de LDL ou de não-HDL mais próxima antes dele; senão, a primeira depois."""
    ultimas = {alvo: max((m.end() for m in re.finditer(padrao, antes)), default=-1)
               for alvo, padrao in (("meta de LDL", r"\bldl"), ("meta de não-HDL", r"nao-?hdl"))}
    if max(ultimas.values()) >= 0:
        return max(ultimas, key=ultimas.get)
    if re.search(r"^\W*(mg/dl)?\W*(de |do |para o |para )?(colesterol )?nao-?hdl", depois):
        return "meta de não-HDL"
    return "meta de LDL"


def verificar(texto, g, exigir_conteudo=True, fracao_epsilon=FRACAO_EPSILON):
    violacoes, afirmacoes, omissoes = [], [], []
    risco = g["risco_pct"]
    soma = sum(abs(v) for v in g["atribuicao"].values()) or 1.0
    eps = fracao_epsilon * soma
    origens = _origens_numericas(g)
    agravantes = set(g["entradas"].get("agravantes") or [])
    regra_ldl = any("LDL-c" in r for r in g["regras_aplicadas"][1:])
    categoria_do_escore = "baixo" if risco < 5 else ("intermediário" if risco < 20 else "alto")
    direcoes_ditas = {}  # variável → conjunto de direções afirmadas (para a cobertura)
    citou = {"risco": False, "categoria": False, "meta de LDL": False, "meta de não-HDL": False}

    def violar(tipo, trecho, mensagem, **extra):
        violacoes.append(dict(tipo=tipo, trecho=trecho, mensagem=mensagem, **extra))

    for original, norm in _trechos(texto):
        fora, mascarado = _mencoes(norm, FORA_DO_MODELO)
        modelo, _ = _mencoes(mascarado, MODELO)
        tem_causa = re.search(CAUSA, norm) is not None
        nao_afirma = re.search(NAO_AFIRMA, norm) is not None
        alvo_categoria = re.search(ALVO_CATEGORIA, norm) is not None

        # ---------------- FORA: variável que não entra no cálculo apresentada como causa do risco
        for var, ini, _fim in fora:
            if not tem_causa or nao_afirma or re.search(GERAL, norm) or re.search(EXCLUI, norm):
                continue
            # Alvo "categoria" (§5.2): agravante informado ou regra do LDL explicam a categoria, não o número.
            if alvo_categoria and ((var == "história familiar" and "historia_familiar_prematura" in agravantes)
                                   or (var == "LDL" and (regra_ldl or g["entradas"].get("ldl") is not None))
                                   or (var == "lipoproteína(a)" and "lpa_elevada" in agravantes)
                                   or (var == "PCR" and "pcr_us_elevada" in agravantes)):
                continue
            if var == "LDL" and re.search(r"\bmetas?\b|\balvo\b|\bobjetivo\b", norm):
                continue
            afirmacoes.append(dict(tipo="FORA", variavel=var, trecho=original))
            violar("FORA", original, "O texto apresenta %s como causa do risco calculado, mas essa informação não entra "
                   "no cálculo. Retire a relação de causa ou diga que ela não faz parte do cálculo." % var, variavel=var)

        # ---------------- POL: direção atribuída a cada variável do modelo
        if tem_causa and not nao_afirma and not re.search(GERAL, norm):
            for var, ini, fim in modelo:
                pista = _direcao_mais_proxima(norm, (ini + fim) // 2)
                if pista is None:
                    continue
                _, d, palavra = pista
                if re.search(NEGACAO, norm):
                    d = 0
                phi = g["atribuicao"].get(var, 0.0)
                afirmacoes.append(dict(tipo="DIR", variavel=var, direcao=d, trecho=original))
                direcoes_ditas.setdefault(var, set()).add(d)
                if abs(phi) < eps:
                    continue  # contribuição desprezível: qualquer direção é aceita
                esperado = 1 if phi > 0 else -1
                if d == "peso" or d == esperado:
                    continue
                if d == 0:
                    msg = "O texto diz que %s não influenciou, mas esse fator %s o risco em relação à pessoa de referência." % (
                        NOMES[var], "aumentou" if esperado > 0 else "diminuiu")
                else:
                    msg = "O texto diz que %s %s o risco, mas no cálculo esse fator %s o risco em relação à pessoa de referência." % (
                        NOMES[var], "aumentou" if d > 0 else "diminuiu", "aumentou" if esperado > 0 else "diminuiu")
                violar("POL", original, msg, variavel=var, encontrado=d, esperado=esperado)

        # ---------------- CAT: categoria afirmada
        sem_negadas = re.sub(r"\bnao (e|esta|fica|seria)( considerad[oa])?[^,.;]*?(,|;|$)", " ", norm)
        citadas = [CATEGORIAS[m.group(1)] for m in re.finditer(CAT_RE, sem_negadas)]
        definicao = len(set(citadas)) >= 2 and len(re.findall(r"\d+ ?%", norm)) >= 2
        hipotetico = re.search(r"\bseria\b|pelo (calculo|escore|numero)|apenas pel[oa]|sozinh[oa]|\bantes\b|inicialmente|\bde (baixo|intermediario|alto) para\b", norm)
        if citadas and not definicao:
            citou["categoria"] = True
            for c in set(citadas):
                afirmacoes.append(dict(tipo="CAT", valor=c, trecho=original))
                if c == g["categoria"] or (hipotetico and c == categoria_do_escore):
                    continue
                violar("CAT", original, "O texto indica categoria de risco %s, mas a categoria pela diretriz é %s." % (
                    c, g["categoria"]), encontrado=c, esperado=g["categoria"])

        # ---------------- NUM e META: todo número precisa ter origem
        em_meta = re.search(r"\bmetas?\b|\balvo\b|\bobjetivo\b|\bideal\b", norm) is not None
        for m in re.finditer(NUMERO, norm):
            bruto = m.group(0)
            apos = norm[m.end():m.end() + 28]
            antes = norm[max(0, m.start() - 30):m.start()]
            # Ponto seguido de 3 dígitos lê-se como milhar em pt-BR: número sem origem possível.
            try:
                v = abs(_num(bruto))
            except ValueError:
                continue
            casas = len(bruto.split(",")[1]) if "," in bruto else 0
            percentual = re.match(r"\s*(%|por cento)", apos) is not None
            frequencia = re.match(r"\s*(pessoas? )?(em|a|de) (cada |um grupo de |grupo de )?(100|1\.?000)\b", apos)
            tol = lambda ref: max(0.05 * abs(ref), 0.5 * 10 ** (-casas))  # noqa: E731

            if frequencia:
                base = 100.0 if frequencia.group(4) == "100" else 1000.0
                esperado = risco * base / 100.0
                afirmacoes.append(dict(tipo="NUM", valor=v, trecho=original))
                if abs(v - esperado) > max(0.5, 0.05 * esperado):
                    violar("NUM", original, "O texto diz %s em %s pessoas, mas o risco calculado é %s%% (cerca de %s em %s)." % (
                        bruto, _fmt(base), _fmt(risco, 1), _fmt(round(esperado)), _fmt(base)), encontrado=v, esperado=esperado)
                else:
                    citou["risco"] = True
                continue
            # 100 é número livre ("em 100 pessoas"), mas também é meta (LDL-c do intermediário, não-HDL-c do alto).
            if v in NUMEROS_LIVRES and not percentual and not (em_meta and v in (origens["meta de LDL"], origens["meta de não-HDL"])):
                continue

            if percentual:
                afirmacoes.append(dict(tipo="NUM", valor=v, trecho=original))
                comparador = re.search(r"(menos de|menor que|abaixo de|inferior a|ate|mais de|maior que|acima de|superior a)\s*$", antes)
                if abs(v - risco) <= tol(risco):
                    citou["risco"] = True
                    continue
                if comparador and ((comparador.group(1) in ("menos de", "menor que", "abaixo de", "inferior a", "ate") and risco < v)
                                   or (comparador.group(1) in ("mais de", "maior que", "acima de", "superior a") and risco > v)):
                    if v not in (5.0, 20.0):
                        citou["risco"] = True
                    continue
                if v in (5.0, 20.0) and re.search(r"\bcorte\b|\blimi\w+|\bfaixa\b|\bentre\b|abaixo de|acima de|menos de|mais de|a partir de|\bate\b", norm):
                    continue
                if v == origens["redução mínima de LDL"] and re.search(r"\bredu\w+|\bdiminu\w+|\bbaixar\b", norm) and re.search(r"\bldl|\bcolesterol|\bmetas?\b", norm):
                    continue
                violar("NUM", original, "O texto cita %s%%, que não corresponde ao risco calculado (%s%%) nem a outro valor "
                       "fornecido. Use só os números fornecidos." % (bruto, _fmt(risco, 1)), encontrado=v, esperado=risco)
                continue

            # Meta de colesterol: o número ligado a "meta" tem de ser o da categoria.
            if em_meta and re.match(r"\s*(mg|$|[.,;)]|\s*e\b)", apos) and 30 <= v <= 200 and not re.search(r"\banos\b|mmhg", apos):
                afirmacoes.append(dict(tipo="META", valor=v, trecho=original))
                alvo = _alvo_da_meta(norm[max(0, m.start() - 60):m.start()], norm[m.end():m.end() + 25])
                outra = "meta de LDL" if alvo == "meta de não-HDL" else "meta de não-HDL"
                valores_do_paciente = ({origens.get("LDL")} - {None}) | {
                    origens["não-HDL"], origens["colesterol total"], origens["HDL"], 160.0, 190.0}
                if v == origens[alvo]:
                    citou[alvo] = True
                    continue
                # Valor do próprio paciente, ou o limiar de LDL-c de 145 mg/dL do risco baixo (Tabela 5.1, nota),
                # citado na frase da meta. 145 também é a meta de não-HDL-c do risco baixo: só vale no alvo LDL.
                if v != origens[outra] and (v in valores_do_paciente or (v == 145.0 and alvo == "meta de LDL")):
                    continue
                rotulo = "LDL-c" if alvo == "meta de LDL" else "não-HDL-c"
                violar("META", original, "O texto cita %s mg/dL como meta de %s, mas a meta de %s para a categoria %s é %s mg/dL." % (
                    bruto, rotulo, rotulo, g["categoria"], g["metas"]["ldl" if alvo == "meta de LDL" else "nao_hdl"]),
                    encontrado=v, esperado=origens[alvo])
                continue

            if any(abs(v - ref) <= tol(ref) for ref in origens.values()):
                continue
            if v < 10 and casas == 0 and not re.match(r"\s*(mg|mmhg|ml|anos|pontos?|vezes)", apos):
                continue  # ordinais e contagens pequenas ("os 3 fatores", "2 medidas")
            afirmacoes.append(dict(tipo="NUM", valor=v, trecho=original))
            violar("NUM", original, "O texto cita o número %s, que não está entre os valores fornecidos. Use só os números "
                   "fornecidos e não calcule valores novos." % bruto, encontrado=v)

    # ---------------- Cobertura (§6b) e conteúdo obrigatório
    principais = [v for v in g["ranking"] if abs(g["atribuicao"][v]) >= eps][:3]
    certas = [v for v in principais
              if (1 if g["atribuicao"][v] > 0 else -1) in direcoes_ditas.get(v, ()) or "peso" in direcoes_ditas.get(v, ())]
    cobertura = (len(certas) / len(principais)) if principais else None
    if exigir_conteudo:
        if not citou["risco"]:
            omissoes.append("O texto não informa o risco calculado (%s%%)." % _fmt(risco, 1))
        if not citou["categoria"]:
            omissoes.append("O texto não informa a categoria de risco (%s)." % g["categoria"])
        if not citou["meta de LDL"]:
            omissoes.append("O texto não informa a meta de LDL-c (%s mg/dL)." % g["metas"]["ldl"])
        if not citou["meta de não-HDL"]:
            omissoes.append("O texto não informa a meta de não-HDL-c (%s mg/dL)." % g["metas"]["nao_hdl"])
        if principais and not certas:
            omissoes.append("O texto não diz quais fatores mais pesaram. Os principais são: %s." % ", ".join(
                NOMES[v] for v in principais))

    return {
        "versao": VERSAO,
        "aceito": not violacoes and not omissoes,
        "fiel": not violacoes,
        "violacoes": violacoes,
        "omissoes": omissoes,
        "afirmacoes": afirmacoes,
        "cobertura": cobertura,
        "principais": principais,
        "epsilon": eps,
    }


def mensagem_de_correcao(resultado):
    """Texto devolvido ao Explicador quando a explicação é rejeitada (crítico por regras)."""
    linhas = ["A explicação anterior foi rejeitada. Reescreva-a corrigindo estes pontos e mantendo o restante:"]
    for v in resultado["violacoes"]:
        linhas.append("- %s (trecho: “%s”)" % (v["mensagem"], v["trecho"][:140]))
    linhas += ["- " + o for o in resultado["omissoes"]]
    return "\n".join(linhas)


assert set(NOMES) == set(prevent.VARIAVEIS), "glossário e variáveis do modelo divergem"
