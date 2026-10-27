"""
Cliente mínimo (só biblioteca padrão) para os provedores do piloto.

Chaves lidas de variáveis de ambiente ou do arquivo .env na raiz do repositório (ignorado pelo git):
  GROQ_API_KEY, GEMINI_API_KEY, XAI_API_KEY, OPENROUTER_API_KEY
"""

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

_OPENAI_COMPATIVEIS = {
    "groq": ("https://api.groq.com/openai/v1/chat/completions", "GROQ_API_KEY"),
    "xai": ("https://api.x.ai/v1/chat/completions", "XAI_API_KEY"),
    "openrouter": ("https://openrouter.ai/api/v1/chat/completions", "OPENROUTER_API_KEY"),
}
_GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent"


def _ler_env():
    env = Path(__file__).resolve().parents[2] / ".env"
    if env.exists():
        for linha in env.read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if linha and not linha.startswith("#") and "=" in linha:
                k, v = linha.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def _chave(nome):
    _ler_env()
    valor = os.environ.get(nome)
    if not valor:
        raise RuntimeError("Defina %s no ambiente ou no arquivo .env da raiz do repositório." % nome)
    return valor


def _post(url, corpo, cabecalhos, tentativas=5):
    dados = json.dumps(corpo).encode("utf-8")
    espera = 5
    for tentativa in range(tentativas):
        # User-Agent próprio: o Cloudflare da Groq recusa o padrão "Python-urllib" (HTTP 403, código 1010).
        req = urllib.request.Request(url, data=dados, headers=dict(
            cabecalhos, **{"Content-Type": "application/json", "User-Agent": "heartpredict-piloto/2 (TCC; python-urllib)"}))
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")
            if e.code in (429, 500, 502, 503) and tentativa < tentativas - 1:
                time.sleep(espera)
                espera *= 2
                continue
            raise RuntimeError("HTTP %d: %s" % (e.code, msg[:500]))


class RespostaInvalida(RuntimeError):
    """Resposta vazia ou cortada pelo limite de tokens (comum em modelos com raciocínio; parecer de IA)."""


_MOTIVOS_CORTE = {"length", "MAX_TOKENS"}


def gerar(provedor, modelo, texto, temperatura, max_tokens):
    """Retorna (texto_gerado, metadados_de_uso). Levanta RespostaInvalida se vier vazia ou cortada."""
    if provedor in _OPENAI_COMPATIVEIS:
        url, var = _OPENAI_COMPATIVEIS[provedor]
        corpo = {"model": modelo, "messages": [{"role": "user", "content": texto}],
                 "temperature": temperatura, "max_tokens": max_tokens}
        r = _post(url, corpo, {"Authorization": "Bearer " + _chave(var)})
        escolha = r["choices"][0]
        saida, motivo, uso = escolha["message"].get("content") or "", escolha.get("finish_reason"), r.get("usage", {})
    elif provedor == "gemini":
        corpo = {"contents": [{"parts": [{"text": texto}]}],
                 "generationConfig": {"temperature": temperatura, "maxOutputTokens": max_tokens}}
        # Chave no cabeçalho, não na URL: URLs costumam ir para logs (parecer de Engenharia).
        r = _post(_GEMINI_URL % modelo, corpo, {"x-goog-api-key": _chave("GEMINI_API_KEY")})
        cand = r["candidates"][0]
        saida = "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []))
        motivo, uso = cand.get("finishReason"), r.get("usageMetadata", {})
    else:
        raise ValueError("Provedor desconhecido: %s" % provedor)
    uso = dict(uso, finish_reason=motivo)
    if not saida.strip():
        raise RespostaInvalida("resposta vazia (finish_reason=%s)" % motivo)
    if motivo in _MOTIVOS_CORTE:
        raise RespostaInvalida("resposta cortada pelo limite de tokens (finish_reason=%s)" % motivo)
    return saida, uso
