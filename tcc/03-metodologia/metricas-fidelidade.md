---
titulo: Definição operacional das métricas de fidelidade
status: rascunho
atualizado: 2026-10-06
resumo: Definições operacionais das 4 métricas novas (polaridade, exatidão numérica, variáveis fora do modelo, afirmações não sustentadas), com unidade de análise, gabarito, regras de decisão, agregação e validação.
---

# Definição operacional das métricas de fidelidade

> Resolve o item **C1** da [auditoria](../02-argumentacao/auditoria-decisoes-autorais.md). Cada escolha é marcada como **[P]** (fundamento primário), **[S]** (secundário/analogia) ou **[A]** (autoral, com justificativa e teste de sensibilidade).
>
> **Status:** definição escrita. **Falta validação** contra anotação humana (seção 7). Até lá, as métricas são condicionais.

## 0. Objeto e princípio

- **Objeto avaliado:** o **texto final** entregue ao usuário (não o JSON intermediário — brecha B6).
- **Princípio:** medir **fidelidade ao sistema de cálculo**, não correção clínica. Uma afirmação é fiel se é consistente com o que a ferramenta calculou e com as regras fornecidas ao modelo. A distinção fidelidade ≠ plausibilidade vem de [jacovi2020faithfulness](../01-literatura/fichamentos/jacovi2020faithfulness.md) **[S]** (li só o resumo).
- **Nome do construto (corrigido após a banca):** em Jacovi & Goldberg, *faithfulness* é refletir o raciocínio **do próprio modelo que explica**. Aqui o LLM explica **outro** sistema (o PREVENT e as regras da SBC). O construto medido é a **fidelidade ao modelo explicado**, isto é, a aderência do texto ao pacote de referência. Não se mede o processo interno do LLM. As métricas só se aplicam às configurações em que o LLM recebe o pacote (C-ferramenta e C-verificador); em C-isolado, o que se mede é **correção**.
- **Convenções das quais "fiel" depende:** (1) método *baseline Shapley*, com um único ponto de referência; (2) referência = valores de centralização do PREVENT; (3) interações divididas igualmente entre as variáveis (simetria do Shapley); (4) escala de log-odds; (5) ε = 5% de Σ|φ|. A banca mostrou, com uma referência alternativa ilustrativa, inversão de sinal da PAS em 4 de 24 vinhetas e top-3 alterado em 14 de 24 (`05-banca/anexos/ia/`). Reportar quantas afirmações mudam de "correta" para "incorreta" entre convenções.
- **Origem das métricas 1 e 2:** correspondem a *Sign Agreement* e *Value Agreement* de [ichmoukhamedov2024story](../01-literatura/fichamentos/ichmoukhamedov2024story.md), usadas também por [he2026agenticnarratives](../01-literatura/fichamentos/he2026agenticnarratives.md). O que se acrescenta: afirmação atômica como unidade, tolerância ε, distinção de alvo (§5.2), números do risco, das metas e das entradas, e variáveis fora do modelo.

## 1. Pacote de referência (gabarito) de cada vinheta

Para cada vinheta *v*, o sistema gera, de forma determinística, o pacote *R(v)*:

| Campo | Conteúdo | Origem |
|---|---|---|
| `entradas` | valores do paciente (idade, sexo, CT, HDL, PAS, anti-hipertensivo, estatina, DM, tabagismo, TFGe, agravantes) | vinheta |
| `risco` | risco de DCVA em 10 anos (%) | PREVENT-ASCVD (D009) |
| `categoria` | categoria SBC | motor de regras (D010) |
| `metas` | metas de LDL-c / não-HDL-c e redução percentual da categoria | SBC 2025, Tabela 5.1 |
| `atribuicao` | φⱼ de cada variável do modelo (Shapley exato, log-odds, referência de centralização) | D012 |
| `regras_aplicadas` | quais regras da SBC foram disparadas (ex.: "agravante → intermediário para alto") | motor de regras |

**Variáveis do modelo** (conjunto *M*): idade, colesterol (CT/não-HDL), HDL, PAS, anti-hipertensivo, estatina, diabetes, tabagismo, TFGe **[P]** ([khan2024prevent](../01-literatura/fichamentos/khan2024prevent.md), Methods).
**Sexo** seleciona a equação, mas não é um termo aditivo: não tem φ. É tratado como "variável do modelo **sem atribuição**" (seção 3.4) **[A]**.

## 2. Unidade de análise: a afirmação atômica

- O texto é segmentado em **afirmações atômicas**, frases curtas que carregam uma única informação **[P-pendente]** (FActScore, Min et al., EMNLP 2023 — existe, mas ainda não li; mesma lógica de "cada sentença" em Asgari 2025 **[S]**).
- Cada afirmação recebe **um** tipo:

