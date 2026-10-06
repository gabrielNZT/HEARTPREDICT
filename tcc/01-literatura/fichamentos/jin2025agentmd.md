---
chave: jin2025agentmd
titulo: AgentMD: Empowering language agents for risk prediction with large-scale clinical tool learning
autores: [Qiao Jin, Zhizheng Wang, Yifan Yang, Qingqing Zhu, Donald Wright, Thomas Huang, Nikhil Khandekar, Nicholas Wan, Xuguang Ai, W. John Wilbur, Zhe He, R. Andrew Taylor, Qingyu Chen, Zhiyong Lu]
ano: 2025
veiculo: Nature Communications
volume: 16
paginas: 9377
tipo_bib: article
doi: 10.1038/s41467-025-64430-x
url: https://www.nature.com/articles/s41467-025-64430-x
temas: [llm-ferramentas, calculadoras-clinicas, agentes-llm]
leitura: completa
lido_em: 2026-09-29
relevancia: central
---

# AgentMD (Jin et al., 2025)

## Referência
JIN, Q. et al. AgentMD: Empowering language agents for risk prediction with large-scale clinical tool learning. **Nature Communications**, v. 16, art. 9377, 2025. DOI: 10.1038/s41467-025-64430-x. Preprint: arXiv:2402.13225 (fev. 2024).

## Problema
Calculadoras clínicas (ex.: HEART, CURB-65) são subutilizadas: o clínico precisa saber qual usar, os parâmetros não são padronizados, a entrada é manual. LLMs sozinhos erram cálculos. Existe uma lacuna de *toolbox* abrangente e de métodos para **aplicar** ferramentas clínicas com LLMs.

## Método
- **Dois papéis:** *tool maker* e *tool user*.
- **Tool maker:** busca no PubMed (2000–abr/2023) → 339.952 artigos → GPT-3.5 faz triagem (33.033) → GPT-4 redige 24.190 calculadoras estruturadas (Python + interpretação) → **GPT-4 autoverifica** com 6 critérios (parâmetros definidos, fidelidade ao artigo, sem suposições, interpretação útil, sem bugs) → **2.164 calculadoras (RiskCalcs)**.
- **Tool user:** (1) seleção: MedCPT recupera top-10, LLM escolhe as elegíveis; (2) computação: LLM gera código Python e executa num interpretador, com re-tentativa em caso de erro; (3) sumarização em parágrafo. Parâmetros ausentes → estimativa de melhor/pior caso.
- **LLMs:** GPT-3.5 e GPT-4 (versão 0613, Azure), **temperatura 0**.
- **Avaliação:**
  - Qualidade das ferramentas: 100 calculadoras (top-50 citadas + 50 aleatórias), 3 anotadores + consenso; testes unitários (500 conjuntos gerados pelo GPT-4 + 100 manuais com casos-limite).
  - **RiskQA:** 350 questões de múltipla escolha estilo USMLE, **vinhetas geradas pelo GPT-4** a partir de parâmetros validados manualmente.
  - 698 notas de emergência reais (Yale), 16 calculadoras, 80 pares paciente-calculadora avaliados por 2 médicos.
  - 9.822 notas de admissão do MIMIC-III (análise populacional; AUROC para mortalidade intra-hospitalar).

## Resultados
- Correção da lógica de cálculo: 87,6%; da interpretação: 89,0%.
- Testes unitários: 91,6% (458/500) consistentes; 84,0% nos 100 casos manuais de fronteira.
- RiskQA: AgentMD-GPT-4 **0,877** vs CoT-GPT-4 **0,409**; AgentMD-GPT-3.5 0,546 vs CoT-GPT-3.5 0,321. AgentMD com GPT-3.5 supera CoT com GPT-4.
- Seleção de ferramenta: GPT-4 0,823; GPT-3.5 0,663; MedCPT top-1 0,723.
- Notas reais: 80,6% elegíveis; processo correto 52,3% + parcialmente correto 28,5%; resultado útil 68,6% + parcialmente útil 29,1%. **HEART Score** e Canadian C-Spine ficaram abaixo de 60% por **suposições incorretas sobre valores ausentes**.
- MIMIC-III: 113 calculadoras com AUROC maior que GPT-4 puro na predição de mortalidade.

