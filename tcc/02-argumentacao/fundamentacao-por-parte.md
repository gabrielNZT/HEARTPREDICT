---
titulo: Fundamentação por parte do projeto e brechas
status: vigente
atualizado: 2026-09-29
resumo: Cada componente do projeto com seu fundamento (primário, secundário ou proposta própria) e as brechas que a banca pode explorar, com correções.
---

# Fundamentação por parte do projeto

Legenda do nível de fundamento:
- **[P] Primário:** vem diretamente de artigo ou diretriz lido na íntegra.
- **[S] Secundário:** vem de fonte secundária, resumo ou analogia com outro domínio.
- **[A] Autoral:** decisão minha de projeto; precisa ser justificada no texto ou testada.

## 1. Cálculo do risco (PREVENT)
| Elemento | Nível | Fonte |
|---|---|---|
| Usar o PREVENT | [P] | SBC 2025, seção 4.2 (FORTE/ALTA) |
| Usar o modelo de DCVA em 10 anos | [P] | SBC 2025, seção 4.2; PREVENT, Methods |
| Variáveis e valores de centralização (idade 55, não-HDL 3,5, HDL 1,3, PAS 130) | [P] | PREVENT, nota da Tabela 2 |
| Existência da forma simplificada (R² ≥ 0,99) | [P] | PREVENT, Results |
| Forma logística `exp(L)/(1+exp(L))` e lista de termos | [S] | Código do pacote `preventr` (CRAN), que implementa a Tabela S12 |
| Coeficientes (β) | **pendente** | Tabela S12 não obtida |
| Caso de teste (3,6% / 6,0%) | [P] | PREVENT, Results |

**Brecha:** até baixar a Tabela S12, a implementação depende de fonte secundária. **Correção:** obter a S12 e conferir contra `preventr` e contra a calculadora da AHA.

## 2. Classificação em categorias (SBC)
| Elemento | Nível | Fonte |
|---|---|---|
| Cortes 5% e 20% | [P] | Tabela 4.1 |
| Domínio do escore (sem DCV, sem DM, LDL < 160) | [P] | Seção 4.1 |
| LDL 160 inclusive; meta < 40 no extremo | [P] | Texto da seção 4.1; Tabela 5.1 (PT e EN) |
| Agravante sobe exatamente uma categoria | [A] | Tabela 4.1 sugere regra; seção 4.3 fala em julgamento |

**Brecha:** a regra dos agravantes é interpretação. **Correção:** análise de sensibilidade (com e sem promoção por agravante) — D010.

## 3. Atribuição de referência (Shapley exato)
| Elemento | Nível | Fonte |
|---|---|---|
| Valores de Shapley e SHAP | [P] | Shapley (1953); Lundberg & Lee, NeurIPS 2017 (a fichar) |
| Uso de modelos com atribuição conhecida como gabarito de fidelidade | [S] | Benchmarks sintéticos de XAI (Liu et al., 2021, arXiv:2106.12543; M4, NeurIPS 2023; OpenXAI, NeurIPS 2022) — a fichar |
| Referência = valores de centralização do PREVENT | [A] | Escolha minha |
| Escala = log-odds | [A] | Escolha minha |

**Brechas:**
- **O valor de Shapley depende da referência escolhida** (Sundararajan & Najmi, ICML 2020 — a fichar). Um HDL de 45 mg/dL "aumenta o risco" em relação à referência de 50 mg/dL, mas pode ser clinicamente "normal". A banca pode perguntar: "fiel a quê?".
- A escala (log-odds × probabilidade) e a divisão das interações com a idade também afetam a atribuição.

**Correção:** (1) justificar a referência como o "paciente de referência" definido pelos próprios autores do modelo; (2) repetir com a média da amostra NHANES como referência e mostrar se o ranking e os sinais mudam; (3) definir fidelidade como "fiel à atribuição do modelo **sob a referência declarada**", e declarar isso como limitação.

## 4. Arquitetura (separar cálculo de linguagem)
| Elemento | Nível | Fonte |
|---|---|---|
| LLM não calcula; ferramenta determinística calcula | [P] | Roeschl 2026; AgentMD; MedCalc-Bench |
| Híbrido ML convencional + agentes LLM | [P] | MedAgentBoard (trabalho futuro recomendado); ColaCare |
| Agentes por função, não por persona médica | [P] | MedAgentBoard, Apêndice H.4 |
| Mensagens estruturadas entre agentes | [P] | MAST, Apêndice G |
| JADE/FIPA-ACL como forma de padronização | [S] | Analogia: o MAST cita MCP e A2A, não FIPA |

**Brecha:** "por que JADE e não um framework atual?". **Correção:** apresentar o JADE como plataforma que já implementa um padrão de comunicação (FIPA), sem afirmar que o MAST o recomenda especificamente; deixar claro que a contribuição independe da plataforma.

## 5. Verificador e ciclo de correção
| Elemento | Nível | Fonte |
|---|---|---|
| Verificação multinível | [P] | MAST, Insight 3 |
| Números e lógica checados por código; LLM só para variação de linguagem | [S] | PROVE (preprint, outro domínio) |
| **Autocorreção sem feedback externo não funciona** | [P] | Huang et al., ICLR 2024 (a fichar) |
| **Autocorreção com feedback de ferramenta funciona** | [P] | CRITIC, Gou et al., ICLR 2024 (a fichar) |
| Número máximo de ciclos, bloqueio | [A] | Escolha minha |

