---
titulo: Auditoria das decisões autorais
status: vigente
atualizado: 2026-09-29
resumo: Separa o que é decisão autoral defensável, o que só se sustenta se for validado no TCC e o que era especulação ou erro (e como foi tratado).
---

# Auditoria das decisões autorais

Critério: um bom projeto científico consegue justificar cada decisão. Cada item abaixo foi classificado como:

- **✅ Defensável:** há justificativa clara (literatura, diretriz, teoria ou princípio metodológico padrão).
- **🟡 Condicional:** é uma operacionalização razoável, mas só se sustenta se for **definida com precisão e validada dentro do TCC**.
- **❌ Especulação ou erro:** não tinha base suficiente; foi removido, reformulado ou corrigido.

---

## ✅ Defensáveis

| # | Decisão | Justificativa |
|---|---|---|
| A1 | O LLM não calcula; cálculo por ferramenta determinística | Roeschl 2026; AgentMD; MedCalc-Bench; **Santos 2026** (recalcular deterministicamente eleva κw de 0,69 para 0,85–0,90, em português) |
| A2 | Escopo inicial (30–79 anos, sem DCV, sem DM, LDL < 160) | Transcrição literal da SBC 2025, seção 4.1 |
| A3 | Agravante sobe uma categoria | Leitura literal da Tabela 4.1 + análise de sensibilidade (o texto da 4.3 fala em julgamento) |
| A4 | Referência da atribuição = paciente de referência do PREVENT | Todo valor de Shapley exige uma referência (Lundberg & Lee 2017); a escolhida é a definida pelos autores do modelo; sensibilidade com a média do NHANES |
| A5 | Atribuição na escala de log-odds | O PREVENT é aditivo em log-odds; é a escala em que a decomposição de Shapley é exata para um modelo linear, e é a escala padrão ao explicar modelos logísticos |
| A6 | Ciclo de correção com feedback externo e específico | Huang et al. ICLR 2024 (sem feedback externo não funciona); CRITIC ICLR 2024 (com feedback de ferramenta funciona) |
| A7 | ≥ 2 LLMs, versão e temperatura fixas | ColaCare, MedAgentBoard, Roeschl, Santos (11 LLMs); limitação declarada em Lee 2025 |
| A8 | Atualizar o modelo Gemini | **Confirmado:** o Gemini 1.5 foi desligado e as chamadas retornam 404 (página oficial de depreciações do Gemini) |
| A9 | NHANES + casos sintéticos dirigidos | Diao 2024 e Anderson 2024 (NHANES + PREVENT); RiskQA, MedCalc-Bench, Santos 2026 (vinhetas simuladas) |
| A10 | Teste de invariância apenas para raça/etnia | O PREVENT não usa raça como preditor (Khan 2024); sexo muda o risco legitimamente |
| A11 | Avaliação do verificador por procedimento **independente** | Princípio metodológico básico: não avaliar com o mesmo instrumento usado para otimizar (evita vitória por construção) |
| A12 | Baseline isolado forte (equação no prompt) | Wolfrath et al. 2024; one-shot do MedCalc-Bench |
| A13 | Anotação por 2 anotadores **não médicos**, com κ, **restrita à fidelidade** | Conferir se o texto bate com os números e sinais fornecidos não exige julgamento clínico; κ é prática padrão (MAST). Julgamento clínico (recomendação adequada?) fica fora do escopo ou exige médicos |
| A14 | McNemar e bootstrap para comparações pareadas | Estatística padrão; McNemar usado no piloto de Santos; bootstrap em Zhu 2026 e MedAgentBoard |
| A15 | Métricas top-k e Jaccard | Lee 2025 e Zhu 2026 — permitem comparar com a literatura |

---

## 🟡 Condicionais (defensáveis só se validadas no TCC)

