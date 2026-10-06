#!/usr/bin/env python3
"""
Indexador da base de conhecimento do TCC.

Varre os arquivos Markdown de `tcc/` que possuem front-matter YAML simples,
valida os campos obrigatórios dos fichamentos e gera:

  - tcc/INDEX.md                      (índice navegável de tudo)
  - tcc/01-literatura/referencias.bib (BibTeX consolidado dos fichamentos)

Também oferece busca textual em toda a base.

Uso:
  python3 tcc/tools/indexar.py              # regenera INDEX.md e referencias.bib
  python3 tcc/tools/indexar.py validar      # só valida, sem escrever
  python3 tcc/tools/indexar.py buscar TERMO # busca TERMO (case-insensitive)

Sem dependências externas (Python >= 3.8).
"""

import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FICHAMENTOS = RAIZ / "01-literatura" / "fichamentos"
INDEX = RAIZ / "INDEX.md"
BIB = RAIZ / "01-literatura" / "referencias.bib"

OBRIGATORIOS_FICHAMENTO = [
    "chave", "titulo", "autores", "ano", "veiculo", "tipo_bib",
    "url", "temas", "leitura", "relevancia",
]
LEITURA_VALIDOS = {"completa", "parcial", "resumo", "pendente"}
RELEVANCIA_VALIDOS = {"central", "alta", "media", "baixa"}

# Seções de fichamento cujos itens "- [Cn] ..." viram evidências citáveis no índice.
SECAO_EVIDENCIAS = "Dados citáveis"


def parse_front_matter(texto):
    """Parser mínimo de front-matter: `chave: valor` e listas `[a, b]`."""
    if not texto.startswith("---\n"):
        return {}, texto
    fim = texto.find("\n---", 4)
    if fim == -1:
        return {}, texto
    bloco, corpo = texto[4:fim], texto[fim + 4:]
    meta = {}
    for linha in bloco.splitlines():
        if not linha.strip() or linha.lstrip().startswith("#") or ":" not in linha:
            continue
        chave, valor = linha.split(":", 1)
        valor = valor.strip()
        if valor.startswith("[") and valor.endswith("]"):
            valor = [v.strip().strip("\"'") for v in valor[1:-1].split(",") if v.strip()]
        else:
            valor = valor.strip("\"'")
        meta[chave.strip()] = valor
    return meta, corpo


def como_lista(valor):
    if isinstance(valor, list):
        return valor
    return [valor] if valor else []


def carregar_documentos():
    docs = []
    for caminho in sorted(RAIZ.rglob("*.md")):
        if caminho == INDEX or "textos" in caminho.parts:
            continue
        meta, corpo = parse_front_matter(caminho.read_text(encoding="utf-8"))
        docs.append({"caminho": caminho, "meta": meta, "corpo": corpo})
    return docs


def validar(docs):
    erros = []
    chaves = {}
    for d in docs:
        if FICHAMENTOS not in d["caminho"].parents:
            continue
        m, rel = d["meta"], d["caminho"].relative_to(RAIZ)
        for campo in OBRIGATORIOS_FICHAMENTO:
            if not m.get(campo):
                erros.append(f"{rel}: campo obrigatório ausente: {campo}")
        if m.get("leitura") and m["leitura"] not in LEITURA_VALIDOS:
            erros.append(f"{rel}: leitura inválida '{m['leitura']}' (use {sorted(LEITURA_VALIDOS)})")
        if m.get("relevancia") and m["relevancia"] not in RELEVANCIA_VALIDOS:
            erros.append(f"{rel}: relevancia inválida '{m['relevancia']}' (use {sorted(RELEVANCIA_VALIDOS)})")
        chave = m.get("chave")
        if chave:
            if chave in chaves:
                erros.append(f"{rel}: chave duplicada '{chave}' (também em {chaves[chave]})")
            chaves[chave] = rel
            if d["caminho"].stem != chave:
                erros.append(f"{rel}: nome do arquivo deve ser igual à chave ('{chave}.md')")
    return erros


def extrair_evidencias(corpo):
    """Retorna itens '- [Cn] texto' da seção 'Dados citáveis'."""
    padrao = re.compile(r"^##\s+" + re.escape(SECAO_EVIDENCIAS) + r"\s*$(.*?)(?=^##\s|\Z)", re.M | re.S)
    achado = padrao.search(corpo)
    if not achado:
        return []
    itens = []
    for linha in achado.group(1).splitlines():
        m = re.match(r"^\s*-\s*\[(C\d+)\]\s*(.+)$", linha)
        if m:
            itens.append((m.group(1), m.group(2).strip()))
    return itens


def link(caminho):
    return caminho.relative_to(RAIZ).as_posix()


