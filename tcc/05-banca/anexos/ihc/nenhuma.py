"""Reproduz: marcar 'Nenhuma destas' na pergunta de agravantes (clique no cartão, como um usuário)."""
from playwright.sync_api import sync_playwright
URL="http://127.0.0.1:4173/"
def cont(p): p.get_by_role("button", name="Continuar").click(); p.wait_for_timeout(300)
def num(p,v): p.locator("input[type=text]").first.fill(str(v)); cont(p)
def esc(p,r): p.get_by_label(r, exact=True).check(); cont(p)
with sync_playwright() as pw:
    b=pw.chromium.launch(channel="chrome",headless=True)
    for larg in (1280,390):
        p=b.new_page(viewport={"width":larg,"height":900})
        p.goto(URL); p.wait_for_timeout(300); p.get_by_role("button", name="Começar").click(); p.wait_for_timeout(250)
        num(p,58); esc(p,"Masculino"); esc(p,"Não"); esc(p,"Não"); num(p,210); num(p,44); num(p,""); num(p,140); esc(p,"Não"); esc(p,"Não"); esc(p,"Sim")
        p.get_by_label("TFG estimada", exact=True).check(); p.locator("#campo-renal-valor").fill("80"); cont(p)
        p.locator(".opcao", has_text="Nenhuma destas").click(); p.wait_for_timeout(150)
        print(larg,"marcado:", p.locator("input[type=checkbox]:checked").evaluate_all("els=>els.map(e=>e.value)"))
        cont(p); print(larg,"após Continuar:", p.url.split("4173")[1], p.locator(".campo__erro").all_inner_texts())
        p.screenshot(path=f"bug-nenhuma-destas-{larg}.png", full_page=True)
        p.close()
    b.close()
