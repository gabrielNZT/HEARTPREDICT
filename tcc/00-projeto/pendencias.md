---
titulo: Pendências e verificações
status: vigente
atualizado: 2026-09-29
resumo: O que precisa ser conferido, lido ou decidido. Marque [x] ao concluir e anote a data.
---

# Pendências

> **Prioridades e ordem de execução:** ver [proximos-passos.md](proximos-passos.md) (riscos que mudam o rumo, bloqueios técnicos e piloto de viabilidade).

## Verificar antes de citar (metadados e números)
- [ ] **jabbour2023jama** — abrir o PDF (JAMA 2023;330(23):2275–2284), conferir números, lista de autores e ler o texto completo.
- [x] **khan2024prevent** — metadados conferidos no PMC e texto completo lido (2026-09-29). Lista de autores anterior estava errada e foi corrigida.
- [ ] *(Mitigado em 29/09/2026: o piloto usa os coeficientes do `preventr`, que reproduzem os 6 valores publicados no artigo — ainda assim conferir contra a S12 original antes do experimento final.)* **PREVENT – Tabela S12 (coeficientes)** — o download automático foi bloqueado (PMC e AHA pedem verificação humana). **Baixar manualmente pelo navegador** o arquivo `NIHMS1953934-supplement-Supplemental_Tables.xlsx` em https://pmc.ncbi.nlm.nih.gov/articles/PMC10910659/ e guardar em `tcc/01-literatura/textos/`. Usar o pacote R `preventr` (CRAN, MIT) apenas como verificação cruzada.
- [x] **sbc2025dislipidemias** — DOI, autores e capítulos 1, 2, 4, 5 lidos na íntegra (2026-09-29).
- [ ] **SBC 2025 – Figura 4.1** (fluxograma de estratificação) — é imagem; abrir o PDF e conferir se a ordem das regras bate com D010.
- [ ] **SBC 2025 – levar ao orientador** as inconsistências internas listadas no fichamento e as escolhas de D010.
- [ ] **isern2016agents** — conferir volume, número e DOI (J Med Syst 2016;40:43?).
- [ ] **jacovi2020faithfulness** — conferir páginas (4198–4205?) e DOI.
- [ ] **hevner2004dsr** — conferir metadados (MIS Quarterly 28(1):75–105?).
- [ ] **han2023llmukb** — verificar se há versão publicada em periódico e usar essa.
- [ ] **tang2024medagents**, **kim2024mdagents** — conferir lista de autores.
- [ ] **asgari2025hallucination** — conferir lista de autores.
- [ ] **chan2025vies** — conferir DOI e ler o texto completo (base de H3).
- [ ] **zhu2025medagentboard**, **cemri2025mast** — conferir volume/páginas nos anais do NeurIPS 2025.
- [ ] **ahmed2025mentalhealth** — verificar como os "99%" foram medidos antes de citar.

## Ler na íntegra (prioridade)
- [x] khan2024prevent (texto principal) — 2026-09-29.
- [x] sbc2025dislipidemias (capítulos relevantes) — 2026-09-29.
- [ ] chan2025vies — método de prompts pareados para H3.
- [ ] turpin2023unfaithful e jacovi2020faithfulness — fundamentação teórica de fidelidade.
- [ ] collins2024tripodai — checklist para a parte de ML.

## Fichar (fundamentação das partes — ver 02-argumentacao/fundamentacao-por-parte.md)
- [ ] Huang et al. — Large Language Models Cannot Self-Correct Reasoning Yet (ICLR 2024) — https://arxiv.org/abs/2310.01798
- [ ] Gou et al. — CRITIC: LLMs Can Self-Correct with Tool-Interactive Critiquing (ICLR 2024) — https://arxiv.org/abs/2305.11738
- [ ] Wolfrath et al. — Stronger Baseline Models (arXiv 2024) — https://arxiv.org/abs/2409.12116
- [ ] Lundberg & Lee — A Unified Approach to Interpreting Model Predictions (NeurIPS 2017) — https://arxiv.org/abs/1705.07874
- [ ] Sundararajan & Najmi — The Many Shapley Values for Model Explanation (ICML 2020) — conferir metadados
- [ ] Liu et al. — Synthetic Benchmarks for Scientific Research in Explainable ML (2021) — https://arxiv.org/abs/2106.12543
- [ ] Kusner et al. — Counterfactual Fairness (NeurIPS 2017) — conferir metadados

