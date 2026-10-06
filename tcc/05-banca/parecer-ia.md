---
titulo: Parecer da banca — Inteligência Artificial, LLMs e Explicabilidade (XAI)
status: vigente
atualizado: 2026-09-29
resumo: Auditoria da parte de IA/LLM/XAI do TCC (novidade, Shapley exato, métricas, protocolo do piloto, verificador, escolha de LLMs, efeito teto), com verificações executadas e referências conferidas.
---

# Parecer — IA, LLMs e Explicabilidade (XAI)

**Avaliador(a):** membro da banca, área de IA (PLN, LLMs e XAI)
**Material examinado:** `tcc/INDEX.md`; `tcc/01-literatura/sintese-leitura.md` e fichamentos centrais (com conferência pontual nos textos completos de Lee 2025 e Zhu 2026); `tcc/03-metodologia/metricas-fidelidade.md`; `tcc/02-argumentacao/*`; `tcc/00-projeto/decisoes.md` (D002–D005, D012, D014, D017, D018, D023, D024); código `experimentos/piloto/*.py` e `backend-gateway/app/avaliacao.py`.
**Verificações próprias:** scripts e resultados em `tcc/05-banca/anexos/ia/` (seção 6).
**Data da busca bibliográfica própria:** 29/09/2026.

---

## 1. Parecer resumido e veredito

O projeto está bem acima da média de um TCC de graduação na parte técnica. A atribuição de referência (Shapley exato sobre o log-odds do PREVENT) está **correta**: conferi com três implementações independentes, incluindo a biblioteca `shap`, e as diferenças ficaram na ordem de 10⁻¹². As decisões estão documentadas com rastreabilidade rara (níveis [P]/[S]/[A], auditoria das próprias afirmações, brecha B1 da circularidade reconhecida antes que alguém a apontasse). A leitura dos artigos centrais é fiel: conferi as citações de Lee 2025 (erros de polaridade, Tabela 3; trabalho futuro "monitoring layer") e de Zhu 2026 (Jaccard 0,171 × 0,077; "attribution-based checks") nos textos completos.

O **ponto fraco é a novidade**. A lacuna, do jeito que está escrita ("verificador da explicação + métricas de polaridade/exatidão numérica + ablação do verificador"), **não se sustenta** diante de trabalhos que o projeto não cita:
- **He & Martens (arXiv, mar/2026)** implementam exatamente um ciclo Narrador → Críticos de fidelidade, com extração por LLM e comparação **determinística** de posto, **sinal** e **valor** contra a tabela SHAP. Fazem a ablação de cinco desenhos, inclusive um crítico só por regras, em 5 LLMs e 5 bases (duas delas de saúde: diabetes e AVC). Relatam redução de 90% das narrativas infiéis.
- **Ichmoukhamedov, Hinns & Martens (2024)** definiram as métricas *Sign/Rank/Value Agreement* para narrativas de SHAP.
- **XstrAI (ago/2026)** faz narrativas de SHAP para pacientes e clínicos em risco de diabetes e AVC, com fase de validação contra o SHAP e ciclo de revisão.
- **FAX (mai/2026)** decompõe a explicação em afirmações e confere cada uma contra ferramentas fiéis por construção.

Ainda sobra contribuição defensável, mas ela está em outro lugar (seção 4, problema C1).

Há também problemas de **protocolo** que afetam a validade do piloto:
- o prompt induz erros que depois serão medidos (números em notação inglesa com ponto, que em pt-BR se lê como milhar; IMC entregue como dado sem aviso de que não entra no modelo);
- a pré-anotação heurística teve recall de 32% no meu teste adversarial e **0% em polaridade**;
- a regra de decisão do piloto é frágil para 24 vinhetas escolhidas a dedo para provocar erro.

**Veredito: APROVÁVEL COM RESSALVAS (revisão maior do posicionamento e do protocolo do piloto antes da qualificação).** O núcleo técnico é sólido. A contribuição precisa ser reescrita em relação a He & Martens 2026, Ichmoukhamedov 2024, XstrAI 2026 e FAX 2026. As correções de protocolo são baratas e devem entrar antes de gastar chamadas de API.

---

## 2. Notas por critério (0–10)