| Tipo | Definição | Exemplo |
|---|---|---|
| **NUM** | contém valor numérico sobre o paciente ou o resultado | "Seu risco é de 6%." |
| **DIR** | atribui efeito com direção a um fator | "O tabagismo aumentou seu risco." |
| **CAT** | afirma a categoria de risco | "Você está no risco intermediário." |
| **REC** | recomendação ou meta | "Sua meta de LDL é abaixo de 100 mg/dL." |
| **GER** | conhecimento geral, não específico do paciente | "O tabagismo é um fator de risco cardiovascular." |
| **OUT** | demais (cortesia, ressalvas) | "Converse com seu médico." |

- Uma frase com duas informações vira duas afirmações (ex.: "Seu risco é 6% e a principal causa é o tabagismo" → NUM + DIR).
- **Alvo** de cada afirmação DIR: **risco calculado** (o número do PREVENT) ou **categoria/conduta** (regras SBC). O alvo muda o gabarito (seção 5) **[A]**.

## 3. Métrica 1 — Polaridade por variável

**Pergunta:** quando o texto diz que um fator aumenta ou reduz o risco, a direção bate com o sinal da atribuição do modelo?

### 3.1 Aplicação
Afirmações **DIR** com alvo = risco calculado, cuja variável pertence a *M* (com atribuição).

### 3.2 Mapeamento de termos para variáveis [A]
Glossário fixo e versionado, definido antes de rodar o experimento. Exemplos: "pressão", "pressão sistólica", "PAS", "hipertensão tratada" → PAS / anti-hipertensivo; "colesterol bom" → HDL; "colesterol total", "colesterol ruim"* → CT/não-HDL; "rins", "função renal", "TFG" → TFGe.
\*Menção a **LDL** como causa do risco calculado: tratada na métrica 3 (o PREVENT usa não-HDL, não LDL).

### 3.3 Regra de decisão
Direção textual *d* ∈ {+1 (aumenta, eleva, piora, contribui para), −1 (reduz, protege, diminui), 0 (não influenciou)}, extraída por léxico fixo.

Com **ε = 0,05 · Σₖ|φₖ|** (limiar de contribuição desprezível) **[A]**:

| Situação do gabarito | Afirmação correta se |
|---|---|
| φⱼ ≥ ε | d = +1 |
| φⱼ ≤ −ε | d = −1 |
| \|φⱼ\| < ε | qualquer d (contribuição desprezível) |

- **Justificativa de ε:** sem tolerância, contribuições praticamente nulas gerariam "erros" sem significado. O valor 5% é convenção autoral → **análise de sensibilidade** com ε ∈ {0; 0,02; 0,05; 0,10}.
- **Negação e cautela:** "pode contribuir para aumentar" conta como d = +1; "não foi o tabagismo que…" conta como d = 0 para aquela variável.

### 3.4 Casos especiais [A]
- **Sexo:** afirmações DIR sobre sexo **não entram** na polaridade (sem φ). São registradas à parte e usadas na análise exploratória de H3 (D017).
- **Interações com idade:** já distribuídas pelo Shapley (D012); nenhum tratamento extra.
- **Caracterizações clínicas** ("seu HDL está normal"): não são afirmações DIR sobre o modelo, então **não entram** na polaridade. Isso evita confundir "normal clinicamente" com "contribuição negativa em relação à referência" (brecha B4).

### 3.5 Fórmula
- **Polaridade (micro)** = nº de afirmações DIR corretas / nº de afirmações DIR avaliáveis.
- Se a explicação não tem afirmações DIR avaliáveis → "não aplicável" (não entra no denominador; o número de casos é reportado).

**Fundamento:** erros de polaridade foram observados qualitativamente em Lee 2025 (Tabela 3) **[P]**. Zhu 2026 mede consistência de direção no nível do rótulo **[P]**; aqui ela é medida **por variável** (extensão autoral).

## 4. Métrica 2 — Exatidão numérica

**Pergunta:** os números citados no texto batem com o pacote de referência?

### 4.1 Aplicação
Todas as afirmações **NUM**. Cada número é ligado a um campo de *R(v)* (risco, entrada, meta, limiar da categoria).

### 4.2 Regras de decisão
| Tipo de número | Correto se |
|---|---|
| Valor **ecoado da entrada** (ex.: "sua PAS de 160") | igual ao valor de entrada, após conversão de unidade |
| **Risco calculado** e demais valores derivados | \|x_texto − x_ref\| ≤ max(0,05·\|x_ref\|; metade da unidade de precisão usada no texto) |
| **Metas e limiares da diretriz** | iguais ao valor da Tabela 5.1 / Tabela 4.1 para a categoria de referência |
| Número **sem campo correspondente** em *R(v)* | incorreto (e conta também na métrica 4) |