def gerar_index(docs):
    fich = [d for d in docs if FICHAMENTOS in d["caminho"].parents]
    outros = [d for d in docs if d not in fich and d["caminho"].name != "README.md"]
    ordem_rel = {"central": 0, "alta": 1, "media": 2, "baixa": 3}
    fich.sort(key=lambda d: (ordem_rel.get(d["meta"].get("relevancia"), 9), d["meta"].get("chave", "")))

    L = ["# Índice da base de conhecimento do TCC", ""]
    L.append(f"> Arquivo **gerado automaticamente** por `tcc/tools/indexar.py` em {date.today().isoformat()}. "
             "Não edite à mão; edite os arquivos de origem e rode o script.")
    L.append("")

    L += ["## Documentos do projeto", "", "| Documento | Status | Atualizado | Resumo |", "|---|---|---|---|"]
    for d in outros:
        m = d["meta"]
        titulo = m.get("titulo", d["caminho"].stem)
        L.append(f"| [{titulo}]({link(d['caminho'])}) | {m.get('status', '—')} | "
                 f"{m.get('atualizado', '—')} | {m.get('resumo', '')} |")
    L.append("")

    total = len(fich)
    por_leitura = {}
    for d in fich:
        por_leitura.setdefault(d["meta"].get("leitura", "?"), []).append(d)
    resumo_leitura = ", ".join(f"{k}: {len(v)}" for k, v in sorted(por_leitura.items()))
    L += ["## Literatura", "", f"**{total} fichamentos** ({resumo_leitura}).", ""]
    L += ["| Chave | Ano | Veículo | Leitura | Relevância | Temas |", "|---|---|---|---|---|---|"]
    for d in fich:
        m = d["meta"]
        L.append(f"| [{m.get('chave')}]({link(d['caminho'])}) | {m.get('ano', '')} | {m.get('veiculo', '')} | "
                 f"{m.get('leitura', '')} | {m.get('relevancia', '')} | {', '.join(como_lista(m.get('temas')))} |")
    L.append("")

    temas = {}
    for d in fich:
        for t in como_lista(d["meta"].get("temas")):
            temas.setdefault(t, []).append(d["meta"].get("chave"))
    L += ["### Por tema", ""]
    for t in sorted(temas):
        L.append(f"- **{t}**: " + ", ".join(f"[{c}](01-literatura/fichamentos/{c}.md)" for c in sorted(temas[t])))
    L.append("")

    pend = [d for d in fich if d["meta"].get("leitura") in ("resumo", "pendente", "parcial")]
    if pend:
        L += ["### Leitura incompleta (verificar antes de citar números)", ""]
        for d in pend:
            m = d["meta"]
            L.append(f"- [{m.get('chave')}]({link(d['caminho'])}) — leitura: {m.get('leitura')}")
        L.append("")

    L += ["## Evidências citáveis", "",
          "Afirmações extraídas das seções *Dados citáveis* dos fichamentos, com localização no texto original.", "",
          "| Fonte | Id | Evidência |", "|---|---|---|"]
    for d in fich:
        chave = d["meta"].get("chave")
        for cid, txt in extrair_evidencias(d["corpo"]):
            L.append(f"| [{chave}]({link(d['caminho'])}) | {cid} | {txt.replace('|', '/')} |")
    L.append("")
    return "\n".join(L)


def escapar_bib(s):
    return s.replace("&", r"\&").replace("%", r"\%")


def gerar_bib(docs):
    entradas = []
    for d in docs:
        if FICHAMENTOS not in d["caminho"].parents:
            continue
        m = d["meta"]
        tipo = m.get("tipo_bib", "misc")
        campo_veiculo = {"article": "journal", "inproceedings": "booktitle"}.get(tipo, "howpublished")
        # "et al." nos fichamentos vira "others", a convenção do BibTeX para lista incompleta.
        autores = " and ".join("others" if a.strip().lower() in ("et al.", "et al") else a
                               for a in como_lista(m.get("autores")))
        campos = [
            ("title", "{" + escapar_bib(m.get("titulo", "")) + "}"),
            ("author", autores),
            ("year", m.get("ano", "")),
            (campo_veiculo, escapar_bib(m.get("veiculo", ""))),
            ("volume", m.get("volume", "")),
            ("pages", m.get("paginas", "")),
            ("doi", m.get("doi", "")),
            ("url", m.get("url", "")),
        ]
        corpo = ",\n".join(f"  {k} = {{{v}}}" for k, v in campos if v)
        entradas.append(f"@{tipo}{{{m.get('chave')},\n{corpo}\n}}")
    cabecalho = "% Gerado automaticamente por tcc/tools/indexar.py. Não edite à mão.\n\n"
    return cabecalho + "\n\n".join(entradas) + "\n"


def normalizar(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def buscar(termo):
    alvo = normalizar(termo)
    achou = False
    for caminho in sorted(RAIZ.rglob("*.md")):
        if caminho == INDEX or "textos" in caminho.parts:
            continue
        for n, linha in enumerate(caminho.read_text(encoding="utf-8").splitlines(), 1):
            if alvo in normalizar(linha):
                achou = True
                print(f"{link(caminho)}:{n}: {linha.strip()[:200]}")
    if not achou:
        print(f"Nada encontrado para '{termo}'.")


def main(argv):
    if len(argv) >= 2 and argv[1] == "buscar":
        if len(argv) < 3:
            sys.exit("Uso: indexar.py buscar TERMO")
        buscar(" ".join(argv[2:]))
        return
    docs = carregar_documentos()
    erros = validar(docs)
    for e in erros:
        print("ERRO:", e)
    if len(argv) >= 2 and argv[1] == "validar":
        sys.exit(1 if erros else 0)
    INDEX.write_text(gerar_index(docs), encoding="utf-8")
    BIB.write_text(gerar_bib(docs), encoding="utf-8")
    n = sum(1 for d in docs if FICHAMENTOS in d["caminho"].parents)
    print(f"INDEX.md e referencias.bib gerados ({n} fichamentos, {len(erros)} erro(s)).")


if __name__ == "__main__":
    try:
        main(sys.argv)
    except BrokenPipeError:  # saída cortada por `| head`, por exemplo
        sys.stderr.close()
