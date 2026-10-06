---
titulo: Parecer de banca — correção clínica e epidemiológica (Cardiologia / Epidemiologia Clínica)
avaliador: membro de banca simulado (cardiologista, epidemiologia clínica e prevenção cardiovascular)
data: 2026-09-29
objeto: HEARTPREDICT — PREVENT-ASCVD 10 anos + Diretriz SBC 2025 + CKD-EPI 2021 + atribuição de Shapley + explicação por LLM
anexos: tcc/05-banca/anexos/cardiologia/ (verificacoes.py, saida-verificacoes.txt, saida-gateway.txt)
---

# Parecer de banca: correção clínica e epidemiológica

## 1. Parecer resumido e veredito

O núcleo de cálculo está **correto**. Reimplementei a equação PREVENT-ASCVD de 10 anos de forma independente, a partir da forma da Tabela S12 e sem usar `prevent._termos`. Nas 24 vinhetas, a diferença máxima para o projeto foi de **3,6 × 10⁻¹⁵ pontos percentuais**. O caso publicado por Khan et al. (3,6% e 6,0%) é reproduzido, e a CKD-EPI 2021 confere com Inker et al. até o arredondamento. As regras da Tabela 4.1 (cortes de 5% e 20%, agravante que sobe uma categoria, LDL-c 160–189 e ≥ 190) e as metas da Tabela 5.1 estão transcritas sem erro. O projeto também é incomumente honesto: coeficientes marcados como provisórios, texto de IA rotulado como "não verificado" e limites declarados na própria tela.

O problema está na **camada que fala com o paciente**. O projeto é todo sobre fidelidade da explicação, mas a explicação exibida hoje tem um risco clínico real:

- **"Uso de estatina" aparece na lista "Aumentaram o seu risco"** sempre que o não-HDL passa de cerca de 195 mg/dL. Isso vale para os dois sexos e todas as idades (varredura §6.3, saída do gateway §6.5). O texto "Como ler" não fala de estatina. Ele só explica o anti-hipertensivo, e fica recolhido.
- **"Uso de anti-hipertensivo" aparece sempre como "aumentou"** (φ ≈ +0,16 a +0,25). Isso inclui a paciente com pressão controlada (PAS 118). A frase "Não pare nenhum remédio" só é vista por quem abre o "Como ler".
- **O prompt do LLM não tem nenhuma instrução sobre medicamentos.** O texto é gerado com temperatura 0,7 e mostrado ao paciente sem verificador (o próprio projeto declara isso).

Há ainda lacunas de escopo em relação à diretriz: aterosclerose subclínica, Lp(a) > 180 mg/dL e LDL-c não informado com não-HDL muito alto. Há também uma escala de categoria que diz "Alto: 20% ou mais em 10 anos — Sua categoria" a um paciente com risco de 7,1%. Por fim, a discussão de validade externa **ignora a validação do PREVENT no ELSA-Brasil** (Pedroso et al., 2025), que é justamente a melhor resposta à pergunta mais previsível da banca.

**Veredito: APROVARIA COM RESSALVAS.** Como TCC de Engenharia de Computação, o trabalho é sólido, rastreável e tecnicamente correto no cálculo. As ressalvas C1 e C2 (seção 4) devem ser corrigidas **antes de qualquer demonstração com usuários reais**, e as ressalvas Maiores devem ser corrigidas ou declaradas como limitação no texto final. Não aprovaria o uso da interface com pacientes no estado atual.

## 2. Notas por critério (0–10)

| Critério | Nota | Justificativa |
|---|---|---|
| Correção do cálculo | **8,5** | Reprodução exata do caso publicado; reimplementação independente idêntica (§6.1–6.2); CKD-EPI 2021 correta (§6.4); faixas de derivação corretas. Descontos: (a) os coeficientes vêm do `preventr` e ainda não foram conferidos com a Tabela S12; (b) o único caso publicado é **feminino**, e nele estatina, diabetes, TFGe < 60 e as interações correspondentes valem zero, de modo que **8 dos 20 coeficientes não nulos do modelo feminino de DCVA e todo o modelo masculino** não têm verificação contra fonte primária; (c) jovens saudáveis com TFGe calculada > 140 são recusados (§6.4). |
| Fidelidade à diretriz | **7,0** | Tabela 4.1 e Tabela 5.1 corretas; exclusão de diabetes, DCV prévia e idade fora de 30–79 correta; ambiguidades documentadas (D010). Faltam: aterosclerose subclínica (CAC > 100 ou > 300, placa, aneurisma de aorta), Lp(a) > 180 → alto, tratamento de LDL-c ausente, regra de ordem LDL × agravante e dois fatores femininos da Tabela 4.3. |
| Segurança dos textos ao paciente | **5,0** | A maioria das frases está correta ("12 por 8 → 120", definições de agravantes, metas, 30%/50%). Mas estatina e anti-hipertensivo são apresentados como fatores que "aumentaram o seu risco", a mitigação fica escondida e o LLM não tem guarda-corpos (C1, C2). |
| Comunicação de risco | **7,0** | Risco absoluto, frequência natural e pictograma antropomórfico seguem a evidência (Zipkin 2014; Galesic 2009; Zikmund-Fisher 2014). Descontos: a escala mostra a faixa percentual da categoria mesmo quando a categoria veio de reclassificação (M1); o arredondamento produz "cerca de 5 em 100" com categoria "menos de 5%" (m1); não há risco em 30 anos para jovens. |
| Validade externa | **6,0** | A limitação "dados dos EUA" é declarada na tela e no fichamento, mas o projeto afirma que o escore é "não validado em brasileiros" sem citar a validação no ELSA-Brasil (C = 0,76; P/O = 1,21) nem as validações na Ásia e no Oriente Médio, que mostram superestimação e necessidade de recalibração (M6). |
| Honestidade das limitações | **8,0** | Coeficientes "PROVISORIO" no JSON; pendência T1; aviso "ainda não passa pelo verificador"; bloco "Limites deste resultado"; D010 declara que o gabarito é operacionalização. Desconto: D010 afirma que o gabarito "não precisa de validação clínica externa". Isso vale para o experimento de fidelidade, **não** para uma interface exposta ao paciente. |

