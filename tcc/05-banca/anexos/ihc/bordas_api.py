"""Procura entradas cuja apresentação fica contraditória nas fronteiras (5% e 20%) e testa o arredondamento."""
import json, itertools, urllib.request
def av(**k):
    base=dict(idade=55,sexo="masculino",dcv_previa=False,diabetes=False,colesterol_total=200,hdl=50,ldl=None,pas=130,
              anti_hipertensivo=False,estatina=False,tabagismo=False,tfge=90,creatinina=None,agravantes=[])
    base.update(k); req=urllib.request.Request("http://127.0.0.1:8000/api/avaliacao",data=json.dumps(base).encode(),headers={"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e: return {"erro":e.code,"detail":json.loads(e.read())}
achados={}
for idade in range(40,80):
    for sexo in ("feminino","masculino"):
        for pas in range(100,200,2):
            for fuma in (False,True):
                r=av(idade=idade,sexo=sexo,pas=pas,tabagismo=fuma)
                p=r["risco_pct"]; n=r["em_100_pessoas"]
                chave=None
                if p==5.0 and r["categoria"]=="baixo": chave="5,0% exibido mas categoria baixo (<5%)"
                elif p==20.0 and r["categoria"]=="intermediário": chave="20,0% exibido mas categoria intermediário (<20%)"
                elif n==5 and p<5: chave="pictograma 5/100 com categoria baixo (<5%)"
                elif n==20 and p<20: chave="pictograma 20/100 com categoria intermediário (<20%)"
                elif p in (0.5,1.5,2.5,3.5,4.5,5.5,6.5) : chave="meio exato %.1f -> %d figuras"%(p,n)
                elif n==0: chave="0 figuras (risco %.1f%%)"%p
                if chave and chave not in achados:
                    achados[chave]=dict(entrada=dict(idade=idade,sexo=sexo,pas=pas,tabagismo=fuma),risco_pct=p,em_100=n,categoria=r["categoria"])
for k,v in achados.items(): print(k,"=>",v)
print("colesterol 340:",av(colesterol_total=340).get("detail"))
print("pas 85:",av(pas=85).get("detail"))
print("mulher com fator mulher? masculino+fator_especifico_mulher:",{k:av(agravantes=["fator_especifico_mulher"])[k] for k in ("categoria","regras_aplicadas","agravantes")})
