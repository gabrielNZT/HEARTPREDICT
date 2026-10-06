---
titulo: Justificativa do uso do JADE
status: rascunho
atualizado: 2026-09-29
resumo: O que o JADE/FIPA agrega de concreto ao projeto (protocolo de proposta/aceitação para verificação, recusa tipada, rastro auditável, ablação por composição), com fundamento, custos e respostas à banca.
---

# Por que JADE? O que ele agrega ao projeto

## 1. O problema da justificativa anterior
"O código já existia" e "o FIPA é um padrão" **não bastam**: nenhum dos dois mostra ganho para a pergunta de pesquisa. Além disso, no código atual os agentes trocam mensagens de forma *ad hoc* (filtros por remetente, sem `conversation-id`, sem protocolo), ou seja, **o JADE ainda não está sendo usado naquilo em que é bom**.

A justificativa passa a ser: **usar o JADE para formalizar a interação entre os agentes com protocolos FIPA e atos de fala, tornando a verificação explícita, terminável e auditável.** Isso ataca diretamente modos de falha documentados em sistemas multiagente com LLM.

## 2. O que o JADE agrega (4 contribuições concretas)

### 2.1 O ciclo Explicador ↔ Verificador vira um protocolo formal (FIPA-Propose)
| Passo | Ato de fala (performativa) | Significado |
|---|---|---|
| 1 | Explicador → Verificador: **PROPOSE** (explicação) | "Proponho entregar esta explicação ao usuário" |
| 2a | Verificador → Explicador: **ACCEPT-PROPOSAL** | Explicação fiel; pode ser entregue |
| 2b | Verificador → Explicador: **REJECT-PROPOSAL** (lista estruturada de violações) | "Não; corrija: sinal do HDL invertido; IMC citado como causa" |
| 3 | Nova PROPOSE na **mesma conversa** | Nova rodada de correção |
| fim | Após N rejeições: **FAILURE** / bloqueio | Término explícito, sem laço infinito |

- **Fundamento:** o protocolo está especificado no padrão FIPA SC00036 ([fipa2002propose](../01-literatura/fichamentos/fipa2002propose.md)) e já implementado no JADE (`jade.proto.ProposeInitiator` / `ProposeResponder`).
- **O que isso resolve:** o MAST ([cemri2025mast](../01-literatura/fichamentos/cemri2025mast.md)) documenta falhas como **não reconhecer a condição de término** (12,4%), **repetição de passos** (15,7%), **perda de histórico** (2,8%), **término prematuro** (6,2%) e **verificação ausente ou incorreta** (8,2% e 9,1%). Um protocolo com estados finitos, término explícito e `conversation-id` ataca essas falhas **por construção**, e o MAST recomenda protocolos de comunicação padronizados como estratégia estrutural (Apêndice G).
- **Ganho conceitual:** a decisão do verificador deixa de ser texto livre e vira um **ato de fala tipado** (aceita/rejeita) com conteúdo estruturado. Isso é verificável por máquina e é o que o feedback externo precisa ser para a autocorreção funcionar (CRITIC; Huang et al. 2024).

### 2.2 Recusa tipada para dados inválidos (FIPA-Request)
O Agente de Entrada e o Classificador usam o protocolo FIPA-Request (`AchieveREInitiator` / `AchieveREResponder`), que prevê **AGREE / REFUSE / FAILURE / INFORM**.
- Dado ausente ou fora das faixas do PREVENT → **REFUSE** com o motivo, em vez de supor um valor.
- **Fundamento:** suposições sobre valores ausentes foram a principal causa de erro em notas reais no AgentMD ([jin2025agentmd](../01-literatura/fichamentos/jin2025agentmd.md) [C4]); Zhu 2026 recomenda expor a ausência de dados; o MAST lista "não pedir esclarecimento" como modo de falha (FM-2.2, 6,8%).

### 2.3 Rastro auditável como instrumento de pesquisa
Toda mensagem ACL carrega performativa, remetente, destinatário, `conversation-id` e conteúdo. Registradas, essas mensagens formam um **rastro completo de cada caso**:
- **Métricas do verificador:** rodadas até a aceitação, taxa de rejeição por tipo de violação, taxa de bloqueio, custo por caso.
- **Análise de falhas no estilo MAST**, que trabalha justamente sobre rastros de execução.
- **Demonstração na defesa:** o *Sniffer* do JADE mostra graficamente a troca de mensagens de um caso.

Isso atende à exigência de auditabilidade do AI Act (Art. 13) e do PL 2338/2023 citada na justificativa do TCC.

