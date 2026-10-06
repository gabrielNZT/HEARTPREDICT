---
titulo: Registro de decisões
status: vigente
atualizado: 2026-09-29
resumo: Decisões de projeto e de pesquisa, com data, motivo e fontes. Nunca apague; marque como substituída.
---

# Registro de decisões

Formato: **D### — título** · data · status (vigente / substituída por D###) · motivo · fontes.

## D001 — Adotar a Opção A (verificação de explicações) como rumo do TCC
- **Data:** 2026-09-28 · **Status:** vigente
- **Decisão:** o TCC deixa de ser "sistema multiagente de classificação de risco" e passa a investigar se um verificador reduz explicações infiéis em uma arquitetura híbrida ML + LLM.
- **Motivo:** o orientador apontou falta de fundamentação e de posicionamento. A Opção A tem pergunta de pesquisa clara, pode ser refutada e reaproveita o código existente.
- **Alternativas descartadas:** (B) estudo de reprodução/leakage no `cardio_train`, que abandona multiagentes; (C) avaliação de arquitetura JADE/MQTT, com contribuição acadêmica fraca.
- **Fontes:** [sintese-leitura](../01-literatura/sintese-leitura.md).

## D002 — O LLM não calcula risco
- **Data:** 2026-09-28 · **Status:** vigente
- **Decisão:** todo número de risco vem de ferramenta determinística (PREVENT) ou de modelo treinado (XGBoost). O LLM só extrai, explica ou verifica.
- **Fontes:** khandekar2024medcalc, jin2025agentmd, roeschl2026pipeline.

## D003 — Contribuição reformulada de forma mais estreita
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão:** a novidade **não** é "usar LLM para explicar SHAP" (já existe: ColaCare, Lee 2025, NEURON, Zhu 2026). A novidade é **o verificador da explicação + métricas de polaridade e exatidão numérica + ablação do verificador**, no domínio cardiovascular/PREVENT/SBC em PT-BR.
- **Motivo:** a leitura completa e a busca de 29/09/2026 mostraram o campo ativo.
- **Fontes:** [sintese-leitura §3](../01-literatura/sintese-leitura.md).

## D004 — O agente explicador recebe o SHAP e o número calculado
- **Data:** 2026-09-29 · **Status:** vigente
- **Motivo:** em Zhu 2026 os geradores não recebiam o SHAP e a fidelidade foi baixíssima (Jaccard 0,08–0,17).
- **Fontes:** zhu2026agenticexpl [C4].

## D005 — Verificador híbrido e multinível
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão:** nível 1 determinístico (números, polaridade, categoria); nível 2 com LLM (coerência semântica, recomendações sem base). Em caso de reprovação, a explicação volta ao Explicador com o erro apontado; após N ciclos, é bloqueada.
- **Fontes:** cemri2025mast [C4][C7], lu2026prove, lee2025shapllm [C5].

## D006 — Manter o JADE, justificado por comunicação padronizada
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão:** manter o JADE/FIPA-ACL, com conteúdo das mensagens em JSON validado por esquema.
- **Motivo:** o MAST recomenda protocolos padronizados para reduzir desalinhamento entre agentes. O JADE vira decisão de projeto justificada, não só preferência tecnológica.
- **Fontes:** cemri2025mast [C7].

## D007 — Agentes definidos por função verificável, não por persona médica
- **Data:** 2026-09-29 · **Status:** vigente
- **Motivo:** personas de especialidade rendem pouco conhecimento real (MedAgentBoard, Apêndice H.4).
- **Fontes:** zhu2025medagentboard [C5].

## D008 — Fora do escopo: ECG em tempo real, TimescaleDB, MQTT de sensores
- **Data:** 2026-09-28 · **Status:** vigente
- **Motivo:** não respondem à pergunta de pesquisa. Viram trabalhos futuros.