| Critério | Nota | Justificativa |
|---|---|---|
| **Novidade e posicionamento** | **5,0** | A formulação atual (D003, `sintese-leitura` §3.2, `trabalhos-relacionados`) afirma que o verificador da explicação, as métricas de polaridade e números e a ablação "não aparecem em nenhum trabalho". Isso é falso: He & Martens 2026 têm os três; Ichmoukhamedov 2024 tem as métricas; XstrAI 2026 tem ciclo de validação contra SHAP em saúde. O que resta é original e defensável: gabarito **exato**, camada de regras da diretriz, variáveis fora do modelo com gabarito publicado, avaliação independente do verificador e armadilhas contraintuitivas. Mas precisa ser reescrito. |
| **Correção técnica do Shapley** | **9,0** | A implementação está correta: eficiência, simetria, jogador nulo e linearidade foram verificados, e o resultado coincide com permutações (9!), com a forma fechada e com `shap` 0.42.1 (Kernel e Exact). Desconto por dois pontos. (i) O método é o *baseline Shapley* (Sundararajan & Najmi 2020), não o SHAP "interventional" com distribuição de fundo, e isso não é nomeado. (ii) Não há discussão da convenção de dividir as interações pela metade: no meu teste, outra convenção inverte um sinal real e desloca 4 classes em torno de ε. |
| **Métricas** | **6,5** | Definições operacionais boas, com princípios claros (fidelidade ≠ plausibilidade; distinção de alvo risco × categoria; 5.2 é muito boa). Faltam: medida de omissão e de informatividade (o verificador pode "ganhar" fazendo o texto dizer menos); o tratamento de **frequências naturais** ("x em cada 100") e de afirmações contrafactuais numéricas; e uma análise do extrator. ε relativo a Σ\|φ\| é dominado pela idade. FActScore é citado como [P] sem ter sido fichado. |
| **Protocolo do piloto** | **5,5** | É bom que o piloto exista (D023) e que registre metadados, hash do prompt e commit. Mas: o prompt tem vieses de indução; a pré-anotação não detecta polaridade; a regra de decisão ignora o IC e o desenho adversarial das vinhetas; não há controle de truncamento e de conteúdo vazio em modelos com raciocínio (GPT-OSS, Gemini 2.5 Flash); 3 repetições a T = 0,7 não estimam a taxa por vinheta. |
| **Viabilidade do verificador** | **7,0** | É viável e tem precedente direto (He & Martens 2026 mostram que funciona, inclusive com crítico só por regras). A divisão determinístico × LLM é correta. O risco real é a **extração** das afirmações do texto livre, que é o gargalo, e não a comparação. Isso não está especificado, e a brecha B1 exige dois extratores diferentes. |
| **Uso da literatura** | **6,0** | Os artigos lidos são usados com fidelidade e honestidade: as correções da `sintese-leitura` §1 são exemplares. Mas há três falhas. (i) A busca não foi estruturada (o próprio projeto admite, em C8) e perdeu justamente a linha mais próxima (grupo de Martens, Antuérpia). (ii) Referências-chave estão marcadas [P] sem terem sido fichadas: FActScore, CRITIC, Huang 2024, Sundararajan & Najmi, Lundberg & Lee. (iii) Asgari 2025 e PROVE foram lidos só no resumo. |

**Média simples: 6,5.**

---

## 3. Pontos fortes

1. **Gabarito de atribuição exato.** Sobre um escore clínico publicado e linear em log-odds, o gabarito elimina a crítica de que "SHAP aproximado também é infiel" (AlMarri 2025, já fichado). Nos trabalhos concorrentes (Lee, Zhu, He & Martens, XstrAI), o SHAP de XGBoost é tomado como verdade sem que se saiba se ele próprio é fiel ao modelo.
2. **Separação entre alvo "risco calculado" e alvo "categoria/conduta"** (métricas §5.2). Ela resolve de forma elegante o caso do agravante: a história familiar elevar a categoria é legítimo, mas culpar a história familiar pelo número é erro. Não vi isso em nenhum trabalho da área.
3. **"Variáveis fora do modelo" com gabarito objetivo.** O IMC é plausível, mas não entra no PREVENT-ASCVD, e isso é demonstrável: o teste `test_imc_nao_altera_risco_de_dcva` e os coeficientes de IMC zerados no JSON confirmam. É a melhor operacionalização de Jacovi & Goldberg que já vi em um TCC.
4. **Vinhetas-armadilha contraintuitivas:** anti-hipertensivo com φ > 0 (V07, V08, V14); idade < 55 com φ < 0 (V01–V05, V20); HDL alto protetor (V04, V20). Ichmoukhamedov et al. 2024 mostraram que, quando o SHAP contraria o conhecimento prévio, os LLMs "corrigem" o sinal: a concordância de sinal cai para cerca de 30% com tabelas invertidas. As armadilhas miram exatamente essa fraqueza. **Esse é o argumento mais forte contra o efeito teto (R2) e não está explicitado no projeto.**
5. **Consciência metodológica:** B1 (Goodhart), B2 (baseline espantalho), B3 (contrafactual de sexo inválido), agregação das repetições por vinheta e κ com PABAK.
6. **Reprodutibilidade do código:** piloto sem dependências externas; testes contra os 6 valores publicados do PREVENT (7 testes passam); registro de modelo, temperatura, commit e hash do prompt.

---

## 4. Problemas

### Críticos