## 3. Pontos fortes (com evidência)

1. **Equação implementada corretamente.** Termos centrados, splines (PAS com nó em 110; TFGe com nó em 60), interações de tratamento e de idade e a conversão de 38,67 mg/dL por mmol/L estão todos certos (`experimentos/piloto/prevent.py:83-101`; Khan 2024, Statistical Analysis, `khan2024prevent.txt:40`). O resultado da reimplementação é idêntico (§6.2).
2. **Desfecho correto para a SBC.** O projeto usa PREVENT-**ASCVD** e não DCV total, como manda a seção 4.2 da diretriz ("risco de evento cardiovascular aterosclerótico em 10 anos pelo escore PREVENT", `sbc2025dislipidemias.txt:774`). Isso está registrado em D009.
3. **IMC tratado com fidelidade ao artigo e não à descrição resumida da diretriz.** O IMC tem coeficiente 0 no modelo de DCVA (Khan 2024; `coeficientes_prevent_base_10a.json`), há teste unitário para isso (`test_prevent.py:361-364`), e a inconsistência da diretriz está documentada (fichamento SBC, item 5).
4. **Faixas de derivação corretas e recusa em vez de extrapolação.** Idade 30–79, CT 130–320, HDL 20–100, PAS 90–200 e IMC < 40 (`prevent.py:39-46`; Khan 2024, Methods). A mensagem de recusa é clara.
5. **CKD-EPI 2021 sem raça correta.** As constantes 142, κ 0,7/0,9, α −0,241/−0,302, −1,200, 0,9938^idade e 1,012 (`renal.py:227-235`) conferem com Inker et al. 2021, com erro ≤ 0,5 por arredondamento (§6.4). Também é a mesma equação usada na derivação do PREVENT.
6. **Tabela 4.1 e Tabela 5.1 transcritas sem erro** (`sbc.py:169-173` × `sbc2025dislipidemias.txt:954-960`). A ambiguidade "> 160-189" foi resolvida pelo texto da seção 4.1 ("entre 160 e 189", linha 757). O erro de digitação "> 40" no risco extremo foi identificado. A tensão entre regra e julgamento para os agravantes (Tabela 4.1 × seção 4.3, linha 777) foi reconhecida, com análise de sensibilidade prevista (D010).
7. **Critérios de exclusão logo no início e bem redigidos** (`perguntas.js:13-34`). O texto sobre DCV prévia ("risco muito alto") está correto pela Tabela 4.1.
8. **Comunicação de risco baseada em evidência.** Risco absoluto, frequência natural, pictograma de figuras humanas com eventos agrupados, escala sequencial segura para daltonismo e ausência de contagem animada do número (`interface-design.md` §3.4, §5, §6).
9. **Transparência sobre a IA e os limites.** Selo "Texto gerado por inteligência artificial", aviso de ausência do verificador e a frase "Se algo no texto divergir dos números, considere os números" (`Resultado.jsx:421-452`), além do bloco "Limites deste resultado" (`TelaResultado.jsx:300-308`).
10. **Dicas de conteúdo clínico corretas:** "12 por 8 → 120" (`perguntas.js:112`), Lp(a) ≥ 50 mg/dL ou 125 nmol/L e PCR-us ≥ 2 mg/L (`perguntas.js:171-172`, iguais à Tabela 4.3), idade de corte da história familiar (55/65) e lista de doenças inflamatórias crônicas.

## 4. Problemas

### Críticos

**C1 — Medicamentos preventivos apresentados ao paciente como fatores que "aumentaram o seu risco".**
- **Evidência:**
  - Varredura (§6.3): φ(estatina) fica **positivo** para não-HDL ≥ ~195 mg/dL, nos dois sexos e em todas as idades (ex.: homem, não-HDL 235 → +0,061; 275 → +0,120). A causa é o termo estatina × não-HDL (β = +0,084 F / +0,115 M), que supera o efeito principal (−0,059 / −0,087).
  - Saída real do gateway (§6.5, `anexos/cardiologia/saida-gateway.txt`): homem de 62 anos com estatina e não-HDL 238 → `"uso de estatina", "direcao": "aumentou"`. Mulher de 58 anos com estatina e anti-hipertensivo → **os dois** em "aumentou".
  - φ(anti-hipertensivo) fica entre +0,16 e +0,25 **para qualquer PAS** (§6.3). A mulher de 45 anos com PAS 118 controlada vê "Uso de anti-hipertensivo" em "Aumentaram o seu risco".
  - A mitigação está em um `<details>` fechado por padrão (`Resultado.jsx:403-416`) e fala **só** do anti-hipertensivo. Não há nenhuma frase sobre estatina.
  - No próprio modelo, com mesma PAS e mesmo não-HDL, usar anti-hipertensivo aumenta o risco estimado de 3,26% para 3,98% (F) e usar estatina de 3,26% para 3,49% (§6.3, bloco 5). O coeficiente captura **confusão por indicação**: quem usa o remédio tem hipertensão ou dislipidemia de base. Não é efeito do fármaco.
