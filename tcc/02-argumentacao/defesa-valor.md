---
titulo: Defesa do valor da pesquisa
status: rascunho
atualizado: 2026-10-06
resumo: Argumentação para a banca (relevância, lacuna, contribuição, rigor), revista após a leitura completa e após a banca simulada (D030).
---

# Defesa do valor da pesquisa (versão revisada após leitura completa)

A banca costuma verificar quatro coisas: **(1)** o problema importa? **(2)** há lacuna real? **(3)** a contribuição é clara e refutável? **(4)** o método permite confiar no resultado?

## 1. Relevância
- **Carga da doença:** DCV são a principal causa de morte no Brasil. **O percentual ainda não tem fonte conferida:** usar Oliveira et al., *Estatística Cardiovascular – Brasil 2023* (Arq Bras Cardiol 2024;121(2):e20240079), depois de ler o dado na fonte. Até lá, não citar número.
- **Momento de transição:** a SBC 2025 adotou o PREVENT no lugar de Framingham ([sbc2025dislipidemias](../01-literatura/fichamentos/sbc2025dislipidemias.md)).
- ~~Adoção já em curso: 20–30% dos médicos já usam LLMs~~ **Retirado:** não há fonte fichada. Só volta ao texto com a fonte lida.
- **Orientação e tendência regulatória (não exigência):** a OMS 2024 publica **orientação**, não norma ([who2024lmm](../01-literatura/fichamentos/who2024lmm.md), lido só no resumo); o AI Act vale na União Europeia e não se aplica a este protótipo; o PL 2338/2023 **não é lei** (segundo o parecer de Ética, em 02/09/2026 aguardava parecer na Câmara).
- **Frase-chave:** *a pergunta deixou de ser "se" LLMs serão usados e passou a ser "como usá-los com segurança".*

## 2. Lacuna — cadeia de evidências
Profundidade de leitura: as linhas 1, 2, 4, 5, 7 e 9 vêm de fontes lidas na íntegra. A linha 3 vem de dois resumos (Turpin, Jacovi); as linhas 6 (Jabbour) e 8 (He & Martens), de leitura parcial.
| # | Evidência | Implicação |
|---|---|---|
| 1 | LLMs isolados erram cálculo clínico; no escore de regressão EuroSCORE II, reproduziram o próprio cálculo em 0–15,8% dos casos ([roeschl2026pipeline](../01-literatura/fichamentos/roeschl2026pipeline.md) [C2]; [khandekar2024medcalc](../01-literatura/fichamentos/khandekar2024medcalc.md) [C1]) | O LLM não deve calcular o PREVENT |
| 2 | Com ferramenta determinística: α 0,78 vs 0,32 (Roeschl) e 0,877 vs 0,409 (AgentMD) | Separar cálculo de linguagem resolve **o número** |
| 3 | Explicações de LLM podem não refletir o processo real ([turpin2023unfaithful](../01-literatura/fichamentos/turpin2023unfaithful.md)); fidelidade ≠ plausibilidade ([jacovi2020faithfulness](../01-literatura/fichamentos/jacovi2020faithfulness.md)) | Acertar o número não garante explicação correta |
| 4 | Com prompt estruturado, o **GPT-4** acertou o trio top-3 SHAP em 42,5% **das gerações** (um único LLM, 10 gerações por caso em 40 casos), e houve **erros de polaridade** ([lee2025shapllm](../01-literatura/fichamentos/lee2025shapllm.md) [C1][C2]) | O problema foi medido em contexto clínico, e o prompt sozinho não basta |
| 5 | Num *preprint* com 14 casos e um modelo de 3 bilhões de parâmetros, o pipeline agêntico teve alinhamento com o SHAP **numericamente menor** que o do LLM isolado (Jaccard 0,077 × 0,171), **com intervalos de confiança sobrepostos**; a "direção" medida ali é em relação ao rótulo previsto, não ao sinal do SHAP ([zhu2026agenticexpl](../01-literatura/fichamentos/zhu2026agenticexpl.md) [C1]) | Indício, não resultado: mais agentes não garantem fidelidade |
| 6 | Explicações (visuais) não ajudaram 457 clínicos a detectar modelo enviesado ([jabbour2023jama](../01-literatura/fichamentos/jabbour2023jama.md) [C1][C2]) | Por analogia: a verificação deve acontecer antes da explicação chegar ao humano |
| 7 | Verificadores superficiais são causa frequente de falha em MAS; recomenda-se verificação multinível e simbólica ([cemri2025mast](../01-literatura/fichamentos/cemri2025mast.md) [C4][C7]) | O verificador precisa ser multinível e, onde possível, determinístico |
| 8 | Um ciclo narrador → avaliador → crítico reduziu narrativas infiéis em 5 LLMs e 5 bases tabulares; 31 de 100 narrativas iniciais tinham erro; a fidelidade final é medida pelo próprio avaliador do ciclo, e os falsos positivos ficam fora do estudo ([he2026agenticnarratives](../01-literatura/fichamentos/he2026agenticnarratives.md) [C1][C3]) | **O ciclo de crítica já foi testado.** Falta saber se o efeito se mantém com referência exata, regras clínicas e desfecho independente |
| 9 | Os próprios autores recomendam o próximo passo: cálculos fora do LLM + camada de monitoramento (Lee [C5]); checagens baseadas em atribuição (Zhu 2026 [C3]); arquiteturas híbridas (MedAgentBoard [C4]) | **A lacuna foi nomeada pela literatura** |

