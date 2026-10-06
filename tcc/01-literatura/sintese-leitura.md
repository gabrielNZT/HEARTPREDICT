---
titulo: Síntese da leitura completa e correções
status: vigente
atualizado: 2026-09-29
resumo: O que mudou no posicionamento depois de ler os artigos centrais na íntegra; correções de afirmações feitas antes.
---

# Síntese da leitura completa (29/09/2026)

Lidos na íntegra: [jin2025agentmd](fichamentos/jin2025agentmd.md), [khandekar2024medcalc](fichamentos/khandekar2024medcalc.md), [zhu2025medagentboard](fichamentos/zhu2025medagentboard.md), [wang2025colacare](fichamentos/wang2025colacare.md), [cemri2025mast](fichamentos/cemri2025mast.md), [lee2025shapllm](fichamentos/lee2025shapllm.md), [roeschl2026pipeline](fichamentos/roeschl2026pipeline.md), [zhu2026agenticexpl](fichamentos/zhu2026agenticexpl.md).
Leitura parcial: [jabbour2023jama](fichamentos/jabbour2023jama.md) (o texto completo não pôde ser baixado).

## 1. Correções de afirmações feitas antes da leitura completa

| Afirmação anterior | Correção após leitura | Fonte |
|---|---|---|
| "O melhor LLM acerta só 50,9% dos cálculos médicos" | Correto, mas é o GPT-4 **com one-shot CoT**. Em zero-shot CoT foram 37,9%; com interpretador de código, 48,5%. Os modelos testados são de 2023–2024. | khandekar2024medcalc [C1][C3] |
| "Narrativas de LLM sobre SHAP tiveram fidelidade de 0,783" | A "fidelidade" desse estudo mede **só** se as 3 variáveis principais aparecem no texto. O trio completo só foi acertado em **42,5%**. **Polaridade e números não foram medidos**; houve erros de polaridade. | lee2025shapllm [C1][C2][C3] |
| "Explicações não ajudaram clínicos a detectar modelo enviesado" | Correto, mas as explicações eram **mapas de calor em imagem (Grad-CAM)**, não textos. Usar como **analogia**, com ressalva. | jabbour2023jama [C3] |
| "AgentMD não tem verificador" | AgentMD tem **autoverificação por GPT-4 na curadoria das calculadoras**. O que ele não tem é verificação da **explicação entregue** na inferência. | jin2025agentmd [C5] |
| "ColaCare é multiagente com ML" | Mais preciso: ColaCare **entrega logits e SHAP aos agentes** (muito próximo do nosso desenho), mas **não mede a fidelidade** do relatório e **reinjeta o texto** na predição. Ganhos sobre o ensemble ficam dentro do desvio-padrão. | wang2025colacare [C1][C3][C4] |

## 2. O que a leitura completa **reforçou**

1. **O LLM não deve calcular.** Três fontes independentes:
   - MedCalc-Bench: LLMs isolados erram fórmula, extração e aritmética; nem o interpretador de código resolve.
   - AgentMD: ferramenta validada leva de 0,409 para 0,877.
   - **Roeschl 2026 (cardiologia, revisado por pares):** pipeline com cálculo determinístico α=0,78 vs LLM isolado 0,32 vs médicos 0,31. Em escores **de regressão** (como o PREVENT), LLMs isolados reproduziram o próprio cálculo em só 0–15,8% dos casos.
2. **ML convencional deve fazer a predição com dados estruturados.** MedAgentBoard e a ablação do ColaCare (sem modelos especialistas o AUPRC cai de 54 para 28).
3. **A literatura de ponta recomenda arquitetura híbrida.** MedAgentBoard pede explicitamente, como trabalho futuro, "hybrid architectures that synergize conventional models with LLM-based agents".
4. **A lacuna de fidelidade da explicação é real e está nomeada pelos próprios autores:**
   - Lee et al. propõem, como trabalho futuro, "perform all calculations outside the LLM" + "a monitoring layer that flags or blocks" recomendações.
   - Zhu et al. (2026) concluem que o pipeline agêntico "should be paired with attribution-based checks".
5. **O verificador precisa ser multinível e, onde possível, simbólico/determinístico.** MAST (Insight 3 e Apêndice G), PROVE (validadores programados para números).
6. **Mais agentes não é igual a melhor.** MedAgentBoard (ganhos inconsistentes; papéis de especialidade rendem pouco), MAST (41–86,7% de falha), Zhu 2026 (pipeline agêntico **reduziu** a fidelidade ao SHAP).

## 3. O que a leitura completa **mudou**

### 3.1 O campo está mais ativo do que parecia
Busca feita em 29/09/2026 encontrou trabalhos de 2025–2026 na mesma família (SHAP → narrativa LLM): Zhu 2026, NEURON 2026, Ahmed 2025, além do ColaCare. **A novidade não pode ser "usar LLM para explicar SHAP".** Ela precisa ser formulada com precisão (ver 3.2).