**C1 — A lacuna declarada é pré-empitada por trabalhos não citados.**
- **Evidência:** `trabalhos-relacionados.md` diz que a combinação "verificador da explicação + polaridade e números + ablação do verificador não aparece em nenhum dos trabalhos identificados"; D003 e `defesa-valor` §2 dizem o mesmo. Porém:
  - **He & Martens 2026** (arXiv 2603.20003) têm um Narrador e Críticos de fidelidade. O *Faithful Evaluator* extrai por LLM posto/sinal/valor de cada variável e compara **por regra, sem LLM** (ou seja, verificador híbrido). Há um crítico só por regras e cinco desenhos em ablação, com 5 LLMs (incluindo Claude 4.5 Sonnet e DeepSeek-V3.2) e 5 bases (incluindo Diabetes e Stroke Prediction). Na linha de base, 31 de 100 narrativas eram infiéis (acurácias de posto/sinal/valor de 0,900/0,958/0,990). Com o crítico, a redução chegou a 90% em três rodadas.
  - **Ichmoukhamedov et al. 2024** (arXiv 2412.10220) propõem Rank/Sign/Value Agreement com extrator GPT-4o.
  - **XstrAI 2026** (arXiv 2608.11033): multiagente com validação de "attribution consistency" contra SHAP e ciclos de revisão, para pacientes e clínicos, em diabetes e AVC.
  - **FAX 2026** (arXiv 2605.27879): decomposição em afirmações e checagem contra ferramentas fiéis.
- **Impacto:** a banca derruba a contribuição central com uma única pergunta ("qual a diferença para He & Martens?"). A tabela comparativa fica incorreta.
- **Recomendação:** fichar os quatro trabalhos e reescrever D003, `trabalhos-relacionados` e `defesa-valor` §2, deslocando a contribuição para o que eles **não** têm:
  1. gabarito de atribuição **exato**, de um escore clínico adotado por diretriz, e não SHAP de XGBoost;
  2. **camada de regras clínicas** (categoria, reclassificação por agravante, metas), com distinção de alvo;
  3. **variáveis fora do modelo** com gabarito publicado (fidelidade × plausibilidade);
  4. **avaliação independente** do verificador. He & Martens usam o **mesmo** avaliador no ciclo e na métrica final, que é exatamente a brecha B1. O projeto pode e deve dizer isso;
  5. unidade de **afirmação atômica** com anotação humana e κ, em vez de extrator LLM validado em poucos casos;
  6. **atribuições contraintuitivas** (medicação como marcador, idade abaixo da referência) como estresse do verificador;
  7. diretriz brasileira.

  A pergunta de pesquisa passa a ser "o efeito relatado em bases genéricas (He & Martens) se mantém quando a verdade é exata, há regras clínicas e a avaliação é independente?". Isso é replicação + extensão, e é legítimo para um TCC. Refazer a busca de forma estruturada (C8) com os termos "XAI narrative", "narrator critic", "sign agreement", "faithful evaluator".

**C2 — A pré-anotação heurística não é confiável e não mede polaridade.**
- **Evidência:** teste adversarial com 26 textos escritos por mim (`anexos/ia/testar_preanotacao.py`): **recall 6/19 = 32%, precisão 6/11 = 55%**. Por tipo de erro: polaridade 0/6; fora do modelo 2/5; numérico 1/4; categoria 3/3; recomendação 0/1. Casos que escapam:
  - "O HDL de 55 aumentou o seu risco" (sinal invertido);
  - "a pressão de 105 **pode contribuir** para aumentar" (cautela com direção errada);
  - "**Não foi** a pressão que pesou" (negação, com φ da PAS ≥ ε);
  - "excesso de peso está por trás" e "índice de massa corporal" (sinônimos de IMC);
  - "por ser homem negro" (raça sem a palavra "raça", o que afeta H3);
  - "aumenta seu risco em **30%**" (lista branca de 30%/50%);
  - "12 em cada 100" (frequência natural);
  - "meta abaixo de 70 […] ideal 100" (a meta passa só porque o número aparece no texto).

  Falsos positivos:
  - "menos de 1%" com risco de 0,3%;
  - limiares da diretriz (5%, 20%) marcados como erro numérico;
  - agravante legítimo (C04) marcado como FORA;
  - "IMC não entra neste cálculo" marcado como FORA;
  - "não é alto nem baixo, é moderado" gerou erro de CAT.
- **Impacto:** o README avisa que a pré-anotação "não é a avaliação". Mas o anotador único do piloto tende a ancorar no que foi sinalizado (viés de automação). Com 0% de recall em polaridade, a principal métrica nova fica sem apoio. E se esta heurística virar o "extrator diferente" de B1, a avaliação independente será cega aos erros principais.
- **Recomendação:**
  - anotar **sem** a coluna `pre_anotacao` visível (ou revelá-la só depois de uma primeira passada);
  - usar os casos de `testar_preanotacao.py` como **teste de regressão** do extrator;
  - para polaridade, extrair pares (variável, direção) com glossário e léxico de negação e cautela, ou com um LLM extrator validado contra humanos (como fazem Ichmoukhamedov et al., que reportam 1/53 falsos negativos);
  - tratar "x em cada 100" como NUM;
  - só aceitar a meta de LDL se ela estiver ligada à expressão "meta".

