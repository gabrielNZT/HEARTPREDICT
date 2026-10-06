"""Cenários de uso: Voltar do navegador, erros, fora do escopo, Alterar, logo, zoom/reflow, movimento reduzido, cores forçadas, impressão."""
import json
from playwright.sync_api import sync_playwright
URL="http://127.0.0.1:4173/"; log=[]
def L(*a): s=" ".join(str(x) for x in a); log.append(s); print(s)
def cont(p): p.get_by_role("button", name="Continuar").click(); p.wait_for_timeout(300)
def num(p,v): p.locator("input[type=text]").first.fill(str(v)); cont(p)
def esc(p,r): p.get_by_label(r, exact=True).check(); cont(p)
def h1(p): return p.locator("h1").first.inner_text()
def erros(p): return [e.inner_text() for e in p.locator(".campo__erro").all()]
def ate_revisao(p, sexo="Feminino", agr="Situações da saúde da mulher", ct=210, pas=140):
    p.goto(URL+"#/"); p.wait_for_timeout(300); p.get_by_role("button", name="Começar").click(); p.wait_for_timeout(300)
    num(p,58); esc(p,sexo); esc(p,"Não"); esc(p,"Não"); num(p,ct); num(p,44); num(p,""); num(p,pas)
    esc(p,"Não"); esc(p,"Não"); esc(p,"Sim")
    p.get_by_label("Só a creatinina", exact=True).check(); p.locator("#campo-renal-valor").fill("1,1"); cont(p)
    p.get_by_label(agr).check(); cont(p)