## D009 — Ferramenta de cálculo: PREVENT-ASCVD em 10 anos (modelo base)
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão:** implementar a equação PREVENT-**ASCVD** de 10 anos, modelo **base** (sem UACR/HbA1c/SDI), na forma logística da Tabela S12, com validação das faixas de entrada da derivação.
- **Motivo:** é o desfecho que a SBC 2025 usa para as categorias; o modelo base usa só variáveis de rotina.
- **Verificação:** reproduzir o caso publicado (mulher, 50 anos → DCVA 3,6%; 6,0% se fumante) e conferir contra o pacote `preventr` e a calculadora da AHA.
- **Fontes:** [khan2024prevent](../01-literatura/fichamentos/khan2024prevent.md) [C4][C5][C6]; [sbc2025dislipidemias](../01-literatura/fichamentos/sbc2025dislipidemias.md) [C1].

## D010 — Gabarito de categoria: motor de regras SBC operacionalizado e versionado
- **Data:** 2026-09-29 · **Status:** vigente (revisada no mesmo dia após conferir a versão em inglês da diretriz)
- **Decisão:** a categoria de referência vem de um motor de regras determinístico baseado na Tabela 4.1. As ambiguidades foram resolvidas **pela própria diretriz**, sem depender de opinião:
  - **LDL-c 160 mg/dL:** entra como intermediário. O texto da seção 4.1 diz "entre 160 e 189" (PT) / "between 160 and 189" (EN); a tabela ("> 160-189") é a formulação ambígua.
  - **Meta do risco extremo:** < 40 mg/dL. Aparece assim na Tabela 5.1, no quadro de recomendações GRADE e no texto que abre a seção 5.2.5; o "> 40" é erro de digitação presente nas duas línguas.
  - **"Tabela 4.3" na seção 4.7:** erro de remissão presente nas duas línguas; as categorias estão na Tabela 4.1.
  - **IMC no PREVENT:** segue-se o artigo original (IMC não entra no modelo de DCVA), não a descrição resumida da diretriz.
  - **Agravantes:** única ambiguidade genuína (regra na Tabela 4.1 × julgamento na seção 4.3). Operacionalização: regra da Tabela 4.1 (≥ 1 agravante sobe uma categoria), com **análise de sensibilidade** rodando o experimento também sem essa promoção.
- **Por que não precisa de validação clínica externa:** o experimento mede se a explicação do LLM é **fiel à saída da ferramenta**, e as três configurações usam o mesmo motor. O gabarito precisa ser **consistente e documentado**, não "clinicamente perfeito"; a escolha de interpretação não favorece nenhuma configuração. Isso deve constar como limitação.
- **Errata:** nenhuma errata publicada encontrada em 29/09/2026. Reverificar antes da defesa.
- **Fontes:** [sbc2025dislipidemias](../01-literatura/fichamentos/sbc2025dislipidemias.md) (seção 4.1, Tabela 4.1, Tabela 5.1, seção 5.2.5; versões PT e EN).

## D011 — Escopo inicial das vinhetas
- **Data:** 2026-09-29 · **Status:** vigente (confirmada pela diretriz)
- **Decisão:** adultos de 30–79 anos, sem evento cardiovascular prévio, sem aterosclerose subclínica, sem diabetes e com LDL-c < 160 mg/dL. Casos com diabetes, LDL ≥ 160 e agravantes específicos entram como **casos de teste dirigidos** do verificador.
- **Motivo:** é **exatamente** o domínio em que a diretriz manda usar o escore: "Para os adultos sem evento cardiovascular pregresso ou aterosclerose subclínica, sem DM e com LDL-c < 160 mg/dL, a categorização do risco cardiovascular aterosclerótico pode ser definida pelo uso de equações ou escores de risco" (seção 4.1). A faixa 30–79 anos é a do PREVENT.
- **Fontes:** [sbc2025dislipidemias](../01-literatura/fichamentos/sbc2025dislipidemias.md) (seção 4.1); [khan2024prevent](../01-literatura/fichamentos/khan2024prevent.md) [C1].

## D012 — Atribuição de referência exata para o PREVENT
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão:** calcular a contribuição de cada variável original por **valores de Shapley exatos** sobre o log-odds do PREVENT (≈ 10 variáveis, 2¹⁰ coalizões), usando como referência os valores de centralização do modelo (idade 55, não-HDL 3,5 mmol/L, HDL 1,3 mmol/L, PAS 130, sem DM, não fumante, sem medicação, TFGe 90).
- **Motivo:** dá um gabarito de atribuição **sem aproximação** para medir a fidelidade (polaridade e ranking).

