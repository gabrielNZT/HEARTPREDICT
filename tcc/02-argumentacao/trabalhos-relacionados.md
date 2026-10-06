---
titulo: Tabela comparativa de trabalhos relacionados
status: rascunho
atualizado: 2026-09-29
resumo: Comparação critério a critério entre os trabalhos mais próximos e a proposta; base do capítulo de Trabalhos Relacionados.
---

# Trabalhos relacionados — tabela comparativa

Legenda: ✔ sim · ✗ não · ◐ parcial · ? não verificado.

| Trabalho | Predição por ML/ferramenta | LLM gera explicação | SHAP entregue ao LLM | Verificador da explicação | Fidelidade: top-k | Fidelidade: polaridade | Fidelidade: números | Baseline sem verificador | Viés demográfico | Cardiovascular | PT-BR / diretriz BR | Revisado por pares |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [AgentMD](../01-literatura/fichamentos/jin2025agentmd.md) (2025) | ✔ calculadoras | ◐ resumo do resultado | ✗ | ◐ só na curadoria | ✗ | ✗ | ✗ | ✗ | ✗ | ◐ | ✗ | ✔ |
| [MedCalc-Bench](../01-literatura/fichamentos/khandekar2024medcalc.md) (2024) | ✗ (avalia LLM calculando) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | — | ✗ | ◐ | ✗ | ✔ |
| [Roeschl](../01-literatura/fichamentos/roeschl2026pipeline.md) (2026) | ✔ motor determinístico | ✗ | ✗ | ◐ consistência interna | ✗ | ✗ | ✗ | — | ✗ | ✔ | ✗ | ✔ |
| [ColaCare](../01-literatura/fichamentos/wang2025colacare.md) (2025) | ✔ modelos de prontuário | ✔ relatório | ✔ | ✗ (consenso) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✔ |
| [Lee et al.](../01-literatura/fichamentos/lee2025shapllm.md) (2025) | ✔ XGBoost | ✔ | ✔ | ✗ (só prompt) | ✔ | ◐ qualitativo | ✗ | ✗ | ✗ | ✗ | ✗ | ✔ |
| [Zhu et al.](../01-literatura/fichamentos/zhu2026agenticexpl.md) (2026) | ✔ XGBoost | ✔ | ✗ | ✗ | ✔ Jaccard | ◐ direção do rótulo | ✗ | ✔ isolado vs agêntico | ✗ | ✗ | ✗ | ✗ preprint |
| [NEURON](../01-literatura/fichamentos/chandrasekaran2026neuron.md) (2026) | ✔ ML + ontologia | ✔ | ✔ | ? | ? | ? | ? | ? | ? | ◐ IC aguda | ✗ | ✗ preprint |
| [MedAgentBoard](../01-literatura/fichamentos/zhu2025medagentboard.md) (2025) | ✔ baselines | ✗ (avalia predição) | ✗ | ✗ | ✗ | ✗ | ✗ | — | ✗ | ✗ | ✗ | ✔ |
| [Chan & Kwek](../01-literatura/fichamentos/chan2025vies.md) (2025) | ✗ | ✔ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✔ | ✔ | ✗ | ✔ |
| [Santos et al.](../01-literatura/fichamentos/santos2026escllm.md) (2026) | ◐ recálculo post hoc | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | — | ✗ | ✔ | ◐ português, diretriz ESC | ✔ |
| **Este TCC** | ✔ PREVENT (+ XGBoost opcional) | ✔ | ✔ | **✔ híbrido** | ✔ | **✔** | **✔** | **✔ ablação** | **✔** | ✔ | **✔ diretriz BR** (idioma não é diferencial — D018) | — |

## Leitura da tabela (texto base para o capítulo)
- A combinação de **verificador da explicação** + **métricas de polaridade e números** + **ablação do verificador** não aparece em nenhum dos trabalhos identificados até 29/09/2026 (busca ainda não estruturada — ver auditoria C8).
- Os trabalhos mais próximos em arquitetura são **ColaCare** (entrega SHAP a agentes LLM, mas busca consenso e não mede fidelidade) e **Lee et al.** (mede fidelidade top-3, mas sem verificador nem baseline; propõe o verificador como trabalho futuro).
- O mais próximo em desenho experimental é **Zhu et al. (2026)**, que compara LLM isolado vs pipeline agêntico e **recomenda** checagens baseadas em atribuição, sem implementá-las; é preprint, com n=14 e sem entregar o SHAP ao LLM.
- **Santos et al. (2026)** mostram, com vinhetas em português, que o erro dos LLMs está no cálculo e não na extração — outro apoio a H1 — e que o idioma não é uma lacuna por si só.
- **Roeschl et al. (2026)** e **AgentMD** estabelecem a separação cálculo/linguagem que este trabalho assume como ponto de partida (H1).

> Os itens marcados com "?" (NEURON) exigem leitura do texto completo antes da versão final.