- **Tolerância de 5%:** a mesma usada pelo MedCalc-Bench **[P]**. Escopo na fonte: calculadoras por equação de exames laboratoriais e físicos e de conversão de dose. Aplicá-la a um risco percentual derivado de equação é analogia minha **[A]**.
- **Tolerância pela precisão do texto** **[A]**: "6%" (inteiro) aceita 5,5–6,5, porque um texto que arredonda para inteiro não deve ser penalizado pelo arredondamento. "Cerca de" não amplia a tolerância.

### 4.3 Fórmula
**Exatidão numérica (micro)** = números corretos / números citados. Reportar também por tipo (entrada, risco, meta).

**Fundamento:** erros numéricos e de cálculo de LLMs (MedCalc-Bench, tipos B e C **[P]**; Roeschl 2026 **[P]**; valores alucinados nas primeiras versões do prompt de Lee 2025 **[P]**).

## 5. Métrica 3 — Variáveis fora do modelo

**Pergunta:** o texto atribui o **risco calculado** a fatores que o modelo não usa?

### 5.1 Aplicação
Afirmações **DIR** com alvo = **risco calculado** cuja variável **não pertence a *M***.
Lista inicial de variáveis fora do modelo **[P]** (PREVENT-ASCVD, Methods): IMC/peso/obesidade, raça/etnia, história familiar, LDL-c, triglicérides, Lp(a), PCR, sedentarismo, dieta, estresse.

### 5.2 Distinção pelo alvo [A]
| Afirmação | Classificação |
|---|---|
| "Seu IMC aumentou seu risco de 6%." | **fora do modelo** (erro) |
| "Sua história familiar eleva sua **categoria** para alto." | **não** é erro, **se** a regra de agravante foi disparada em `regras_aplicadas` |
| "Obesidade é um fator de risco cardiovascular." | GER → não entra nesta métrica |

Sem essa distinção, fatores que a diretriz usa legitimamente na **reclassificação** seriam contados como erro.

### 5.3 Fórmula
- **Taxa por explicação** = proporção de explicações com ≥ 1 afirmação fora do modelo (binária, adequada ao teste pareado de McNemar).
- **Taxa por afirmação** = afirmações fora do modelo / afirmações DIR com alvo = risco calculado.

**Fundamento:** é a operacionalização direta da distinção fidelidade × plausibilidade (Jacovi & Goldberg 2020 **[S]**, só o resumo), com gabarito objetivo porque a lista de preditores do PREVENT é publicada **[P]**. Também serve para H3: raça/etnia está nessa lista (D017).

## 6. Métrica 4 — Afirmações não sustentadas

**Pergunta:** quanto do texto afirma, sobre este paciente, coisas que não decorrem do pacote de referência?

### 6.1 Aplicação
Afirmações **NUM, DIR, CAT e REC**. **Excluídas:** GER e OUT, porque esta métrica mede fidelidade ao sistema, não exatidão factual geral **[A]** (conhecimento geral fica fora do escopo e é declarado como limitação).

### 6.2 Regra de decisão
Uma afirmação é **sustentada** se decorre de *R(v)*:
- **NUM:** correta pela métrica 2;
- **DIR:** correta pela métrica 1, ou sobre categoria com regra disparada;
- **CAT:** igual a `categoria`;
- **REC:** meta/conduta igual à prevista para a categoria (Tabela 5.1) ou explicitamente contida nas regras fornecidas.

Caso contrário, é **não sustentada**. Subtipos registrados: (a) fato do paciente inventado; (b) número sem origem; (c) atribuição causal sem base (inclui a métrica 3); (d) recomendação fora das regras fornecidas.

### 6.3 Fórmula
- **Taxa de não sustentação (micro)** = não sustentadas / afirmações avaliáveis.
- **Explicação totalmente fiel (binária)** = 1 se zero afirmações não sustentadas → **desfecho principal para o teste pareado (McNemar)** entre configurações.

**Fundamento:** definição de afirmação suportada por uma fonte (FActScore **[P-pendente]**) e de alucinação como conteúdo não sustentado pela fonte, com subtipos (Asgari 2025 **[S]**, lido só no resumo — ler antes de citar).

## 6b. Métrica 5 — Cobertura (guarda contra omissão)

**Por que existe.** O desfecho principal é "totalmente fiel". Um texto vago ("vários fatores influenciaram; converse com seu médico") é 100% fiel. Um verificador que rejeita e pede reescrita empurra o texto nessa direção. Sem uma medida de cobertura, H2 poderia ser confirmada porque as explicações passaram a dizer menos (pareceres de Metodologia, CR2, e de IA, M3).

