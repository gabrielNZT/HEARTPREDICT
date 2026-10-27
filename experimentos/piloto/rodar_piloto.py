"""
Executa o piloto (D023): configuração C-ferramenta (sem verificador).

Exemplos:
  python3 rodar_piloto.py --seco                                   # só gera gabarito e prompts, sem LLM
  python3 rodar_piloto.py --provedor groq --modelo <id> --repeticoes 3
  python3 rodar_piloto.py --provedor gemini --modelo <id> --atraso 7
"""

import argparse
import datetime
import json
import subprocess
import time
from pathlib import Path

import gabarito
import llm
import prompt
import vinhetas

DIR = Path(__file__).parent / "resultados"


def commit_atual():
    try:
        # --dirty: marca quando o código em execução difere do commit (parecer de Engenharia, C1)
        return subprocess.check_output(["git", "describe", "--always", "--dirty"], cwd=Path(__file__).parent,
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "desconhecido"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provedor", choices=["groq", "gemini", "xai", "openrouter"])
    ap.add_argument("--modelo")
    ap.add_argument("--repeticoes", type=int, default=3)
    ap.add_argument("--temperatura", type=float, default=0.7)
    ap.add_argument("--max-tokens", type=int, default=2048)
    ap.add_argument("--atraso", type=float, default=3.0, help="segundos entre chamadas (limites do plano gratuito)")
    ap.add_argument("--vinhetas", help="ids separados por vírgula (padrão: todas)")
    ap.add_argument("--seco", action="store_true", help="não chama o LLM")
    ap.add_argument("--novas-tentativas", type=int, default=2,
                    help="tentativas extras quando a resposta vem vazia ou cortada (todas ficam registradas)")
    a = ap.parse_args()

    DIR.mkdir(exist_ok=True)
    vs = vinhetas.todas()
    if a.vinhetas:
        ids = set(a.vinhetas.split(","))
        vs = [v for v in vs if v["id"] in ids]
    gabs = [gabarito.montar(v) for v in vs]
    (DIR / "gabarito.json").write_text(json.dumps(gabs, ensure_ascii=False, indent=1), encoding="utf-8")

    if a.seco:
        (DIR / "prompt_exemplo.txt").write_text(prompt.construir(gabs[0]), encoding="utf-8")
        for g in gabs:
            print("%s %5.1f%% %-14s top: %s" % (g["id"], g["risco_pct"], g["categoria"], ", ".join(g["ranking"][:3])))
        return

    if not (a.provedor and a.modelo):
        ap.error("--provedor e --modelo são obrigatórios (ou use --seco)")

    carimbo = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    saida = DIR / ("%s_%s_%s.jsonl" % (carimbo, a.provedor, a.modelo.replace("/", "-")))
    meta = {"provedor": a.provedor, "modelo": a.modelo, "temperatura": a.temperatura, "max_tokens": a.max_tokens,
            "prompt_versao": prompt.VERSAO, "commit": commit_atual(), "configuracao": "C-ferramenta"}
    with saida.open("w", encoding="utf-8") as f:
        for g in gabs:
            texto = prompt.construir(g)
            for rep in range(1, a.repeticoes + 1):
                reg = dict(meta, vinheta=g["id"], repeticao=rep, prompt_hash=prompt.hash_prompt(texto),
                           inicio=datetime.datetime.now().isoformat(timespec="seconds"))
                # Respostas vazias/cortadas não contam como explicação válida: são registradas e refeitas.
                # A taxa de invalidez é reportada à parte (não entra na fidelidade). Parecer de IA/Metodologia.
                reg["tentativas_invalidas"] = []
                for _ in range(1 + a.novas_tentativas):
                    try:
                        reg["resposta"], reg["uso"] = llm.gerar(a.provedor, a.modelo, texto, a.temperatura, a.max_tokens)
                        break
                    except llm.RespostaInvalida as e:
                        reg["tentativas_invalidas"].append(str(e))
                        time.sleep(a.atraso)
                    except Exception as e:
                        reg["erro"] = str(e)
                        break
                else:
                    reg["erro"] = "sem resposta válida após %d tentativas" % (1 + a.novas_tentativas)
                f.write(json.dumps(reg, ensure_ascii=False) + "\n")
                f.flush()
                print("%s rep %d %s" % (g["id"], rep, "ERRO: " + reg["erro"][:120] if "erro" in reg else "ok"))
                time.sleep(a.atraso)
    print("Resultados em", saida)


if __name__ == "__main__":
    main()