## Da auditoria (itens condicionais e especulações)
- [x] C1: definição operacional escrita em `03-metodologia/metricas-fidelidade.md` (2026-09-29).
- [ ] C1 (cont.): validar as métricas — protocolo de anotação, 2 anotadores, κ (seção 7 do documento).
- [ ] Criar o glossário de termos → variáveis e o léxico de direção (métrica 1) antes de rodar o experimento.
- [ ] Fichar FActScore (Min et al., EMNLP 2023) — https://arxiv.org/abs/2305.14251
- [ ] Fichar a revisão de LLM-como-juiz em saúde (arXiv 2605.25273).
- [ ] Ler asgari2025hallucination na íntegra (subtipos de alucinação usados na métrica 4).
- [ ] C5: cálculo de tamanho de amostra após piloto (poder para McNemar).
- [ ] C6: buscar medida de inteligibilidade validada para o português ou retirar a métrica.
- [ ] C8: fazer e documentar uma **busca estruturada** (bases, termos, datas, critérios) para sustentar a lacuna.
- [ ] E6/E7: trocar dados de uso de LLM por médicos e de mortalidade por fontes primárias (preferencialmente brasileiras).
- [ ] E8: fichar estudo de viés de automação com LLM em texto (medRxiv 2025, "Automation Bias in Large Language Model Assisted Diagnostic Reasoning Among AI-Trained Physicians").
- [ ] Ler o texto completo de santos2026escllm (confirmar se o português é europeu e o método de recálculo).
- [x] Modelo do Gemini agora configurável por `GEMINI_MODEL` (2026-09-29). **Falta escolher e registrar o modelo** (bloqueio T3).

## Código (da revisão de arquitetura — D019)
- [x] Remover AgenteNotificador, `mosquitto/`, `ai-services/realtime-anomaly-service/`, `docker-compose.yml` vazio e `create_structure.sh` (2026-09-29).
- [x] Remover dependências MQTT e PostgreSQL do `pom.xml` (2026-09-29).
- [x] Reescrever o README; mover `instructions.md` e `architect.md` para `docs/historico/` com aviso (2026-09-29).
- [x] Apagar a lógica de faixas/"ações" do AgenteJulgador; hoje ele só encaminha ao Explicador (2026-09-29).
- [x] Modelo do Gemini configurável por `GEMINI_MODEL`, endpoint v1beta (2026-09-29).
- [x] Corrigir rótulo "Precisão do modelo" → AUC-ROC (Explicador, gateway, frontend); números do JSON com `Locale.ROOT` (2026-09-29).
- [ ] **Compilar e testar de ponta a ponta** (`mvn clean package`; ainda não verificado — sem Maven no ambiente em que a limpeza foi feita).
- [ ] Remover a regra "IMC > 25 → alerta" do prompt do Explicador **quando o serviço passar a usar o PREVENT** (no modelo atual o IMC é variável de entrada; removê-la agora só trocaria uma heurística por outra).
- [ ] Definir a licença do repositório (o README antigo citava MIT, mas não havia arquivo LICENSE).
- [ ] Implementar um script único de execução (o `docker-compose.yml` estava vazio e foi removido).
- [ ] Definir temperatura fixa do LLM para o experimento (hoje 0,7 no `GeminiClient`).
- [ ] Ler o capítulo de TCC de Wazlawick e o regulamento de TCC do curso.
- [ ] Fichar Wooldridge & Jennings (1995) e Jennings (2000).

