---
chave: lee2025shapllm
titulo: A prompt framework for enhancing LLM-based explainability of medical machine learning models: an intensive care unit application
autores: [Sujung Lee, Won Ik Cho, Youngrong Lee, Duck Ju Kim, Kyeng Hyun Nam, Sangmin Lee, Jungyo Suh, Taehoon Ko]
ano: 2025
veiculo: BMC Medical Informatics and Decision Making
volume: 25
paginas: 430
tipo_bib: article
doi: 10.1186/s12911-025-03239-6
url: https://link.springer.com/article/10.1186/s12911-025-03239-6
temas: [xai-shap, llm-explicacao, fidelidade, trabalho-mais-proximo]
leitura: completa
lido_em: 2026-09-29
relevancia: central
---

# Framework de prompt para explicar SHAP com LLM (Lee et al., 2025)

## Referência
LEE, S. et al. A prompt framework for enhancing LLM-based explainability of medical machine learning models: an intensive care unit application. **BMC Medical Informatics and Decision Making**, v. 25, art. 430, 2025. DOI: 10.1186/s12911-025-03239-6. PMID: 41299597. PMCID: PMC12659558.

## Problema
Valores SHAP são pouco intuitivos para clínicos ("XAI-to-reality gap"). Uma revisão de 2024 citada pelos autores indica que 83% dos estudos de XAI não tinham envolvimento clínico significativo. Hipótese: LLMs guiados por prompts estruturados podem "traduzir" SHAP em narrativas clínicas.

## Método
- **Estudo exploratório de viabilidade.**
- Modelo: XGBoost para falha de extubação na UTI (MIMIC-III, 747 eventos, 16 variáveis) → valores SHAP.
- 40 casos de teste (10 VP, 10 VN, 10 FP, 10 FN), com ruído ≤3% nos valores numéricos.
- **Prompt zero-shot estruturado:** (a) persona de intensivista + definições das variáveis; (b) princípios de segurança (não alucinar, não imputar dado ausente, evitar viés de gênero salvo se SHAP indicar); (c) raciocínio em 3 passos: extrair os 3 principais fatores por |SHAP|, reconciliar predição com desfecho real, propor plano clínico; (d) template de entrada/saída.
- GPT-4 via interface ChatGPT (versão de maio de 2024), **10 gerações por caso**.
- **Métricas quantitativas:** acerto exato do trio top-3 (1 se os 3 batem); **"fidelidade"** = 1 / 0,66 / 0,33 para 3/2/1 variáveis corretas no top-3; **entropia** da variação dos trios entre as 10 gerações.
- **Avaliação qualitativa:** 7 médicos (3 intensivistas, 4 não intensivistas), Likert 1–5, 7 itens (6 de utilidade, 1 de segurança).

## Resultados
- **Fidelidade 0,783; acerto exato do top-3 apenas 0,425**; entropia 0,226 (Tabela 1).
- Por tipo de caso: VN e FN têm fidelidade menor (0,70 e 0,73) e entropia maior — o LLM é **menos consistente para explicar "normalidade"/ausência de risco**.
- Utilidade 3,94 ± 0,48; segurança 4,21 ± 0,68. **Intensivistas deram notas bem menores** (segurança 3,45 vs 4,79 dos não especialistas).
- **Erros observados (Tabela 3):** 3 casos de **erro de polaridade do SHAP** (valor negativo interpretado como aumento de risco), 2 sugestões potencialmente inseguras (ex.: traqueostomia), 1 imprecisão clínica (FR baixa descrita como "alta"), 1 problema de concisão.
- Versões iniciais do prompt produziam **valores alucinados**; a versão final exigiu citação explícita dos números e mensagem de erro para dados ausentes.

## Limitações declaradas (muito relevantes)
1. Um único LLM (GPT-4).
2. Uma única tarefa e base (MIMIC-III).
3. Viés de seleção da coorte.
4. **Sem comparação com baseline** (SHAP sem narrativa).
5. Amostra de 7 clínicos, por conveniência.
6. O LLM não acessa a lógica interna do classificador; as narrativas podem ser especulativas.
7. **Erros de interpretação persistem apesar das salvaguardas no prompt.** Como trabalho futuro, os autores propõem: **"(i) incorporate a preprocessing module that validates numeric inputs and performs all calculations outside the LLM, and (ii) deploy a monitoring layer that flags or blocks any high-risk clinical recommendation until it is verified by a clinician"** (Seção Limitation).

## Leitura crítica
- **Atenção à definição de "fidelidade":** aqui ela mede apenas se as 3 variáveis mais importantes aparecem no texto. **Não mede polaridade (direção), magnitude nem números citados.** Os erros de polaridade foram detectados só qualitativamente pelos avaliadores. Portanto, a fidelidade real é **menor ou igual** a 0,783.
- Uso da interface ChatGPT (não API com versão fixa e temperatura controlada) prejudica a reprodutibilidade.
- Não há verificador; toda a proteção está no prompt.

## Relação com o meu TCC
- **É a evidência mais direta da minha lacuna.** Mostra que (a) o problema de fidelidade existe e foi medido em contexto clínico; (b) salvaguardas só no prompt **não bastam** (erros de polaridade persistiram); (c) os próprios autores propõem, como trabalho futuro, exatamente meu desenho: **cálculos fora do LLM + camada de monitoramento/verificação**.
- **Métrica herdada e estendida:** reutilizo "fidelidade top-k" e entropia (comparabilidade com a literatura) e **acrescento** métricas que eles não mediram: **concordância de sinal (polaridade)**, **exatidão dos números citados** e **taxa de afirmações não sustentadas**.
- **Baseline que eles não tiveram:** minha configuração 2 (LLM + ferramenta, sem verificador) é o baseline para medir o valor do verificador.
- **Reprodutibilidade:** usar API com versão fixa e temperatura definida, e registrar tudo — diferencial em relação a este estudo.
- **Achado sobre VN/FN:** incluir casos de **baixo risco** na amostra, estratificados, porque é onde o LLM é menos consistente.

## Dados citáveis
- [C1] Com prompt estruturado, o GPT-4 recuperou os 3 fatores SHAP mais importantes com fidelidade média de 0,783, mas acertou o trio completo em apenas 42,5% das gerações (Results; Tabela 1).
- [C2] Foram observados erros de polaridade do SHAP (valores negativos interpretados como aumento de risco) em 3 casos, apesar das salvaguardas no prompt (Tabela 3).
- [C3] A métrica de fidelidade usada considera apenas a presença das 3 variáveis principais, não a direção nem a magnitude do efeito (Methods, "Quantitative assessment").
- [C4] Intensivistas atribuíram nota de segurança 3,45 contra 4,79 dos não intensivistas (Tabela 2).
- [C5] Os autores propõem como trabalho futuro realizar todos os cálculos fora do LLM e adicionar uma camada de monitoramento que sinalize ou bloqueie recomendações de alto risco (Limitation).
- [C6] Casos verdadeiro-negativos tiveram a maior entropia (0,359) e a menor fidelidade (0,70) (Tabela 1).
- [C7] O estudo não comparou a narrativa do LLM com um baseline de SHAP sem narrativa (Limitation, item 4).
