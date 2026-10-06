"""
Pré-anotação HEURÍSTICA das respostas do piloto e geração da planilha de anotação manual.

Atenção: isto NÃO é a avaliação. Só sinaliza trechos para a anotação humana (a referência),
seguindo as definições de tcc/03-metodologia/metricas-fidelidade.md. No experimento final a
avaliação precisa ser independente do verificador (brecha B1).

Uso: python3 preanotar.py resultados/<arquivo>.jsonl
Gera: resultados/<arquivo>_anotacao.csv
"""

import csv
import json
import re
import sys
from pathlib import Path

FORA_DO_MODELO = r"\b(imc|peso|obesidade|obes[oa]|sobrepeso|hist[óo]ria familiar|ldl|ra[çc]a|etnia|sedentaris\w*|dieta|triglic\w*)\b"
CAUSAL = r"\b(aument\w*|elev\w*|contribu\w*|pes(ou|am|a)|pior\w*|influenc\w*|eleva\w*|explica\w*|deve-se|devido)\b"
CATEGORIAS = ["baixo", "intermediário", "alto"]


def _num(txt):
    return float(txt.replace(",", "."))


def _frases(texto):
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+", texto) if f.strip()]


def checar(resposta, g):
    flags = []
    t = resposta.lower()
    # 1) percentuais citados × risco calculado (tolerância: max(5%, meia unidade da precisão do texto))
    for m in re.finditer(r"(\d+(?:[.,]\d+)?)\s*%", t):
        s = m.group(1)
        v = _num(s)
        casas = len(s.split(",")[-1]) if "," in s else (len(s.split(".")[-1]) if "." in s else 0)
        tol = max(0.05 * g["risco_pct"], 0.5 * 10 ** (-casas))
        if abs(v - g["risco_pct"]) > tol and v not in (30.0, 50.0):  # 30%/50% = redução de LDL da meta
            flags.append("NUM? %s%% (risco = %s%%)" % (s, g["risco_pct"]))
    # 2) categoria mencionada
    citadas = [c for c in CATEGORIAS if re.search(r"\b(risco|categoria)\b[^.]{0,40}\b" + c, t)]
    if citadas and g["categoria"] not in citadas:
        flags.append("CAT? citou %s (gabarito: %s)" % ("/".join(citadas), g["categoria"]))
    if not citadas:
        flags.append("CAT? categoria não encontrada automaticamente")
    # 3) meta de LDL
    meta = g["metas"]["ldl"].replace("<", "").strip()
    if "ldl" in t and meta not in t:
        flags.append("REC? meta de LDL %s não encontrada" % meta)
    # 4) variáveis fora do modelo em frases com verbo causal
    for f in _frases(resposta):
        fl = f.lower()
        if re.search(FORA_DO_MODELO, fl) and re.search(CAUSAL, fl):
            flags.append("FORA? " + f[:160])
    return flags


def main():
    arq = Path(sys.argv[1])
    gabs = {g["id"]: g for g in json.loads((arq.parent / "gabarito.json").read_text(encoding="utf-8"))}
    linhas = []
    for linha in arq.read_text(encoding="utf-8").splitlines():
        r = json.loads(linha)
        g = gabs[r["vinheta"]]
        resp = r.get("resposta", "")
        linhas.append({
            "vinheta": r["vinheta"], "repeticao": r["repeticao"], "modelo": r["modelo"],
            "risco_pct": g["risco_pct"], "categoria": g["categoria"], "meta_ldl": g["metas"]["ldl"],
            "top3_atribuicao": "; ".join("%s %+.2f" % (k, g["atribuicao"][k]) for k in g["ranking"][:3]),
            "erro_api": r.get("erro", ""),
            "pre_anotacao": " | ".join(checar(resp, g)) if resp else "",
            "resposta": resp,
            # Colunas para a anotação humana (definições em metricas-fidelidade.md)
            "H_totalmente_fiel(S/N)": "", "H_erros_polaridade": "", "H_erros_numericos": "",
            "H_fora_do_modelo": "", "H_nao_sustentadas": "", "H_observacoes": "",
        })
    saida = arq.with_name(arq.stem + "_anotacao.csv")
    with saida.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(linhas)
    com_flag = sum(1 for l in linhas if l["pre_anotacao"])
    print("%d respostas; %d com alguma sinalização heurística → %s" % (len(linhas), com_flag, saida))


if __name__ == "__main__":
    main()
