"""
Reteste dos defeitos de interface apontados pela banca (parecer-ihc.md, parecer-cardiologia.md,
parecer-engenharia.md), depois das correções de 29/09/2026.

Uso (gateway em 127.0.0.1:8000 e `vite preview` em 127.0.0.1:4173):
  python retestar_banca.py <pasta_de_saida>
Imprime uma linha PASSOU/FALHOU por caso e grava capturas <pasta>/reteste-*.png.
"""
import json
import sys
import urllib.request

from playwright.sync_api import sync_playwright

OUT = sys.argv[1]
URL = "http://127.0.0.1:4173/"
API = "http://127.0.0.1:8000/api/avaliacao"
resultados = []


def registrar(nome, ok, detalhe=""):
    resultados.append(ok)
    print("%s  %s%s" % ("PASSOU" if ok else "FALHOU", nome, (" — " + detalhe) if detalhe else ""))


def cont(p):
    p.get_by_role("button", name="Continuar").click()
    p.wait_for_timeout(250)


def num(p, v):
    p.locator("input[type=text]").first.fill(str(v))
    cont(p)


def esc(p, rotulo):
    p.get_by_label(rotulo, exact=True).check()
    cont(p)


def ate_agravantes(p, sexo="Masculino", colesterol=210):
    p.goto(URL)
    p.wait_for_timeout(300)
    p.get_by_role("button", name="Começar").click()
    p.wait_for_timeout(250)
    num(p, 58)
    esc(p, sexo)
    esc(p, "Não")   # DCV prévia
    esc(p, "Não")   # placa em exame de imagem
    esc(p, "Não")   # diabetes
    num(p, colesterol)
    num(p, 44)
    num(p, "")      # LDL opcional
    num(p, 140)
    esc(p, "Não")
    esc(p, "Não")
    esc(p, "Sim")
    p.get_by_label("TFG estimada", exact=True).check()
    p.locator("#campo-renal-valor").fill("80")
    cont(p)