- **Impacto clínico:** a baixa adesão a estatina e a anti-hipertensivos já é o principal problema da prevenção no Brasil. Só 6,7% dos adultos pós-IAM/AVC na ESF usavam estatina (SBC 2025, seção 2.3). Uma interface que diz ao leigo que "usar estatina aumentou o seu risco" pode levar à **interrupção do tratamento**. Esse dano é plausível, grave e evitável.
- **Correção recomendada:**
  1. **Agrupar as variáveis na atribuição**: "pressão arterial" = {PAS, anti-hipertensivo} e "colesterol" = {não-HDL, estatina}, usando Shapley de grupos (valores de Owen ou jogadores agregados). O grupo tem interpretação clínica, e as interações passam a ficar dentro do grupo. No caso da PAS 118 tratada, o grupo dá ≈ +0,003 ("pouco influenciou").
  2. Se o agrupamento não for adotado, **nunca exibir medicamento na lista "Aumentaram"**. Nesse caso, mostrar como "Diagnóstico de pressão alta (em tratamento)" ou "Colesterol alto (em tratamento)", com a frase sobre não parar remédios **fora** do recolhível.
  3. Criar um teste unitário que falhe se qualquer medicamento sair com direção "aumentou" no texto ao paciente.

**C2 — Explicação do LLM mostrada ao paciente sem guarda-corpos clínicos e sem verificador.**
- **Evidência:**
  - `prompt.py:396-403`: as regras são "use apenas as informações", "contribuição positiva = aumentou o risco" e "recomende conversar com o médico". **Não há** nenhuma instrução para não sugerir iniciar, parar ou trocar medicamentos, não citar doses nem fármacos, não reinterpretar a categoria, ou explicar que medicamento com contribuição positiva é marcador de doença.
  - Ao contrário: o prompt manda explicar a direção de cada fator, o que **induz** a frase "o uso de anti-hipertensivo aumentou seu risco".
  - `avaliacao.py:132`: `temperatura=0.7`, `"verificado": False`.
  - Não consegui gerar texto no ambiente (`/explicacao` → 503, sem `.env`; `saida-gateway.txt`). O risco decorre do desenho do prompt e da ausência do verificador, que o próprio projeto declara (D025).
- **Impacto:** o texto livre é o que o leigo mais lê. Os erros que o TCC pretende medir (polaridade, número, categoria) aparecem ao paciente justamente na única configuração em que ninguém os bloqueia.
- **Correção:**
  1. Acrescentar ao prompt regras de segurança: não recomendar começar, parar ou mudar remédio; não citar fármacos nem doses; explicar que remédio com contribuição positiva indica a condição tratada; frase fixa "não interrompa medicamentos sem orientação médica".
  2. Até o verificador existir, aplicar no mínimo um **filtro determinístico** que bloqueie o texto que associe estatina ou anti-hipertensivo a "aumentou" ou "piorou", ou que traga número diferente de `risco_pct`. Ou exibir a explicação só no modo de pesquisa.
  3. Usar temperatura baixa na interface; a 0,7 pode ficar para o experimento, onde a variabilidade é objeto de estudo.

### Maiores

**M1 — A escala de categoria atribui ao paciente uma faixa de risco que não é a dele.**
- **Evidência:** `Resultado.jsx:343-366` rotula cada categoria com a faixa do escore ("Alto — 20% ou mais em 10 anos") e marca "Sua categoria". Na captura `04-evidencias/interface/desk-08-resultado.png`, o risco é **7,1%** e a escala diz "Alto — 20% ou mais em 10 anos — Sua categoria". O parágrafo de reclassificação logo abaixo atenua, mas as duas mensagens se contradizem visualmente.
- **Impacto:** superestimação percebida de quase 3 vezes e ansiedade. Também confunde "categoria de conduta" com "probabilidade".
- **Correção:** quando houver reclassificação, trocar o rótulo da faixa por "Alto (por agravante ou LDL)", ou mostrar só os nomes das categorias. Escrever explicitamente: "a categoria define a meta de tratamento; o seu risco calculado continua 7,1%".

**M2 — O escopo não exclui aterosclerose subclínica nem hipercolesterolemia familiar.**
- **Evidência:** a SBC só autoriza o escore "para os adultos sem evento cardiovascular pregresso **ou aterosclerose subclínica**, sem DM e com LDL-c < 160" (`sbc2025dislipidemias.txt:757`). A Tabela 4.1 classifica placa carotídea < 50%, CAC > 100 UA ou percentil > 75, placa na angiotomografia e **aneurisma de aorta abdominal** como **alto**, e CAC > 300 UA ou obstrução ≥ 50% como **muito alto** (linhas 764-765; Tabela 4.4, linhas 848-852). A pergunta sobre DCV prévia (`perguntas.js:60-66`) cita angina, ponte, stent e doença arterial periférica, mas não exames de imagem. O D011 diz "sem aterosclerose subclínica", mas nada na interface garante isso.
- **Impacto:** uma pessoa com CAC de 400 e escore de 3% recebe "baixo, meta LDL < 115", quando a diretriz manda "muito alto, meta < 50". A meta fica mais que o dobro da correta.
- **Correção:** criar uma pergunta de exclusão ("Algum exame já mostrou placa nas artérias, cálcio nas coronárias ou aneurisma da aorta?" → fora do escopo, com texto próprio). Fazer o mesmo para diagnóstico de hipercolesterolemia familiar.

