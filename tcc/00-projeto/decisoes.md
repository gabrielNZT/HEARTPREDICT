---
titulo: Registro de decisões
status: vigente
atualizado: 2026-10-06
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
- **Data:** 2026-09-29 · **Status:** vigente, **revista por D030** (a lacuna como estava escrita não se sustenta frente a He & Martens 2026)
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
- **Data:** 2026-09-29 · **Status:** vigente, **regras revistas por D026** (ordem das regras, Lp(a) > 180, arredondamento)
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
- **Data:** 2026-09-29 · **Status:** vigente, **complementada por D026** (exclusão de aterosclerose subclínica e LDL obrigatório com não-HDL ≥ 190)
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
- **Data:** 2026-09-29 · **Status:** **enquadramento ético substituído por D031** (a resolução citada aqui estava errada)
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
- **Data:** 2026-09-29 · **Status:** vigente, **operacionalizada por D027** (raça/cor entra no prompt; H3 passa a exploratória)
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
- **Data:** 2026-09-29 · **Status:** **redação substituída por D032** (duas afirmações desta decisão estavam erradas; a escolha pelo JADE foi mantida)
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
- **Data:** 2026-09-29 · **Status:** vigente, **atualizada por D033 e restrita por D028**
- **Decisão:** modelo **aberto** via **Groq** (plano gratuito, sem cartão; GPT-OSS 120B ou Llama 3.3 70B) + modelo **fechado** via **Gemini** (plano gratuito, linha Flash/Flash-Lite). **xAI Grok** fica como opção secundária: não é gratuito (US$ 25 de crédito inicial; o programa de US$ 150/mês exige gasto mínimo de US$ 5 e compartilhamento de dados) e é fechado.
- **Motivo:** custo zero; o GPT-OSS e o Llama têm pesos abertos, o que atende à exigência de um modelo aberto (reprodutibilidade) sem depender da GPU local (RTX 3050 de 6 GB, insuficiente para modelos de porte médio).
- **Limites (fontes secundárias; conferir no console):** Groq ≈ 30 req/min, 1.000 req/dia e 100 mil tokens/dia no Llama 3.3 70B e ≈ 200 mil tokens/dia nos GPT-OSS; Gemini varia por modelo e muda sem aviso (verificar no AI Studio).
- **Registrar sempre:** ID exato do modelo e data das execuções.

## D025 — Nova interface e integração transitória
- **Data:** 2026-09-29 · **Status:** vigente
- **Decisão (do usuário):** nova interface no escopo PREVENT/SBC ligada a `POST /api/avaliacao` no gateway, que reutiliza o núcleo testado do piloto; a explicação chama o LLM diretamente (configuração C-ferramenta), **sem passar pelos agentes JADE por enquanto**. A reintegração com o JADE (FIPA-Propose com o Verificador) segue D021.
- **Justificativas de design:** [interface-design](../03-metodologia/interface-design.md). **Evidências:** [04-evidencias/interface](../04-evidencias/interface/) (capturas e auditoria axe-core: 0 violações em 14 auditorias).
- **Risco declarado:** enquanto durar a transição, a demonstração não exercita a arquitetura de agentes nem o verificador; a interface informa ao usuário que o texto não é verificado.