## D013 — Fonte dos perfis de pacientes: NHANES + casos sintéticos dirigidos (resolve P001)
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão:** (1) perfis **reais** do NHANES (público, sem necessidade de comitê de ética), filtrados pelo escopo de D011 e amostrados de forma estratificada por categoria de risco; (2) casos **sintéticos dirigidos** para situações que o NHANES não cobre bem: pares contrafactuais (só sexo ou raça/etnia alterados, H3), valores de fronteira (ex.: risco 4,9% × 5,1%), agravantes e armadilhas de fidelidade (ex.: IMC alto com risco baixo).
- **Motivo:**
  - O NHANES tem todas as variáveis do PREVENT e **já foi usado para aplicar o PREVENT** em estudos publicados no JAMA e no JAMA Internal Medicine em 2024 ([diao2024preventnhanes](../01-literatura/fichamentos/diao2024preventnhanes.md), [anderson2024preventnhanes](../01-literatura/fichamentos/anderson2024preventnhanes.md)).
  - Dá distribuição conjunta **realista** das variáveis, respondendo à crítica de Roeschl 2026 contra vinhetas puramente sintéticas.
  - Casos sintéticos a partir de parâmetros controlados têm precedente no RiskQA do AgentMD e nas notas por template do MedCalc-Bench.
- **Limitação a declarar:** o NHANES é da população dos EUA (coerente com a origem do PREVENT, mas não com a brasileira); não há base brasileira pública equivalente com creatinina e perfil lipídico de acesso livre **(verificar microdados laboratoriais da PNS 2014–2015)**.

## D014 — LLMs do experimento (resolve P002)
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão:** **pelo menos 2 LLMs**: (1) Gemini, já integrado ao projeto, numa versão **atual e fixada** (o código usa `gemini-1.5-flash`, que deve ser atualizado); (2) um modelo **de pesos abertos**, rodando localmente, de porte médio ou grande (evitar modelos muito pequenos). Temperatura fixa, versão registrada, N repetições por caso.
- **Motivo:**
  - Rankings variam com o LLM base (MedAgentBoard, Limitations; ColaCare, Tabela 5).
  - Usar um único LLM é limitação declarada em Lee 2025.
  - Roeschl 2026 testou 6 LLMs, incluindo abertos.
  - O modelo de 3B de Zhu 2026 é um dos motivos da evidência fraca; o MedCalc-Bench mostra que modelos maiores vão melhor.
  - O modelo aberto garante reprodutibilidade independente de API (limitação apontada no AgentMD).
- **O que depende só de você:** qual modelo aberto cabe no seu hardware ou orçamento.

## D015 — Avaliação humana (resolve P003 em parte)
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão:**
  - **Obrigatória (validação das métricas):** anotação manual de uma amostra das explicações por **dois anotadores** (você + um colega), com **concordância medida por Cohen κ** e percentual de concordância simples. Serve para validar as métricas automáticas e o verificador (falsos positivos e negativos). Precedentes: MAST (κ = 0,88 entre humanos; κ = 0,77 humano × LLM); revisão de LLM-como-juiz em saúde (κ entre 0,59 e 0,88).
  - **Opcional (complemento):** pequena avaliação por médicos (Likert de utilidade e segurança), como em Lee 2025 (n = 7) e ColaCare (n = 12). É claramente complementar e não sustenta nenhuma hipótese sozinha.
- **Ponto institucional (não é da literatura):** se houver avaliação por médicos, confirmar com o CEP da sua universidade se ela se enquadra como pesquisa de opinião com participantes não identificados (Res. CNS 510/2016, art. 1º, parágrafo único), dispensada de registro, ou se exige submissão.
- **Fontes:** [cemri2025mast](../01-literatura/fichamentos/cemri2025mast.md) [C2]; [lee2025shapllm](../01-literatura/fichamentos/lee2025shapllm.md); [wang2025colacare](../01-literatura/fichamentos/wang2025colacare.md).

