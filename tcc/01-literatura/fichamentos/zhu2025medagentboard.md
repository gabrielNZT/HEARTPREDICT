---
chave: zhu2025medagentboard
titulo: MedAgentBoard: Benchmarking Multi-Agent Collaboration with Conventional Methods for Diverse Medical Tasks
autores: [Yinghao Zhu, Ziyi He, Haoran Hu, Xiaochen Zheng, Xichen Zhang, Zixiang Wang, Junyi Gao, Liantao Ma, Lequan Yu]
ano: 2025
veiculo: Advances in Neural Information Processing Systems 38 (NeurIPS 2025) - Datasets and Benchmarks Track
tipo_bib: inproceedings
doi: 10.48550/arXiv.2505.12371
url: https://arxiv.org/abs/2505.12371
temas: [multiagentes-llm, benchmarks, ml-convencional]
leitura: completa
lido_em: 2026-09-29
relevancia: central
---

# MedAgentBoard (Zhu et al., 2025)

## Referência
ZHU, Y. et al. MedAgentBoard: Benchmarking Multi-Agent Collaboration with Conventional Methods for Diverse Medical Tasks. In: **NeurIPS 2025, Datasets and Benchmarks Track**. arXiv:2505.12371 (v2, 30 out. 2025, lida). Código e dados: https://medagentboard.netlify.app/.

> Verificar na página oficial do NeurIPS 2025 o número do volume e as páginas antes da versão final do TCC.

## Problema
As vantagens de sistemas multiagente com LLM em medicina são pouco compreendidas: avaliações anteriores se limitam a QA de múltipla escolha e **omitem comparação com métodos convencionais** (ML/DL treinados na tarefa).

## Método
Três paradigmas — **convencional**, **LLM único** e **multiagente** — comparados em 4 tarefas:
1. QA e VQA médicas (MedQA, PubMedQA, PathVQA, VQA-RAD). Multiagente: MedAgents, ReConcile, MDAgents, ColaCare.
2. Resumo leigo (Cochrane, eLife, PLOS, Med-EASi, PLABA). Multiagente: pipeline de 9 agentes inspirado no AgentSimp.
3. **Predição com prontuário estruturado** (MIMIC-IV mortalidade e readmissão em 30 dias; TJH mortalidade COVID-19). Convencional: Decision Tree, XGBoost, GRU, LSTM, AdaCare, ConCare, GRASP. Métricas: AUROC e AUPRC.
4. Automação de fluxo de análise de dados clínicos (100 tarefas; SmolAgents, OpenManus, Owl), avaliada por painel de 6 especialistas (Fleiss κ 0,40–0,61).
- Amostras de 200 itens por conjunto de teste; bootstrap para desvio-padrão. Agentes com DeepSeek-V3-0324 como LLM base.

## Resultados
- **QA textual:** LLM único forte empata ou supera multiagente (CoT-SC 89,90% no MedQA vs MedAgents 85,25%) (Tabela 3).
- **VQA:** modelos convencionais especializados dominam.
- **Resumo leigo:** modelos seq2seq ajustados (BART, PEGASUS) superam LLMs e multiagente em ROUGE-L/SARI.
- **Predição com prontuário (Tabela 5):** convencionais superam LLMs com folga (AdaCare AUROC 94,28 no MIMIC-IV mortalidade; XGBoost 98,05 no TJH). Multiagente melhora sobre o próprio LLM base (ColaCare 82,91 vs DeepSeek-V3 76,86), mas **não supera o melhor LLM único** (GPT-4o 85,99) e fica bem abaixo dos convencionais. Os autores atribuem os ganhos modestos ao LLM base, não à estratégia multiagente.
  - Nuance: no MIMIC-IV, XGBoost usando só a última visita teve AUROC 64,62, **abaixo** do GPT-4o — o que vence é o modelo **sequencial** especializado.