**M3 — Lp(a) > 180 mg/dL (> 390 nmol/L) não classifica como alto.**
- **Evidência:** Tabela 4.1, categoria Alto: "Lipoproteína(a) > 180 mg/dL (> 390 nmol/L)" (linha 764). Seção 4.4.1: "Níveis muito elevados, acima de 180 mg/dL ou 390 nmol/L, indicam alto risco" (linha 826). O projeto só tem o agravante binário `lpa_elevada` ≥ 50 (`sbc.py:181`, `perguntas.js:171`). O caso "escore < 5% + Lp(a) elevada" dá intermediário (§6.6).
- **Correção:** perguntar o valor de Lp(a) (ou oferecer duas opções, 50–180 e > 180) e implementar a regra "> 180 → alto".

**M4 — LDL-c não informado com não-HDL muito alto: o escore é aplicado fora do domínio da diretriz.**
- **Evidência:** o LDL é opcional (`perguntas.js:98-107`). Com CT 300 e HDL 45 (não-HDL 255), sem LDL, o gateway devolve **baixo, 3,3%, meta < 115** (`saida-gateway.txt`, 4º caso). Com não-HDL de 255, o LDL-c muito provavelmente é ≥ 190, e a diretriz exige classificar como **alto** e não usar o escore (seção 4.1).
- **Correção:** tornar o LDL obrigatório quando o não-HDL for ≥ 190 mg/dL, ou alertar e recusar. Uma alternativa é estimar o LDL pela equação de Martin/Hopkins, recomendada pela SBC (fichamento §5), mas isso exige triglicerídeos.

**M5 — Coeficientes masculinos e metade dos termos femininos sem verificação contra fonte primária.**
- **Evidência:**
  - A origem é o `preventr` v0.12.0 (`coeficientes_prevent_base_10a.json`, `_origem.status: PROVISORIO`; pendência T1).
  - Os 6 valores publicados são todos do caso feminino (`test_prevent.py:330-349`).
  - No caso publicado, valem zero: diabetes, estatina, estatina × não-HDL, TFGe < 60, TFGe ≥ 60 (TFGe = 90), PAS < 110, idade × diabetes e idade × TFGe. Um erro de transcrição nesses termos, ou em qualquer coeficiente masculino, **passaria nos testes**.
  - Os coeficientes femininos de DCVA coincidem com os que conheço da Tabela S12, mas o parecer não pode substituir a fonte.
- **Risco:** é aceitável para um protótipo acadêmico, desde que (i) a Tabela S12 seja obtida e comparada automaticamente antes da defesa e (ii) haja testes com pelo menos 10 perfis masculinos e perfis com diabetes (modelo), estatina e TFGe < 60, conferidos contra a calculadora oficial da AHA. Sem isso, não é aceitável declarar "implementação validada".

**M6 — A validade externa está subdiscutida e omite evidência brasileira existente.**
- **Evidência:** o fichamento da SBC diz "Adota um escore **não validado em brasileiros**" (Leitura crítica). O fichamento do PREVENT e a tela só citam "dados dos EUA". Porém:
  - **Pedroso et al., 2025** (Am J Prev Cardiol; ELSA-Brasil, n = 11.077) validaram o PREVENT-ASCVD em brasileiros sem recalibração: **C = 0,76 (IC95% 0,72–0,80)**, **razão predito/observado = 1,21** (superestimação de 21%, contra 57% do escore da OMS) e NRI de 0,19 a favor do PREVENT.
  - Em outras populações, o desempenho foi pior: na China (CHARLS, n = 10.068, ≥ 45 anos), C ≈ 0,61–0,62, com inclinações de calibração de 0,47–0,51 e superestimação sistemática (Fan et al., Sci Rep 2026). Nos Emirados Árabes (n = 897), a discriminação foi boa em mulheres (C 0,81–0,82), com subestimação em mulheres e calibração irregular em homens; os autores recomendam recalibração (Al-Shamsi & Govender, BMC Cardiovasc Disord 2025). Há também uma validação nacional coreana (Am J Prev Cardiol 2025).
- **Impacto:** a banca vai perguntar "funciona no Brasil?". Hoje o projeto responderia "não se sabe", quando a resposta correta é mais precisa e mais favorável: há uma validação em coorte brasileira, com discriminação boa e superestimação moderada, relevante perto do corte de 5%.
- **Correção:** incluir Pedroso 2025 no fichamento e no texto. Discutir que, com P/O ≈ 1,2, parte dos pacientes com risco calculado entre 5% e 6% teria risco observado < 5%, o que afeta a classificação. Registrar a recalibração como trabalho futuro. Ajustar a frase da tela para: "Foi desenvolvida nos EUA; um estudo brasileiro (ELSA-Brasil) mostrou bom desempenho, com tendência a superestimar o risco."

**M7 — A ordem das regras muda a categoria no caso LDL 160–189 + agravante com escore < 5%.**
- **Evidência:** `sbc.py:205-219` aplica o agravante antes da regra do LDL. O caso "escore 3% + LDL 170 + história familiar" sai **intermediário** (§6.6). Pela Tabela 4.1, porém, LDL 160–189 já define "intermediário", e "pacientes classificados como risco intermediário, com presença de fator agravante" são **alto** (linhas 763-764). A meta muda de < 100 para < 70.
- **Correção:** documentar essa ambiguidade no D010 (hoje ela não consta) e escolher uma regra explícita. Minha recomendação: aplicar primeiro os pisos (LDL, Lp(a) > 180) e depois a promoção por agravante, o que é coerente com a redação da Tabela 4.1. Incluir o caso na análise de sensibilidade.

