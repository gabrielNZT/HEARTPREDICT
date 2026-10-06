---
chave: cemri2025mast
titulo: Why Do Multi-Agent LLM Systems Fail?
autores: [Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, Joseph E. Gonzalez, Ion Stoica]
ano: 2025
veiculo: Advances in Neural Information Processing Systems 38 (NeurIPS 2025) - Datasets and Benchmarks Track
tipo_bib: inproceedings
doi: 10.48550/arXiv.2503.13657
url: https://arxiv.org/abs/2503.13657
temas: [multiagentes-llm, falhas-e-verificacao, engenharia-de-sistemas]
leitura: completa
lido_em: 2026-09-29
relevancia: central
---

# MAST — Why Do Multi-Agent LLM Systems Fail? (Cemri et al., 2025)

## Referência
CEMRI, M. et al. Why Do Multi-Agent LLM Systems Fail? In: **NeurIPS 2025, Datasets and Benchmarks Track**. arXiv:2503.13657 (v3, 26 out. 2025, lida). Dados e código: https://github.com/multi-agent-systems-failure-taxonomy/MAST.

> Nota: há versões do resumo com números diferentes (v1 citava "MAD, 1000+ traces"; a v3 fala em "MAST-Data, 1642 traces"). **Cite pela v3**, que é a lida.

## Problema
Sistemas multiagente (MAS) com LLM trazem ganhos mínimos sobre agente único ou baselines simples (best-of-N). Não havia entendimento sistemático de **por que** falham.

## Método
- **Grounded Theory** sobre 150 traces (média >15 mil linhas cada) de 5 frameworks (HyperAgent, AppWorld, AG2, ChatDev, MetaGPT), 6 anotadores especialistas.
- Refinamento da taxonomia por **concordância entre anotadores** (3 rodadas, Cohen κ = 0,88; validação fora do domínio κ = 0,79).
- **LLM-como-juiz** (o1 com few-shot) para escalar a anotação: acurácia 0,94, κ = 0,77 vs humanos.
- **MAST-Data:** 1.642 traces anotados de 7 frameworks e 4 famílias de LLM (GPT-4, Claude 3, Qwen2.5, CodeLlama); tarefas de programação, matemática e agentes gerais.
- Estudos de intervenção (ChatDev, AG2) alterando prompts e topologia.

## Resultados
- Taxa de falha de **41% a 86,7%** nos 7 MAS de código aberto (Seção 1).
- **14 modos de falha em 3 categorias:**
  - **FC1 – Problemas de projeto do sistema:** desobedecer especificação da tarefa (11,8%), desobedecer papel (1,5%), repetição de passos (15,7%), perda de histórico (2,8%), não reconhecer término (12,4%).
  - **FC2 – Desalinhamento entre agentes:** reset de conversa (2,2%), **não pedir esclarecimento (6,8%)**, desvio da tarefa (7,4%), reter informação (0,85%), ignorar outro agente (1,9%), **descompasso raciocínio-ação (13,2%)**.
  - **FC3 – Verificação da tarefa:** término prematuro (6,2%), **verificação ausente ou incompleta (8,2%)**, **verificação incorreta (9,1%)**.
- Sistemas com **verificador explícito** (MetaGPT, ChatDev) têm menos falhas no total, mas "a presença de um verificador não é bala de prata": muitos verificadores fazem **checagens superficiais** (ex.: o código compila) (Seção 4, FC3).
- **Insight 3:** "Multi-level verification is needed" — checar correção de baixo nível **e** objetivos de alto nível. Adicionar verificação de objetivo de alto nível ao ChatDev deu **+15,6%** de sucesso.
- Ajustar só a especificação de papéis no ChatDev deu +9,4% (mesmo LLM).
- **Seção 5.3:** melhorar o modelo base não basta; falhas vêm de **projeto organizacional** do sistema.
- **Apêndice G:** estratégias estruturais recomendadas: verificação forte, **protocolos de comunicação padronizados** (mensagens estruturadas em vez de texto livre), **quantificação de confiança**, gestão de estado. Verificação por domínio: "reasoning benefits from **symbolic validation**".

## Limitações declaradas
- A taxonomia não é exaustiva.
- Domínios cobertos: programação, matemática, agentes gerais — **não inclui medicina**.
- Anotação em larga escala feita por LLM (κ 0,77, não perfeito).

## Leitura crítica
- Forte como referência de **engenharia de sistemas multiagente**; é um paper de Berkeley (grupo de Stoica/Zaharia/Gonzalez) — credibilidade alta para a banca de Engenharia de Computação.
- Nenhum modo de falha é específico de saúde; eu preciso **transpor** a taxonomia para o meu domínio.

## Relação com o meu TCC
- **Justifica o agente verificador** e, mais importante, **o tipo de verificador**: não superficial, **em múltiplos níveis** (baixo nível: números e sinais batem? alto nível: a explicação responde ao objetivo clínico?).
- **Justifica verificação simbólica/determinística** (Apêndice G) no meu verificador híbrido.
- **Justifica mensagens estruturadas** entre agentes (JSON com esquema) em vez de texto livre — alinhado com FIPA-ACL do JADE, que já é um protocolo padronizado. **Esse é um argumento legítimo para manter o JADE.**
- **Modo FM-2.2 (não pedir esclarecimento)** conecta com o achado do AgentMD sobre valores ausentes: o sistema deve **recusar ou pedir o dado**, não supor.
- A taxonomia pode ser usada para **classificar as falhas** observadas nos meus experimentos (seção de discussão).

## Dados citáveis
- [C1] Sete MAS de código aberto apresentaram taxas de falha entre 41% e 86,7% (Seção 1; Apêndice B).
- [C2] A taxonomia MAST tem 14 modos de falha em 3 categorias, com concordância entre anotadores κ = 0,88 (Abstract; Seção 3.2).
- [C3] Verificação ausente/incompleta (8,2%) e verificação incorreta (9,1%) estão entre os modos de falha da categoria de verificação (Seção 4, FC3).
- [C4] Muitos verificadores existentes fazem apenas checagens superficiais; os autores defendem verificação em múltiplos níveis (Seção 4, Insight 3).
- [C5] Adicionar uma etapa de verificação do objetivo de alto nível ao ChatDev aumentou o sucesso em 15,6% (Seção 4; Apêndice H).
- [C6] Os autores argumentam que melhorar o LLM base não basta, pois muitas falhas vêm do projeto organizacional do sistema (Seção 5.3).
- [C7] Entre as estratégias estruturais, os autores citam protocolos de comunicação padronizados, quantificação de confiança e validação simbólica para raciocínio (Apêndice G).