## D026 — Regras da SBC e escopo revistos após a banca (atualiza D010 e D011)
- **Data:** 2026-09-29 · **Status:** vigente
- **Origem:** pareceres de Cardiologia (M2, M3, M4, M7, m2), Engenharia (C2) e IHC (P6). Cada regra foi conferida no texto da diretriz antes de entrar no código ([verificação](../05-banca/verificacao-alegacoes.md)).
- **Decisão (implementada em `experimentos/piloto/sbc.py` e `backend-gateway/app/avaliacao.py`, com testes):**
  1. **Arredondamento único.** A categoria é calculada sobre o risco arredondado a 0,1 ponto percentual, o mesmo valor exibido. Antes, 4,951% aparecia como "5,0% → baixo".
  2. **Ordem das regras.** Escore → piso do LDL-c 160–189 (intermediário) → agravante sobe uma categoria → LDL-c ≥ 190 e Lp(a) > 180 mg/dL classificam como alto. Consequência: escore baixo + LDL-c 160–189 + agravante passa a **alto** (antes, intermediário). Base: seção 4.1 ("considerados de risco intermediário") e Tabela 4.1 ("risco intermediário, com presença de fator agravante" → alto).
  3. **Lp(a) > 180 mg/dL (> 390 nmol/L) → alto** (Tabela 4.1; seção 4.4.1).
  4. **Aterosclerose subclínica fora do escopo.** A interface pergunta por placa em exame de imagem e recusa o cálculo (a diretriz classifica esses casos direto como alto ou muito alto).
  5. **LDL-c obrigatório quando o não-HDL é ≥ 190 mg/dL**, porque o escore só vale com LDL-c < 160.
  6. **TFGe acima de 140** (calculada ou informada) é tratada como 140, limite da faixa de derivação do PREVENT, em vez de recusar pessoas com função renal normal.
- **O que é interpretação minha:** os itens 2 (ordem) e 5 (limiar de 190 para exigir o LDL) e 6 (truncamento) não estão escritos literalmente na diretriz nem no artigo do PREVENT. São operacionalizações declaradas e entram na análise de sensibilidade prevista em D010.
- **Não implementado:** hipercolesterolemia familiar como exclusão; risco em 30 anos para jovens; LDL-c basal de quem já usa estatina (hoje há só um aviso na tela).

## D027 — Prompt do piloto v2 e raça/cor nas vinhetas (operacionaliza D017)
- **Data:** 2026-09-29 · **Status:** vigente
- **Origem:** pareceres de IA (M1, m7), Metodologia (m2, M3), Cardiologia (C2) e Ética (M5).
- **Decisão (`experimentos/piloto/prompt.py`, versão `piloto-v2`):** números em formato brasileiro, sem ponto decimal; lista explícita das variáveis que entram no cálculo; IMC e raça/cor apresentados como "outros dados do cadastro (não entram no cálculo)"; contribuições com magnitude e direção por extenso; regra de segurança sobre medicamentos; TFGe da referência declarada.
- **Raça/cor:** as 24 vinhetas recebem raça/cor autodeclarada nas cinco categorias do IBGE, em rodízio, para que nenhuma categoria fique associada a um perfil de risco.
- **H3 passa a exploratória e descritiva,** sem teste confirmatório: o evento esperado é raro e o poder seria insuficiente (parecer de Metodologia, M3).
- **Consequência para o desenho:** dizer ao LLM que o IMC e a raça/cor não entram no cálculo torna a tarefa mais fácil do que na v1. É deliberado: um erro que só aparece por ambiguidade do prompt não mede o LLM. A v1 fica registrada como condição "armadilha" para comparação, se houver orçamento.
- **Limite:** o prompt é único. Os resultados podem depender da redação (ameaça à validade externa, a declarar).

## D028 — Dados de pessoas reais: explicação opcional, consentimento e provedores
- **Data:** 2026-09-29 · **Status:** vigente (a base legal e o aviso completo dependem de dados do orientando e da instituição)
- **Origem:** parecer de Ética (C1, C2, M2), IHC (P12) e Engenharia (M8–M11). Termos do Gemini conferidos na fonte.
- **Decisão (implementada, com testes):**
  1. A explicação por IA **só é pedida depois de consentimento explícito** na tela de resultado; o cálculo não depende dela.
  2. **O plano gratuito do Gemini não recebe dados de pessoas reais** (os termos proíbem dados sensíveis, permitem treino e revisão humana e vedam aconselhamento médico). O gateway recusa `LLM_PROVEDOR=gemini`, salvo declaração explícita de plano sem uso dos dados (`LLM_PLANO_SEM_USO_DOS_DADOS=1`).
  3. O Gemini gratuito **continua permitido no experimento**, que só usa vinhetas sintéticas.
  4. O fluxo legado (`/predict`, `/explanation`, `/pending`) fica **desligado por padrão**; CORS restrito às origens da interface; logs sem dados de paciente; chave do Gemini no cabeçalho.
  5. Temperatura da interface configurável, padrão 0,2.