### Menores

| # | Problema | Evidência | Correção |
|---|---|---|---|
| m1 | Arredondamento incoerente: com risco de 4,6% a tela diz "cerca de **5** em 100" e a categoria diz "menos de 5%"; com 19,5% diz "cerca de 20" e a categoria é intermediário | `avaliacao.py:100` usa `round`; §6.7 | Mostrar uma casa decimal na frase ("cerca de 4 a 5") ou usar "em 1.000 pessoas" para riscos baixos |
| m2 | TFGe calculada > 140 recusa jovens saudáveis (homem de 30 anos, Cr 0,5 → 141 → "fora da faixa"), com mensagem sobre um valor que o usuário não digitou | §6.4; `saida-gateway.txt` | Truncar em 140 com nota, ou mensagem específica ("sua função renal é normal/alta") |
| m3 | Não há checagem de LDL-c > não-HDL-c (impossível fisiologicamente); LDL 250 com não-HDL 150 dá "alto" | `saida-gateway.txt` (3º caso); `validacao.js` não cruza campos | Recusar LDL > CT − HDL |
| m4 | O backend aceita "fator específico da mulher" para o sexo masculino e descarta agravantes desconhecidos em silêncio | `avaliacao.py:76`; `saida-gateway.txt` | Validar sexo × agravante e recusar código inválido |
| m5 | Fatores femininos incompletos: faltam menarca **tardia (≥ 17 anos)** e **restrição de crescimento intrauterino** | `perguntas.js:169` × Tabela 4.3 (linha 785) | Completar a dica |
| m6 | "Remédio para baixar o colesterol" inclui ezetimiba e fibrato; a variável do PREVENT é **estatina** | `perguntas.js:127-133` | Perguntar "Você toma **estatina**?" e manter os exemplos |
| m7 | "TFG estimada" do laudo pode vir da CKD-EPI 2009 com coeficiente racial (ainda comum no Brasil), cerca de 16% maior em quem é marcado como negro | `perguntas.js:143-156` | Preferir a creatinina; na dica, pedir TFGe "CKD-EPI 2021" |
| m8 | PAS de uma única medida, sem orientação; o PREVENT usa medida de consultório | `perguntas.js:109-118` | "Use a média de duas medidas feitas em repouso" (Diretriz Brasileira de HA 2020) |
| m9 | Para o risco **baixo**, a meta aparece sem contexto; a SBC indica fármaco no baixo risco só se o LDL-c for persistentemente ≥ 145 apesar do estilo de vida | `TelaResultado.jsx:269-288` × `sbc2025dislipidemias.txt:963,976` | No baixo risco: "tratamento com remédio só é indicado se o LDL continuar ≥ 145 apesar de mudanças no estilo de vida" |
| m10 | Em quem já usa estatina, o LDL informado é **sob tratamento**; a regra LDL ≥ 190 e a "redução de 30/50%" pressupõem o valor basal | `sbc.py:212-219` | Nota na tela e na regra |
| m11 | "Como ler" omite a TFGe 90 da pessoa de referência (o prompt inclui) e não diz que a própria referência tem risco de ~2–3% (F 2,15%, M 2,93%) | `Resultado.jsx:405-409` | Completar |
| m12 | Jovens: a idade "diminuiu" o risco e o escore de 10 anos é baixo mesmo com fatores descontrolados. A SBC sugere o risco em 30 anos para conscientização (seção 4.9, linha 929) | V01, V03, V24 | Mostrar mensagem de risco ao longo da vida para menores de 45 anos com fatores alterados |
| m13 | Texto de exclusão para ≥ 80 anos não informa que a SBC trata essa faixa como de alto risco quase sempre (seção 4.8, linha 924) | `perguntas.js:14-20` | Acrescentar a frase |
| m14 | D010 diz que o gabarito "não precisa de validação clínica externa"; isso vale para o experimento, não para a interface ao paciente | `decisoes.md` D010 | Delimitar a afirmação ao experimento |
| m15 | Síndrome metabólica e PCR-us: o leigo raramente sabe o diagnóstico; a PCR-us deve ser medida fora de quadro inflamatório agudo | `perguntas.js:165,172` | Acrescentar as dicas |

## 5. Perguntas da banca

