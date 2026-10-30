# Piloto de viabilidade (D023)

Mede se, **sem verificador**, os LLMs atuais ainda erram ao explicar o resultado do PREVENT. Se quase não errarem, a hipótese H2 do TCC fica sem objeto e a tarefa precisa ser ajustada (ver `tcc/00-projeto/proximos-passos.md`, seção C).

Configuração testada: **C-ferramenta** — o LLM recebe dados do paciente, risco calculado, categoria SBC, meta de LDL-c e contribuição de cada fator, e só precisa explicar.

## Arquivos
| Arquivo | Função |
|---|---|
| `prevent.py` | PREVENT-ASCVD 10 anos + atribuição de Shapley exata (D009, D012) |
| `coeficientes_prevent_base_10a.json` | Coeficientes (fonte **provisória**: pacote R `preventr`; conferir contra a Tabela S12 original) |
| `sbc.py` | Categoria e metas da Diretriz SBC 2025 no escopo D011 (D010) |
| `vinhetas.py` | 24 vinhetas sintéticas, incluindo casos-armadilha |
| `gabarito.py` | Pacote de referência de cada vinheta |
| `prompt.py` | Prompt da configuração C-ferramenta (versão `piloto-v1`) |
| `llm.py` | Cliente Groq / Gemini / xAI / OpenRouter (só biblioteca padrão) |
| `rodar_piloto.py` | Executa e salva respostas em `resultados/*.jsonl` com metadados (modelo, temperatura, commit, hash do prompt) |
| `preanotar.py` | Sinalização **heurística** e planilha CSV para anotação humana |
| `resumir.py` | Taxa de explicações com erro (IC 95% de Wilson) e regra de decisão |
| `test_prevent.py` | Testes: reproduz os 6 valores publicados no artigo do PREVENT |

Nenhuma dependência além do Python 3.8+, exceto `planilha_cega.py`, que usa `openpyxl` para gerar e ler a planilha .xlsx.

## Como rodar
```bash
cd experimentos/piloto
python3 -m unittest test_prevent          # 7 testes
python3 rodar_piloto.py --seco            # gabarito + prompt de exemplo, sem LLM
```

Crie um arquivo `.env` na **raiz do repositório** (já ignorado pelo git):
```
GROQ_API_KEY=...
GEMINI_API_KEY=...
```

Rode com um modelo aberto (Groq) e um fechado (Gemini). **Confira os IDs vigentes no console de cada provedor**:
```bash
python3 rodar_piloto.py --provedor groq   --modelo <id do gpt-oss-120b no Groq> --repeticoes 3 --atraso 3
python3 rodar_piloto.py --provedor gemini --modelo <id de um Gemini Flash/Flash-Lite> --repeticoes 3 --atraso 7
```
24 vinhetas × 3 repetições = 72 chamadas por modelo.

Depois, anotação **cega** (sem pré-anotação, modelo nem repetição; ordem aleatória):
```bash
python3 planilha_cega.py gerar resultados/<a>.jsonl resultados/<b>.jsonl --repeticao 1   # D035; gera anotacao_cega_<carimbo>.xlsx e _CHAVE.csv
# preencher as colunas H_* (definições em tcc/03-metodologia/metricas-fidelidade.md) SEM abrir o _CHAVE.csv
python3 planilha_cega.py revelar resultados/anotacao_cega_<carimbo>.xlsx    # junta com a chave → _revelada.csv
python3 resumir.py resultados/anotacao_cega_<carimbo>_revelada.csv
```
Guia de anotação: `tcc/03-metodologia/guia-anotacao-piloto.md`.
`preanotar.py` fica para depois da anotação (comparar heurística × humano), nunca antes.

Prompt vigente: `piloto-v3` (D036, metas de LDL-c e não-HDL-c). As execuções com `piloto-v2` (`20261006-011741_groq_openai-gpt-oss-120b.jsonl`, `20261026-225229_groq_qwen-qwen3.8-27b.jsonl` e a interrompida `20261006-012816_groq_qwen-qwen3.8-27b.jsonl`) ficam como histórico e não entram na decisão do piloto, que é refeito com o v3.

## Parâmetros do piloto (registrar no TCC)
- Temperatura 0,7 (a mesma do sistema atual); 3 repetições; máximo de 2048 tokens.
- Limiar de decisão: 10% das respostas com algum erro (**autoral; confirmar com o orientador**).

## Limitações
- Vinhetas sintéticas e escolhidas para provocar erros: a taxa de erro do piloto **não** estima a taxa em uso real.
- Anotação por uma pessoa, sem κ: serve para decidir o rumo, não como resultado do TCC.
- A pré-anotação é heurística e não mede polaridade: a anotação humana é a referência.