- **Base legal pretendida:** consentimento específico e destacado (LGPD, art. 11, I; art. 33, VIII para a transferência internacional).
- **Ainda falta:** aviso de privacidade completo (controlador, contato, finalidade, direitos); mostrar empresa e país do provedor antes do consentimento (o endpoint `/api/avaliacao/explicacao/provedor` existe, a tela ainda não o usa); conferir os termos da Groq na fonte (o parecer diz "not for consumer use"); seção de enquadramento ANVISA no texto do TCC.
- **Regra para a defesa:** demonstração com perfis fictícios, sem dados de pessoas da plateia.

## D029 — Plano de análise de H2 (pré-especificado)
- **Data:** 2026-10-06 · **Status:** proposta registrada antes de qualquer resultado comparativo; **validar com o orientador**
- **Origem:** parecer de Metodologia (CR1, CR2, CR3, M4, M6) e de IA (M2, M3). Cálculos da banca em `05-banca/anexos/metodologia/`.
- **Contraste primário:** C-ferramenta × C-verificador, no mesmo LLM, pareado por vinheta.
- **Desfecho primário:** explicação **entregue e totalmente fiel** (nenhuma afirmação incorreta ou não sustentada), decidido por **anotação humana cega** à configuração.
- **Explicações bloqueadas:** contam como **falha** na análise primária (intenção de tratar). Reporta-se também o desfecho em três níveis (fiel / infiel / bloqueada) e uma análise de sensibilidade que as exclui.
- **Unidade de análise:** a vinheta. Para o teste primário usa-se a **primeira repetição** de cada vinheta; as demais entram em análise de sensibilidade e na estimativa de variabilidade.
- **Teste:** McNemar mid-p (Fagerland et al. 2013), com a diferença pareada e IC95%. **Holm** entre os 2 LLMs. H2 é considerada sustentada se os dois LLMs mostrarem efeito na mesma direção e ao menos um for significativo após a correção; resultado divergente é reportado como heterogeneidade.
- **Efeito mínimo de interesse:** redução absoluta de 10 pontos percentuais na taxa de explicações não fiéis.
- **Guarda contra "vencer dizendo menos":** métrica de **cobertura** (proporção das 3 variáveis de maior |φ| acima de ε mencionadas com a direção correta) e número de afirmações por texto, reportados por configuração. H2 não é declarada sustentada se a cobertura cair mais de 10 pontos percentuais.
- **Verificador contra o padrão humano:** sensibilidade e especificidade do verificador, por tipo de erro.
- **Tamanho da amostra:** fórmula de Connor (1987), com a taxa de erro de C-ferramenta (pA) medida no piloto e α = 0,025. Referência da banca: 92–202 vinhetas se pA = 20%; 360–1.381 se pA = 10%.
- **Regra do piloto (substitui o limiar pontual de D023; implementada em `resumir.py`):** IC95% por conglomerado (reamostragem de vinhetas); segue se o limite inferior for ≥ 10%; ajusta a tarefa se o limite superior for < 10%; caso contrário, amplia o piloto. Taxas reportadas por vinheta.
- **Limitações que este plano não resolve (a declarar):** não há controle de "mais tentativas sem correção específica", então o ganho não pode ser atribuído só ao feedback; prompt único; vinhetas escolhidas para provocar erro (a taxa do piloto não estima a de uso real).
- **Em aberto:** C-isolado com ou sem a equação no prompt (H1 fica como verificação de sanidade, com amostra pequena); temperatura do experimento.

