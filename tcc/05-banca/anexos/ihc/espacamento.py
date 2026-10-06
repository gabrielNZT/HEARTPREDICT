"""WCAG 1.4.12: aplica o espaçamento de texto do critério e mede transbordo em 390 px e 320 px."""
from playwright.sync_api import sync_playwright
CSS="*{line-height:1.5 !important;letter-spacing:.12em !important;word-spacing:.16em !important} p{margin-bottom:2em !important}"
URL="http://127.0.0.1:4173/"
def cont(p): p.get_by_role("button", name="Continuar").click(); p.wait_for_timeout(250)
def num(p,v): p.locator("input[type=text]").first.fill(str(v)); cont(p)
def esc(p,r): p.get_by_label(r, exact=True).check(); cont(p)
with sync_playwright() as pw:
    b=pw.chromium.launch(channel="chrome",headless=True)
    for w in (390,320):
        p=b.new_page(viewport={"width":w,"height":800})
        p.goto(URL); p.wait_for_timeout(300); p.get_by_role("button", name="Começar").click(); p.wait_for_timeout(250)
        num(p,58); esc(p,"Masculino"); esc(p,"Não"); esc(p,"Não"); num(p,210); num(p,44); num(p,""); num(p,140); esc(p,"Não"); esc(p,"Não"); esc(p,"Sim")
        p.get_by_label("TFG estimada", exact=True).check(); p.add_style_tag(content=CSS); p.wait_for_timeout(100)
        o=p.evaluate("()=>[document.documentElement.scrollWidth,document.documentElement.clientWidth]"); print(w,"renal",o)
        p.screenshot(path=f"esp-renal-{w}.png", full_page=True)
        p.locator("#campo-renal-valor").fill("80"); cont(p); print("  url:",p.url, p.locator(".campo__erro").all_inner_texts()); p.get_by_label("Transplante de órgão").check(); cont(p); print("  url:",p.url, p.locator(".campo__erro").all_inner_texts())
        p.get_by_role("button", name="Confirmar e ver o resultado").click(); p.wait_for_timeout(2500); p.add_style_tag(content=CSS)
        o=p.evaluate("()=>[document.documentElement.scrollWidth,document.documentElement.clientWidth]"); print(w,"resultado",o)
        p.screenshot(path=f"esp-resultado-{w}.png", full_page=True)
        # medir a marca e o alvo "Voltar"
        p.close()
    b.close()