### 3.2 Reformulação da contribuição (mais estreita e defensável)
> **Avaliar empiricamente se um verificador de fidelidade — determinístico para números e polaridade, com LLM para coerência semântica — reduz explicações infiéis em relação a (a) um LLM isolado e (b) um LLM com a ferramenta de cálculo, no domínio de risco cardiovascular preventivo (PREVENT/SBC 2025), com métricas de fidelidade que vão além da presença das top-k variáveis (polaridade, números citados e afirmações não sustentadas).**

Os elementos que, **juntos**, não aparecem em nenhum trabalho lido:
1. Verificador explícito da **explicação** (não do cálculo) — ausente em AgentMD, ColaCare, Lee, Zhu 2026, Roeschl.
2. Métricas de fidelidade com **polaridade + exatidão numérica** — Lee mede só top-3; Zhu mede Jaccard e direção do rótulo, não polaridade por variável.
3. **Ablação do verificador** (config. 2 vs 3) — Zhu compara isolado vs pipeline, mas sem verificador; Lee não tem baseline.
4. Domínio **cardiovascular preventivo** com **PREVENT** e **diretriz brasileira**, em **português**.
5. **Avaliação de viés** por troca de atributo demográfico no mesmo pipeline.

### 3.3 Correção de desenho vinda do Zhu 2026
Os agentes que explicam **devem receber o SHAP** e o número calculado. Sem isso, o LLM "adivinha" o que dirigiu o modelo (causa provável do Jaccard baixíssimo em Zhu 2026).

### 3.4 Correção de desenho vinda do Roeschl 2026 e do AgentMD
- Extração/validação **componente a componente** com definições operacionais explícitas.
- **Dados ausentes:** recusar ou pedir o dado, nunca supor (principal fonte de erro no AgentMD e alerta explícito em Zhu 2026).

### 3.5 Argumento para manter o JADE ficou mais forte
MAST (Apêndice G) recomenda **protocolos de comunicação padronizados** entre agentes para reduzir desalinhamento. FIPA-ACL (JADE) é exatamente isso. Isso transforma o JADE de "escolha de tecnologia" em **decisão de projeto justificada** — desde que as mensagens carreguem conteúdo estruturado (JSON com esquema), não texto livre.

## 4. Riscos que continuam abertos
- **Risco de novidade:** o campo se move rápido. Repetir a busca por trabalhos similares antes da qualificação e antes da defesa. Termos: "verifier", "faithfulness", "SHAP", "LLM explanation", "clinical risk", "agentic".
- **Validade externa:** sem avaliação clínica, os resultados valem para a camada técnica (fidelidade), não para utilidade clínica.
- **Dependência de LLM:** resultados variam entre modelos (ColaCare Tab. 5; MedAgentBoard). Testar ≥2 modelos.

## 5. Leitura do PREVENT e da diretriz SBC 2025 (29/09/2026)
Fichamentos: [khan2024prevent](fichamentos/khan2024prevent.md) (texto completo; suplemento pendente) e [sbc2025dislipidemias](fichamentos/sbc2025dislipidemias.md) (capítulos 1, 2, 4 e 5 completos).

**O que mudou:**
1. **Modelo exato a implementar:** PREVENT-**ASCVD** em 10 anos (não DCV total), porque é o desfecho que a SBC usa nas categorias. Forma implementável: logística com termos centrados e interações com a idade (Tabela S12) → D009.
2. **O gabarito de categoria não é trivial:** a SBC usa o escore só para parte dos pacientes; diabetes, LDL ≥ 160, aterosclerose subclínica e agravantes mudam a categoria, e a diretriz tem **inconsistências internas** (seis listadas no fichamento). Solução: motor de regras explícito e versionado → D010, com escopo inicial reduzido → D011.
3. **Gabarito de atribuição exato:** como o PREVENT é linear em log-odds, dá para calcular Shapley exato por variável. Isso é mais forte do que usar SHAP aproximado sobre XGBoost → D012.
4. **Novo tipo de erro mensurável:** o IMC **não** entra no PREVENT-ASCVD. Uma explicação que culpe o IMC é plausível, mas infiel ao modelo. É um caso limpo para demonstrar fidelidade ≠ plausibilidade e para testar o verificador (nova métrica "variáveis fora do modelo" na proposta).
5. **Novo argumento para a defesa:** as próprias inconsistências da diretriz mostram por que regras clínicas devem estar **explícitas no código**, e não "interpretadas" por um LLM.
6. **Correção:** a lista de autores do PREVENT no fichamento anterior estava errada (era a da declaração científica de 2023).

## 6. Auditoria das decisões autorais (29/09/2026)
Ver [auditoria-decisoes-autorais](../02-argumentacao/auditoria-decisoes-autorais.md). Principais consequências:
- **Erro corrigido:** "português é lacuna" era falso — [santos2026escllm](fichamentos/santos2026escllm.md) avaliou 11 LLMs com vinhetas em português (D018).
- **Confirmado:** o Gemini 1.5 usado no código foi desligado (retorna 404) — atualização obrigatória.
- **H3 reformulada** com mecanismo explícito (D017).
- **Nova evidência para H1:** em Santos 2026, recalcular o escore de forma determinística elevou κw de 0,69 para 0,85–0,90.
- Nove itens ainda são **condicionais** (métricas novas, juiz LLM, tamanho da amostra etc.) e precisam de validação dentro do TCC.