## D016 — XGBoost / `cardio_train` fora do núcleo (resolve P004)
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão:** o núcleo do experimento usa **só o PREVENT**. O XGBoost fica como **extensão opcional** para mostrar que o verificador funciona também com atribuição aproximada (SHAP de modelo de árvore), o que daria comparabilidade direta com Lee 2025 e Zhu 2026. Se feito, **não usar o `cardio_train`** como base principal.
- **Motivo:** o `cardio_train` é transversal (não mede risco futuro), não tem as variáveis do PREVENT e tem risco de leakage na literatura (kapoor2023leakage); o PREVENT dá gabarito exato (D012).
- **O que depende de você e do orientador:** se o cronograma comporta a extensão.

## D017 — H3 reformulada com mecanismo explícito
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão:** H3 passa a ser: *"Como o PREVENT não usa raça/etnia, a configuração com verificador terá menos explicações que atribuem o risco a raça/etnia (afirmações não sustentadas) do que as configurações sem verificador."* A variação por sexo é analisada de forma **exploratória**, comparando taxas de fidelidade entre grupos, sem direção prevista.
- **Motivo:** a versão anterior não tinha mecanismo — o verificador checa fidelidade, não viés. Ver [auditoria C9](../02-argumentacao/auditoria-decisoes-autorais.md).

## D018 — Português não é apresentado como contribuição
- **Data:** 2026-09-29 · **Status:** vigente (substitui parte de D003)
- **Decisão:** o idioma deixa de ser diferencial. O diferencial passa a ser **diretriz brasileira (PREVENT/SBC 2025) + verificação da fidelidade da explicação**.
- **Motivo:** Santos et al. 2026 já avaliaram LLMs em estratificação cardiovascular com vinhetas em português e encontraram desempenho semelhante ao inglês ([santos2026escllm](../01-literatura/fichamentos/santos2026escllm.md)). Ver [auditoria E1](../02-argumentacao/auditoria-decisoes-autorais.md).

## D019 — Arquitetura enxuta: 4 agentes, remoção de componentes sem função
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão:** manter Entrada, Classificador, Explicador e Verificador (antigo Julgador). **Remover** AgenteNotificador (não é chamado nem iniciado), MQTT/Mosquitto e realtime-anomaly-service (sem código), e as menções no README a PostgreSQL/TimescaleDB, Prometheus, CI e SHAP/LIME (não implementados). Apagar a lógica atual do Julgador (faixas arbitrárias e "ações" clínicas sem base).
- **Enquadramento:** "arquitetura orientada a agentes em JADE", não "sistema multiagente autônomo" (Wooldridge & Jennings 1995; Jennings 2000).
- **Fontes:** [escopo-e-arquitetura](escopo-e-arquitetura.md).

## D020 — Escopo em núcleo × extensões
- **Data:** 2026-09-29 · **Status:** vigente (confirmar prazos com o orientador — O001)
- **Decisão:** núcleo = ferramenta + 4 agentes + verificador determinístico + NHANES + 3 configurações × 2 LLMs + desfecho "totalmente fiel" + anotação dupla + H1/H2. Tudo o mais é extensão (ver [escopo-e-arquitetura §4](escopo-e-arquitetura.md)).
- **Motivo:** o desenho acumulado tinha porte de mestrado; um TCC de graduação é avaliado pela coerência e viabilidade.

## D021 — JADE justificado por protocolos FIPA, rastro auditável e ablação por composição (resolve O004)
- **Data:** 2026-09-29 · **Status:** vigente (substitui a justificativa "pragmática" de D006 e D019)
- **Decisão:** manter o JADE e **usá-lo de fato**: (1) Explicador ↔ Verificador via **FIPA-Propose** (PROPOSE / ACCEPT-PROPOSAL / REJECT-PROPOSAL, término após N rodadas); (2) Entrada → Classificador via **FIPA-Request**, com REFUSE para dado inválido ou ausente; (3) `conversation-id` por caso; (4) registro de todas as mensagens ACL como dado da pesquisa; (5) configurações experimentais definidas pelos agentes ativos.
- **Motivo:** o protocolo com estados e término explícitos ataca modos de falha documentados pelo MAST (término, repetição, perda de histórico, verificação) e transforma a decisão do verificador em ato de fala tipado. Posicionamento: Botti 2025 (incorporar padrões de SMA aos agentes com LLM).
- **O que não se afirma:** o JADE não melhora a fidelidade por si; quem melhora é o Verificador.
- **Fontes:** [justificativa-jade](../02-argumentacao/justificativa-jade.md).