### 6b.1 Definição
Seja *T* o conjunto das até **3 variáveis de maior |φ|** do caso, restritas às que têm |φ| ≥ ε.
- **Cobertura** = nº de variáveis de *T* mencionadas no texto **com a direção correta** / |*T*|.
- Se *T* é vazio, a métrica é "não aplicável".
- Reporta-se também o **número de afirmações avaliáveis** por explicação.

### 6b.2 Uso
- Reportada por configuração, ao lado do desfecho principal.
- H2 não é declarada sustentada se a cobertura média cair mais de 10 pontos percentuais de C-ferramenta para C-verificador (D029).
- k = 3 segue Lee et al. (2025), que medem o trio principal **[P]**; a exigência de direção correta e o limiar de 10 pontos são autorais **[A]**.

## 7. Validação das métricas (obrigatória antes de usar os resultados)

1. **Protocolo de anotação** escrito com estas definições e exemplos.
2. **Dois anotadores** (A13) anotam de forma independente uma amostra estratificada por configuração e categoria de risco (tamanho a definir no piloto — C5).
3. **Concordância:** Cohen κ por métrica e percentual de concordância simples; reportar também PABAK se as classes forem muito desbalanceadas **[P-pendente]** (a revisão de LLM-como-juiz que eu citava aqui não foi fichada).
4. **Extrator automático** (usado para escalar a avaliação a todas as vinhetas) comparado com o consenso humano: precisão/recall por tipo de afirmação e κ.
5. **Independência (brecha B1):** o extrator de avaliação **não** pode ser o mesmo componente usado pelo verificador. Reportar separadamente "aprovado pelo verificador" e "fiel segundo a avaliação".
6. **Critério de uso:** métrica com κ < 0,60 entre humanos → definição revisada e reanotada. Se continuar baixo, a métrica é reportada apenas de forma descritiva **[A]**. O limiar de 0,60 segue a convenção usual de concordância (Landis & Koch, 1977; McHugh, 2012) **[P-pendente]**: a fonte anterior, uma revisão de 2026, não foi lida e saiu.
7. **Cegamento:** os anotadores não sabem de qual configuração veio o texto (identificadores aleatórios, ordem embaralhada). A coluna de pré-anotação automática fica oculta na primeira passada. O contraste primário é anotado também por alguém que não o autor.
8. **Tamanho da dupla anotação:** com menos de 100 textos anotados em dobro, não dá para afirmar κ ≥ 0,60 com segurança (cálculo da banca: com 100 textos e κ real de 0,70, 95% dos κ amostrais ficam entre 0,52 e 0,85).

## 8. Resumo de agregação e testes

| Métrica | Nível do caso | Uso estatístico |
|---|---|---|
| 1. Polaridade | proporção por explicação | comparação pareada de proporções / bootstrap |
| 2. Exatidão numérica | proporção por explicação | idem |
| 3. Fora do modelo | binária (≥ 1 ocorrência) | **McNemar** entre pares de configurações |
| 4. Não sustentadas | binária "totalmente fiel" | **McNemar** (desfecho principal de H2) |
| 5. Cobertura | proporção por explicação | diferença pareada com IC; condição de H2 (D029) |

Todas com intervalos de confiança por bootstrap sobre as vinhetas. A mesma vinheta repetida não é observação independente **[A]**. **Regra de agregação (D029):** o teste primário usa a primeira repetição de cada vinheta; as demais entram na análise de sensibilidade. Explicações bloqueadas contam como falha na análise primária. Teste: McNemar mid-p, com Holm entre os 2 LLMs.

## 9. Parâmetros autorais e sensibilidade

| Parâmetro | Valor base | Sensibilidade |
|---|---|---|
| ε (contribuição desprezível) | 5% de Σ\|φ\| | 0; 2%; 10% |
| Tolerância numérica | max(5%; meia unidade de precisão) | 5% fixo |
| Referência da atribuição | centralização do PREVENT | média NHANES (B4) |
| Regra de agravante | sobe 1 categoria | sem promoção (D010) |
| Limiar de κ | 0,60 | — |

## 10. Referências usadas
[P] khandekar2024medcalc (tolerância de 5%; tipos de erro) · lee2025shapllm (erros de polaridade; alucinação numérica) · zhu2026agenticexpl (direção) · khan2024prevent (preditores do modelo) · roeschl2026pipeline
[P], leitura parcial: he2026agenticnarratives · ichmoukhamedov2024story (origem de sinal e valor)
[P-pendente] (existem, não li): FActScore (Min et al., EMNLP 2023) · Landis & Koch (1977) · McHugh (2012) · Sundararajan & Najmi (ICML 2020)
[S] jacovi2020faithfulness (só o resumo) · asgari2025hallucination (só o resumo)
