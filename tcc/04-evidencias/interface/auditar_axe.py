import json, sys
from playwright.sync_api import sync_playwright
AXE = open("axe.min.js").read()
def auditar(p, nome):
    p.add_script_tag(content=AXE)
    r = p.evaluate("async () => await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}})")
    v = [(x['id'], x['impact'], len(x['nodes'])) for x in r['violations']]
    print("%-14s violações: %d %s | aprovadas: %d" % (nome, len(v), v, len(r['passes'])))
    return v
def c(p): p.get_by_role("button", name="Continuar").click(); p.wait_for_timeout(250)
with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome", headless=True)
    for larg in (1280, 390):
        p = b.new_page(viewport={"width": larg, "height": 900}); print("== largura", larg)
        p.goto("http://127.0.0.1:4173/"); p.wait_for_timeout(400); auditar(p, "inicio")
        p.get_by_role("button", name="Começar").click(); p.wait_for_timeout(300); c(p); auditar(p, "erro")
        p.locator("input[type=text]").first.fill("58"); c(p); auditar(p, "escolha")
        for r in ["Masculino","Não","Não","Não"]: p.get_by_label(r, exact=True).check(); c(p)
        for v in [210,44,130,140]: p.locator("input[type=text]").first.fill(str(v)); c(p)
        for r in ["Não","Não","Sim"]: p.get_by_label(r, exact=True).check(); c(p)
        p.get_by_label("Só a creatinina", exact=True).check(); p.locator("#campo-renal-valor").fill("1,1"); auditar(p, "renal"); c(p)
        p.get_by_label("Pai, mãe, irmão ou irmã teve infarto ou AVC cedo").check(); auditar(p, "multipla"); c(p)
        auditar(p, "revisao")
        p.get_by_role("button", name="Confirmar e ver o resultado").click(); p.wait_for_timeout(2500); auditar(p, "resultado")
        p.get_by_role("button", name="Concordo e quero gerar a explicação").click(); p.wait_for_timeout(1500); auditar(p, "explicacao")
        p.goto("http://127.0.0.1:4173/#/fora/diabetes"); p.wait_for_timeout(300)
    b.close()