- **Automação de fluxo:** multiagente com execução de código aumenta a **completude** (ex.: OpenManus 64,0% correto na modelagem TJH vs LLM único com 50% sem resultado), mas a taxa de soluções corretas fica tipicamente abaixo de 40–50%.
- **Custo (Apêndice D):** multiagente custa em geral 2–10× mais que LLM único zero-shot.
- **Apêndice H.4:** frameworks baseados em *role-playing* (MDAgents, ColaCare, MedAgents) frequentemente **não conseguem extrair conhecimento especializado real** do papel atribuído (ex.: "internista" vs "cirurgião"); há fragilidade técnica (erros de parsing JSON, loops, chamadas de ferramenta irracionais) e alta sensibilidade ao prompt.

## Quando multiagente ajuda (Discussão dos autores)
Em tarefas com **alta decomponibilidade**, papéis explícitos, refinamento iterativo e **integração com ferramentas externas**. Não ajuda quando um modelo monolítico já é forte ou quando modelos especializados dominam.

## Limitações declaradas
- Rankings dependem dos LLMs base e podem mudar.
- Escopo não cobre todo o espectro clínico.
- Falta avaliação humana qualitativa mais profunda (utilidade clínica, confiança).

## Trabalhos futuros sugeridos pelos autores (importante para mim)
- "Exploring **hybrid architectures that synergize the feature extraction strengths of conventional models with the complex reasoning capabilities of LLM-based agents**" (Seção 5, Future work).
- Investigar robustez, interpretabilidade, justiça, viés e privacidade.

## Leitura crítica
- Amostras de 200 itens por tarefa → intervalos de confiança largos em algumas comparações.
- A "predição com prontuário" pelos multiagentes é feita **com o LLM prevendo o desfecho a partir do texto** — não há arquitetura híbrida em que o modelo convencional prevê e o LLM explica. É exatamente o que os autores recomendam como trabalho futuro.
- Não avalia fidelidade de explicações.

## Relação com o meu TCC
- **Principal argumento de posicionamento:** a própria literatura de ponta diz que (a) modelos convencionais devem fazer a predição com dados estruturados e (b) o caminho promissor é o **híbrido** convencional + agentes LLM. Minha arquitetura segue essa recomendação.
- **Justifica H2 como pergunta aberta:** multiagente não é presumidamente melhor; preciso de baseline de LLM único com ferramenta (configuração 2).
- **Design:** definir agentes por **função verificável** (calcular, explicar, verificar), não por *persona* de especialidade médica — o Apêndice H.4 mostra que papéis de especialidade rendem pouco.
- **Métrica de custo:** reportar custo (tokens/latência) por configuração, como no Apêndice D.
- **Robustez técnica:** esperar e medir falhas de parsing/formato (saída estruturada com esquema validado).

## Dados citáveis
- [C1] Multiagente não supera consistentemente LLMs únicos avançados nem métodos convencionais especializados; ganhos aparecem sobretudo na completude de fluxos de trabalho com ferramentas (Abstract; Seção 5).
- [C2] Na predição de mortalidade no MIMIC-IV, ColaCare obteve AUROC 82,91 vs 76,86 do seu LLM base (DeepSeek-V3), mas abaixo do GPT-4o (85,99) e do AdaCare convencional (94,28) (Tabela 5).
- [C3] Os autores atribuem as melhorias modestas dos multiagentes ao LLM base, e não a uma vantagem transformadora da estratégia multiagente (Seção 4.3).
- [C4] Os autores recomendam explorar arquiteturas híbridas que combinem modelos convencionais com o raciocínio de agentes LLM (Seção 5, Future work).
- [C5] Frameworks baseados em role-playing frequentemente não conseguem extrair conhecimento específico do papel atribuído (Apêndice H.4).
- [C6] Multiagentes apresentaram fragilidade técnica: erros de parsing JSON, loops e chamadas de ferramenta irracionais (Apêndice H.4).
- [C7] Frameworks multiagente custaram, em geral, várias vezes mais que um LLM único zero-shot (Apêndice D, Tabela 13).