## D030 — Contribuição reposicionada: replicação com extensão (revisa D003)
- **Data:** 2026-10-06 · **Status:** vigente
- **Origem:** parecer de IA (C1) e de Literatura (K1). Leitura própria de [he2026agenticnarratives](../01-literatura/fichamentos/he2026agenticnarratives.md) e [ichmoukhamedov2024story](../01-literatura/fichamentos/ichmoukhamedov2024story.md).
- **O que deixa de ser afirmado:** que nenhum trabalho combina verificador da explicação, métricas de sinal e valor e ablação. He & Martens (2026) têm os três, em 5 LLMs e 5 bases (duas de saúde).
- **O que o TCC acrescenta (cada item é uma limitação declarada ou observada naquele trabalho):**
  1. **Referência exata.** A atribuição é calculada sem aproximação sobre um escore clínico publicado; lá, a referência é o SHAP de um Random Forest, tomado como fiel por hipótese.
  2. **Regras de diretriz clínica:** categoria, reclassificação por agravante e meta, com distinção entre o alvo "risco calculado" e o alvo "categoria".
  3. **Variáveis fora do modelo** tratadas como erro (IMC, raça/cor), com gabarito demonstrável.
  4. **Desfecho independente do verificador.** Lá, a fidelidade final é medida pelo mesmo avaliador que atua no ciclo, e os falsos positivos ficam fora do estudo; aqui, o desfecho primário é anotação humana cega (D029).
  5. **Atribuições contraintuitivas, mas verdadeiras** (remédio como marcador de doença; idade abaixo da referência), cenário em que Ichmoukhamedov et al. mostram que os LLMs tendem a "corrigir" o sinal.
- **Pergunta de pesquisa reescrita:** *o ganho de fidelidade relatado para ciclos de crítica em bases genéricas se mantém quando a referência é exata, há regras de uma diretriz clínica e o desfecho é avaliado de forma independente do verificador?*
- **Pendente:** busca de literatura com protocolo documentado (parecer de Literatura, §6.3). Até lá, a lacuna é escrita como "nos trabalhos lidos", nunca como "ninguém fez".

## D031 — Enquadramento ético revisto (substitui o trecho de CEP de D015)
- **Data:** 2026-10-06 · **Status:** vigente para o experimento; **em aberto, sem bloquear, para as atividades com participantes** (decisão do orientando: conversar com o orientador)
- **Correção:** D015 citava a Res. CNS 510/2016, que trata de Ciências Humanas e Sociais. A norma de tramitação aplicável é a **Res. CNS 674/2022**, cujo art. 26, VIII, "a" exclui os TCCs da dispensa por atividade de ensino (conferido no texto). Marco legal: Lei 14.874/2024 e Decreto 12.651/2025 (citados pelo parecer; **ainda não conferidos por mim**).
- **Por atividade:**
  - vinhetas sintéticas → LLM → métricas: não envolve participantes; **sem CEP**;
  - anotação pelo autor e por um colega: o colega atua como membro da equipe e nenhum dado sobre ele é analisado; **sem CEP**, documentar;
  - NHANES (se for usado): dados públicos desidentificados; conferir os termos de uso do NCHS;
  - **avaliação por médicos e teste de usabilidade:** exigem protocolo no CEP ou dispensa por escrito. **Ficam fora do caminho crítico** até a conversa com o orientador; se não houver tempo, saem do TCC e viram trabalho futuro.
- **Demonstração:** não é pesquisa; rege-se pela LGPD (D028).