### Maiores

**M1 — O prompt induz parte dos erros que serão medidos (validade de construto do piloto).**
- **Evidência** (`prompt.py`; `resultados/prompt_exemplo.txt`):
  - (a) as contribuições são impressas com `%+.3f`, por exemplo "idade: -1.567". Em pt-BR, "1.567" é mil quinhentos e sessenta e sete, enquanto o risco vem com vírgula ("0,3%"). A notação mista é um gatilho de erro numérico que não existe no uso real;
  - (b) todo paciente recebe "IMC: 25 kg/m²", mesmo quando a vinheta não informa IMC (`_PADRAO` em `vinhetas.py`), e o prompt manda "use apenas as informações fornecidas". O IMC **é** informação fornecida, e nada diz que ele não entra no cálculo. Uma menção causal ao IMC fica parcialmente autorizada pelo próprio prompt;
  - (c) a unidade "log-odds" não é explicada. O prompt não proíbe traduzir as contribuições em percentuais ("aumentou seu risco em 1,5%"), que seriam números sem origem;
  - (d) as variáveis com φ = 0 somem da tabela (`gabarito.ranking`). O LLM não sabe se o tabagismo "não conta" ou "não foi informado".
- **Impacto:** a taxa de erro do piloto mistura a fraqueza do LLM com artefatos do prompt. Se o objetivo é refutar o efeito teto (R2), o piloto será criticado por "prompt armadilha". Se o objetivo é medir o verificador, o baseline C-ferramenta fica artificialmente fraco (B2 às avessas).
- **Recomendação:**
  - formatar com vírgula decimal ou, melhor, entregar **direção + magnitude qualitativa** ("aumentou muito / pouco") junto com o número;
  - declarar explicitamente a lista de variáveis que **não** entram no modelo (é o que um sistema bem projetado faria);
  - não fabricar IMC;
  - proibir a conversão de contribuições em percentuais;
  - manter uma **versão "armadilha"** e uma **versão "boa prática"** do prompt e reportar as duas. A diferença entre elas já é um resultado.

**M2 — A regra de decisão do piloto é frágil.**
- **Evidência:**
  - `resumir.py` decide com base na **estimativa pontual** (≥ 10%) sobre as respostas, com Wilson ignorando o agrupamento por vinheta. Mas `metricas-fidelidade` §8 manda agregar por vinheta;
  - com n efetivo de 24 vinhetas, 2/24 dá IC 95% de 2,3–25,8%, e 0/24 ainda é compatível com até 13,8%;
  - as vinhetas foram **escolhidas para provocar erro** (docstring de `vinhetas.py`), então a taxa é um limite superior de uso real (o README reconhece isso);
  - "vinheta com erro se alguma repetição errou" depende do número de repetições.
- **Impacto:** a decisão "segue × ajusta a tarefa" pode ser tomada com base em ruído.
- **Recomendação:** pré-registrar a regra com IC, por exemplo "segue se o limite inferior do IC 95% por vinheta for maior que 5%". Reportar à parte a taxa nas vinhetas-armadilha e nas vinhetas "típicas". Reportar a probabilidade de erro por vinheta (proporção entre as repetições) em vez do "alguma errou".

**M3 — As métricas não capturam omissão nem informatividade, o que abre caminho para a lei de Goodhart dentro do verificador.**
- **Evidência:**
  - o desfecho principal é "totalmente fiel" (zero afirmações não sustentadas, §6.3). Uma explicação vaga ("vários fatores influenciaram; converse com seu médico") é 100% fiel;
  - um verificador que reprova e pede reescrita empurra o Explicador para textos com **menos afirmações verificáveis**;
  - a omissão aparece só como "oportunidade" (fundamentação §B, item 4) e em B5, sem métrica;
  - FAX (2026) reporta fidelidade **junto com** informatividade exatamente por esse motivo;
  - Lukassen et al. 2026 mostram que narrativas de alta qualidade não melhoram decisões e aumentam a confiança subjetiva.
- **Impacto:** a hipótese H2 pode ser confirmada por um mecanismo indesejado (o texto deixa de afirmar).
- **Recomendação:**
  - adicionar **cobertura**: proporção dos top-k de |φ| (acima de ε) mencionados com a direção correta;
  - reportar o número de afirmações avaliáveis por explicação;
  - definir como desfecho **conjunto** "totalmente fiel **e** cobertura ≥ k", ou reportar a fronteira fidelidade × cobertura por configuração.