## Dependências (D022)
- [x] `backend-gateway/requirements.txt` enxugado para fastapi, uvicorn, pydantic e httpx; instalação limpa e `/health` testados (2026-09-29).
- [ ] Enxugar `ai-services/chronic-risk-service/requirements.txt` (91 linhas, parece `pip freeze`) — fazer junto com a troca para o PREVENT.
- [ ] Confirmar a versão de Python usada e registrar no README.

## Interface (D025)
- [ ] Teste de usabilidade com ~5 pessoas do público-alvo (interface-design.md §8).
- [ ] Mover o núcleo (`experimentos/piloto/{prevent,sbc,renal,gabarito,prompt,llm}.py`) para um pacote próprio; hoje o gateway o importa por caminho (transitório).
- [ ] Religar a explicação ao fluxo JADE com o Verificador (D021) e trocar o aviso "não verificado" pelo resultado real da verificação.
- [ ] Remover o endpoint antigo `/predict` e os modelos Pydantic do dataset do Kaggle quando o JADE for migrado.

## JADE (D021)
- [ ] Reescrever Explicador ↔ Julgador com `ProposeInitiator`/`ProposeResponder` (FIPA-Propose) e limite de rodadas.
- [ ] Reescrever Gerenciador → Classificador com `AchieveREInitiator`/`AchieveREResponder`, com REFUSE para entrada inválida.
- [ ] `conversation-id` por caso e log JSON Lines de todas as mensagens ACL.
- [ ] Configurações experimentais pelos agentes ativos (C-isolado, C-ferramenta, C-verificador).
- [ ] Ler na íntegra: Botti 2025, especificação FIPA SC00036, capítulo de protocolos do JADE Programmer's Guide.

## Brechas a tratar no desenho (B1–B7)
- [ ] B1: definir a avaliação independente do verificador (anotação humana + extrator diferente).
- [ ] B2: definir o baseline isolado forte (equação no prompt ou interpretador de código).
- [ ] B3: restringir o teste de invariância a raça/etnia; sexo por taxa de fidelidade.
- [ ] B4: análise de sensibilidade da referência da atribuição (centralização × média NHANES).
- [ ] B5: escolher a medida de inteligibilidade em português.

## Buscas a repetir
- [ ] Repetir busca de trabalhos similares antes da qualificação e antes da defesa (última: 29/09/2026). Termos: "verifier" + "faithfulness" + "SHAP" + "LLM explanation" + "clinical risk"; "agentic explanation clinical prediction"; "PREVENT LLM".

## Decisões pendentes com o orientador
As pendências científicas P001–P004 foram resolvidas com base na literatura (D013–D016, 2026-09-29). Restam só questões institucionais e de cronograma (O001–O003 em [decisoes.md](decisoes.md)).

## Novas verificações (29/09/2026)
- [ ] Conferir se há microdados laboratoriais públicos da PNS 2014–2015 (colesterol, HDL, creatinina) que permitam uma base brasileira (D013).
- [x] (duplicada da anterior) Modelo configurável; escolha pendente em T3.
- [ ] Verificar a existência e o conteúdo da diretriz de dislipidemia ACC/AHA de 2026, que aparece em buscas como adotando limiares do PREVENT-ASCVD (contexto internacional).
- [ ] Reverificar errata da SBC 2025 antes da defesa.

## Fontes citadas na conversa, ainda sem fichamento
- Survey de GPs no Reino Unido sobre IA generativa (PMC12647557) — autores a identificar.
- Survey de médicos em Omã (PMC12716350) — autores a identificar.
- Estatística Cardiovascular – Brasil 2023 (Arq Bras Cardiol) — metadados a identificar.
- Reportagem Agência Brasil (2024) sobre 400 mil óbitos/ano — **fonte jornalística; preferir a Estatística Cardiovascular** como citação principal.
- AI Act (Regulamento UE 2024/1689), Art. 13 — citar o texto oficial.
- PL 2338/2023 (Senado Federal) — citar a página oficial e registrar o status na data da defesa.
- Dataset `cardio_train` (Kaggle, Ulianova) — citar como conjunto de dados.
- Wazlawick, *Metodologia de Pesquisa para Ciência da Computação* — conferir edição.
