---
titulo: Pendências e verificações
status: vigente
atualizado: 2026-10-30
resumo: O que precisa ser conferido, lido ou decidido. Marque [x] ao concluir e anote a data.
---

# Pendências

> **Prioridades e ordem de execução:** ver [proximos-passos.md](proximos-passos.md) (riscos que mudam o rumo, bloqueios técnicos e piloto de viabilidade).

## Da banca simulada (pareceres em `05-banca/`, 29/09 a 06/10/2026)

Feito (código, com testes): regras da SBC e escopo (D026); prompt v2 e raça/cor (D027); consentimento, bloqueio do Gemini gratuito e fluxo legado desligado (D028); regra do piloto com IC (D029); defeitos de interface (P1–P9, P11 do parecer de IHC); fichamentos de He & Martens, Ichmoukhamedov, Pedroso e Neuen; justificativa do JADE reescrita (D032); rótulos de leitura corrigidos.

**Pendências críticas (mudam o rumo ou bloqueiam a defesa)**
- [ ] **Piloto:** anotar as respostas (orientando), sem ver a pré-anotação, e aplicar `resumir.py`.
  - [x] Execução completa (2026-10-26): `gpt-oss-120b` 72/72 (commit `03c2712-dirty`, 06/10) e `qwen3.8-27b` 72/72 (commit limpo `d3712eb`, 26/10; refeita inteira porque a de 06/10 parou em 16/72). Prompt idêntico nas 24 vinhetas (mesmo hash); nenhuma resposta vazia, cortada ou com erro.
  - [x] Planilha cega gerada (2026-10-30, D035): `experimentos/piloto/planilha_cega.py --repeticao 1` → `resultados/anotacao_cega_20261030-153928.xlsx` (48 respostas = 1ª repetição × 24 vinhetas × 2 modelos, embaralhadas, sem modelo nem pré-anotação; coluna `fatores(gabarito)` com aumentaram/diminuíram/desprezíveis; chave em `_CHAVE.csv`). Substitui a planilha de 144 de 26/10, apagada sem anotação. Fluxo gerar → revelar → `resumir.py` testado com dados falsos. Em .xlsx desde 30/10 (o CSV quebrava colunas no LibreOffice); altura de linha fixa, S/N com lista; conferido que o LibreOffice lê 17 colunas em todas as linhas.
  - [x] Guia de anotação com exemplos inventados: `tcc/03-metodologia/guia-anotacao-piloto.md` (2026-10-30).
  - [x] Prompt `piloto-v3` e verificador `verificador-v2` com a meta de não-HDL-c (D036, 2026-10-30; 22 testes do verificador, testes de SBC/PREVENT e 18 do gateway passando). As execuções e a planilha acima (v2) ficam obsoletas; a planilha v2 foi apagada sem anotação.
  - [ ] **Refazer as execuções com `piloto-v3`** nos dois modelos, a partir de um commit limpo.
  - [ ] Gerar a nova planilha cega (`planilha_cega.py gerar … --repeticao 1`).
  - [ ] **Anotar** a planilha (orientando) sem abrir a chave; depois `planilha_cega.py revelar` e `resumir.py`.
  - [ ] Declarar no TCC: origens diferentes das duas execuções (commit sujo × limpo, mesmo prompt) e cegueira só quanto ao rótulo (o estilo pode denunciar o modelo).
- [ ] **Tamanho da amostra** com a taxa de erro do piloto (D029).
- [ ] **Validar o plano de análise (D029) com o orientador** — O006.
- [ ] **Verificador como módulo Python** (D034), com extrator testado contra os 26 casos adversariais da banca; segundo extrator, diferente, para a avaliação.
  - [x] Módulo `experimentos/piloto/verificador.py` (nível 1, determinístico) e `test_verificador.py` com os 26 casos (2026-10-06; 21 testes passando em 2026-10-25). Acertar esses casos não valida o extrator.
  - [ ] Segundo extrator, diferente, para a avaliação (B1).
  - [ ] Não rodar o verificador nas respostas do piloto antes de terminar a anotação cega.
- [ ] **Executor único** das três configurações.
- [ ] **JADE (D032):** serviço Python fino; `AchieveREResponder` no Calculador; `ProposeInitiator`/`ProposeResponder` no ciclo; `conversation-id` e `reply-by`; log JSON Lines; teste de ponta a ponta; versionar o jar; religar o Calculador ao PREVENT.
- [ ] **Busca de literatura com protocolo** (parecer de Literatura, §6.3; 25–40 h). Até lá, a lacuna é escrita como "nos trabalhos lidos".
- [ ] **Decidir com o orientador** as atividades com participantes (O005) e se "multiagente" é requisito (O004).

**Metodologia**
- [ ] Definir o C-isolado: com a equação no prompt ou com interpretador de código (B2).
- [ ] Definir a temperatura do experimento (o piloto usa 0,7; a literatura de referência usa 0).
- [ ] Seção de método no formato de Peffers et al. (2007) e tabela de ameaças à validade (Wohlin et al., 2012). Ler as duas fontes e Hevner (2004).
- [ ] Sensibilidade da referência da atribuição com o NHANES real (B4) e contagem de afirmações que mudam de veredito entre convenções.
- [ ] Controle "mais tentativas sem correção específica": incluir como 4ª condição ou declarar como limitação.
- [ ] Anotação cega e ≥ 100 textos em dupla anotação para o κ.