**M4 — A atribuição depende de convenções não discutidas: referência, divisão das interações e ε.**
- **Evidência** (`anexos/ia/verificar_shapley.py`, `resultado_verificar_shapley.json`):
  - **(a) Referência.** Com uma referência alternativa ilustrativa (aproximação de médias populacionais; **não** é o NHANES processado):
    - há **inversão real de sinal da PAS** em 4 de 24 vinhetas (V02, V05, V15, V22: PAS 125–128 fica abaixo de 130, mas acima de 124);
    - o **top-3 muda em 14 de 24** vinhetas;
    - as binárias ausentes passam de φ = 0 para φ < 0: sob a referência de centralização, "não fumar" **nunca** contribui; sob a referência média, "não fumar reduziu seu risco" passa a ser verdadeiro;
  - **(b) Interações idade × fator.** Atribuir a interação inteira ao fator, em vez de metade, inverte o sinal do não-HDL em V17 e muda a classe (acima ou abaixo de ε) em 4 vinhetas;
  - **(c) Escala.** A escala de probabilidade não inverteu nenhum sinal (a ligação é monótona e a referência é a mesma), mas o top-3 mudou em 4 de 24;
  - **(d) ε.** Com ε = 0, 2%, 5% e 10% de Σ|φ|, o número de pares (vinheta, variável) classificados como desprezíveis é 0, 32, 45 e 62. Como a idade domina Σ|φ|, em idosos fatores relevantes caem abaixo de ε.
- **Impacto:** "fiel" significa "fiel sob a referência de centralização, a divisão simétrica das interações, a escala log-odds e ε = 5%". Uma parte dos "erros de polaridade" será, na verdade, desacordo de convenção. O paciente entende "aumentou seu risco" em termos absolutos, não relativos a uma pessoa de 55 anos.
- **Recomendação:**
  - nomear o método (*baseline Shapley*, Sundararajan & Najmi 2020) e declarar as quatro convenções;
  - rodar a sensibilidade já prevista (NHANES) e reportar **quantas afirmações mudam de "correta" para "incorreta"** entre convenções. Isso é uma banda de incerteza do gabarito;
  - considerar ε absoluto em log-odds (por exemplo, |φ| < 0,05, cerca de 5% no odds), em vez de relativo;
  - para interações, considerar a entrega ao LLM de efeito principal + interação separados, ou declarar a convenção de Shapley como escolha.

**M5 — Os modelos com raciocínio podem truncar ou devolver texto vazio sem que isso seja detectado.**
- **Evidência:**
  - `llm.py` devolve `content or ""` e o registra como resposta válida;
  - `max_tokens = 2048` para GPT-OSS-120B (Groq), que é um modelo de raciocínio: os tokens de raciocínio contam na saída. O mesmo vale para Gemini 2.5 Flash, em que os *thinking tokens* entram em `maxOutputTokens`;
  - não se registra `finish_reason` nem `reasoning_effort`, nem se fixa o orçamento de raciocínio.
- **Impacto:** respostas vazias ou cortadas viram "explicações" (vazias são "fiéis"; cortadas podem omitir a categoria), e o efeito do raciocínio não é controlado.
- **Recomendação:**
  - registrar `finish_reason`, `usage` e o `id`/`system_fingerprint` do modelo;
  - tratar vazio ou truncado como falha técnica, reportada à parte;
  - fixar `reasoning_effort` (Groq) e `thinkingBudget` (Gemini).

### Menores

- **m1 — Temperatura 0,7 com 3 repetições.** É defensável como condição de uso (é a mesma da interface), mas a literatura de referência usa T = 0 (AgentMD, Roeschl). E T = 0 não garante determinismo nas APIs (Ouyang et al. 2023). Recomendo T = 0 como condição principal de comparação entre configurações e T = 0,7 com ≥ 5 repetições para estimar variabilidade, ou justificar a escolha única.
- **m2 — Referências marcadas [P] sem fichamento.** FActScore, CRITIC, Huang et al. 2024, Sundararajan & Najmi e Lundberg & Lee aparecem como "a fichar" (`fundamentacao-por-parte`, `metricas` §10). CRITIC e Huang estão **corretamente** usados no argumento: autocorreção intrínseca não funciona em raciocínio (Huang), e crítica com ferramentas externas funciona (CRITIC). Mas é preciso notar que em Huang os ganhos com *feedback* dependiam de rótulos-oráculo. Aqui o nível 1 do verificador **é** um oráculo, porque o gabarito é exato. Isso fortalece o argumento e deveria ser dito.
- **m3 — MAST usado com cuidado.** O "verificador multinível" e a "validação simbólica" estão corretos (Insight 3; Apêndice G). O próprio projeto já corrigiu a extrapolação para FIPA/JADE (E4). Só lembrar que o MAST não inclui domínio médico nem avalia explicações.
- **m4 — Frequência natural na interface.** `avaliacao.py` expõe `em_100_pessoas = round(risco_pct)`. Para 0,3%, isso dá "0 em cada 100", que é enganoso. Usar "menos de 1 em 100" ou "em cada 1.000".
- **m5 — A interface já rotula a direção de forma determinística** ("aumentou / diminuiu / pouco influenciou", com o mesmo ε). É bom para o usuário, mas se esse mesmo rótulo for entregue ao Explicador numa configuração, o verificador de polaridade vira quase tautológico. Declarar qual informação cada configuração recebe.
- **m6 — Ética da fidelidade contraintuitiva.** Dizer ao paciente que "usar remédio para pressão aumentou seu risco" (V07, V08) é **fiel**, mas pode induzir abandono do tratamento. O verificador vai **premiar** essa frase. O TCC precisa de uma regra de redação (por exemplo, "o uso de anti-hipertensivo indica pressão tratada, o que o modelo associa a maior risco") e de uma discussão explícita de fidelidade × segurança.
- **m7 — H3 com poucos casos.** Nenhuma vinheta do piloto informa raça ou etnia. H3 depende de um conjunto próprio de pares contrafactuais que ainda não existe.