## D032 — JADE: implementar em versão mínima (substitui a redação de D021)
- **Data:** 2026-10-06 · **Status:** vigente · **Decisão do orientando**
- **Origem:** parecer de SMA (revisão maior) e de Metodologia (M8).
- **Erros de D021 que esta decisão corrige:**
  1. O **FIPA-Propose tem uma única rodada** (SC00036H). O ciclo de correção é uma **composição**: um FIPA-Request externo abre e encerra o caso (é ele que admite FAILURE) e cada rodada é uma instância de FIPA-Propose sob o mesmo `conversation-id`. O limite de N rodadas é política do agente, não do padrão.
  2. O **MAST não diz que protocolos padronizados "atacam por construção"** falhas de término e repetição. Ele associa protocolos padronizados à categoria de desalinhamento entre agentes e afirma que soluções centradas em protocolo são frequentemente insuficientes. Aqui, término e repetição são evitados pelo controle determinístico do laço, que se obtém também sem JADE.
- **O que o JADE agrega (e o que não agrega):** atos de fala com semântica padronizada, `conversation-id` e prazos prontos, rastro auditável da conversa. **Não agrega fidelidade.** É defendido como propriedade de engenharia, demonstrada por testes, e não como fator do experimento. A afirmação de "ablação por composição" sai do texto.
- **Arquitetura:**
  - cálculo, prompt, cliente do LLM e verificador ficam em **Python**, como módulos únicos (D034);
  - o **experimento roda em Python**, com as três configurações no mesmo executor;
  - os agentes JADE usam os **mesmos módulos**, por um serviço HTTP fino, e implementam só a conversa;
  - um único ponto de saída: nada é entregue sem ACCEPT-PROPOSAL (elimina o canal HTTP lateral do Explicador).
- **Atributos de agente:** reatividade e habilidade social (após a ACL com protocolos). Autonomia e proatividade são fracas em todos; o Verificador "detém a decisão de entrega", não "tem autonomia".
- **Riscos declarados:** JADE 4.6.0 é de 2022 e não está no Maven Central; o repositório oficial apresenta cadeia TLS incompleta. O jar será versionado no repositório (a LGPL permite).

## D033 — LLMs do piloto (atualiza D024)
- **Data:** 2026-10-06 · **Status:** vigente
- **Fato:** em 06/10/2026 a Groq não lista mais o Llama 3.3 70B. Modelos de texto disponíveis na conta: `openai/gpt-oss-120b`, `openai/gpt-oss-20b` e `qwen/qwen3.8-27b`.
- **Decisão:** piloto com **`openai/gpt-oss-120b`** e **`qwen/qwen3.8-27b`**, de desenvolvedores diferentes e ambos de pesos abertos. O Gemini entra quando houver chave, só com dados sintéticos (D028).
- **Registro por execução:** ID do modelo, data, temperatura, versão e hash do prompt, `finish_reason`, uso de tokens e estado do repositório (`git describe --dirty`). Respostas vazias ou cortadas são refeitas e contadas à parte.
- **Limite:** os dois modelos vêm do mesmo provedor, que pode servir versões quantizadas.

## D034 — Verificador como módulo independente do LLM
- **Data:** 2026-10-06 · **Status:** vigente (implementação em andamento)
- **Decisão:** o verificador é um módulo Python sem dependência do LLM explicador. Entrada: texto e pacote de referência do caso. Saída: aceito ou lista estruturada de violações. O nível principal é determinístico.
- **Não adotado:** verificador como ferramenta que o próprio LLM decide chamar. A verificação deixaria de ser garantida e o experimento mediria outra coisa. Fica como extensão possível.
- **Exigência herdada da banca (B1):** o extrator usado na avaliação final é diferente do usado pelo verificador, e o desfecho primário é humano (D029).
- **Teste de regressão:** os 26 textos adversariais do parecer de IA (`05-banca/anexos/ia/testar_preanotacao.py`).

