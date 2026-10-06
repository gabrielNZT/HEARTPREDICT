---
titulo: Proposta do TCC (documento-mestre)
status: rascunho
atualizado: 2026-09-29
resumo: Tese, pergunta de pesquisa, hipóteses, contribuições, arquitetura, protocolo experimental e escopo. Fonte única da verdade do projeto.
---

# Proposta do TCC — documento-mestre

> Este é o documento de referência do projeto. Toda decisão que alterar algo aqui deve ser registrada em [decisoes.md](decisoes.md).

## 1. Título provisório
**Verificação de fidelidade em explicações geradas por LLM para estratificação de risco cardiovascular: uma arquitetura multiagente híbrida e sua avaliação empírica**

## 2. Tese (uma frase)
LLMs já são usados para interpretar risco clínico, mas erram cálculos e produzem explicações nem sempre fiéis ao modelo; este trabalho propõe uma arquitetura em que o cálculo fica com ferramentas validadas e um agente verificador confere a fidelidade da explicação, e mede se isso reduz erros em comparação a alternativas mais simples.

## 3. Problema
- LLMs isolados erram cálculos clínicos, sobretudo escores baseados em regressão ([khandekar2024medcalc](../01-literatura/fichamentos/khandekar2024medcalc.md), [roeschl2026pipeline](../01-literatura/fichamentos/roeschl2026pipeline.md)).
- Usar ferramentas resolve grande parte do **número** ([jin2025agentmd](../01-literatura/fichamentos/jin2025agentmd.md), [roeschl2026pipeline](../01-literatura/fichamentos/roeschl2026pipeline.md)), mas **não garante que a explicação seja fiel** ao que o modelo fez ([lee2025shapllm](../01-literatura/fichamentos/lee2025shapllm.md), [zhu2026agenticexpl](../01-literatura/fichamentos/zhu2026agenticexpl.md)).
- Humanos não são filtro confiável para erros de IA, mesmo com explicação ([jabbour2023jama](../01-literatura/fichamentos/jabbour2023jama.md) — por analogia).
- Multiagentes não são automaticamente melhores ([zhu2025medagentboard](../01-literatura/fichamentos/zhu2025medagentboard.md), [cemri2025mast](../01-literatura/fichamentos/cemri2025mast.md)).

## 4. Pergunta de pesquisa
> Um agente verificador de fidelidade — determinístico para números e polaridade, com LLM para coerência semântica — reduz explicações infiéis sobre o risco cardiovascular, em comparação com um LLM isolado e com um LLM que usa a ferramenta de cálculo sem verificação?

## 5. Hipóteses
- **H1 (verificação de sanidade):** LLM + ferramenta (PREVENT determinístico) tem maior concordância de categoria de risco com a diretriz SBC 2025 do que o LLM isolado.
- **H2 (contribuição central):** a configuração com verificador tem **maior fidelidade** (polaridade, números e top-k SHAP) e **menos afirmações não sustentadas** do que LLM + ferramenta sem verificador.
- **H3 (equidade, D017):** como o PREVENT não usa raça/etnia, a configuração com verificador terá menos explicações que atribuem o risco a raça/etnia do que as configurações sem verificador. Diferenças por sexo são analisadas de forma exploratória (taxas de fidelidade por grupo).

Todas as hipóteses podem ser refutadas; um resultado negativo em H2 também é contribuição.

## 6. Contribuições
- **C1 – Arquitetura:** padrão com separação entre cálculo (ferramenta determinística + ML) e linguagem (LLM), e um verificador híbrido multinível.
- **C2 – Protocolo e métricas de fidelidade:** top-k SHAP (comparável com Lee 2025) + **polaridade por variável** + **exatidão numérica** + **afirmações não sustentadas** + consistência entre execuções + viés contrafactual.
- **C3 – Evidência empírica:** comparação controlada de 3 configurações × ≥2 LLMs.
- **C4 – Artefatos abertos:** código, vinhetas alinhadas à SBC 2025, logs de execução. (O idioma português não é apresentado como contribuição — D018.)

## 7. Enquadramento metodológico
Design Science Research ([hevner2004dsr](../01-literatura/fichamentos/hevner2004dsr.md)): artefato + avaliação rigorosa. Relato da parte de ML segundo TRIPOD+AI ([collins2024tripodai](../01-literatura/fichamentos/collins2024tripodai.md)), com calibração ([vancalster2019calibration](../01-literatura/fichamentos/vancalster2019calibration.md)) e auditoria de leakage ([kapoor2023leakage](../01-literatura/fichamentos/kapoor2023leakage.md)).

## 8. Arquitetura (alvo)