**Lacuna em uma frase (D030):** ciclos de crítica já reduziram narrativas infiéis em bases genéricas (He & Martens, 2026), mas, **nos trabalhos lidos**, a referência é uma aproximação tomada como verdadeira, não há regras de diretriz clínica e o resultado final é medido pelo mesmo avaliador que corrige o texto. Este trabalho testa se o efeito se mantém com atribuição exata sobre o PREVENT, regras da SBC 2025 e desfecho decidido por anotação humana independente.

> A expressão "nos trabalhos lidos" é deliberada: a busca ainda não tem protocolo documentado (pendência C8). O idioma **não** é diferencial (D018).

## 3. Contribuição
Ver [proposta §6](../00-projeto/proposta.md). Tabela comparativa: [trabalhos-relacionados](trabalhos-relacionados.md).

## 4. Rigor
Experimento controlado pareado com plano de análise pré-especificado (D029); ≥ 2 LLMs; repetições; versões fixas; desfecho por anotação humana cega; validação do verificador contra essa anotação. TRIPOD+AI, calibração e auditoria de *leakage* só se aplicam à extensão com modelo treinado (D016), não ao núcleo.

## 5. Parágrafo para a Justificativa (revisado)
> *As doenças cardiovasculares são a principal causa de morte no Brasil, e a estratificação de risco — recentemente atualizada pela SBC com a adoção do escore PREVENT — orienta a prevenção. Modelos de linguagem erram cálculos clínicos, sobretudo em escores baseados em regressão (Roeschl et al., 2026), e produzem explicações nem sempre fiéis ao processo que as gerou (Turpin et al., 2023). Arquiteturas que delegam o cálculo a ferramentas determinísticas resolvem grande parte do problema numérico (Jin et al., 2025; Roeschl et al., 2026), mas a fidelidade da explicação continua em aberto: com prompts estruturados, o GPT-4 recuperou as três variáveis SHAP mais importantes em apenas 42,5% das gerações e cometeu erros de polaridade (Lee et al., 2025). Ciclos em que um agente critica e outro reescreve reduziram as narrativas infiéis em bases tabulares genéricas (He; Martens, 2026), mas com uma referência aproximada e com o mesmo avaliador atuando no ciclo e na medida final. Este trabalho verifica, de forma empírica e reprodutível, se esse ganho se mantém quando a atribuição de referência é exata, há regras de uma diretriz clínica brasileira e o desfecho é avaliado de forma independente do verificador.*
