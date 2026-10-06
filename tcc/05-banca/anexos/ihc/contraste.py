"""Recalcula contrastes WCAG 2.x (fórmula de luminância relativa) dos tokens de frontend/src/estilos/tokens.css."""
def lum(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c]
    return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def cr(a,b):
    la,lb=sorted([lum(a),lum(b)],reverse=True); return (la+0.05)/(lb+0.05)
T=dict(papel='#f7f4ee',superficie='#fffdf9',tinta='#17222e',tinta_suave='#44505c',acento='#0e5a5e',
 acento_escuro='#0a474a',acento_claro='#e3efee',erro='#a4231b',erro_claro='#f8e9e7',linha='#8c8579',
 linha_suave='#e2ddd3',risco_baixo='#ead9b5',risco_intermediario='#d9a15f',risco_alto='#8e2f1f',
 evento='#8e2f1f',sem_evento='#c4bcad',diminuiu='#5b7083',branco='#ffffff')
pares=[
 # (primeiro plano, fundo, uso, afirmado, exigido)
 ('tinta','papel','texto principal','14,7',4.5),('tinta','superficie','texto em cartões',None,4.5),
 ('tinta_suave','papel','texto secundário','7,5',4.5),('tinta_suave','superficie','dica/nota em cartão',None,4.5),
 ('tinta_suave','acento_claro','dica de opção marcada',None,4.5),
 ('acento','papel','links/botão secundário','7,2',4.5),('acento','superficie','link em cartão',None,4.5),
 ('acento','acento_claro','texto botão secundário em hover',None,4.5),
 ('branco','acento','texto do botão primário','7,95',4.5),('branco','acento_escuro','botão primário hover',None,4.5),
 ('acento_escuro','papel','link hover','9,5',4.5),
 ('erro','papel','mensagem de erro','6,8',4.5),('erro','erro_claro','link no resumo de erros',None,4.5),
 ('tinta','erro_claro','título do resumo de erros',None,4.5),
 ('linha','papel','borda de campo (1.4.11)','3,3',3),('linha','superficie','borda de campo sobre cartão',None,3),
 ('tinta_suave','superficie','borda de campo em hover',None,3),
 ('acento','superficie','borda opção marcada',None,3),('acento','acento_claro','borda opção marcada vs fundo interno',None,3),
 ('erro','superficie','borda de campo com erro',None,3),
 ('acento','papel','anel de foco (acento) sobre papel',None,3),
 ('acento','linha_suave','barra de progresso vs trilho',None,3),('linha_suave','papel','trilho de progresso vs fundo',None,3),
 ('risco_baixo','papel','faixa Baixo vs fundo',None,3),('risco_intermediario','papel','faixa Intermediário vs fundo',None,3),
 ('risco_alto','papel','faixa Alto vs fundo',None,3),
 ('risco_baixo','risco_intermediario','faixa Baixo vs Intermediário (adjacentes)',None,3),
 ('risco_intermediario','risco_alto','faixa Intermediário vs Alto',None,3),
 ('tinta','risco_baixo','texto sobre Baixo (afirmado; não existe no código)','11,6',4.5),
 ('tinta','risco_intermediario','texto sobre Intermediário (afirmado; não existe)','7,1',4.5),
 ('branco','risco_alto','branco sobre Alto (afirmado; não existe)','8,2',4.5),
 ('evento','sem_evento','pictograma: evento vs sem evento','4,3',3),
 ('sem_evento','superficie','pictograma: figura sem evento vs fundo do cartão',None,3),
 ('evento','superficie','pictograma: figura evento vs fundo',None,3),
 ('evento','linha_suave','barra "aumentou" vs trilho',None,3),('diminuiu','linha_suave','barra "diminuiu/pouco" vs trilho',None,3),
 ('linha_suave','papel','trilho das barras vs fundo',None,3),
 ('evento','diminuiu','barra aumentou vs diminuiu',None,3),
 ('tinta_suave','papel','selo "Protótipo acadêmico" texto',None,4.5),('linha','papel','borda do selo',None,3),
]
print("%-52s %-9s %-9s %-7s %s"%("par (uso)","medido","afirmado","mínimo","ok?"))
for f,b,u,a,m in pares:
    v=cr(T[f],T[b]); print("%-52s %-9s %-9s %-7s %s"%(f"{f}/{b} ({u})"[:52],("%.2f:1"%v).replace('.',','),a or '-',m,'SIM' if v>=m else 'NÃO'))
