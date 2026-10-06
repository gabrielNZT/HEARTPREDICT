---
chave: wang2025colacare
titulo: ColaCare: Enhancing Electronic Health Record Modeling through Large Language Model-Driven Multi-Agent Collaboration
autores: [Zixiang Wang, Yinghao Zhu, Huiya Zhao, Xiaochen Zheng, Dehao Sui, Tianlong Wang, Wen Tang, Yasha Wang, Ewen Harrison, Chengwei Pan, Junyi Gao, Liantao Ma]
ano: 2025
veiculo: Proceedings of the ACM Web Conference 2025 (WWW '25)
tipo_bib: inproceedings
doi: 10.1145/3696410.3714877
url: https://arxiv.org/abs/2410.02551
temas: [multiagentes-llm, hibrido-ml-llm, xai-shap, trabalho-mais-proximo]
leitura: completa
lido_em: 2026-09-29
relevancia: central
---

# ColaCare (Wang et al., 2025)

## Referência
WANG, Z. et al. ColaCare: Enhancing Electronic Health Record Modeling through Large Language Model-Driven Multi-Agent Collaboration. In: **Proceedings of the ACM Web Conference 2025 (WWW '25)**. Sydney: ACM, 2025. DOI: 10.1145/3696410.3714877. arXiv:2410.02551 (v2 lida). Código: https://colacare.netlify.app.

## Problema
Modelos de deep learning para prontuário estruturado são "caixas-pretas", e técnicas como SHAP dão interpretabilidade limitada, sem ligação com conhecimento médico. LLMs, por outro lado, predizem mal a partir de dados estruturados. Frameworks multiagente anteriores (MedAgents etc.) trabalham só com texto e não usam diretrizes médicas confiáveis.

## Método (arquitetura)
1. **Modelos especialistas** (AdaCare, ConCare, RETAIN) processam a série temporal do prontuário → logit de risco **+ pesos SHAP**.
2. **DoctorAgents** (um por modelo especialista, LLM DeepSeek-V2.5): recebem logit, SHAP, dados básicos e documentos recuperados por **RAG do Manual MSD** (MedCPT, top-3) → revisão inicial.
3. **MetaAgent** sintetiza relatório; rodadas de consulta (máx. 3) até consenso: DoctorAgents concordam ou discordam com evidências; MetaAgent revisa.
4. **Rede de fusão**: embedding do relatório final (GatorTron) concatenado com as representações dos modelos especialistas → MLP → predição final.
- Dados: MIMIC-IV (mortalidade e readmissão 30d), CDSL (COVID-19), ESRD (doença renal terminal). Teste ~1.000 pacientes (146 no ESRD). Bootstrap 100×.
- Baselines: modelos especialistas isolados, 5 tipos de ensemble, LLM único (zero/few-shot, self-consistency), multiagente (MAD, MedAgents, ReConcile).

## Resultados
- ColaCare obtém melhor AUPRC na maioria das tarefas (ex.: MIMIC-IV mortalidade AUPRC 54,05 vs melhor ensemble 53,59; AUROC 88,80 vs 88,60) (Tabela 2).
- **Métodos só-LLM ficam muito abaixo**: MedAgents AUPRC 27,73; LLM zero-shot 31,01 no MIMIC-IV mortalidade.
- **Ablação (Tabela 3):** removendo os modelos especialistas, AUPRC cai de 54,05 para **27,73** — o desempenho vem do ML convencional. Sem RAG: 51,57; sem processo multiagente (MDT): 50,63; sem rede de fusão (LLM dá a predição final): 42,61.
- Número de agentes: 1–2 DoctorAgents não ajudam; 3 melhora (Tabela 4).
- Robusto a diferentes LLMs (GPT-4o, Claude 3.5, Llama 3 etc.) (Tabela 5).
- Custo: ~US$0,013 por paciente com DeepSeek-V2.5; ~60–124 mil tokens de prompt e 8–12 chamadas de API por paciente (Tabela 6).
- Avaliação humana: 12 médicos de nefrologia (5 hospitais), escala de concordância 1–5: ColaCare 4,4 vs ConCare 3,2.

## Limitações declaradas
- Generalização (poucas tarefas e datasets; testar mais LLMs, inclusive Gemini e Llama).
- Avaliação humana precisa de mais clínicos.
- Modelos especialistas fixos após treino (sem aprendizado contínuo).
- Futuro: mecanismos de **estimativa de confiança**.

## Leitura crítica
- **Ganhos pequenos e dentro do desvio-padrão:** ex.: AUPRC 54,05±4,88 vs ensemble 53,59±4,52. Não há teste estatístico de significância. No ESRD, AUROC do ColaCare (71,61) fica **abaixo** do EnsembleDeep (73,76).
- A ablação mostra que o valor **preditivo** vem dos modelos especialistas; o LLM contribui pouco para o número (coerente com MedAgentBoard).
- **O relatório gerado não é avaliado quanto à fidelidade** aos valores SHAP e logits fornecidos. O relatório é usado como *feature* para a rede de fusão e avaliado por um estudo de caso e por um questionário de concordância — não por uma métrica sistemática de fidelidade.
- O processo busca **consenso**: no estudo de caso, agentes "revisam suas avaliações" para concordar com o MetaAgent — risco de conformidade, não de correção. Não há agente com papel explícito de **verificar** contra a fonte.
- A predição final depende da rede de fusão treinada, então o texto influencia o número — o que dificulta atribuir a explicação ao modelo original.
- Detalhes da avaliação humana são escassos no corpo do artigo.

## Relação com o meu TCC
- **É o trabalho relacionado mais próximo:** modelos convencionais + SHAP entregues a agentes LLM que produzem relatório interpretável. **Minha arquitetura é da mesma família.**
- **Diferenças que definem minha contribuição:**
  1. Eu **não** reinjeto o texto na predição: o número vem só da ferramenta validada (PREVENT/XGBoost). Isso mantém a explicação atribuível ao modelo.
  2. Eu **meço a fidelidade** do texto ao SHAP e aos números (métrica sistemática), algo que o ColaCare não faz.
  3. Eu uso um **verificador** (determinístico + LLM) no lugar de consenso por debate.
  4. Domínio: risco cardiovascular preventivo (não UTI/mortalidade), português, diretriz SBC 2025.
- A ablação do ColaCare (sem modelos especialistas → colapso) é evidência forte para meu princípio "o LLM não calcula".
- Sensibilidade a LLMs diferentes: justifica testar pelo menos 2 LLMs (um fechado, um aberto).
- Custo por paciente: benchmark para reportar o meu.

## Dados citáveis
- [C1] No ColaCare, os modelos especialistas convencionais produzem logits e pesos SHAP que são fornecidos aos agentes LLM (Seção 4.1, Eq. 3–4).
- [C2] Sem os modelos especialistas, o AUPRC na mortalidade do MIMIC-IV caiu de 54,05 para 27,73 (Tabela 3).
- [C3] A vantagem do ColaCare sobre o melhor ensemble convencional na mortalidade do MIMIC-IV foi de 54,05±4,88 vs 53,59±4,52 de AUPRC, dentro do desvio-padrão (Tabela 2).
- [C4] O relatório final é codificado e fundido com as representações dos modelos para gerar a predição; a fidelidade do relatório aos valores SHAP não é medida (Seção 4.3; Seção 6).
- [C5] Custo médio de ~US$0,013 por paciente, com 8–12 chamadas de API (Seção 6.6, Tabela 6).
- [C6] Os autores apontam como trabalho futuro mecanismos de estimativa de confiança e avaliação humana mais ampla (Apêndice A).
