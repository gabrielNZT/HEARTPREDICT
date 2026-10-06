"""Percorre o fluxo SOMENTE com teclado (Tab/Shift+Tab/Espaço/setas/Enter) e registra o foco a cada passo."""
from playwright.sync_api import sync_playwright
URL="http://127.0.0.1:4173/"
log=[]
def foco(p):
    return p.evaluate("""()=>{const e=document.activeElement;if(!e)return'-';
      const n=e.tagName.toLowerCase();const t=(e.getAttribute('aria-label')||e.innerText||e.value||e.id||'').trim().slice(0,45).replace(/\\n/g,' ');
      const bs=getComputedStyle(e).boxShadow;const par=e.closest('.opcao');const bsp=par?getComputedStyle(par).boxShadow:'none';
      return `${n}${e.type?'['+e.type+']':''}${e.checked?'(marcado)':''} "${t}" | anel visível: ${(bs!=='none'||bsp!=='none')?'sim':'não'}`}""")
def estado(p): return f"url={p.url.split('4173')[1]} | h1='{p.locator('h1').first.inner_text()[:55]}'"
def tab(p,shift=False):
    k="Shift+Tab" if shift else "Tab"; p.keyboard.press(k); log.append(f"{k:9} -> {foco(p)}")
def key(p,k,espera=350): p.keyboard.press(k); p.wait_for_timeout(espera); log.append(f"{k:9} -> {foco(p)} || {estado(p)}")
def tipo(p,s): p.keyboard.type(s); log.append(f"digita '{s}'")
with sync_playwright() as pw:
    b=pw.chromium.launch(channel="chrome",headless=True)
    p=b.new_page(viewport={"width":1280,"height":900})
    try:
        p.goto(URL); p.wait_for_timeout(600); log.append("carregou  -> "+foco(p))
        tab(p,True); tab(p,True); p.screenshot(path="tec-01-foco-marca-cabecalho.png"); tab(p); tab(p)
        p.screenshot(path="tec-02-foco-comecar.png")
        key(p,"Enter")
        tab(p); tipo(p,"58"); p.screenshot(path="tec-03-foco-campo-numero.png"); key(p,"Enter")
        log.append("## sexo: Tab entra no grupo, seta escolhe, Enter envia?")
        tab(p); key(p,"ArrowDown",100); p.screenshot(path="tec-04-foco-opcao-radio.png"); key(p,"Enter")
        if "sexo" in p.url:
            log.append("   Enter em rádio NÃO enviou; usando Tab até Continuar"); tab(p); key(p,"Enter")
        for _ in range(2):  # dcv, diabetes: Não
            tab(p); key(p,"ArrowDown",100); key(p,"Enter")
            if "dcv" in p.url or "diabetes" in p.url and p.locator("input:checked").count(): pass
        for v in ["210","44",""]:
            tab(p);
            if v: tipo(p,v)
            key(p,"Enter")
        tab(p); tipo(p,"140"); key(p,"Enter")
        for _ in range(2): tab(p); key(p,"ArrowDown",100); key(p,"Enter")
        log.append("## tabagismo: Espaço no 1º rádio (Sim)")
        tab(p); key(p,"Space",100); key(p,"Enter")
        log.append("## renal: seta para 'Só a creatinina', Tab para o campo revelado")
        tab(p); key(p,"ArrowDown",150); tab(p); tipo(p,"1,1"); p.screenshot(path="tec-05-renal-revelado.png"); key(p,"Enter")
        log.append("## agravantes: Espaço marca caixa; Enter envia")
        tab(p); key(p,"Space",100); p.screenshot(path="tec-06-foco-checkbox.png"); key(p,"Enter")
        log.append("## revisão: Tab até Confirmar")
        for _ in range(40):
            tab(p)
            if "Confirmar" in foco(p): break
        p.screenshot(path="tec-07-revisao-foco-confirmar.png")
        log.append("## Shift+Tab volta ao último Alterar"); tab(p,True); tab(p)
        key(p,"Enter",3000)
        log.append("## resultado")
        for _ in range(20):
            tab(p)
            if "Como ler" in foco(p): break
        p.screenshot(path="tec-08-foco-como-ler.png")
        key(p,"Enter",250); p.locator(".como-ler").screenshot(path="tec-09-como-ler-aberto.png")
        for _ in range(6):
            tab(p)
            if "Imprimir" in foco(p): break
        p.screenshot(path="tec-10-foco-imprimir.png")
    except Exception as ex:
        log.append('FALHA: '+str(ex)[:200]); p.screenshot(path='tec-falha.png', full_page=True)
    b.close()
open("teclado-log.txt","w").write("\n".join(log)); print("\n".join(log))