**Ponto forte:** o ciclo Explicador → Verificador → Explicador usa feedback **externo e específico** (ex.: "o sinal do HDL está invertido"), que é exatamente o cenário em que a literatura mostra que a correção funciona.

## 6. Dados
| Elemento | Nível | Fonte |
|---|---|---|
| NHANES para calcular o PREVENT | [P] | Diao et al., JAMA 2024; Anderson et al., JAMA Intern Med 2024 (resumos) |
| Casos sintéticos a partir de parâmetros controlados | [P] | AgentMD (RiskQA); MedCalc-Bench |
| Estratificar por categoria, incluindo muitos casos de baixo risco | [P] | Lee 2025, Tabela 1 (menor consistência em verdadeiros negativos) |

**Brecha:** o NHANES não tem todos os agravantes (ex.: Lp(a)) e é da população dos EUA. **Correção:** agravantes via casos sintéticos; declarar a limitação populacional.

## 7. Desenho experimental
| Elemento | Nível | Fonte |
|---|---|---|
| Três configurações com ablação | [P] | Zhu 2026 (isolado × agêntico); ablação do ColaCare |
| ≥ 2 LLMs, versão e temperatura fixas | [P] | Roeschl 2026; AgentMD; limitações de Lee 2025 |
| Métrica top-k | [P] | Lee 2025 |
| Jaccard e direção | [P] | Zhu 2026 |
| Polaridade por variável, exatidão numérica, variáveis fora do modelo | [A] | Proposta minha, inspirada nos erros relatados por Lee 2025 e na distinção de Jacovi & Goldberg |
| Teste pareado (McNemar), bootstrap | [P] | Estatística padrão; bootstrap usado em Zhu 2026 e MedAgentBoard |
| Concordância entre anotadores (κ) | [P] | MAST; revisão de LLM-como-juiz em saúde |

## 8. Viés (H3)
| Elemento | Nível | Fonte |
|---|---|---|
| Prompts pareados por atributo demográfico | [S] | Chan & Kwek 2025 (resumo) |
| Justiça contrafactual | [P] | Kusner et al., NeurIPS 2017 (a fichar) |

---

# Brechas críticas (a banca pode explorar)

## B1 — Circularidade entre verificador e métrica  ⚠️ a mais grave
Se o verificador e a métrica de avaliação usarem **o mesmo checador**, a configuração 3 vence **por construção** (ela é otimizada para passar naquele teste — lei de Goodhart).
**Correção:**
- a métrica final é calculada por um **procedimento independente**: anotação humana de uma amostra (2 anotadores, κ) + extrator diferente do usado pelo verificador;
- medir também **dimensões que o verificador não checa** (ex.: omissões, legibilidade);
- reportar separadamente "passou no verificador" e "correto segundo avaliação independente".

## B2 — Baseline fraco (espantalho)
Um LLM sem acesso à equação do PREVENT obviamente vai errar; comparar só com isso infla o ganho (Wolfrath et al., 2024).
**Correção:** a configuração isolada recebe a **descrição da equação** (como no one-shot do MedCalc-Bench) ou um interpretador de código. E H1 é apresentada como **replicação** de Roeschl e AgentMD, não como contribuição.

## B3 — O contrafactual de sexo é inválido
O PREVENT é **específico por sexo**: trocar o sexo muda legitimamente o número. Uma diferença na explicação pode ser correta.
**Correção:** teste de invariância só para **raça/etnia** (o PREVENT não usa raça, então qualquer mudança vem do LLM). Para sexo, comparar **taxas de fidelidade** entre grupos, e não a igualdade das saídas.

## B4 — Referência da atribuição
Ver seção 3 acima.

## B5 — Fiel, mas inútil
Uma explicação pode ser 100% fiel e incompreensível ou clinicamente irrelevante.
**Correção:** incluir uma medida de inteligibilidade (legibilidade em português e/ou avaliação humana opcional) e declarar que utilidade clínica está fora do escopo.

## B6 — O que exatamente é avaliado: texto ou JSON?
Se o Explicador produz afirmações estruturadas **e** um texto, é preciso avaliar o **texto final entregue ao usuário**, não só o JSON.
**Correção:** a avaliação independente (B1) incide sobre o texto final.

## B7 — Novidade em campo ativo
Trabalhos de 2026 se aproximam do tema. **Correção:** repetir a busca antes da qualificação e da defesa; manter a contribuição estreita (D003).

# Oportunidades (lacunas exploráveis)
1. **Gabarito de atribuição exato em contexto clínico real.** A maioria dos estudos (Lee, Zhu, ColaCare) mede fidelidade contra SHAP aproximado, que também pode ser infiel (AlMarri 2025). Usar um escore clínico transparente como gabarito exato é uma contribuição metodológica defensável, com precedente nos benchmarks sintéticos de XAI.
2. **Fidelidade × plausibilidade com exemplo clínico limpo.** O IMC, que não entra no PREVENT-ASCVD, permite medir quantas explicações são plausíveis mas infiéis.
3. ~~Português~~ **Corrigido (auditoria E1):** Santos et al. 2026 já avaliaram LLMs em estratificação cardiovascular com vinhetas em português. O idioma não é lacuna por si só; o que segue sem estudo encontrado é a **fidelidade de explicações** sob a **diretriz brasileira**.
4. **Análise descritiva dos erros de explicação** (rebaixada de "taxonomia" — auditoria E2) (polaridade, número, variável fora do modelo, omissão, recomendação sem base), aproveitando MedCalc-Bench (tipos A/B/C), Asgari 2025 e MAST.