| # | Pergunta | O que a boa resposta deve conter | O projeto responde hoje? |
|---|---|---|---|
| 1 | Por que PREVENT-ASCVD e não DCV total ou o escore da OMS/Globorisk-LAC calibrados para o Brasil? | SBC 2025 §4.2 recomenda o PREVENT para DCVA (FORTE/ALTA); OMS e Globorisk-LAC "podem ser utilizados"; o PREVENT inclui TFGe e estatina e tem calibração superior no ELSA-Brasil (Pedroso 2025) | **Parcial**: D009 e fichamento SBC; falta Pedroso 2025 |
| 2 | O PREVENT funciona em brasileiros? | ELSA-Brasil: C 0,76, P/O 1,21; superestimação moderada; implicação no corte de 5%; populações asiáticas com pior desempenho; recalibração como trabalho futuro | **Não**: o fichamento diz "não validado em brasileiros" |
| 3 | Como vocês garantem que os coeficientes estão certos, se a Tabela S12 não foi obtida? | Reprodução dos 6 valores publicados; reimplementação independente; comparação com a calculadora AHA em perfis masculinos, com diabetes, estatina e TFGe < 60; conferência com a S12 | **Parcial**: só o caso feminino (`test_prevent.py`); pendência T1 aberta |
| 4 | O paciente que usa estatina vê "uso de estatina aumentou seu risco". O que ele deve fazer? | Reconhecer o problema; confusão por indicação; agrupamento {não-HDL, estatina}; frase de segurança visível; teste que impede "medicamento aumentou" | **Não**: o "Como ler" só trata o anti-hipertensivo, e fica recolhido |
| 5 | Por que a pessoa de referência tem 55 anos e não um perfil "ideal"? Isso não induz falsa tranquilidade em jovens? | É a centralização do modelo e dá gabarito exato (D012); a escolha da referência muda sinais; alternativas: perfil ideal, média populacional brasileira; risco em 30 anos para jovens | **Parcial**: D012 justifica pela exatidão; nada sobre o efeito clínico |
| 6 | Como fica o paciente com CAC de 400 ou placa carotídea? | O escore não se aplica (SBC §4.1); muito alto/alto pela Tabela 4.1; o projeto deve excluir | **Não**: D011 cita, mas a interface não pergunta |
| 7 | Um agravante sempre sobe uma categoria? A diretriz não pede julgamento? | Tabela 4.1 (regra) × §4.3 (julgamento, Figura 4.2); operacionalização declarada; análise de sensibilidade | **Sim**: D010 e fichamento SBC, itens 3 e 6 |
| 8 | E se o LDL não for informado e o não-HDL for 250? | O escore só vale com LDL < 160; exigir o LDL, recusar ou estimar | **Não** (M4) |
| 9 | O paciente com 7% de risco e categoria "alto" entende que tem ≥ 20% de risco? | Diferença entre categoria de conduta e probabilidade; a escala precisa refletir a reclassificação | **Parcial**: há o parágrafo de reclassificação, mas a escala contradiz |
| 10 | Por que frequência natural e pictograma? Existe evidência em população brasileira de baixo letramento? | Zipkin 2014; Galesic 2009; Zikmund-Fisher 2014; ausência de teste com usuários brasileiros (declarada) | **Sim** para a evidência (`interface-design.md` §5); **Não** para teste com usuários (§8) |
| 11 | A CKD-EPI 2021 sem raça é a adequada? E se o laudo trouxer a 2009? | Inker 2021; é a mesma equação da derivação do PREVENT; a TFGe da 2009 com raça superestima em negros | **Parcial**: correta no código; não trata o laudo com a 2009 |
| 12 | Um texto não verificado, com temperatura 0,7, pode ser mostrado a pacientes? | Não, sem ao menos um filtro determinístico e regras de segurança no prompt; justificar a transição (D025) e limitar ao modo de pesquisa | **Parcial**: há o aviso na tela; faltam guarda-corpos |
| 13 | O risco de 4,9% e o de 5,1% têm condutas diferentes. Qual a incerteza do número? | O intervalo do modelo não é reportado; P/O de 1,21 no Brasil; a categoria perto do corte deve ser comunicada como limítrofe | **Não** |
| 14 | O que o sistema diz a quem já usa estatina sobre a meta e a redução de 30/50%? | A redução é sobre o LDL basal; o LDL informado está sob tratamento; nota específica | **Não** (m10) |

## 6. Verificações executadas

Script: `tcc/05-banca/anexos/cardiologia/verificacoes.py`. Saída integral: `saida-verificacoes.txt`. Chamadas ao gateway em execução (`http://127.0.0.1:8000`): `saida-gateway.txt`.

### 6.1 Testes do projeto
`cd experimentos/piloto && python3 -m unittest test_prevent` → **7 testes, OK** (caso publicado não fumante e fumante; eficiência do Shapley; IMC não altera a DCVA; tabagismo positivo; recusa de dado ausente e fora de faixa).

### 6.2 PREVENT recalculado (reimplementação independente)
| Caso | Publicado (Khan 2024) | Independente | Projeto |
|---|---|---|---|
| F 50, CT 240, HDL 55, PAS 160 tratada, TFGe 90, não fumante | 3,6% | 3,64% | 3,6% |
| idem, fumante | 6,0% | 5,99% | 6,0% |
| 24 vinhetas (V01–V24) | — | máx. \|Δ\| = **3,6 × 10⁻¹⁵ p.p.** | — |

Exemplos: V06 (M 58) 4,91% → baixo; V13 (M 74, fumante, tratado) 21,08% → alto; V14 (F 72) 10,64% → intermediário. Pessoa de referência (todos os termos = 0): **F 2,15%, M 2,93%**.

### 6.3 Sinal das atribuições de medicamentos
| Perfil (idade indiferente) | não-HDL 115 | 155 | 195 | 235 | 275 |
|---|---|---|---|---|---|
| φ(estatina), F | −0,081 | −0,038 | **+0,006** | **+0,050** | **+0,093** |
| φ(estatina), M | −0,117 | −0,057 | **+0,002** | **+0,061** | **+0,120** |

φ(anti-hipertensivo): **sempre positivo**, de +0,163 (M, PAS 180) a +0,246 (F, PAS 110).

