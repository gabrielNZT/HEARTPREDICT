---
titulo: Perguntas prováveis da banca
status: rascunho
atualizado: 2026-09-29
resumo: Perguntas difíceis e respostas fundamentadas, com fontes.
---

# Perguntas prováveis da banca

## "O AgentMD já não fez isso?"
Não. O AgentMD avalia se o agente escolhe e aplica a calculadora certa (o número). A verificação que ele tem é **na curadoria** das calculadoras (GPT-4 checando GPT-4), não na explicação entregue. A explicação final não é avaliada quanto à fidelidade. → [jin2025agentmd](../01-literatura/fichamentos/jin2025agentmd.md) [C5]

## "O ColaCare já entrega SHAP a agentes LLM. Qual a diferença?"
O ColaCare busca **consenso** entre agentes e **reinjeta o texto** na predição; não mede se o relatório é fiel ao SHAP. Aqui o número nunca depende do texto, e a fidelidade é medida e verificada. Além disso, a vantagem preditiva do ColaCare sobre o ensemble ficou dentro do desvio-padrão. → [wang2025colacare](../01-literatura/fichamentos/wang2025colacare.md) [C3][C4]

## "Zhu et al. (2026) já comparou LLM isolado com pipeline agêntico."
Sim, e concluiu que o pipeline **precisa** de checagens baseadas em atribuição — que é exatamente o que este trabalho implementa e avalia. Além disso, lá o LLM não recebia o SHAP, o modelo tinha 3B parâmetros e a comparação teve n=14; é preprint. → [zhu2026agenticexpl](../01-literatura/fichamentos/zhu2026agenticexpl.md) [C3][C4][C5]

## "Por que multiagente e não um LLM com ferramenta?"
É exatamente a comparação entre as configurações 2 e 3 (ablação do verificador). A literatura está dividida (MedAgentBoard, MAST, Zhu 2026), então o trabalho **testa** em vez de presumir.

## "Se o escore já dá o número, para que o LLM?"
O número não diz ao clínico ou paciente *por que* o risco é aquele nem *o que fazer*. OMS e AI Act exigem inteligibilidade. A pergunta é se o LLM pode fazer essa tradução **sem distorcer** o que o modelo calculou.

## "Quem verifica o verificador?"
O nível 1 é **determinístico** (números, polaridade, categoria): não depende de LLM. O nível 2 (LLM) é avaliado: falsos positivos e negativos do verificador são medidos contra uma amostra anotada manualmente. → [cemri2025mast](../01-literatura/fichamentos/cemri2025mast.md) [C7]; [lu2026prove](../01-literatura/fichamentos/lu2026prove.md)

## "Sem validação clínica, qual o valor?"
O escopo é a validade técnica (*in silico*). Um sistema que produz explicações infiéis não deve ser testado com pacientes; fidelidade é pré-requisito. Os próprios trabalhos de referência (AgentMD, Lee) declaram que avaliação clínica é etapa posterior.

## "Vinhetas sintéticas não invalidam o estudo?"
O RiskQA do AgentMD (Nature Communications) usa vinhetas geradas a partir de parâmetros validados. A diferença aqui é que os parâmetros vêm de perfis realistas (NHANES ou estratificação controlada) e o gabarito é calculado de forma determinística. Limitação declarada: não há ruído de documento real (Roeschl mostra que isso importa). → jin2025agentmd [C6]; roeschl2026pipeline

## "LLMs mudam o tempo todo. Dá para reproduzir?"
Versão fixa, temperatura definida, N repetições, variância reportada, ≥2 modelos (um aberto e local), prompts e logs versionados.

## "E se o verificador não melhorar nada?"
Um resultado negativo é contribuição (hipótese refutável) e dialoga com MedAgentBoard e Zhu 2026, que já mostraram ganhos inconsistentes ou negativos de decomposição.

## "Por que JADE?"
**Resposta atualizada:** ver [justificativa-jade](justificativa-jade.md) (protocolo FIPA-Propose no ciclo de verificação, recusa tipada, rastro auditável, ablação por composição).

*Resposta anterior:*
O MAST recomenda protocolos de comunicação padronizados entre agentes; FIPA-ACL é um padrão consolidado. O conteúdo das mensagens é JSON validado por esquema. A contribuição é o padrão arquitetural, independente da plataforma. → cemri2025mast [C7]

## "Por que PREVENT e não Framingham?"
É o escore recomendado pela diretriz brasileira vigente (SBC 2025). Limitação: foi desenvolvido na população dos EUA.

## "O dataset do Kaggle não é problemático?"
Sim, e isso é declarado: é transversal (presença de doença, não risco em 10 anos) e não tem colesterol numérico nem TFGe, logo não serve para o PREVENT. Resultados muito altos nele devem ser vistos com ceticismo por risco de leakage. → [kapoor2023leakage](../01-literatura/fichamentos/kapoor2023leakage.md)