---

## 5. Perguntas da banca

| # | Pergunta | Resposta esperada | O projeto responde hoje? |
|---|---|---|---|
| 1 | Qual a diferença entre o seu verificador e o ciclo Narrador/Crítico de He & Martens (2026), que já mede sinal/posto/valor e reduz 90% das narrativas infiéis? | Gabarito exato (não SHAP de XGBoost); regras clínicas e alvo categoria × risco; variáveis fora do modelo; avaliação independente do ciclo (lá o avaliador do ciclo é o da métrica final); afirmações atômicas com anotação humana; atribuições contraintuitivas. | **Não** — o trabalho não é citado. |
| 2 | Suas métricas de polaridade e exatidão não são as *Sign/Value Agreement* de Ichmoukhamedov et al. (2024)? | Em parte, sim. A diferença: unidade de afirmação atômica, tolerância ε, distinção de alvo, números da diretriz e das entradas, e fora do modelo. Adotar SA/RA/VA também para comparabilidade. | **Não**. |
| 3 | O seu Shapley é o SHAP? Com que distribuição de fundo? | É o *baseline Shapley* (um único ponto de referência), exato; difere do SHAP interventional com fundo populacional. Conferido contra `shap` com fundo de 1 ponto. | **Parcial** — D012 e A4 falam de referência, mas não nomeiam o método. |
| 4 | "Fiel a quê?" Se mudo a referência, quantos erros de polaridade viram acertos? | Fiel sob convenções declaradas; reportar a banda de sensibilidade (a análise desta banca achou inversão de sinal da PAS em 4/24 vinhetas e top-3 alterado em 14/24 com uma referência alternativa). | **Parcial** — fundamentação §3 (B4) prevê a análise; ainda não foi feita. |
| 5 | Por que dividir a interação idade × fator meio a meio? | Axioma de simetria do Shapley; alternativas (Shapley-Taylor, efeito principal + interação separados); declarar e medir a sensibilidade. | **Não** — métricas §3.4 diz "nenhum tratamento extra". |
| 6 | O verificador não vence por fazer o texto dizer menos? | Métrica de cobertura/informatividade e desfecho conjunto. | **Não** — só B5 (legibilidade), sem métrica. |
| 7 | Quem extrai as afirmações do texto para o verificador e para a avaliação? Com que precisão? | Dois extratores diferentes, validados contra 2 anotadores (κ ≥ 0,6), com precisão/recall por tipo. | **Parcial** — métricas §7 prevê; a única ferramenta existente (heurística) tem recall de 32% e 0% em polaridade. |
| 8 | O efeito teto não mata H2? Modelos atuais erram o sinal em 4%. | A literatura mostra 31% de narrativas com algum erro na linha de base (He & Martens) e colapso da concordância de sinal quando o SHAP contraria o senso comum (Ichmoukhamedov). As armadilhas V07/V08/V14/V01–V05 exploram isso; o piloto mede. | **Parcial** — D023 e o piloto existem; falta citar essa evidência. |
| 9 | O prompt não fabrica os erros (ponto como separador decimal, IMC fornecido)? | Versões "armadilha" e "boa prática" do prompt; formatação pt-BR. | **Não**. |
| 10 | Por que T = 0,7 e 3 repetições, se Roeschl e AgentMD usam T = 0? | Condição de uso × condição de comparação; reportar as duas ou justificar; o número de repetições depende da variância observada no piloto. | **Parcial** — "a mesma do sistema atual" (README). |
| 11 | Os modelos gratuitos mudam ou somem. Como reproduzir? | ID e data, logs completos, modelo de pesos abertos (GPT-OSS/Llama) reexecutável em outro provedor; declarar que a quantização do provedor pode diferir. | **Parcial** — D014/D024; falta registrar `finish_reason`, fingerprint e orçamento de raciocínio. |
| 12 | O LLM-juiz do nível 2 não herda os vieses do Explicador (mesma família)? | Usar juiz de outra família; medir κ do juiz contra os humanos; restringir ao nível 1 se κ for baixo. | **Parcial** — C2 da auditoria. |
| 13 | Dizer ao paciente que o anti-hipertensivo "aumentou" o risco é aceitável? | Fidelidade não é segurança; regra de redação para marcadores de tratamento; discutir. | **Não**. |
| 14 | Qual o tamanho de amostra para o McNemar com agregação por vinheta? | Cálculo de poder a partir das proporções discordantes do piloto. | **Não** — C5 em aberto. |