## D035 — Anotação do piloto: só humana, na 1ª repetição de cada vinheta
- **Data:** 2026-10-30 · **Status:** vigente · registrada **antes** de qualquer anotação
- **Decisão:** o orientando anota manualmente, sem pré-anotação nem veredito automático, a **1ª repetição** de cada vinheta nos dois modelos: 48 respostas (`experimentos/piloto/planilha_cega.py gerar … --repeticao 1`). As repetições 2 e 3 ficam guardadas e não entram na regra do piloto.
- **Motivo:** a 1ª repetição já é a unidade da análise primária (D029); reduz o esforço a um terço sem nova questão metodológica. Com uma repetição por vinheta, o IC por conglomerado de `resumir.py` equivale ao IC por resposta.
- **Não adotado:** anotar com o veredito da máquina à vista e só "confirmar" (viés de automação; ver jabbour2023jama) e usar o verificador como anotador (repete a falha que D030 aponta em He & Martens). Anotação automática validada contra uma amostra humana cega fica como opção para o experimento final, junto com a dupla anotação para o κ.
- **Apoio à anotação:** a planilha traz a coluna `fatores(gabarito)`, que só reorganiza a atribuição (aumentaram / diminuíram / desprezíveis, com ε = 5% de Σ|φ|); não julga a resposta. Guia: [guia-anotacao-piloto](../03-metodologia/guia-anotacao-piloto.md).
- **Limite:** um anotador, sem κ; serve para decidir o rumo (D023), não como resultado do TCC.

## D036 — Meta de não-HDL-c na explicação (prompt piloto-v3, verificador-v2)
- **Data:** 2026-10-30 · **Status:** vigente · tomada **antes** de qualquer anotação do piloto
- **Fato:** o prompt `piloto-v2` fornecia e pedia só a meta de LDL-c. Na SBC 2025, o não-HDL-c é **meta coprimária** junto ao LDL-c (`01-literatura/textos/sbc2025dislipidemias.txt`, l. 282), e as recomendações dão as duas metas para cada categoria (l. 371–375; Tabela 5.1). Além disso, o PREVENT usa o não-HDL, não o LDL, e na interface o LDL é opcional. A omissão não tinha decisão registrada; era simplificação do prompt.
- **Decisão (do orientando):** corrigir já, em vez de declarar como limitação do piloto. Prompt `piloto-v3`: fornece e pede as metas de LDL-c **e** de não-HDL-c, com a redução mínima do LDL-c. Verificador `verificador-v2`: confere cada meta pelo alvo citado (LDL ou não-HDL), acusa metas trocadas e exige as duas como conteúdo obrigatório.
- **Consequências:** as execuções do piloto com `piloto-v2` (gpt-oss de 06/10; Qwen de 26/10) ficam como histórico e **não entram** na decisão do piloto; o piloto é refeito com `piloto-v3` nos dois modelos. A planilha cega de 30/10 (v2, sem nenhuma anotação) foi apagada. A explicação da interface passa a usar o v3 pelo gateway; a tela de resultado já mostrava as duas metas.
- **Fora do escopo:** ApoB (meta complementar na SBC 2025, l. 283) não entra: não é coletada no cadastro.
- **Correção junto:** o verificador ignorava o número 100 como "número livre" mesmo na frase da meta (meta de LDL-c do intermediário e de não-HDL-c do alto); agora ele é conferido como meta.

## O que ainda precisa do orientador (institucional/cronograma, não científico)
- **O001 — Cronograma:** a extensão com XGBoost (D016) e a avaliação com médicos (D015) cabem no semestre?
- **O002 — Normas do curso:** formato do TCC, qualificação, exigências de CEP da instituição.
- ~~O004 — JADE × workflow em Python~~ → resolvida por D032 (implementar em versão mínima). Confirmar com o orientador se "multiagente" é requisito do trabalho.
- **O003 — Acesso a médicos:** se a avaliação opcional de D015 for feita, o orientador tem contatos?
- **O005 — Atividades com participantes (D031):** a avaliação por médicos e o teste de usabilidade ficam no TCC? Os dois exigem CEP ou dispensa por escrito. Em aberto, sem bloquear o restante.
- **O006 — Plano de análise (D029):** validar o desfecho primário, a regra das explicações bloqueadas e o efeito mínimo de interesse antes de rodar o experimento.
