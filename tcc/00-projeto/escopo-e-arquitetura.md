---
titulo: Revisão de escopo e arquitetura para TCC de graduação
status: vigente
atualizado: 2026-09-29
resumo: Avaliação de cada componente existente no repositório (fundamento e destino), redimensionamento do escopo para TCC de graduação (núcleo × extensões) e enquadramento honesto do uso de agentes.
---

# Revisão de escopo e arquitetura

## 1. O que uma banca espera de um TCC de graduação

Expectativas usuais de TCC em Computação: problema bem delimitado, objetivos mensuráveis, fundamentação, trabalhos relacionados, método, desenvolvimento, **avaliação** e conclusões honestas. A originalidade exigida é **menor** que em mestrado ou doutorado; conta mais a **coerência entre problema, método e avaliação** e a **viabilidade** no prazo. Referência de apoio: Wazlawick, *Metodologia de Pesquisa para Ciência da Computação* (obra voltada da graduação ao doutorado — ler o capítulo sobre TCC). **Conferir o regulamento de TCC do seu curso**, que é a regra que vale.

**Diagnóstico honesto:** ao longo desta conversa o desenho cresceu para um tamanho de **mestrado**: 6 métricas, 2 níveis de verificação, 3 hipóteses, 5 análises de sensibilidade, 2 LLMs, NHANES + sintéticos, anotação dupla, extensão com XGBoost. Para caber num TCC, é preciso separar **núcleo** de **extensões** (seção 4).

## 2. Componentes existentes: fundamento e destino

Inspeção do repositório em 29/09/2026.

| Componente | O que faz hoje (verificado no código) | Fundamento | Destino |
|---|---|---|---|
| **Frontend React** (formulário conversacional) | Coleta dados e mostra a explicação | Requisito de interface; não é objeto de pesquisa | **Mantém**, adaptando os campos às variáveis do PREVENT |
| **backend-gateway** (FastAPI) | Recebe do frontend, repassa ao JADE, espera a explicação por *polling* (60 s) | Integração; não precisa de fundamento acadêmico | **Mantém** |
| **chronic-risk-service** (XGBoost + `cardio_train`) | Prevê presença de doença; faixas de risco **0,3 / 0,6 / 0,8** e textos de interpretação fixos | ❌ Dataset transversal; faixas **arbitrárias**; interpretação cita IMC (fora do PREVENT-ASCVD) | **Substituir o conteúdo**: PREVENT-ASCVD + regras SBC + Shapley (D009–D012). O serviço (contêiner/API) é reaproveitado |
| **AgenteGerenciadorPacientes** | Servidor HTTP que recebe e repassa ao Classificador | Entrada do sistema | **Mantém**, acrescentando validação das faixas do PREVENT e recusa de dado ausente (AgentMD; Zhu 2026) |
| **AgenteClassificador** | Chama o serviço de risco | Envolve a ferramenta | **Mantém** |
| **AgenteJulgador** | Reclassifica com **outras** faixas (0,2 / 0,4 / 0,6 / 0,8) e **imprime "ações"** ("alertar equipe de emergência", "notificar familiares") | ❌ Faixas arbitrárias e **inconsistentes** com as do serviço; condutas **sem base** e **inadequadas** para risco preventivo em 10 anos | **Reaproveitar como Verificador** (núcleo da pesquisa; MAST, CRITIC, Huang 2024). Remover a lógica atual |
| **AgenteExplicador** + `GeminiClient` | Monta prompt e chama o Gemini | Papel correto, mas: usa **Gemini 1.5 (desligado → 404)**; o prompt classifica **IMC > 25 como "alerta"**, induzindo exatamente o erro "variável fora do modelo" | **Mantém o papel**; trocar o modelo; entrada estruturada (risco, categoria, atribuições) |
| **AgenteNotificador** | Só imprime mensagens; **nenhum agente envia mensagens a ele e ele nem é iniciado** no `run-agents.sh` | ❌ Sem função | **Remover** |
| **Mosquitto (MQTT)** | Só o arquivo de configuração; **nenhum código** usa MQTT | ❌ Era para ECG em tempo real, fora do escopo | **Remover do TCC** (trabalho futuro) |
| **realtime-anomaly-service** | Só `requirements.txt`; **sem código** | ❌ Fora do escopo | **Remover** |
| **PostgreSQL/TimescaleDB, Prometheus, CI, SHAP/LIME** | Citados no README; **não implementados** | ❌ | **Tirar do README** (a banca pode abrir o repositório) |
| **docker-compose.yml** | **Vazio** | — | Implementar **ou** substituir por script de execução; reprodutibilidade é esperada |
| **trigger/disparar_registro.py** | Envia um paciente de teste | Utilitário | **Evoluir para o executor do experimento** (roda as vinhetas nas 3 configurações) |

## 3. O "multiagente" se sustenta? (a pergunta mais provável da banca)