Efeito no próprio modelo (mesma PAS 140 e mesmo CT 240): F 3,26% → 3,98% com anti-hipertensivo e 3,49% com estatina; M 4,61% → 5,50% e 5,02%.

### 6.4 CKD-EPI 2021 (Inker 2021: 142 × min(Scr/κ,1)^α × max(Scr/κ,1)^−1,200 × 0,9938^idade × 1,012[F])
| Cr (mg/dL) | Idade | Sexo | Projeto | Independente | Situação |
|---|---|---|---|---|---|
| 0,7 | 50 | F | 105 | 105,3 | OK |
| 0,9 | 50 | M | 104 | 104,0 | OK |
| 1,0 | 60 | F | 64 | 64,5 | OK |
| 1,2 | 60 | M | 69 | 69,2 | OK |
| 2,0 | 70 | M | 35 | 35,2 | OK |
| 0,5 | 30 | M | 141 | 140,7 | **recusado (> 140)** |
| 0,3 | 30 | F | 146 | 146,3 | **recusado (> 140)** |

### 6.5 Gateway (saída real, resumida)
- M 62, estatina, CT 280/HDL 42, PAS 128 → 8,7%, intermediário; **"uso de estatina: aumentou" (+0,066)**.
- F 58, estatina + anti-hipertensivo, CT 290/HDL 50 → 4,7%, baixo; **anti-hipertensivo +0,233 "aumentou"; estatina +0,055 "aumentou"**.
- F 45, anti-hipertensivo, PAS 118 → 0,9%; **anti-hipertensivo +0,238 "aumentou"** e PAS −0,235 "diminuiu" (a soma ≈ 0).
- M 30, Cr 0,5 → 422 "TFGe de 141 ... fora da faixa".
- M 50, LDL 250 com não-HDL 150 e "fator específico da mulher" → aceito, "alto".
- F 58, CT 300/HDL 45 (não-HDL 255), sem LDL → **baixo, 3,3%, meta < 115**.
- `/explicacao` → 503 (LLM não configurado); o texto do LLM não pôde ser auditado empiricamente.

### 6.6 Regras SBC: código × diretriz
| Item da diretriz (texto PT) | Código | Situação |
|---|---|---|
| Baixo < 5%, intermediário 5 a < 20%, alto ≥ 20% (Tab. 4.1, l. 762-764) | `sbc.py:197-202` | Correto |
| Agravante: baixo → intermediário; intermediário → alto (Tab. 4.1) | `sbc.py:205-210` | Correto (operacionalização D010) |
| LDL-c 160–189 → intermediário (§4.1 "entre 160 e 189", l. 757) | `sbc.py:217` (como piso) | Correto |
| LDL-c ≥ 190 → alto (Tab. 4.1; §4.1) | `sbc.py:214` | Correto |
| Aterosclerose subclínica → alto / CAC > 300 → muito alto (Tab. 4.1, 4.4) | — | **Ausente** (M2) |
| Lp(a) > 180 mg/dL → alto (Tab. 4.1; §4.4.1, l. 826) | só agravante ≥ 50 | **Ausente** (M3) |
| Escore só com LDL < 160 (§4.1) | LDL opcional | **Parcial** (M4) |
| DM2 → Tabelas 4.5–4.8 | recusa (fora do escopo) | Correto para o escopo |
| DCV prévia → muito alto/extremo | recusa | Correto |
| Idade ≥ 80: alto quase sempre (§4.8) | recusa | Aceitável (m13) |
| Metas LDL 115/100/70; não-HDL 145/130/100; redução 30/30/50% (Tab. 5.1, l. 956-958; l. 965-966) | `sbc.py:169-173` | Correto |
| Baixo risco: fármaco se LDL ≥ 145 persistente (l. 963, 976) | — | Não comunicado (m9) |
| Agravantes da Tab. 4.3 (l. 781-787) | 7 opções | Faltam menarca ≥ 17 e RCIU (m5) |

Casos de fronteira do motor: "escore 3% + LDL 170 + agravante" → intermediário (a Tabela 4.1 sugere alto; M7). "3 agravantes" → sobe uma só categoria (coerente com D010; a seção 4.3 admitiria mais).

### 6.7 Frequência natural
| Risco | "em 100 pessoas" | Categoria |
|---|---|---|
| 4,6% | 5 | baixo (< 5%) |
| 4,9% | 5 | baixo |
| 19,5% | 20 | intermediário |

### 6.8 Textos ao paciente conferidos
| Frase | Situação |
|---|---|
| "Se sua pressão foi 12 por 8, digite 120" | Correta (convenção brasileira em cmHg) |
| História familiar "homens antes dos 55 ou mulheres antes dos 65" | Correta (Tab. 4.3) |
| Lp(a) ≥ 50 mg/dL (125 nmol/L); PCR-us ≥ 2 mg/L | Corretas |
| DCV prévia = "risco muito alto" | Correta (Tab. 4.1) |
| Diabetes usa "idade, tempo de diagnóstico, rins e olhos" | Correta (Tabelas 4.5–4.8) |
| "reduzir o LDL em pelo menos 30%/50%" | Correta (§5.1) |
| Metas LDL e não-HDL por categoria | Corretas |
| "Em 100 pessoas com os mesmos dados, cerca de N teriam infarto ou AVC" | Adequada. O desfecho inclui morte coronária e AVC (Khan 2024, l. 30). Ver m1 |
| "Usar remédio para pressão pode aparecer como fator que aumentou…" | Correta, mas recolhida; **não cobre estatina** (C1) |
| "A equação PREVENT foi desenvolvida com dados dos EUA" | Correta, mas incompleta (M6) |