| # | Decisão | O que falta para ficar defensável |
|---|---|---|
| C1 | *(Definição escrita em [03-metodologia/metricas-fidelidade.md](../03-metodologia/metricas-fidelidade.md), 29/09/2026 — falta validação humana)* Métricas novas: **polaridade por variável, exatidão numérica, variáveis fora do modelo, afirmações não sustentadas** | Derivam dos erros relatados por Lee 2025 (polaridade), MedCalc-Bench (numéricos) e Asgari 2025 (alucinação), mas **ainda não têm definição operacional**. Falta: definição escrita de cada uma, tolerância numérica (usar ±5%, como o MedCalc-Bench) e **validação contra anotação humana (κ)** |
| C2 | Nível 2 do verificador (LLM como juiz) | A confiabilidade de LLM-como-juiz em saúde varia (κ 0,59–0,88 na revisão de 2026). **Medir** a concordância do juiz com os anotadores; se for baixa, restringir o verificador ao nível determinístico |
| C3 | Número máximo de ciclos e bloqueio | É um parâmetro de engenharia. Definir por **estudo-piloto** e reportar o efeito (qualidade × custo) |
| C4 | Mensagens JSON com esquema entre agentes | Coerente com MAST, mas o MedAgentBoard relata erros de parsing de JSON → **medir e reportar a taxa de falhas de formato** |
| C5 | Tamanho da amostra | **Ainda não calculado.** Fazer cálculo de poder para teste pareado de proporções (McNemar) a partir de um piloto |
| C6 | Medida de inteligibilidade em português | Ainda não escolhida. **Buscar medida com validação para o português** antes de usar; sem isso, retirar a métrica |
| C7 | "Gabarito exato de atribuição" como contribuição metodológica | O conceito tem base (benchmarks sintéticos de XAI), mas a **novidade no contexto clínico não foi verificada** por busca estruturada. Apresentar como **escolha de desenho** até a busca confirmar |
| C8 | "Nenhum trabalho reúne todos os elementos" | Hoje se baseia em ~35 trabalhos encontrados por busca não sistemática. Para defender, fazer uma **busca estruturada documentada** (bases, termos, datas, critérios de inclusão) e escrever "nos trabalhos identificados pela busca" |
| C9 | H3 (o verificador reduz variação demográfica) | **Falta mecanismo explícito.** O verificador checa fidelidade, não viés. Mecanismo plausível: como o PREVENT ignora raça, qualquer menção à raça como fator seria "afirmação não sustentada" e seria barrada. Reformular H3 com esse mecanismo **ou** torná-la exploratória (ver D017) |

---

## ❌ Especulações ou erros (tratados)

| # | Afirmação feita antes | Problema | Tratamento |
|---|---|---|---|
| E1 | "Não encontrei estudo em português" / "português é uma lacuna" | **Falso.** Santos 2026 (EHJ-DH) avaliou 11 LLMs em estratificação cardiovascular com vinhetas em português, com desempenho semelhante ao inglês; também há benchmarks médicos em português (Revalida, HealthQA-BR) | Português **deixa de ser apresentado como contribuição**. O diferencial passa a ser: diretriz brasileira + fidelidade da explicação (D018) |
| E2 | "Taxonomia de erros" como contribuição | Não havia plano nem validação | Rebaixada a **análise descritiva dos erros** observados |
| E3 | "O teto do `cardio_train` é ~73%" e "artigos com > 90% provavelmente têm leakage" | Um único resumo + inferência minha, sem ler os artigos | **Retirar da argumentação.** O dataset saiu do núcleo por razões sólidas (transversal, sem variáveis do PREVENT); não é preciso acusar outros trabalhos |
| E4 | *(Substituída por D021: justificativa por protocolos FIPA, rastro e ablação — [justificativa-jade](justificativa-jade.md))* "O JADE é justificado pelo MAST" | Exagero: o MAST recomenda padronizar a comunicação, mas cita MCP/A2A, não FIPA | Justificar o JADE de forma **pragmática** (código existente, padrão FIPA disponível) e afirmar que a escolha não afeta a pergunta de pesquisa |
| E5 | "Risco de 6% = 6 em cada 100 pessoas com esse perfil" | Vale para a população em que o PREVENT foi calibrado (EUA); a calibração em brasileiros é desconhecida (reconhecido pela SBC) | Dizer "risco estimado pelo modelo, calibrado na população dos EUA" |
| E6 | "20–30% dos médicos já usam LLMs" | Dois surveys (Reino Unido e Omã), lidos só pelo resumo; não generalizáveis ao Brasil | Citar como dado desses países ou buscar dado brasileiro |
| E7 | "DCV = 30% das mortes, 400 mil/ano" | Fonte jornalística (Agência Brasil) | Substituir por fonte primária (Estatística Cardiovascular – Brasil, ou dados GBD citados pela SBC 2025) |
| E8 | "Jabbour prova que a verificação deve vir antes do humano" | Explicações do estudo eram imagens (Grad-CAM), não texto | Apresentar como analogia **ou** fichar estudo de viés de automação com LLM em texto (medRxiv 2025, encontrado em busca) |
| E9 | Autores do PREVENT; link de Isern & Moreno; "fidelidade 0,783" genérica | Erros factuais | Já corrigidos nos fichamentos |

---

## Regra para daqui em diante
Toda afirmação no texto do TCC precisa estar em uma destas situações:
1. ligada a um "dado citável" [C#] de fichamento com leitura completa;
2. ligada a uma decisão D### com justificativa;
3. marcada como hipótese a ser testada.

Se não estiver em nenhuma das três, é especulação e sai do texto.