---

## 6. Verificações executadas

Ambiente: Python 3.8.11 (venv da sessão), numpy 1.24.4, shap 0.42.1 (instalado para esta auditoria). O projeto não foi modificado.

| # | Verificação | Como | Resultado |
|---|---|---|---|
| V1 | Testes do projeto | `python3 -m unittest test_prevent` | 7/7 OK (reproduz 3,6/5,4/2,5% e 6,0/9,3/4,7% do artigo). |
| V2 | Execução seca do piloto | `rodar_piloto.py --seco` | 24 gabaritos; risco de 0,3% a 24,9%; categorias baixo/intermediário/alto presentes; prompt de exemplo inspecionado (origem de M1). |
| V3 | Eficiência | `verificar_shapley.py` | máx \|Σφ − (L(x) − L(ref))\| = 4,4 × 10⁻¹⁵ nas 24 vinhetas. |
| V4 | Implementação independente por **permutações** (9! = 362.880 ordens) | idem | máx diferença = 3,8 × 10⁻¹². |
| V5 | **Forma fechada** (efeito principal + ½ de cada interação de pares) | idem | máx diferença = 3,1 × 10⁻¹⁵. Também confirma que a interação idade × IMC tem coeficiente 0 no modelo de DCVA. |
| V6 | **`shap.KernelExplainer`** (fundo = referência; 2⁹ coalizões) e **`shap.explainers.Exact`** | idem | máx diferença = 4,0 × 10⁻¹⁵ e 3,1 × 10⁻¹⁵. |
| V7 | Axiomas no algoritmo (jogo sintético via *monkeypatch*) | idem | simetria: φ(idade) = φ(PAS) = 5,667; jogador nulo: φ(estatina) = 0; eficiência: 13,7 = 13,7; linearidade: diferença 0. |
| V8 | Sensibilidade (escala, referência, interação, ε) | idem | ver M4: probabilidade, 0 inversões e top-3 alterado em 4/24; referência alternativa, 4 inversões reais (PAS) e top-3 alterado em 14/24; interação atribuída ao fator, 1 inversão (V17, não-HDL) e 4 mudanças de classe ε; ε 0/2/5/10%, 0/32/45/62 pares desprezíveis. |
| V9 | Teste adversarial da pré-anotação | `testar_preanotacao.py` (26 textos) | recall 32%, precisão 55%; polaridade 0/6 (ver C2). |
| V10 | Conferência de citações nos textos completos | `grep` em `textos/lee2025shapllm.txt` e `zhu2026agenticexpl.txt` | citações [C2] e [C5] de Lee e [C1] e [C3] de Zhu **conferem**. |
| V11 | Busca própria de trabalhos relacionados (2024–2026) | busca web em 29/09/2026 | 4 trabalhos diretamente concorrentes não citados (C1) + 1 sobre utilidade (M3). |

Arquivos: `anexos/ia/verificar_shapley.py`, `anexos/ia/resultado_verificar_shapley.json`, `anexos/ia/testar_preanotacao.py`, `anexos/ia/resultado_testar_preanotacao.json`.

**Ressalva sobre V8:** a referência alternativa é **ilustrativa** (valores aproximados de médias populacionais, com binárias fracionárias), e não o NHANES processado. Ela serve só para mostrar a ordem de grandeza da dependência. O projeto deve refazer a análise com o NHANES real.

---

## 7. Evidência sobre o efeito teto (R2)

- **Contra o teto (há erros):**
  - He & Martens 2026: na linha de base, **31% das narrativas** tinham algum erro de fidelidade; acurácia de sinal de 0,958 por variável;
  - Ichmoukhamedov et al. 2024: GPT-4o com SA = 0,975 em condições normais. Mas com tabelas SHAP invertidas (contraintuitivas) a concordância de sinal **caiu para cerca de 30%**: os modelos "corrigem" o SHAP com conhecimento prévio;
  - Lee 2025: erros de polaridade no GPT-4 mesmo com salvaguardas;
  - XstrAI e FAX só existem porque o problema persiste em 2026.
- **A favor do teto:** em narrativas "normais" os erros por variável são raros (4–5%), e o erro de **valor** é quase nulo (VA ≈ 0,99).
- **Leitura:** o efeito teto é provável para vinhetas típicas e improvável para atribuições contraintuitivas e para regras de categoria. O projeto deve **estratificar o piloto** por tipo de vinheta e citar essa evidência na justificativa de D023.