**Referência clássica:** Wooldridge & Jennings (1995) definem agente pela **autonomia**, **reatividade**, **proatividade** e **habilidade social**. Jennings (2000) discute tanto as vantagens da abordagem orientada a agentes quanto suas **desvantagens**.

**Diagnóstico do sistema atual:** os agentes formam uma **cadeia sequencial de requisição e resposta**. Há **habilidade social** (mensagens FIPA-ACL) e reatividade, mas quase nenhuma autonomia ou proatividade. Na terminologia atual de sistemas com LLM, isso é um **workflow** (caminho definido em código), não um sistema de agentes que decidem o próprio caminho (Anthropic, *Building Effective Agents* — fonte da indústria, não revisada por pares **[S]**). O par **Explicador ↔ Verificador** corresponde ao padrão "avaliador-otimizador" descrito nessa mesma fonte, e é **o único ponto com interação iterativa real** entre agentes.

**Como enquadrar sem se expor:**
- Não vender o trabalho como "sistema multiagente autônomo". Descrever como **arquitetura orientada a agentes, implementada em JADE, em que cada agente encapsula uma responsabilidade**, e o ciclo Explicador–Verificador é a interação central.
- Justificar o JADE **pragmaticamente**: código já existente; comunicação padronizada (FIPA-ACL); separação de responsabilidades facilita trocar componentes (ex.: trocar o LLM). Declarar que a **pergunta de pesquisa não depende da plataforma**.
- Citar MedAgentBoard e MAST para mostrar consciência de que **complexidade de agentes precisa ser justificada** — o trabalho usa o **mínimo necessário**.

**Atualização (D021):** a justificativa foi fortalecida — o JADE passa a ser usado para protocolos FIPA (Propose/Request), recusa tipada, rastro auditável e ablação por composição. Ver [justificativa-jade](../02-argumentacao/justificativa-jade.md).

~~**Alternativa (para discutir com o orientador — O004):**~~ implementar tudo como workflow em Python, sem JADE. Seria mais simples, mas muda o enquadramento original do trabalho ("multiagente"). As duas opções são defensáveis; a atual (manter JADE com enquadramento honesto) aproveita mais o que já existe.

## 4. Escopo redimensionado

### 4.1 Núcleo (o que o TCC precisa entregar)
1. **Ferramenta:** PREVENT-ASCVD 10 anos + categoria SBC (escopo D011) + atribuição Shapley, com **testes unitários** (caso publicado 3,6% / 6,0%).
2. **Arquitetura:** 4 agentes (Entrada, Classificador, Explicador, Verificador), com **Verificador só de nível 1 (determinístico)** e ciclo de correção com limite de tentativas.
3. **Dados:** vinhetas do **NHANES 2017–mar/2020** (mesmo ciclo usado por Anderson 2024) filtradas pelo escopo e estratificadas por categoria, mais um conjunto pequeno de **casos sintéticos dirigidos** (ex.: IMC alto com risco baixo).
4. **Experimento:** 3 configurações × 2 LLMs; desfecho principal **"explicação totalmente fiel"** (McNemar); métricas secundárias: polaridade, exatidão numérica, variáveis fora do modelo, top-k.
5. **Validação:** anotação dupla de uma amostra, com κ, e avaliação **independente** do verificador (B1).
6. **Sensibilidade:** apenas ε (métrica 1) e regra de agravante (D010).
7. **Hipóteses:** H1 (replicação) e **H2 (contribuição)**.

### 4.2 Extensões (só se sobrar tempo; senão, trabalhos futuros)
- Verificador nível 2 (LLM como juiz).
- H3 (viés/raça) — com a métrica 3, que já está no núcleo, os dados para H3 já são coletados; a análise formal é extensão.
- XGBoost como segundo modelo explicado (D016).
- Avaliação por médicos (D015).
- Sensibilidade da referência da atribuição (média NHANES).
- Medida de inteligibilidade em português.

### 4.3 Fora do escopo (declarar como trabalhos futuros)
ECG em tempo real, MQTT, banco temporal, validação clínica prospectiva, uso como dispositivo médico.

## 5. Mapeamento para o documento do TCC
| Capítulo | Conteúdo |
|---|---|
| 1. Introdução | Problema, pergunta, objetivos (geral + específicos = itens 1–5 do núcleo) |
| 2. Fundamentação | Risco CV e PREVENT/SBC; LLMs e alucinação; XAI, Shapley e fidelidade; agentes (Wooldridge & Jennings) |
| 3. Trabalhos relacionados | Tabela comparativa |
| 4. Método | Design Science; arquitetura; dados; métricas; protocolo experimental |
| 5. Desenvolvimento | Implementação e testes da ferramenta, dos agentes e do verificador |
| 6. Resultados e discussão | H1, H2, validação das métricas, análise de erros, limitações |
| 7. Conclusão | Contribuições, limitações, trabalhos futuros |