def overflow(p): return p.evaluate("()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth})")
with sync_playwright() as pw:
    b=pw.chromium.launch(channel="chrome",headless=True)
    p=b.new_page(viewport={"width":1280,"height":900})
    # 1. tamanhos reais de fonte
    p.goto(URL); p.wait_for_timeout(500)
    L("## Tamanhos de fonte computados (px)")
    L(json.dumps(p.evaluate("""()=>{const g=s=>{const e=document.querySelector(s);return e?getComputedStyle(e).fontSize:null};
      return {html:g('html'),body:g('body'),h1:g('h1'),'h2 início':g('.inicio__secao h2'),'.nota':g('.nota'),'.cabecalho__nome':g('.cabecalho__nome'),
      '.cabecalho__descritor':g('.cabecalho__descritor'),'.cabecalho__selo':g('.cabecalho__selo'),'.inicio__lead':g('.inicio__lead'),'rodapé':g('.rodape')}}"""),ensure_ascii=False))
    # 2. erros e validação
    L("## Erros e validação")
    p.get_by_role("button", name="Começar").click(); p.wait_for_timeout(300)
    for v in ["", "abc", "58,5", "15", "150"]:
        p.locator("input[type=text]").first.fill(v); cont(p); L(f"idade '{v}':", erros(p), "| foco:", p.evaluate("document.activeElement.className"))
    p.screenshot(path="cen-01-erro-idade-15.png")
    p.locator("input[type=text]").first.fill("25"); cont(p); L("idade 25 ->", p.url.split('4173')[1], "|", h1(p)); p.screenshot(path="cen-02-fora-idade-25.png", full_page=True)
    p.go_back(); p.wait_for_timeout(300); L("Voltar do navegador após fora do escopo ->", p.url.split('4173')[1], "| valor no campo:", p.locator("input[type=text]").first.input_value())
    # colesterol fora da faixa, pressão '12'
    p.locator("input[type=text]").first.fill("58"); cont(p); esc(p,"Masculino"); esc(p,"Não"); esc(p,"Não")
    p.locator("input[type=text]").first.fill("340"); cont(p); L("colesterol 340:", erros(p)); p.screenshot(path="cen-03-colesterol-340-beco.png", full_page=True)
    num(p,210); num(p,44); num(p,"")
    for v in ["12","12/8","85"]:
        p.locator("input[type=text]").first.fill(v); cont(p); L(f"pressão '{v}':", erros(p))
    p.screenshot(path="cen-04-pressao-12.png", full_page=True)
    # 3. Voltar do navegador preserva respostas?
    L("## Botão Voltar do navegador")
    num(p,140); L("em:",p.url.split('4173')[1])
    p.go_back(); p.wait_for_timeout(300); L("go_back ->", p.url.split('4173')[1], "| campo:", p.locator("input[type=text]").first.input_value(), "| foco:", p.evaluate("document.activeElement.tagName"))
    p.go_back(); p.wait_for_timeout(300); L("go_back ->", p.url.split('4173')[1], "| campo LDL:", repr(p.locator("input[type=text]").first.input_value()))
    p.go_forward(); p.go_forward(); p.wait_for_timeout(300); L("go_forward x2 ->", p.url.split('4173')[1], "|", h1(p))
    # recarregar
    p.reload(); p.wait_for_timeout(500); L("recarregar em pergunta ->", p.url.split('4173')[1], "|", h1(p))
    p.goto(URL+"#/revisao"); p.wait_for_timeout(400); L("#/revisao após recarregar ->", p.url.split('4173')[1], "|", h1(p))
    # fora do escopo direto
    p.goto(URL+"#/fora/diabetes"); p.wait_for_timeout(400); L("#/fora/diabetes ->", h1(p)); p.screenshot(path="cen-05-fora-diabetes.png", full_page=True)
    p.get_by_role("button", name="Alterar minha resposta").click(); p.wait_for_timeout(300); L("Alterar minha resposta ->", p.url.split('4173')[1], "|", h1(p), "| progresso:", p.locator(".progresso__texto").inner_text())
    p.goto(URL+"#/p/inexistente"); p.wait_for_timeout(300); L("#/p/inexistente ->", h1(p))
    # 4. Revisão e Alterar: sexo feminino com fator da mulher, depois muda para masculino
    L("## Revisão / Alterar (inconsistência sexo x fator da mulher)")
    ate_revisao(p); p.screenshot(path="cen-06-revisao.png", full_page=True)
    p.get_by_role("button", name="Alterar sexo").click(); p.wait_for_timeout(300)
    L("Alterar sexo ->", p.url.split('4173')[1], "| progresso:", p.locator(".progresso__texto").inner_text(), "| botão:", p.locator("button[type=submit]").inner_text())
    esc(p,"Masculino"); L("após mudar para Masculino ->", p.url.split('4173')[1])
    linha=p.locator(".revisao__linha").filter(has_text="Situações que ajustam").inner_text().replace("\n"," | "); L("linha agravantes na revisão:", linha)
    p.screenshot(path="cen-07-revisao-homem-com-fator-da-mulher.png", full_page=True)
    p.get_by_role("button", name="Confirmar e ver o resultado").click(); p.wait_for_timeout(2500)
    L("resultado:", p.locator(".destaque__numero").inner_text(), "|", p.locator("#titulo-categoria").inner_text(), "|", p.locator(".reclassificacao").inner_text() if p.locator(".reclassificacao").count() else "-")
    p.screenshot(path="cen-08-resultado-homem-fator-mulher.png", full_page=True)
    # explicação indisponível
    L("explicação:", p.locator(".explicacao").inner_text().replace("\n"," | "))
    L("pictograma aria-label:", p.locator(".pictograma").get_attribute("aria-label"))
    L("summary display/marker:", p.evaluate("getComputedStyle(document.querySelector('.como-ler summary')).display"))
    # 5. clique na marca no meio do fluxo
    L("## Marca no cabeçalho no meio do fluxo")
    ate_revisao(p); p.get_by_role("button", name="Alterar pressão sistólica").click(); p.wait_for_timeout(300)
    p.locator(".cabecalho__marca").click(); p.wait_for_timeout(300); L("clicou na marca ->", p.url.split('4173')[1], "| confirmação pedida? não (sem diálogo)")
    p.goto(URL+"#/revisao"); p.wait_for_timeout(300); L("#/revisao depois ->", h1(p))
    # 6. Reflow 320 px e texto 200%
    L("## Reflow e zoom")
    for nome,vp,fs in [("320px",{"width":320,"height":640},None),("640px + zoom 200% (DPR2)",{"width":640,"height":450},None),("1280px texto 200% (html 225%)",{"width":1280,"height":900},"225%"),("390px texto 200%",{"width":390,"height":844},"225%")]:
        q=b.new_page(viewport=vp, device_scale_factor=2 if "DPR2" in nome else 1)
        ate_revisao(q)
        if fs: q.add_style_tag(content=f"html{{font-size:{fs} !important}}")
        q.wait_for_timeout(200); o=overflow(q); L(nome,"revisão overflow:",o)
        tag=nome.split()[0].replace("%","").replace("+","")
        q.screenshot(path=f"cen-09-revisao-{tag}{'-texto200' if fs else ''}.png", full_page=True)
        q.get_by_role("button", name="Confirmar e ver o resultado").click(); q.wait_for_timeout(2500)
        if fs: q.add_style_tag(content=f"html{{font-size:{fs} !important}}")
        o=overflow(q); L(nome,"resultado overflow:",o)
        largos=q.evaluate("""()=>[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>document.documentElement.clientWidth+1).slice(0,6).map(e=>e.tagName+'.'+e.className)""")
        L("   elementos além da largura:", largos)
        q.screenshot(path=f"cen-10-resultado-{tag}{'-texto200' if fs else ''}.png", full_page=True)
        q.goto(URL+"#/p/renal"); q.wait_for_timeout(300)
        if fs: q.add_style_tag(content=f"html{{font-size:{fs} !important}}")
        q.get_by_label("TFG estimada", exact=True).check(); q.wait_for_timeout(200); L(nome,"renal overflow:",overflow(q))
        q.screenshot(path=f"cen-11-renal-{tag}{'-texto200' if fs else ''}.png", full_page=True)
        q.close()
    # 7. movimento reduzido
    L("## prefers-reduced-motion")
    q=b.new_page(viewport={"width":1280,"height":900}); q.emulate_media(reduced_motion="reduce"); ate_revisao(q)
    q.get_by_role("button", name="Confirmar e ver o resultado").click(); q.wait_for_timeout(300)
    L(json.dumps(q.evaluate("""()=>{const g=(s,pr)=>{const e=document.querySelector(s);if(!e)return null;const c=getComputedStyle(e);return c.animationName+' '+c.animationDuration+' '+c.animationIterationCount+' / trans '+c.transitionDuration}
       return {entrar:g('.entrar'),pessoa:g('.pessoa--evento'),barra:g('.fator__barra'),fantasma:g('.linhas-fantasma span'),progresso:null}}"""),ensure_ascii=False))
    q.screenshot(path="cen-12-resultado-movimento-reduzido-300ms.png"); q.close()
    q=b.new_page(viewport={"width":1280,"height":900}); ate_revisao(q); q.get_by_role("button", name="Confirmar e ver o resultado").click(); q.wait_for_timeout(60)
    L("sem redução, 60 ms após:", json.dumps(q.evaluate("""()=>({opacidadeTela:getComputedStyle(document.querySelector('.entrar')).opacity, fantasma:(()=>{const e=document.querySelector('.linhas-fantasma span');return e?getComputedStyle(e).animationDuration+' '+getComputedStyle(e).animationIterationCount:null})()})""")))
    q.close()
    # 8. cores forçadas (Alto Contraste do Windows)
    L("## forced-colors: active")
    q=b.new_page(viewport={"width":1280,"height":900}); q.emulate_media(forced_colors="active")
    q.goto(URL+"#/p/sexo"); q.wait_for_timeout(400); q.keyboard.press("Tab"); q.keyboard.press("ArrowDown"); q.wait_for_timeout(100)
    q.screenshot(path="cen-13-forced-colors-foco-opcao.png")
    q.keyboard.press("Tab"); q.wait_for_timeout(100); q.screenshot(path="cen-14-forced-colors-foco-botao.png")
    L("foco no botão em forced-colors: outline =", q.evaluate("getComputedStyle(document.activeElement).outlineStyle"), "| box-shadow =", q.evaluate("getComputedStyle(document.activeElement).boxShadow"))
    ate_revisao(q); q.get_by_role("button", name="Confirmar e ver o resultado").click(); q.wait_for_timeout(2500)
    q.screenshot(path="cen-15-forced-colors-resultado.png", full_page=True); q.close()
    # 9. impressão
    L("## Impressão (PDF sem gráficos de fundo = padrão do Chrome)")
    q=b.new_page(viewport={"width":1280,"height":900}); ate_revisao(q); q.get_by_role("button", name="Confirmar e ver o resultado").click(); q.wait_for_timeout(2500)
    q.emulate_media(media="print"); q.pdf(path="impressao-resultado.pdf", format="A4", print_background=False); q.close()
    b.close()
open("cenarios-log.txt","w").write("\n".join(log))
