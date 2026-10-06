# HEARTPREDICT

Protótipo de pesquisa (TCC de Engenharia de Computação) sobre **explicações de risco cardiovascular geradas por LLM**: o risco é calculado por ferramenta determinística, um LLM explica o resultado em português, e um agente verificador confere se a explicação é fiel ao cálculo.

> **Não é um dispositivo médico.** Uso exclusivamente acadêmico.

## Estado atual (transição)

O projeto está migrando da versão inicial para a arquitetura definida no TCC. Hoje:

| Componente | Situação |
|---|---|
| `frontend/` (React + Vite) | **Nova interface** (29/09/2026): perguntas do escopo PREVENT, resultado com pictograma, categoria SBC, fatores e explicação de IA. Especificação: `tcc/03-metodologia/interface-design.md` |
| `backend-gateway/` (FastAPI, porta 8000) | `POST /api/avaliacao` (cálculo PREVENT + SBC) e `POST /api/avaliacao/explicacao` (texto de IA, **ainda sem passar pelos agentes JADE**). O endpoint antigo `/predict` continua ligado ao fluxo JADE |
| `jade-agents/` (JADE) | Funcional com 4 agentes: Gerenciador, Classificador, Julgador e Explicador |
| `ai-services/chronic-risk-service/` (FastAPI, porta 8002) | **Versão inicial:** XGBoost treinado no dataset Cardiovascular Disease (Kaggle). **Será substituído** pelo escore PREVENT + regras da Diretriz SBC 2025 |
| `AgenteJulgador` | Hoje só encaminha resultados ao Explicador; **será o Verificador** de fidelidade |

Decisões, justificativas e referências: [`tcc/`](tcc/INDEX.md) (comece por [`tcc/00-projeto/proposta.md`](tcc/00-projeto/proposta.md)).

## Fluxo atual

```
frontend → backend-gateway (8000) → AgenteGerenciadorPacientes (HTTP 8888)
        → AgenteClassificador → chronic-risk-service (8002)
        → AgenteJulgador → AgenteExplicador → LLM (Gemini)
        → explicação devolvida ao backend-gateway → frontend
```

## Como executar

Pré-requisitos: Python ≥ 3.11, Java 17 + Maven, Node.js ≥ 18, chave da API do Gemini.

```bash
# 1. Serviço de risco
cd ai-services/chronic-risk-service && pip install -r requirements.txt && ./run.sh

# 2. Gateway
cd backend-gateway && pip install -r requirements.txt && python app/main.py

# Explicação por IA na nova interface: no arquivo .env da raiz
#   LLM_PROVEDOR=groq            (ou gemini)
#   LLM_MODELO=<id do modelo>
#   GROQ_API_KEY=...             (ou GEMINI_API_KEY=...)

# 3. Agentes JADE (fluxo antigo /predict)
export GEMINI_API_KEY='sua_chave'
export GEMINI_MODEL='<id de um modelo vigente>'   # ver https://ai.google.dev/gemini-api/docs/deprecations
cd jade-agents && ./run-agents.sh

# 4. Frontend
cd frontend && npm install && npm run dev
```

`GEMINI_MODEL` é obrigatória: o modelo não é fixado no código porque versões do Gemini são desligadas periodicamente. Registre a versão usada em cada experimento.

Para testar sem o frontend: `python trigger/disparar_registro.py`.

## Estrutura

```
ai-services/chronic-risk-service/   serviço de risco (versão inicial, a substituir)
backend-gateway/                    API de integração
jade-agents/                        agentes JADE e cliente do LLM
frontend/                           interface web
trigger/                            script de teste
tcc/                                base de conhecimento do TCC (literatura, decisões, métodos)
docs/historico/                     planejamento da arquitetura original (substituída)
```

## Fora do escopo

A versão original previa ECG em tempo real, MQTT, banco temporal (TimescaleDB) e um serviço XAI separado. Esses componentes **não foram implementados** e foram retirados do escopo do TCC (ver `tcc/00-projeto/decisoes.md`, D008 e D019).

## Licença

A definir.
