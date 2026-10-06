# Executado em 2026-09-29 a partir de backend-gateway/app (python3 verificacao-gateway.py). llm.gerar substituido por funcao falsa: nenhum dado foi enviado a provedor real.
import os, sys, logging, json
os.environ.pop("LLM_PROVEDOR", None)
sys.path.insert(0, os.getcwd())
from fastapi.testclient import TestClient
import main, llm
enviados = []
def falso_gerar(provedor, modelo, texto, temperatura, max_tokens):
    enviados.append(texto); return ("texto de teste", {})
llm.gerar = falso_gerar
os.environ["LLM_PROVEDOR"]="groq"; os.environ["LLM_MODELO"]="modelo-x"
c = TestClient(main.app)
e = {"idade":62,"sexo":"feminino","dcv_previa":False,"diabetes":False,"colesterol_total":220,"hdl":45,"pas":142,
     "tfge":None,"creatinina":1.1,"anti_hipertensivo":True,"estatina":False,"tabagismo":True,"ldl":150,
     "agravantes":["doenca_inflamatoria_cronica","fator_especifico_mulher"]}
print("--- /api/avaliacao"); r=c.post("/api/avaliacao",json=e); print(r.status_code)
print("--- /api/avaliacao/explicacao"); r=c.post("/api/avaliacao/explicacao",json=e); print(r.status_code, r.json())
print("=== PROMPT ENVIADO AO PROVEDOR ===\n"+enviados[0])
print("--- CORS preflight de origem arbitraria")
r=c.options("/api/avaliacao",headers={"Origin":"https://site-qualquer.example","Access-Control-Request-Method":"POST"}); print(r.status_code, r.headers.get("access-control-allow-origin"))
print("--- /predict legado (JADE ausente)")
leg={"user_id":"maria.silva@email.com","age":60,"gender":1,"height":160,"weight":70.0,"ap_hi":140,"ap_lo":90,"cholesterol":2,"gluc":1,"smoke":0,"alco":0,"active":1}
r=c.post("/predict",json=leg); print(r.status_code, r.text[:200])
print("--- /pending"); print(c.get("/pending").json())
print("--- /explanation injection sem autenticacao"); print(c.post("/explanation/qualquer",json={"explanation":"x"}).json())
print("--- rotas:", sorted({getattr(x,'path','') for x in main.app.routes}))
