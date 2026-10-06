"""
Resume a planilha anotada (coluna H_totalmente_fiel preenchida com S/N) e aplica a regra de decisão do piloto.

Uso: python3 resumir.py resultados/<arquivo>_anotacao.csv [--limiar 0.10]

Revisão após a banca (29/09/2026; pareceres de Metodologia e de IA):
- Unidade de análise = vinheta. As repetições de uma vinheta não são independentes, então o IC95% da
  taxa de respostas não fiéis é obtido por bootstrap por conglomerado (reamostra vinhetas, não respostas).
- A regra usa o intervalo, não a estimativa pontual:
    limite inferior ≥ limiar  → SEGUE o desenho (erros frequentes o bastante para medir melhora);
    limite superior < limiar  → AJUSTAR a tarefa (erros raros: efeito teto);
    caso contrário            → INCONCLUSIVO (ampliar o número de vinhetas antes de decidir).
- Também informa, por vinheta, quantas repetições não foram fiéis (estratificação por tipo de vinheta).
"""

import argparse
import csv
import random
from collections import defaultdict

REPLICAS_BOOTSTRAP = 10000
SEMENTE = 20260929


def ic_bootstrap_conglomerado(por_vinheta, replicas=REPLICAS_BOOTSTRAP, semente=SEMENTE):
    """IC95% percentil da taxa de respostas não fiéis, reamostrando vinhetas com reposição."""
    grupos = list(por_vinheta.values())
    rng = random.Random(semente)
    taxas = []
    for _ in range(replicas):
        amostra = [grupos[rng.randrange(len(grupos))] for _ in grupos]
        n = sum(len(g) for g in amostra)
        taxas.append(sum(1 for g in amostra for fiel in g if not fiel) / n)
    taxas.sort()
    return taxas[int(0.025 * replicas)], taxas[int(0.975 * replicas) - 1]


def decidir(lo, hi, limiar):
    if lo >= limiar:
        return "SEGUE o desenho atual"
    if hi < limiar:
        return "AJUSTAR a tarefa (erros raros)"
    return "INCONCLUSIVO: ampliar o número de vinhetas"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--limiar", type=float, default=0.10)
    a = ap.parse_args()
    por_modelo = defaultdict(lambda: defaultdict(list))
    with open(a.csv, encoding="utf-8-sig") as f:
        for linha in csv.DictReader(f, delimiter=";"):
            v = linha["H_totalmente_fiel(S/N)"].strip().upper()
            if v in ("S", "N"):
                por_modelo[linha["modelo"]][linha["vinheta"]].append(v == "S")
    for modelo, vs in por_modelo.items():
        resp = [x for reps in vs.values() for x in reps]
        err_resp = sum(1 for x in resp if not x)
        err_vin = sum(1 for reps in vs.values() if not all(reps))
        lo, hi = ic_bootstrap_conglomerado(vs)
        print("%s: %d/%d respostas não fiéis (%.0f%%; IC95%% por conglomerado %.0f–%.0f%%); "
              "%d/%d vinhetas com ≥ 1 resposta não fiel" % (
                  modelo, err_resp, len(resp), 100 * err_resp / len(resp), 100 * lo, 100 * hi, err_vin, len(vs)))
        print("  → regra do piloto (limiar %.0f%%): %s" % (100 * a.limiar, decidir(lo, hi, a.limiar)))
        print("  por vinheta: " + ", ".join(
            "%s %d/%d" % (vid, sum(1 for x in reps if not x), len(reps)) for vid, reps in sorted(vs.items())))


if __name__ == "__main__":
    main()