## 7. Referências

- Khan SS et al. Development and Validation of the American Heart Association's PREVENT Equations. *Circulation*. 2024;149(6):430-449. doi:[10.1161/CIRCULATIONAHA.123.067626](https://doi.org/10.1161/CIRCULATIONAHA.123.067626) — [PMC10910659](https://pmc.ncbi.nlm.nih.gov/articles/PMC10910659/)
- Rached FH et al. Diretriz Brasileira de Dislipidemias e Prevenção da Aterosclerose – 2025. *Arq Bras Cardiol*. 2025;122(9):e20250640. doi:[10.36660/abc.20250640](https://doi.org/10.36660/abc.20250640) — [PMC12674852](https://pmc.ncbi.nlm.nih.gov/articles/PMC12674852/)
- Inker LA et al. New Creatinine- and Cystatin C–Based Equations to Estimate GFR without Race. *N Engl J Med*. 2021;385:1737-1749. doi:[10.1056/NEJMoa2102953](https://doi.org/10.1056/NEJMoa2102953)
- Pedroso AF, Brant LCC, Ribeiro ALP, Barreto SM, Figueiredo RC, Khera R. Cardiovascular risk stratification without recalibration: a comparative study of the PREVENT and WHO risk scores in a multiethnic Brazilian cohort. *Am J Prev Cardiol*. 2025. [PMC12849047](https://pmc.ncbi.nlm.nih.gov/articles/PMC12849047/) · [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666667725004672)
- PREVENT vs PCE thresholds for coronary artery calcium referral: detection-optimized strategies in ELSA-Brasil. *Am J Prev Cardiol*. [PMC13329528](https://pmc.ncbi.nlm.nih.gov/articles/PMC13329528/)
- Performance of contemporary cardiovascular risk stratification scores in Brazil: an evaluation in the ELSA-Brasil study. [PMC11168182](https://pmc.ncbi.nlm.nih.gov/articles/PMC11168182/)
- Fan WQ et al. External validation of American Heart Association PREVENT equations in a Chinese population. *Sci Rep*. 2026. [PMC13518984](https://pmc.ncbi.nlm.nih.gov/articles/PMC13518984/)
- Al-Shamsi S, Govender RD. External validation of the American Heart Association's PREVENT equations in predicting ASCVD risk among Arab women and men. *BMC Cardiovasc Disord*. 2025. [PMC12512834](https://pmc.ncbi.nlm.nih.gov/articles/PMC12512834/)
- Global validation of the PREVENT equations: a nationwide cohort study of Korean adults. *Am J Prev Cardiol*. 2025. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666667725001941) (resumo não acessado; citado apenas como existente)
- External Validation of the American Heart Association PREVENT Cardiovascular Disease Risk Equations. *JAMA Netw Open*. 2024. [PMC11470385](https://pmc.ncbi.nlm.nih.gov/articles/PMC11470385/)
- Diao JA et al. Projected Changes in Statin and Antihypertensive Therapy Eligibility With the AHA PREVENT Cardiovascular Risk Equations. *JAMA*. 2024. doi:[10.1001/jama.2024.12537](https://doi.org/10.1001/jama.2024.12537)
- Anderson TS et al. Atherosclerotic Cardiovascular Disease Risk Estimates Using the PREVENT Equations. *JAMA Intern Med*. 2024. doi:[10.1001/jamainternmed.2024.1302](https://doi.org/10.1001/jamainternmed.2024.1302)
- Van Calster B et al. Calibration: the Achilles heel of predictive analytics. *BMC Med*. 2019;17:230. doi:[10.1186/s12916-019-1466-7](https://doi.org/10.1186/s12916-019-1466-7)
- Zipkin DA et al. Evidence-based risk communication: a systematic review. *Ann Intern Med*. 2014;161(4):270-280. doi:[10.7326/M14-0295](https://doi.org/10.7326/M14-0295)
- Galesic M, Garcia-Retamero R, Gigerenzer G. Using icon arrays to communicate medical risks: overcoming low numeracy. *Health Psychol*. 2009;28(2):210-216. doi:[10.1037/a0014474](https://doi.org/10.1037/a0014474)
- Zikmund-Fisher BJ et al. Blocks, ovals, or people? Icon type affects risk perceptions and recall of pictographs. *Med Decis Making*. 2014;34(4):443-453. doi:[10.1177/0272989X13511706](https://doi.org/10.1177/0272989X13511706)
- Lundberg SM, Lee S-I. A Unified Approach to Interpreting Model Predictions. NeurIPS 2017. [arXiv:1705.07874](https://arxiv.org/abs/1705.07874)
- Barroso WKS et al. Diretrizes Brasileiras de Hipertensão Arterial – 2020. *Arq Bras Cardiol*. 2021;116(3):516-658. doi:[10.36660/abc.20201238](https://doi.org/10.36660/abc.20201238)
- AHA PREVENT Calculator: <https://professional.heart.org/en/guidelines-and-statements/prevent-calculator>
- Pacote R `preventr` (CRAN): <https://cran.r-project.org/package=preventr>

> Observação de método: a busca na internet foi interrompida por limite de uso depois das consultas acima. Os números de Pedroso 2025, Fan 2026 e Al-Shamsi 2025 foram extraídos das páginas do PMC. O estudo coreano está citado apenas como existente, porque o texto não pôde ser acessado (HTTP 403).