---

## 8. Sobre a escolha de LLMs (D024)

- **Validade interna:** modelos gratuitos não comprometem a pergunta, que é comparativa (com × sem verificador no mesmo modelo). GPT-OSS-120B e Gemini Flash são de porte adequado, bem acima do llama3.2:3b de Zhu 2026.
- **Validade externa:** os resultados valem para esses modelos naquelas datas.
- **Reprodutibilidade:**
  - os provedores descontinuam modelos (o próprio projeto viu o Gemini 1.5 retornar 404; ver também as páginas de *deprecations* do Groq e do Gemini);
  - o comportamento muda sob o mesmo nome (Chen, Zaharia & Zou 2023);
  - há não determinismo mesmo a T = 0 (Ouyang et al. 2023);
  - pesos abertos atenuam o problema, mas o Groq pode servir versões quantizadas: registrar isso.
- **Ponto de atenção:** os planos gratuitos do Gemini podem usar os dados enviados para melhorar produtos. Com vinhetas sintéticas não há problema, mas **a interface com dados reais de pacientes não deve usar o plano gratuito** (LGPD).

---

## 9. Referências (conferidas na internet em 29/09/2026)

**Não citadas pelo projeto e diretamente relevantes**
- HE, Y.; MARTENS, D. *An Agentic Approach to Generating XAI-Narratives*. arXiv:2603.20003, 2026. https://arxiv.org/abs/2603.20003
- ICHMOUKHAMEDOV, T.; HINNS, J.; MARTENS, D. *How good is my story? Towards quantitative metrics for evaluating LLM-generated XAI narratives*. arXiv:2412.10220, 2024. https://arxiv.org/abs/2412.10220
- MUSICCO, et al. *Who Are You Explaining To? A Multi-Agent System for Audience-Aware XAI Narratives (XstrAI)*. arXiv:2608.11033, 2026. https://arxiv.org/abs/2608.11033
- KIM, J. et al. *Towards Faithful Agentic XAI: A Verification Method and an Open-World Benchmark for Better Model Faithfulness (FAX)*. arXiv:2605.27879, 2026. https://arxiv.org/abs/2605.27879
- ZYTEK, A. et al. *Explingo: Explaining AI Predictions using Large Language Models*. IEEE BigData 2024; arXiv:2412.05145. https://arxiv.org/abs/2412.05145
- LUKASSEN, F. et al. *Quality Without Usefulness: LLM-Generated XAI Narratives as Trust Heuristics Rather Than Decision Aids*. arXiv:2605.26770, 2026. https://arxiv.org/abs/2605.26770

**Citadas como "a fichar" e que precisam de fichamento**
- SUNDARARAJAN, M.; NAJMI, A. *The Many Shapley Values for Model Explanation*. ICML 2020. https://arxiv.org/abs/1908.08474
- LUNDBERG, S.; LEE, S.-I. *A Unified Approach to Interpreting Model Predictions*. NeurIPS 2017. https://arxiv.org/abs/1705.07874
- MIN, S. et al. *FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation*. EMNLP 2023. https://arxiv.org/abs/2305.14251
- GOU, Z. et al. *CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing*. ICLR 2024. https://arxiv.org/abs/2305.11738
- HUANG, J. et al. *Large Language Models Cannot Self-Correct Reasoning Yet*. ICLR 2024. https://arxiv.org/abs/2310.01798

**Reprodutibilidade de APIs**
- CHEN, L.; ZAHARIA, M.; ZOU, J. *How is ChatGPT's behavior changing over time?* arXiv:2307.09009, 2023. https://arxiv.org/abs/2307.09009
- OUYANG, S. et al. *LLM is Like a Box of Chocolates: the Non-determinism of ChatGPT in Code Generation*. arXiv:2308.02828, 2023. https://arxiv.org/abs/2308.02828
- Groq — Model deprecations. https://console.groq.com/docs/deprecations
- Google — Gemini API deprecations. https://ai.google.dev/gemini-api/docs/deprecations

**Já no projeto, conferidas**
- LEE, S. et al. BMC Med Inform Decis Mak 25:430, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12659558/
- ZHU, D. et al. arXiv:2608.26109, 2026. https://arxiv.org/abs/2608.26109
- ROESCHL, T. et al. Eur Heart J Digit Health, 2026. https://pmc.ncbi.nlm.nih.gov/articles/PMC13492338/
- ALMARRI, S. et al. *Measuring What LLMs Think They Do: SHAP Faithfulness…* arXiv:2512.00163, 2025. https://arxiv.org/abs/2512.00163
- CEMRI, M. et al. *Why Do Multi-Agent LLM Systems Fail?* NeurIPS 2025 D&B. https://arxiv.org/abs/2503.13657
- NEURON (Chandrasekaran et al.), arXiv:2605.01189, 2026. https://arxiv.org/abs/2605.01189
