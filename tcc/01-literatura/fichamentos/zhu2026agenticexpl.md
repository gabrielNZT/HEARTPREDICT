---
chave: zhu2026agenticexpl
titulo: Standalone LLM and a Pre-specified Agentic Pipeline for Explaining ICU Mortality Predictions: a Feasibility Study on the eICU Demo Dataset
autores: [Di Zhu, Chen Xie, Haoyun Zhang, Zihan Wei, Ziwei Wang, Jiazhao Shi, Ziyu Wang, Qiyang Xie]
ano: 2026
veiculo: arXiv preprint arXiv:2608.26109
tipo_bib: misc
doi: 10.48550/arXiv.2608.26109
url: https://arxiv.org/abs/2608.26109
temas: [llm-explicacao, multiagentes-llm, xai-shap, fidelidade, trabalho-mais-proximo]
leitura: completa
lido_em: 2026-09-29
relevancia: central
---

# LLM isolado vs pipeline agêntico para explicar predições (Zhu et al., 2026)

## Referência
ZHU, D. et al. Standalone LLM and a Pre-specified Agentic Pipeline for Explaining ICU Mortality Predictions: a Feasibility Study on the eICU Demo Dataset. **arXiv preprint** arXiv:2608.26109, 2026 (v1, 21 mai. 2026). **Não revisado por pares.**

## Problema
SHAP identifica variáveis, mas não produz narrativa clínica. LLMs podem produzir narrativas; pipelines agênticos (interpretar dados → aplicar critérios → raciocínio diferencial → síntese) seriam uma extensão natural. **Pergunta RQ3: o pipeline agêntico gera explicações melhores que um LLM isolado?**

## Método
- eICU Demo (2.353 internações, mortalidade 8,1%). XGBoost: AUROC 0,855 (IC95% 0,796–0,906).
- 38 casos estratificados (baixo/intermediário/alto risco); **apenas 14** coincidem com o subconjunto com SHAP revisado → comparação feita em n=14.
- **LLM isolado:** um prompt com dados do paciente + probabilidade prevista → JSON.
- **Pipeline agêntico (4 passos seriais):** intérprete de dados → consultor de diretrizes (SIRS, SOFA, qSOFA, KDIGO) → raciocínio diferencial → sintetizador.
- **Ambos com o mesmo modelo local pequeno: llama3.2:3b (Ollama).**
- Métricas: alinhamento com SHAP (Jaccard com top-3), consistência de direção, plausibilidade, especificidade de valores, ancoragem em diretrizes, profundidade; auditoria de vazamento do desfecho no texto.

## Resultados
- **Pipeline agêntico teve MENOR fidelidade ao SHAP:** Jaccard 0,077 vs 0,171 do LLM isolado; consistência de direção 78,6% vs 92,9%.
- Pipeline teve **mais ancoragem em diretrizes** (0,762 vs 0,143), mais especificidade de valores (0,236 vs 0,143), plausibilidade ligeiramente maior (0,700 vs 0,671) e **nenhum vazamento de desfecho** (vs 1 no LLM isolado).
- **Conclusão dos autores:** a decomposição agêntica é um **trade-off**, não um ganho categórico; "it should be **paired with attribution-based checks** before use in high-stakes risk explanation". Um sistema útil precisaria de "an attribution check for model fidelity and a guideline-grounded language layer".
- Dados ausentes: PAM ausente em 84,7%, temperatura em 93,4%, lactato em 81,5% → "missingness should be surfaced rather than hidden".

## Limitações declaradas
Base pequena; apenas 14 casos comparáveis (ICs largos); um único modelo base pequeno; mapeamento heurístico entre fatores da narrativa e variáveis do modelo; métricas automáticas são proxies.

## Leitura crítica (importante)
- **Pelo texto, nenhum dos dois geradores recebe os valores SHAP no prompt** — recebem dados do paciente e a probabilidade prevista (Seção 4.5). Assim, o baixo alinhamento com SHAP é esperado: o LLM está **adivinhando** o que dirigiu o modelo. Isso é uma fraqueza de desenho, não só do LLM.
- n=14, modelo de 3B parâmetros, preprint: **evidência fraca**, mas **direcionalmente importante**.
- Não há verificador.

## Relação com o meu TCC
- **É o trabalho mais parecido com a minha comparação** (isolado vs pipeline), e a conclusão dele **é literalmente a minha hipótese H2**: falta uma verificação baseada em atribuição.
- **Diferenças que me posicionam:**
  1. Meus agentes **recebem o SHAP e o número calculado** (não adivinham).
  2. Tenho **verificador** determinístico + LLM.
  3. Amostra maior e estratificada, **múltiplas repetições**, **pelo menos 2 LLMs** (um aberto e um fechado), modelos de porte adequado.
  4. Domínio cardiovascular preventivo, PREVENT, português.
- **Achado a levar para a banca:** decompor em mais agentes pode **piorar** a fidelidade — reforça que o valor está na **verificação**, não na quantidade de agentes.
- Reforça o tratamento explícito de dados ausentes.
- **Atenção à novidade:** a área está ativa em 2026. Registrar a data desta busca (29/09/2026) e repetir a busca antes da entrega.

## Dados citáveis
- [C1] Em 14 casos comparáveis, o pipeline agêntico teve menor alinhamento com o SHAP que o LLM isolado (Jaccard 0,077 vs 0,171) e menor consistência de direção (78,6% vs 92,9%) (Results 2.4; Tabela 4).
- [C2] O pipeline agêntico teve maior ancoragem em diretrizes (0,762 vs 0,143) (Tabela 4).
- [C3] Os autores recomendam combinar a decomposição agêntica com verificações baseadas em atribuição antes do uso em explicações de risco de alto impacto (Abstract; Discussion).
- [C4] Ambos os geradores usaram o mesmo modelo local llama3.2:3b e receberam os dados do paciente e a probabilidade prevista, sem os valores SHAP no prompt (Methods 4.5).
- [C5] Trata-se de preprint não revisado por pares, com apenas 14 casos na comparação direta (Discussion, limitações).