**Cálculo e clínica**
- [ ] Conferir os coeficientes contra a Tabela S12 (inclui todo o modelo masculino e os termos de estatina, diabetes e TFGe < 60, que o caso publicado não exercita). Depende do download manual.
- [ ] Testes com ≥ 10 perfis masculinos e perfis com estatina e TFGe < 60 contra a calculadora oficial da AHA.
- [ ] Hipercolesterolemia familiar como exclusão; mensagem sobre risco em 30 anos para jovens; texto para ≥ 80 anos.
- [ ] Ler o texto completo de Pedroso et al. (2025) e de Neuen et al. (2026).

**Ética e regulação**
- [ ] Aviso de privacidade completo (controlador, contato, finalidade, direitos) — precisa de dados do orientando e da instituição.
- [ ] Mostrar na tela a empresa e o país do provedor antes do consentimento (endpoint pronto).
- [ ] Conferir na fonte: termos da Groq; Lei 14.874/2024; Decreto 12.651/2025; RDC 657/2022 e 751/2022; termos de uso do NHANES.
- [ ] Subseção "Enquadramento regulatório" (ANVISA) e subseção "Equidade" no texto do TCC.

**Engenharia**
- [ ] README: versões verificadas (Python, Node ≥ 20.19, JDK 17), `.env.example`, script único.
- [ ] Núcleo como pacote instalável (hoje o gateway o importa por caminho).
- [ ] Enxugar `ai-services/chronic-risk-service/requirements.txt` e `trigger/requirements.txt`.
- [ ] Testes de `renal.py` contra valores de referência; teste *golden* do prompt; testes do front-end.
- [ ] Remover do repositório artefatos de execução do JADE (`APDescription.txt`, `MTPs-Main-Container.txt`).
- [ ] BibTeX: DOIs apontados pelo parecer de Literatura (Isern, Tang, Chan), "et al." indevido em Petrova, DOI de *preprint* em entradas NeurIPS; ensinar o `indexar.py validar` a detectar esses casos.

**Interface**
- [ ] Data e versão do cálculo na impressão.
- [ ] Testes manuais de interface (orientando, ao final): fluxo no computador e no celular; explicação por IA com LLM configurado, estado nunca observado; impressão.
- [ ] As duas últimas mudanças no front-end (nomes dos fatores e frase de frequência) não foram retestadas.

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
- [ ] ~~Fichar a revisão de LLM-como-juiz em saúde (arXiv 2605.25273)~~ — saiu como fundamento (06/10/2026); o limiar de κ passa a se apoiar em Landis & Koch (1977) ou McHugh (2012), a ler.
- [ ] Ler asgari2025hallucination na íntegra (subtipos de alucinação usados na métrica 4).
- [ ] C5: cálculo de tamanho de amostra após piloto (poder para McNemar) — método definido em D029.
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

## JADE (D021 → D032)
> Lista substituída pela de D032, no topo deste arquivo. O protocolo correto é FIPA-Request externo + uma instância de FIPA-Propose por rodada; as "configurações pelos agentes ativos" foram retiradas.
- [ ] Reescrever Explicador ↔ Julgador com `ProposeInitiator`/`ProposeResponder` (FIPA-Propose) e limite de rodadas.
- [ ] Reescrever Gerenciador → Classificador com `AchieveREInitiator`/`AchieveREResponder`, com REFUSE para entrada inválida.
- [ ] `conversation-id` por caso e log JSON Lines de todas as mensagens ACL.
- [ ] Configurações experimentais pelos agentes ativos (C-isolado, C-ferramenta, C-verificador).
- [ ] Ler na íntegra: Botti 2025, especificação FIPA SC00036, capítulo de protocolos do JADE Programmer's Guide.

## Brechas a tratar no desenho (B1–B7)
- [x] B1: definida em D029 e D034 (desfecho por anotação humana cega; extrator da avaliação diferente do extrator do verificador). Falta implementar.
- [ ] B2: definir o baseline isolado forte (equação no prompt ou interpretador de código).
- [x] B3: resolvida por D027 (raça/cor no cadastro; H3 exploratória).
- [ ] B4: análise de sensibilidade da referência da atribuição (centralização × média NHANES).
- [ ] B5: escolher a medida de inteligibilidade em português.

## Buscas a repetir
- [ ] Repetir busca de trabalhos similares antes da qualificação e antes da defesa (última: 29/09/2026, **não estruturada; não encontrou He & Martens 2026**). Acrescentar os termos "XAI narrative", "narrator critic", "sign agreement", "faithful evaluator". Termos anteriores: "verifier" + "faithfulness" + "SHAP" + "LLM explanation" + "clinical risk"; "agentic explanation clinical prediction"; "PREVENT LLM".

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