def api(**k):
    base = dict(idade=55, sexo="masculino", dcv_previa=False, diabetes=False, colesterol_total=200, hdl=50,
                pas=130, anti_hipertensivo=False, estatina=False, tabagismo=False, tfge=90, agravantes=[])
    base.update(k)
    req = urllib.request.Request(API, data=json.dumps(base).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome", headless=True)

    # 1. "Nenhuma destas" leva à revisão (antes: bloqueava a avaliação)
    for larg in (1280, 390):
        p = b.new_page(viewport={"width": larg, "height": 900})
        ate_agravantes(p)
        p.locator(".opcao", has_text="Nenhuma destas").click()
        cont(p)
        ok = p.url.endswith("#/revisao")
        p.screenshot(path="%s/reteste-01-nenhuma-%d.png" % (OUT, larg), full_page=True)
        registrar("“Nenhuma destas” chega à revisão (%d px)" % larg, ok, p.url)
        if larg == 1280:
            p.get_by_role("button", name="Confirmar e ver o resultado").click()
            p.wait_for_timeout(1500)
            registrar("… e ao resultado", p.url.endswith("#/resultado"), p.url)
        p.close()

    # 2. Trocar o sexo na revisão invalida o fator exclusivo da mulher (antes: homem ficava com ele e virava "alto")
    p = b.new_page(viewport={"width": 1280, "height": 900})
    ate_agravantes(p, sexo="Feminino")
    p.get_by_label("Situações da saúde da mulher", exact=True).check()
    cont(p)
    p.get_by_role("button", name="Alterar sexo").click()
    p.wait_for_timeout(250)
    esc(p, "Masculino")
    pediu_de_novo = "#/p/agravantes" in p.url
    p.screenshot(path="%s/reteste-02-troca-de-sexo.png" % OUT, full_page=True)
    registrar("Trocar o sexo pede de novo as situações que dependem dele", pediu_de_novo, p.url)
    opcao_visivel = p.get_by_label("Situações da saúde da mulher", exact=True).count()
    registrar("… e a opção feminina não aparece para homem", opcao_visivel == 0)
    p.close()

    # 3. Escala coerente com o número quando há reclassificação
    p = b.new_page(viewport={"width": 1280, "height": 900})
    ate_agravantes(p)
    p.get_by_label("Pai, mãe, irmão ou irmã teve infarto ou AVC cedo").check()
    cont(p)
    p.get_by_role("button", name="Confirmar e ver o resultado").click()
    p.wait_for_timeout(1500)
    texto = p.locator(".escala").inner_text()
    registrar("Escala marca a faixa do número e a categoria da diretriz",
              "Seu número cai aqui" in texto and "Sua categoria pela diretriz" in texto)
    registrar("Explicação por IA não é pedida sem consentimento",
              p.get_by_role("button", name="Concordo e quero gerar a explicação").count() == 1)
    # 4. Marca volta ao início sem apagar respostas
    p.locator(".cabecalho a").first.click()
    p.wait_for_timeout(300)
    registrar("Marca volta ao início sem apagar respostas",
              p.get_by_role("button", name="Continuar de onde parei").count() == 1)
    p.close()

    # 5. Valor fora da faixa: mensagem diz o que fazer (antes: beco sem saída)
    p = b.new_page(viewport={"width": 1280, "height": 900})
    p.goto(URL)
    p.wait_for_timeout(300)
    p.get_by_role("button", name="Começar").click()
    p.wait_for_timeout(250)
    num(p, 58); esc(p, "Masculino"); esc(p, "Não"); esc(p, "Não"); esc(p, "Não")
    num(p, 340)
    msg = p.locator(".campo__erro").inner_text()
    p.screenshot(path="%s/reteste-05-colesterol-340.png" % OUT, full_page=True)
    registrar("Colesterol 340 orienta o que fazer", "não se aplica" in msg and "médico" in msg)
    p.close()

    # 6. Sem rolagem horizontal a 320 px na pergunta renal (WCAG 1.4.10)
    p = b.new_page(viewport={"width": 320, "height": 800})
    p.goto(URL + "#/")
    p.wait_for_timeout(300)
    p.get_by_role("button", name="Começar").click()
    p.wait_for_timeout(250)
    num(p, 58); esc(p, "Masculino"); esc(p, "Não"); esc(p, "Não"); esc(p, "Não")
    num(p, 210); num(p, 44); num(p, ""); num(p, 140); esc(p, "Não"); esc(p, "Não"); esc(p, "Sim")
    p.get_by_label("TFG estimada", exact=True).check()
    p.wait_for_timeout(200)
    largura = p.evaluate("document.documentElement.scrollWidth")
    p.screenshot(path="%s/reteste-06-renal-320.png" % OUT, full_page=True)
    registrar("Pergunta renal cabe em 320 px", largura <= 320, "scrollWidth=%d" % largura)
    p.close()
    b.close()

# 7. Fronteiras 5% e 20%: número exibido e categoria sempre coerentes (varredura pela API)
contradicoes = 0
casos = 0
for idade in range(40, 80):
    for sexo in ("feminino", "masculino"):
        for pas in range(100, 200, 4):
            for fuma in (False, True):
                r = api(idade=idade, sexo=sexo, pas=pas, tabagismo=fuma)
                casos += 1
                v, c = r["risco_pct"], r["regras_aplicadas"][0]
                esperado = "baixo" if v < 5 else ("intermediário" if v < 20 else "alto")
                if not c.endswith("→ %s (Tabela 4.1)" % esperado):
                    contradicoes += 1
registrar("Categoria do escore coerente com o número exibido nas fronteiras",
          contradicoes == 0, "%d contradições em %d entradas" % (contradicoes, casos))

print("\n%d de %d verificações passaram" % (sum(resultados), len(resultados)))