## D022 — Nível de justificativa das escolhas tecnológicas
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão:** três níveis. (1) Método (LLMs, PREVENT, regras SBC, Shapley, NHANES, estatística): justificativa com fonte, versões e parâmetros na Metodologia. (2) Arquitetura (JADE, Java + Python via HTTP/JSON, mensagens com esquema): um parágrafo cada no Desenvolvimento. (3) Infraestrutura/interface (FastAPI, React, Vite etc.): só tabela com versão e papel.
- **Fontes:** [tecnologias](../03-metodologia/tecnologias.md).

## D023 — Piloto de viabilidade antes da implementação completa
- **Data:** 2026-09-29 · **Status:** vigente (limiar a acertar com o orientador)
- **Decisão:** antes de reescrever o JADE, processar o NHANES e montar o experimento, rodar um piloto (20–30 vinhetas, configuração sem verificador, 2 LLMs) para verificar se os LLMs atuais ainda produzem explicações infiéis nesta tarefa.
- **Motivo:** risco de efeito teto — não há evidência de que o problema observado em Lee 2025 (GPT-4 de 2024) e Zhu 2026 (modelo de 3B) persista nos modelos de 2026. Se não persistir, H2 fica sem objeto.
- **Fontes:** [proximos-passos §C](proximos-passos.md).

## D024 — Modelos de baixo custo ou gratuitos (atualiza D014)
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão:** modelo **aberto** via **Groq** (plano gratuito, sem cartão; GPT-OSS 120B ou Llama 3.3 70B) + modelo **fechado** via **Gemini** (plano gratuito, linha Flash/Flash-Lite). **xAI Grok** fica como opção secundária: não é gratuito (US$ 25 de crédito inicial; o programa de US$ 150/mês exige gasto mínimo de US$ 5 e compartilhamento de dados) e é fechado.
- **Motivo:** custo zero; o GPT-OSS e o Llama têm pesos abertos, o que atende à exigência de um modelo aberto (reprodutibilidade) sem depender da GPU local (RTX 3050 de 6 GB, insuficiente para modelos de porte médio).
- **Limites (fontes secundárias; conferir no console):** Groq ≈ 30 req/min, 1.000 req/dia e 100 mil tokens/dia no Llama 3.3 70B e ≈ 200 mil tokens/dia nos GPT-OSS; Gemini varia por modelo e muda sem aviso (verificar no AI Studio).
- **Registrar sempre:** ID exato do modelo e data das execuções.

## D025 — Nova interface e integração transitória
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão (do usuário):** nova interface no escopo PREVENT/SBC ligada a `POST /api/avaliacao` no gateway, que reutiliza o núcleo testado do piloto; a explicação chama o LLM diretamente (configuração C-ferramenta), **sem passar pelos agentes JADE por enquanto**. A reintegração com o JADE (FIPA-Propose com o Verificador) segue D021.
- **Justificativas de design:** [interface-design](../03-metodologia/interface-design.md). **Evidências:** [04-evidencias/interface](../04-evidencias/interface/) (capturas e auditoria axe-core: 0 violações em 14 auditorias).
- **Risco declarado:** enquanto durar a transição, a demonstração não exercita a arquitetura de agentes nem o verificador; a interface informa ao usuário que o texto não é verificado.

## O que ainda precisa do orientador (institucional/cronograma, não científico)
- **O001 — Cronograma:** a extensão com XGBoost (D016) e a avaliação com médicos (D015) cabem no semestre?
- **O002 — Normas do curso:** formato do TCC, qualificação, exigências de CEP da instituição.
- ~~O004 — JADE × workflow em Python~~ → resolvida por D021 (manter JADE com protocolos FIPA). Apresentar a justificativa ao orientador.
- **O003 — Acesso a médicos:** se a avaliação opcional de D015 for feita, o orientador tem contatos?
