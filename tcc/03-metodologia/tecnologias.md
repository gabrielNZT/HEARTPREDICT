---
titulo: Tecnologias e nível de detalhamento no TCC
status: rascunho
atualizado: 2026-09-29
resumo: Critério para decidir quanto justificar cada escolha tecnológica (método, arquitetura, infraestrutura), tabela das tecnologias do projeto e checklist de reprodutibilidade.
---

# Tecnologias: quanto justificar cada uma

## Princípio
Uma escolha tecnológica merece justificativa **proporcional ao quanto ela pode afetar os resultados ou a validade do trabalho**. A banca espera:
- **justificativa forte** (com fonte) para o que influencia o **resultado científico**;
- **justificativa curta, por requisito**, para o que define a **arquitetura**;
- **apenas registro** (nome, versão e papel) para **infraestrutura e interface**.

Justificar pelo **requisito atendido**, nunca por popularidade ("é o framework mais usado") ou por afirmação não comprovada ("é o mais rápido").

## Nível 1 — Decisões de método (afetam o resultado) → seção própria na Metodologia
| Escolha | O que registrar | Justificativa / fonte |
|---|---|---|
| **LLMs** (Gemini + modelo aberto) | ID exato do modelo, **data das execuções**, temperatura, máximo de tokens, versão dos prompts | ≥ 2 modelos: D014. AgentMD e Roeschl registram versão e usam temperatura 0; Lee 2025 usou 10 repetições por caso |
| **Implementação do PREVENT** | Linguagem, **fonte dos coeficientes** (Tabela S12), testes contra o caso publicado e contra o pacote `preventr` | khan2024prevent; D009 |
| **Categoria SBC** | Regras implementadas e decisões de ambiguidade | D010, D011 |
| **Atribuição (Shapley exato)** | Algoritmo, referência, escala | D012; Lundberg & Lee 2017 |
| **Dados (NHANES)** | Ciclo, arquivos, **data de download**, filtros, semente da amostragem | D013; Diao 2024; Anderson 2024 |
| **Estatística** | Biblioteca e versão usadas para McNemar, κ e bootstrap | [metricas-fidelidade §8](metricas-fidelidade.md) |

## Nível 2 — Decisões de arquitetura → 1 parágrafo cada, no capítulo de Desenvolvimento
| Escolha | Justificativa por requisito |
|---|---|
| **JADE / FIPA-ACL** | Protocolos de interação com término explícito, recusa tipada, rastro auditável ([justificativa-jade](../02-argumentacao/justificativa-jade.md); D021) |
| **Java (agentes) + Python (cálculo e dados), integrados por HTTP/JSON** | O JADE é uma plataforma Java. Cálculo numérico e leitura do NHANES (arquivos XPT) têm suporte direto em Python/pandas. HTTP/JSON desacopla as linguagens e permite trocar componentes |
| **Mensagens com conteúdo JSON validado por esquema** | Reduz falhas de formato entre agentes, relatadas no MedAgentBoard (Apêndice H.4); comunicação estruturada recomendada pelo MAST (Apêndice G) |

## Nível 3 — Infraestrutura e interface → só uma tabela (nome, versão, papel)
Não precisam de literatura. Uma frase de papel basta, e pode-se dizer que "alternativas equivalentes existem; a escolha não afeta os resultados".

| Tecnologia | Versão declarada | Papel |
|---|---|---|
| Python | ≥ 3.11 (confirmar a usada) | Serviço de cálculo, gateway, experimento |
| FastAPI + uvicorn | 0.108.0 / 0.25.0 | APIs HTTP do serviço de risco e do gateway |
| Pydantic | 2.5.3 | Validação dos dados de entrada |
| httpx | 0.26.0 | Chamadas HTTP do gateway |
| Java | 17 | Execução dos agentes |
| JADE | 4.6.0 | Plataforma de agentes |
| Jackson | 2.16.1 | JSON nos agentes |
| React + Vite | 19.1 / 7.0 | Interface web (demonstração) |
| Ant Design | 5.26 | Componentes de interface |

## Checklist de reprodutibilidade (vai no apêndice ou no README)
- [ ] Dependências **apenas as usadas**, com versões fixas (`requirements.txt` enxuto; `package-lock.json` versionado)
- [ ] **Hash do commit** do código que gerou cada resultado
- [ ] ID do modelo LLM, data das execuções, temperatura, máximo de tokens, número de repetições
- [ ] Prompts versionados no repositório
- [ ] Ciclo do NHANES, data de download e semente da amostragem
- [ ] Hardware, se houver modelo rodando localmente
- [ ] Script único que reproduz o experimento a partir dos dados

## O que **não** fazer
- Capítulo descrevendo React, FastAPI ou Java como se fossem objeto de estudo.
- Comparações de desempenho entre frameworks sem medição própria.
- Listar tecnologias que o código não usa (ex.: o `requirements.txt` do gateway declarava MQTT, Redis, PostgreSQL e JWT, mas o código importa só FastAPI, Pydantic, httpx e uvicorn).