### 2.4 Ablação por composição de agentes
As três configurações do experimento são **sociedades de agentes diferentes montadas com o mesmo código**:
| Configuração | Agentes ativos |
|---|---|
| C-isolado | Entrada + Explicador (sem Classificador nem Verificador) |
| C-ferramenta | Entrada + Classificador + Explicador |
| C-verificador | Entrada + Classificador + Explicador + Verificador |

Como o código de cada agente é idêntico entre as configurações, **a diferença entre C-ferramenta e C-verificador é só a presença do Verificador**. Isso reforça a **validade interna** da comparação de H2. O registro de serviços do JADE (Directory Facilitator) permite montar cada configuração de forma declarativa. *(Honestidade: isso também pode ser feito sem JADE, com parâmetros; o JADE apenas torna natural.)*

## 3. Posicionamento na literatura
- **Botti (2025)** critica a onda de "Agentic AI" por reinventar conceitos de agentes e SMA e defende incorporar padrões de plataformas, linguagens de comunicação e coordenação aos agentes com LLM ([botti2025reinventing](../01-literatura/fichamentos/botti2025reinventing.md)). **O TCC faz exatamente isso:** agentes com LLM sobre uma plataforma e uma linguagem de comunicação padronizadas.
- **Petrova et al. (2025)** descrevem a passagem da semântica "na plataforma" (SMA) para a semântica "no modelo" (LLMs) ([petrova2025webofagents](../01-literatura/fichamentos/petrova2025webofagents.md)). No TCC, as duas coexistem: **a semântica da interação fica no protocolo FIPA; a semântica do conteúdo fica no LLM.**
- **Wooldridge & Jennings (1995)**: dos quatro atributos de agente, o sistema exibe claramente **habilidade social** (ACL/protocolos) e **reatividade**; o Verificador tem **autonomia** para aceitar ou rejeitar. A proatividade é limitada, o que deve ser declarado ([wooldridge1995agents](../01-literatura/fichamentos/wooldridge1995agents.md)).

## 4. O que o JADE **não** agrega (declarar)
- Não melhora a qualidade do LLM nem a fidelidade por si só; o que melhora a fidelidade é o **Verificador**. O JADE dá **rigor de interação, término garantido, rastreabilidade e controle experimental**.
- Não é a tecnologia da moda: a indústria migrou para A2A/MCP, mais leves e nativos da web ([ehtesham2025protocols](../01-literatura/fichamentos/ehtesham2025protocols.md); Petrova 2025).
- Custos: Java ↔ Python via HTTP; plataforma madura, mas pouco atualizada (API atual 4.6.0).

## 5. Respostas prováveis à banca
- **"Por que não A2A ou MCP?"** O MCP liga agentes a **ferramentas**; o A2A delega **tarefas** entre agentes. O TCC precisa de uma **negociação com semântica explícita de aceitar/rejeitar e término definido**, que o FIPA-Propose especifica e o JADE implementa pronto. Trocar por A2A é possível e fica como trabalho futuro.
- **"Isso é multiagente de verdade?"** É uma arquitetura orientada a agentes com interação protocolada. A interação central (proposta/aceitação/rejeição entre Explicador e Verificador) é multiagente no sentido de Wooldridge & Jennings; o restante é um fluxo com responsabilidades separadas. O texto do TCC não afirma autonomia além disso.
- **"Um laço em Python não faria o mesmo?"** Faria o laço; não traria de graça o protocolo padronizado com estados e término, a recusa tipada, o `conversation-id` e o rastro de mensagens. Reimplementar isso seria "reinventar a roda" (Botti 2025).

## 6. Consequências no código
1. Explicador ↔ Julgador/Verificador: trocar a troca *ad hoc* por `ProposeInitiator` / `ProposeResponder`.
2. Gerenciador → Classificador: `AchieveREInitiator` / `AchieveREResponder`, com REFUSE para entrada inválida.
3. `conversation-id` = identificador do caso em todas as mensagens.
4. Registro estruturado (JSON Lines) de toda mensagem enviada e recebida.
5. Parâmetro de configuração que define quais agentes sobem (as três configurações).

## 7. Fontes
[P] fipa2002propose · API JADE 4.6.0 (`ProposeInitiator`, `AchieveREInitiator`) · cemri2025mast · jin2025agentmd · zhu2026agenticexpl · Huang et al. 2024 · CRITIC 2024
[S] botti2025reinventing · petrova2025webofagents · ehtesham2025protocols · wooldridge1995agents · jennings2000abse (lidos pelo resumo)