```
Paciente (dados estruturados)
   │
   ▼
[Agente de Entrada] ── valida componentes um a um; dado ausente → pede/recusa (não supõe)
   │
   ▼
[Agente Calculador] ── PREVENT-ASCVD 10 anos (determinístico) + categoria SBC (motor de regras) + atribuição Shapley exata
   │   saída estruturada: {risco_%, categoria_SBC, shap:{var: valor}}
   ▼
[Agente Explicador (LLM)] ── recebe número, categoria e SHAP; gera explicação em PT-BR (JSON com afirmações)
   │
   ▼
[Agente Verificador] ── nível 1 (determinístico): números citados = ferramenta? sinal de cada fator = sinal SHAP? categoria = SBC?
   │                    nível 2 (LLM): coerência semântica, recomendações sem base
   │   reprova → devolve ao Explicador com o erro apontado (máx. N ciclos) → se persistir, bloqueia
   ▼
(Entrega ao usuário via gateway/frontend — o AgenteNotificador foi removido, D019)
```
- Comunicação entre agentes: FIPA-ACL (JADE) com **conteúdo JSON validado por esquema**; Explicador ↔ Verificador via **FIPA-Propose** e Entrada → Classificador via **FIPA-Request** (D021).
- Mapeamento para o código atual: `AgenteGerenciadorPacientes` → Entrada; `AgenteClassificador` → Calculador; `AgenteExplicador` → Explicador; `AgenteJulgador` → **Verificador**; `AgenteNotificador` → removido (D019).
- Escopo núcleo × extensões: ver [escopo-e-arquitetura](escopo-e-arquitetura.md) (D020).

## 9. Protocolo experimental (rascunho)

### 9.1 Configurações
1. **C-isolado:** LLM recebe dados do paciente, calcula risco e explica sozinho.
2. **C-ferramenta:** LLM recebe número + categoria + SHAP e explica (sem verificador).
3. **C-verificador:** igual à 2 + verificador com ciclo de correção.

### 9.2 Dados
- **Vinhetas** geradas a partir de perfis de pacientes com variáveis completas do PREVENT (idade, sexo, colesterol total, HDL, PAS, uso de anti-hipertensivo, diabetes, tabagismo, TFGe, estatina, IMC opcional). Precedente: RiskQA ([jin2025agentmd](../01-literatura/fichamentos/jin2025agentmd.md) [C6]).
- Fonte dos perfis (D013): **NHANES** (perfis reais, precedente em Diao et al., JAMA 2024) + **casos sintéticos dirigidos** (contrafactuais, fronteiras, armadilhas de fidelidade). Ver [decisoes.md](decisoes.md).
- **Estratificação** por categoria de risco (baixo, intermediário, alto), incluindo muitos casos de **baixo risco** (onde LLMs são menos consistentes — [lee2025shapllm](../01-literatura/fichamentos/lee2025shapllm.md) [C6]).
- Pares contrafactuais para H3 (mesmo paciente, só sexo ou raça/etnia alterados).
- Escopo inicial (D011): 30–79 anos, sem DCVA, sem aterosclerose subclínica, sem diabetes, LDL-c < 160; casos fora disso como testes dirigidos.
- Valores de entrada dentro das faixas de derivação do PREVENT (PAS 90–200, CT 130–320, HDL 20–100 mg/dL).
- `cardio_train` (Kaggle) opcional, apenas para um segundo modelo (XGBoost), com limitação declarada (transversal, sem colesterol numérico nem TFGe).

### 9.3 Métricas
Definições operacionais completas: [03-metodologia/metricas-fidelidade.md](../03-metodologia/metricas-fidelidade.md).

| Métrica | Definição | Hipótese |
|---|---|---|
| Concordância de categoria | categoria citada no texto vs categoria SBC calculada | H1 |
| Fidelidade top-k | presença das k variáveis de maior atribuição (Shapley exato no PREVENT; como em Lee 2025) | H2 |
| **Variáveis fora do modelo** | % de explicações que atribuem o risco a variáveis que o modelo não usa (ex.: IMC no PREVENT-ASCVD) | H2 |
| **Polaridade** | % de fatores citados com direção igual ao sinal do SHAP | H2 |
| **Exatidão numérica** | % de números citados que batem com a ferramenta (tolerância definida) | H2 |
| **Afirmações não sustentadas** | afirmações sem suporte nos dados/ferramenta | H2 |
| Consistência | entropia/variação entre N repetições | H2 |
| Variação contrafactual | diferença de saída entre pares que só diferem em atributo demográfico | H3 |
| Custo | tokens, chamadas e latência por paciente | todas |
| Desempenho do verificador | falsos positivos/negativos contra anotação manual de uma amostra | validação |

### 9.4 Controles de reprodutibilidade
Versão fixa do modelo, temperatura definida, N repetições por caso, sementes registradas, prompts versionados, logs completos. **≥2 LLMs**: um fechado (ex.: Gemini, já usado no projeto) e um aberto rodando localmente.

### 9.5 Análise estatística (a detalhar)
Comparação pareada entre configurações (mesmos casos): testes para proporções pareadas (ex.: McNemar) e intervalos por bootstrap. Definir o tamanho da amostra antes de rodar.

## 10. Escopo
**Dentro:** risco cardiovascular preventivo em 10 anos (PREVENT), explicação em PT-BR, avaliação *in silico*.
**Fora (trabalhos futuros):** ECG em tempo real, TimescaleDB, MQTT de sensores, validação clínica prospectiva, dispositivo médico.

## 11. Limitações a declarar
Sem validação clínica; vinhetas sintéticas ou derivadas; PREVENT desenvolvido na população dos EUA; dependência dos LLMs testados; métricas automáticas como proxy.
