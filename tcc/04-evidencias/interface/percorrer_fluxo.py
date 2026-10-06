import sys
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]; LARG = int(sys.argv[2]); ALT = int(sys.argv[3]); PREF = sys.argv[4]
URL = "http://127.0.0.1:4173/"

def continuar(p): p.get_by_role("button", name="Continuar").click(); p.wait_for_timeout(250)
def numero(p, v): p.locator("input[type=text]").first.fill(str(v)); continuar(p)
def escolha(p, rot): p.get_by_label(rot, exact=True).check(); continuar(p)

with sync_playwright() as pw:
    b = pw.chromium.launch(channel="chrome", headless=True)
    p = b.new_page(viewport={"width": LARG, "height": ALT})
    erros = []
    p.on("console", lambda m: erros.append(m.text) if m.type == "error" else None)
    p.goto(URL); p.wait_for_timeout(500)
    p.screenshot(path=f"{OUT}/{PREF}-01-inicio.png", full_page=True)
    p.get_by_role("button", name="Começar").click(); p.wait_for_timeout(300)
    continuar(p)  # enviar vazio -> erro
    p.screenshot(path=f"{OUT}/{PREF}-02-erro.png", full_page=True)
    numero(p, 58)
    p.screenshot(path=f"{OUT}/{PREF}-03-pergunta-escolha.png", full_page=True)
    escolha(p, "Masculino"); escolha(p, "Não"); escolha(p, "Não"); escolha(p, "Não")  # DCV, placa, diabetes
    numero(p, 210); numero(p, 44); numero(p, 130)
    p.screenshot(path=f"{OUT}/{PREF}-04-pergunta-numero.png", full_page=True)
    numero(p, 140); escolha(p, "Não"); escolha(p, "Não"); escolha(p, "Sim")
    p.get_by_label("Só a creatinina", exact=True).check(); p.wait_for_timeout(200)
    p.locator("#campo-renal-valor").fill("1,1")
    p.screenshot(path=f"{OUT}/{PREF}-05-renal.png", full_page=True)
    continuar(p)
    p.get_by_label("Pai, mãe, irmão ou irmã teve infarto ou AVC cedo").check()
    p.screenshot(path=f"{OUT}/{PREF}-06-agravantes.png", full_page=True)
    continuar(p)
    p.screenshot(path=f"{OUT}/{PREF}-07-revisao.png", full_page=True)
    p.get_by_role("button", name="Confirmar e ver o resultado").click()
    p.wait_for_timeout(2500)
    p.screenshot(path=f"{OUT}/{PREF}-08-resultado.png", full_page=True)
    # Explicação por IA só com consentimento (sem LLM configurado, mostra o estado de indisponível)
    p.get_by_role("button", name="Concordo e quero gerar a explicação").click(); p.wait_for_timeout(1500)
    p.screenshot(path=f"{OUT}/{PREF}-09-explicacao-apos-consentimento.png", full_page=True)
    print("título:", p.title()); print("url:", p.url)
    print("erros de console:", erros)
    b.close()
