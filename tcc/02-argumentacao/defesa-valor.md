---
titulo: Defesa do valor da pesquisa
status: rascunho
atualizado: 2026-09-29
resumo: Argumentação para a banca (relevância, lacuna, contribuição, rigor), já corrigida após a leitura completa.
---

# Defesa do valor da pesquisa (versão revisada após leitura completa)

A banca costuma verificar quatro coisas: **(1)** o problema importa? **(2)** há lacuna real? **(3)** a contribuição é clara e refutável? **(4)** o método permite confiar no resultado?

## 1. Relevância
- **Carga da doença:** DCV são a principal causa de morte no Brasil (~30% dos óbitos). Citar a *Estatística Cardiovascular – Brasil* (ABC), não a imprensa. **(verificar metadados — ver pendências)**
- **Momento de transição:** a SBC 2025 adotou o PREVENT no lugar de Framingham ([sbc2025dislipidemias](../01-literatura/fichamentos/sbc2025dislipidemias.md)).
- **Adoção já em curso:** 20–30% dos médicos já usam LLMs na prática clínica (surveys do Reino Unido e de Omã — **fichar antes de citar**).
- **Exigência regulatória de explicabilidade:** OMS 2024 ([who2024lmm](../01-literatura/fichamentos/who2024lmm.md)); AI Act, Art. 13; PL 2338/2023.
- **Frase-chave:** *a pergunta deixou de ser "se" LLMs serão usados e passou a ser "como usá-los com segurança".*

## 2. Lacuna — cadeia de evidências (todas lidas; ver fichamentos)
| # | Evidência | Implicação |
|---|---|---|
| 1 | LLMs isolados erram cálculo clínico; no escore de regressão EuroSCORE II, reproduziram o próprio cálculo em 0–15,8% dos casos ([roeschl2026pipeline](../01-literatura/fichamentos/roeschl2026pipeline.md) [C2]; [khandekar2024medcalc](../01-literatura/fichamentos/khandekar2024medcalc.md) [C1]) | O LLM não deve calcular o PREVENT |
| 2 | Com ferramenta determinística: α 0,78 vs 0,32 (Roeschl) e 0,877 vs 0,409 (AgentMD) | Separar cálculo de linguagem resolve **o número** |
| 3 | Explicações de LLM podem não refletir o processo real ([turpin2023unfaithful](../01-literatura/fichamentos/turpin2023unfaithful.md)); fidelidade ≠ plausibilidade ([jacovi2020faithfulness](../01-literatura/fichamentos/jacovi2020faithfulness.md)) | Acertar o número não garante explicação correta |
| 4 | Com prompt estruturado, o trio top-3 SHAP foi acertado em só 42,5%, e houve **erros de polaridade** ([lee2025shapllm](../01-literatura/fichamentos/lee2025shapllm.md) [C1][C2]) | O problema foi medido em contexto clínico, e o prompt sozinho não basta |
| 5 | Pipeline agêntico **reduziu** a fidelidade ao SHAP em relação ao LLM isolado ([zhu2026agenticexpl](../01-literatura/fichamentos/zhu2026agenticexpl.md) [C1]) | Mais agentes não garantem fidelidade |
| 6 | Explicações (visuais) não ajudaram 457 clínicos a detectar modelo enviesado ([jabbour2023jama](../01-literatura/fichamentos/jabbour2023jama.md) [C1][C2]) | Por analogia: a verificação deve acontecer antes da explicação chegar ao humano |
| 7 | Verificadores superficiais são causa frequente de falha em MAS; recomenda-se verificação multinível e simbólica ([cemri2025mast](../01-literatura/fichamentos/cemri2025mast.md) [C4][C7]) | O verificador precisa ser multinível e, onde possível, determinístico |
| 8 | Os próprios autores recomendam o próximo passo: cálculos fora do LLM + camada de monitoramento (Lee [C5]); checagens baseadas em atribuição (Zhu 2026 [C3]); arquiteturas híbridas (MedAgentBoard [C4]) | **A lacuna foi nomeada pela literatura** |

**Lacuna em uma frase:** a separação cálculo/linguagem já resolve o número, mas ninguém avaliou, com ablação controlada, se um verificador de fidelidade (com polaridade e exatidão numérica) reduz explicações infiéis sobre risco cardiovascular — e não há trabalho em português alinhado à SBC 2025.

## 3. Contribuição
Ver [proposta §6](../00-projeto/proposta.md). Tabela comparativa: [trabalhos-relacionados](trabalhos-relacionados.md).

## 4. Rigor
Design Science Research + TRIPOD+AI + calibração + auditoria de leakage; ≥2 LLMs; repetições; versões fixas; análise pareada; validação do próprio verificador contra anotação manual.

## 5. Parágrafo para a Justificativa (revisado)
> *As doenças cardiovasculares são a principal causa de morte no Brasil, e a estratificação de risco — recentemente atualizada pela SBC com a adoção do escore PREVENT — orienta a prevenção. Modelos de linguagem já são usados por parte dos médicos, mas erram cálculos clínicos, sobretudo em escores baseados em regressão (Roeschl et al., 2026), e produzem explicações nem sempre fiéis ao processo que as gerou (Turpin et al., 2023). Arquiteturas que delegam o cálculo a ferramentas determinísticas resolvem grande parte do problema numérico (Jin et al., 2025; Roeschl et al., 2026), mas a fidelidade da explicação continua em aberto: com prompts estruturados, LLMs recuperaram as três variáveis SHAP mais importantes em apenas 42,5% dos casos e cometeram erros de polaridade (Lee et al., 2025), e a decomposição em múltiplos agentes chegou a reduzir essa fidelidade (Zhu et al., 2026). Os próprios autores desses estudos apontam, como passo seguinte, a verificação da explicação contra a atribuição do modelo. Este trabalho investiga essa lacuna de forma empírica e reprodutível, no contexto da diretriz brasileira.*
