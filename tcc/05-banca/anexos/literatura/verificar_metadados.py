#!/usr/bin/env python3
"""Confere metadados dos fichamentos (central/alta + alguns média) no Crossref e no arXiv.
Uso: python3 tcc/05-banca/anexos/literatura/verificar_metadados.py  (requer internet)
Imprime, para cada DOI: título, veículo, volume, fascículo, páginas/nº do artigo, data, nº de autores e 1º/último autor.
"""
import json, re, time, urllib.request
DOIS = {
 "jin2025agentmd":"10.1038/s41467-025-64430-x", "khan2024prevent":"10.1161/CIRCULATIONAHA.123.067626",
 "lee2025shapllm":"10.1186/s12911-025-03239-6", "roeschl2026pipeline":"10.1093/ehjdh/ztag124",
 "santos2026escllm":"10.1093/ehjdh/ztag073", "sbc2025dislipidemias":"10.36660/abc.20250640",
 "wang2025colacare":"10.1145/3696410.3714877", "diao2024preventnhanes":"10.1001/jama.2024.12537",
 "anderson2024preventnhanes":"10.1001/jamainternmed.2024.1302", "collins2024tripodai":"10.1136/bmj-2023-078378",
 "hevner2004dsr":"10.2307/25148625", "jabbour2023jama":"10.1001/jama.2023.22295",
 "jacovi2020faithfulness":"10.18653/v1/2020.acl-main.386", "jennings2000abse":"10.1016/S0004-3702(99)00107-1",
 "kapoor2023leakage":"10.1016/j.patter.2023.100804", "vancalster2019calibration":"10.1186/s12916-019-1466-7",
 "wooldridge1995agents":"10.1017/S0269888900008122", "asgari2025hallucination":"10.1038/s41746-025-01670-7",
 "isern2016agents (DOI ausente no fichamento)":"10.1007/s10916-015-0376-2",
 "tang2024medagents (DOI ausente no fichamento)":"10.18653/v1/2024.findings-acl.33",
 "chan2025vies (DOI ausente no fichamento)":"10.3389/fdgth.2025.1710594",
}
ARXIV = "2608.26109,2607.28218,2605.01189,2506.01463,2503.13657,2505.12371,2406.12036,2404.15155,2410.02551,2502.00025,2512.00163,2503.17550,2505.02279,2507.10644"

def cr(doi):
    m = json.load(urllib.request.urlopen("https://api.crossref.org/works/" + doi, timeout=30))["message"]
    au = m.get("author", [])
    nome = lambda a: (a.get("given", "") + " " + a.get("family", "")).strip() or a.get("name", "")
    return (f"{m.get('title',[''])[0][:80]} | {(m.get('container-title') or [''])[0]} | v{m.get('volume')} "
            f"i{m.get('issue')} | p/art {m.get('page') or m.get('article-number')} | {m.get('issued',{}).get('date-parts')} "
            f"| {len(au)} autores | 1º {nome(au[0]) if au else '-'} | último {nome(au[-1]) if au else '-'}")

for k, d in DOIS.items():
    try: print(f"{k}: {d}\n   {cr(d)}")
    except Exception as e: print(f"{k}: {d} ERRO {e}")
    time.sleep(0.3)

t = urllib.request.urlopen("https://export.arxiv.org/api/query?max_results=30&id_list=" + ARXIV, timeout=40).read().decode()
print("\n== arXiv ==")
for e in t.split("<entry>")[1:]:
    g = lambda tag: (re.search(f"<{tag}[^>]*>(.*?)</{tag}>", e, re.S) or [None, ""])[1].strip().replace("\n", " ")
    au = re.findall("<name>(.*?)</name>", e)
    print(f"{g('id')} | publicado {g('published')[:10]} | {g('title')[:70]} | {len(au)} autores | comentário: {g('arxiv:comment')[:90]}")