## Limitações declaradas pelos autores
- Calculadoras extraídas só de abstracts (não texto completo).
- Dependência do GPT-4: custo e impossibilidade de rodar localmente; sugerem LLMs abertos (Llama).
- Apenas modalidade texto; dados estruturados como trabalho futuro.
- "Further and more comprehensive evaluations are required before it can be incorporated into the clinical workflow."
- Sem cálculo prévio de tamanho amostral, sem randomização, sem cegamento.

## Limitações que eu identifico (leitura crítica)
- O RiskQA é **sintético** (vinhetas geradas por GPT-4) e em formato de múltipla escolha — mede acerto de alternativa, não qualidade da explicação.
- A etapa de **sumarização** (texto final ao usuário) **não é avaliada quanto à fidelidade** ao resultado computado. "Interpretação correta" no artigo refere-se à interpretação da calculadora (faixas de escore) estar fiel ao artigo-fonte, não à narrativa gerada para o paciente.
- A verificação por LLM existe **só na curadoria** (GPT-4 verificando GPT-4), não na inferência. Não há verificação determinística da saída final.
- Não há avaliação de viés demográfico.
- Não é específico para risco cardiovascular preventivo (PREVENT/SCORE2) nem para o contexto brasileiro.

## Relação com o meu TCC
- **Fundamenta H1** (LLM + ferramenta > LLM puro): replicar o efeito no domínio cardiovascular é verificação de sanidade.
- **Define a fronteira da contribuição:** AgentMD resolve *acerto do número*; meu trabalho ataca a *fidelidade da explicação* e o *papel de um verificador na inferência*.
- **Precedente metodológico:** uso de vinhetas sintéticas geradas a partir de parâmetros validados é aceito numa revista de alto impacto — legitima meu uso de vinhetas.
- **Precedente de reprodutibilidade:** temperatura 0 e versão fixa do modelo.
- **Alerta de design:** valores ausentes são a principal fonte de erro em dados reais → meu sistema deve tratar ausência explicitamente (recusar ou pedir o dado, não supor).
- Possível pergunta da banca: "AgentMD já tem verificador." Resposta: tem **autoverificação na curadoria das ferramentas**, não verificação da explicação entregue ao usuário.

## Dados citáveis
- [C1] AgentMD com GPT-4 obteve acurácia de 0,877 contra 0,409 do GPT-4 com chain-of-thought no RiskQA (N=350) (Results, Fig. 3c).
- [C2] AgentMD com GPT-3.5 (0,546) superou GPT-4 com chain-of-thought (0,409) (Results, Fig. 3b–c).
- [C3] Em 698 notas reais de emergência, o processo de cálculo foi correto em 52,3% e parcialmente correto em 28,5% dos pares avaliados (Results, Fig. 4b).
- [C4] HEART Score teve desempenho abaixo de 60% por suposições incorretas sobre valores ausentes (Results, Fig. 4c).
- [C5] As 2.164 calculadoras passaram por autoverificação do GPT-4 em 6 critérios; 91,6% dos testes unitários foram consistentes com cálculo manual (Methods; Results).
- [C6] RiskQA é composto por vinhetas clínicas geradas pelo GPT-4 a partir de 350 conjuntos de parâmetros validados manualmente (Methods, "Evaluation of AgentMD as a tool user").
- [C7] Os autores afirmam que avaliações mais abrangentes são necessárias antes do uso no fluxo clínico (Introduction; Discussion).

## Referências a seguir (bola de neve)
- "Large language model agents can use tools to perform clinical calculations" — npj Digital Medicine, 2025 (aparece como relacionado).
- OpenMedCalc (ref. 30) e Almanac (ref. 31) — abordagens concorrentes.
- "Benchmarking large language model-based agent systems for clinical decision tasks" — npj Digital Medicine, 2026.
