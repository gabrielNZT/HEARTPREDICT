---
titulo: Parecer de banca — Interação Humano-Computador (nova interface)
avaliador: membro da banca, área de IHC (UX, acessibilidade, comunicação de risco em saúde)
data: 2026-09-29
objeto: interface refeita em 29/09/2026 (frontend/src, frontend/index.html, frontend/public/marca.svg) e tcc/03-metodologia/interface-design.md
anexos: tcc/05-banca/anexos/ihc/ (scripts, logs e capturas; todos os testes podem ser reproduzidos)
---

# Parecer de IHC: nova interface do HeartPredict

## 1. Parecer resumido e veredito

A nova interface é um salto de qualidade real em relação à anterior. O conceito "laudo claro" é coerente. A tipografia foi escolhida com critério, a paleta é sóbria e quase todos os contrastes que o documento declara batem com o recálculo (seção 6.2). O fluxo segue de fato o padrão GOV.UK de uma pergunta por tela, e a navegação só por teclado funciona do início ao fim (seção 6.3). A tela de resultado segue uma ordem defensável: risco absoluto, frequência natural, pictograma, categoria, meta, fatores, texto de IA e limites. O rótulo da IA e o aviso de que o texto não foi verificado também merecem registro positivo. O documento de especificação tem uma disciplina rara num TCC: cada decisão vem com uma justificativa.

O uso real, porém, revelou **um defeito que impede a conclusão do fluxo para a maioria do público-alvo**. Quem não tem nenhum agravante marca "Nenhuma destas" e recebe o erro "Selecione pelo menos uma opção ou marque 'Nenhuma destas'" (captura `bug-nenhuma-destas-1280.png`). As evidências do projeto não pegaram o defeito porque os roteiros de teste (`percorrer_fluxo.py`, `auditar_axe.py`) sempre marcam um agravante. A auditoria axe-core também não poderia pegá-lo, pois não é uma violação de acessibilidade. Há ainda dois problemas graves de comunicação de risco:

- **Contradição na escala.** Com 7,1% de risco, a escala destaca "Alto — 20% ou mais em 10 anos — Sua categoria" (`desk-08-resultado.png` do próprio projeto).
- **Resposta dependente não revisada.** Um homem que corrigiu o sexo na revisão fica com o agravante "Situações da saúde da mulher" e tem a categoria elevada por ele (`cen-08-resultado-homem-fator-mulher.png`).

Várias justificativas atribuem às fontes mais do que elas dizem. O caso mais importante: o próprio padrão GOV.UK citado para a revisão manda perguntar de novo quando uma resposta alterada afeta outras, e a interface não faz isso.

**Veredito: APROVADO COM RESSALVAS OBRIGATÓRIAS.** Antes da defesa, é preciso corrigir os três problemas críticos (P1–P3), revisar as justificativas mal atribuídas (P13) e registrar no texto a ausência de teste com usuários como limitação, com o protocolo mínimo da seção 7 (idealmente, executado).

## 2. Notas por critério (0–10)

| Critério | Nota | Justificativa |
|---|---|---|
| Adequação ao público (30–79 anos, leigos, idosos) | **7,0** | Corpo de 18 px medido, alvos ≥ 48 px, linguagem direta, dicas brasileiras ("12 por 8"). Perdem pontos: becos sem saída para valores fora da faixa (P7), perda silenciosa de respostas (P8), termos não explicados na tela de resultado ("não-HDL", "LDL-c", "<") e ausência de validação com idosos. |
| Identidade visual | **7,5** | Coerente, sem clichês do setor e sem ícones decorativos. A marca, porém, não é a grade 10 × 10 que o documento descreve: é 4 × 4 (1 em 16), e a 32 px os pontos ficam quase invisíveis (P14). |
| Fluxo e usabilidade | **3,5** | A estrutura é exemplar (endereços por etapa, Voltar do navegador preserva as respostas, revisão com "Alterar"), mas o caminho mais comum ("Nenhuma destas") está quebrado (P1), respostas dependentes não são revisadas (P2) e a marca no cabeçalho apaga tudo sem confirmar (P8). |
| Comunicação de risco | **5,5** | Tem as escolhas certas (risco absoluto, denominador 100, pictograma agrupado, figuras humanas, "cerca de"). Tem também contradições entre o número, o pictograma e a escala (P3, P6), fatores de Shapley pouco interpretáveis por leigos (P10) e baixo contraste das figuras do denominador (P9). |
| Acessibilidade | **6,5** | Teclado, rótulos, `lang`, marcos de página, foco no título e resumo de erros estão bons, e o axe deu 0 violações. Falham: foco invisível em cores forçadas (P4), *reflow* a 320 px na tela renal (P5) e impressão que perde a legenda e a escala (P11). |
| Conteúdo e microcopy | **7,5** | Tom honesto e sem alarme, "risco estimado", limites explícitos, texto de privacidade verdadeiro frente ao código. Há mensagens de erro genéricas ou impróprias em alguns casos (P16) e o texto de dados omite pontos relevantes (P12). |
| Qualidade das justificativas | **5,5** | O método é excelente (fonte/medida/decisão), mas há atribuições exageradas ou erradas: NN/g e 7:1, WCAG 1.4.12 e 2.4.11, Zipkin e frequências naturais, GOV.UK e "baixa confiança", AI Act como "exigência". Há também números da escala tipográfica que não correspondem ao código (P13). |
| **Média simples** | **6,1** | |

## 3. Pontos fortes (verificados)

1. **Navegação só por teclado completa e previsível** (`teclado-log.txt`). Tab entra no grupo, as setas escolhem, Espaço marca e Enter envia em todas as 13 perguntas, na revisão e no resultado. O anel de foco aparece em todo elemento interativo (`tec-02`, `tec-04`, `tec-07`, `tec-10`).
2. **Foco movido para o `h1` a cada tela e título da aba atualizado** (`utilitarios/useTituloDaTela.js`). Um leitor de tela anuncia a nova pergunta.
3. **Botão Voltar do navegador funciona e preserva os valores** (`cenarios-log.txt`: voltar de `anti_hipertensivo` para `pas` mostra "140"; LDL vazio continua vazio).
4. **Resumo de erros no padrão GOV.UK**, com link para o campo e mensagem junto ao campo (`cen-01-erro-idade-15.png`). O foco vai para o resumo.
5. **Opções como cartões inteiros com `input` nativo** (`Campos.jsx:94-113`). O rótulo curto é o nome acessível e a dica vem por `aria-describedby`.
6. **Contrastes de texto medidos e corretos**: 9 de 9 valores declarados conferem na segunda casa decimal (seção 6.2).
7. **`prefers-reduced-motion` efetivo**: a duração computada de todas as animações cai para 0,01 ms (`cenarios-log.txt`).
8. **Reflow a 640 px com zoom de 200% sem rolagem horizontal** em revisão, resultado e renal.
9. **Honestidade de produto**: selo "Protótipo acadêmico" também no celular, texto de IA rotulado, aviso de "não verificado", o resultado continua válido sem o texto e há a seção "Limites deste resultado".
10. **O texto "Seus dados" é verdadeiro frente ao código**: as respostas ficam só no estado React (`App.jsx:25`), sem `localStorage`, e `avaliacao.py` não registra o corpo das requisições.

## 4. Problemas

### Críticos

**P1. "Nenhuma destas" impede terminar a avaliação.**
- *Evidência:* `bug-nenhuma-destas-1280.png` e `bug-nenhuma-destas-390.png`; `nenhuma-resultado.txt` registra "marcado: ['Nenhuma destas'] → após Continuar: /#/p/agravantes ['Selecione pelo menos uma opção ou marque “Nenhuma destas”.']".
- *Causa:* o valor da opção exclusiva é o texto do rótulo (`Campos.jsx:80` usa `valor: exclusiva`, e `Telas.jsx:93` passa `exclusiva={pergunta.nenhuma}` = "Nenhuma destas", `perguntas.js:174`). A validação, porém, só aceita a chave `'nenhuma'` (`validacao.js:66`). O mesmo desencontro aparece em `api.js:20` e `Telas.jsx:147`.
- *Impacto:* toda pessoa sem agravantes, provavelmente a maioria, não chega ao resultado. A mensagem ainda a culpa por algo que ela fez certo.
- *Por que as evidências não pegaram:* `percorrer_fluxo.py` e `auditar_axe.py` sempre marcam "Pai, mãe, irmão…". O axe verifica acessibilidade, não a lógica do fluxo.
- *Correção:* usar uma chave estável (`{valor: 'nenhuma', rotulo: pergunta.nenhuma}`). Acrescentar aos roteiros um caminho "sem agravantes" e um teste unitário de `validar()`.

**P2. A mudança de resposta na revisão não revê as respostas dependentes.**
- *Evidência:* `cen-06` → "Alterar sexo" → Masculino → volta direto à revisão, que ainda lista "Situações da saúde da mulher" (`cen-07-revisao-homem-com-fator-da-mulher.png`). O resultado sai "alto" porque "a diretriz eleva a categoria quando há fator de risco específico da mulher" (`cen-08`). O gateway aceita o agravante para `sexo=masculino` (`bordas-api-resultado.txt`).
- *Causa:* `App.jsx:48-50` volta à revisão sem reavaliar dependências. A filtragem por sexo só roda quando a pergunta de agravantes é respondida de novo (`validacao.js:66-67`).
- *Fonte violada:* o padrão GOV.UK *Check answers*, que o próprio documento cita, diz: "If a user changes their response in a way that means you need to ask them more questions, do this before returning them to the check answers page."
- *Correção:* ao mudar `sexo`, remover `fator_especifico_mulher` ou reencaminhar para a pergunta de agravantes. No gateway, recusar o agravante incompatível (hoje ele é aceito sem aviso).

**P3. A escala da categoria contradiz o número quando há reclassificação.**
- *Evidência:* `tcc/04-evidencias/interface/desk-08-resultado.png` (do próprio projeto) mostra "7,1%", 7 figuras e, logo abaixo, "Alto — 20% ou mais em 10 anos — Sua categoria". O mesmo aparece em `cen-08` e `cen-15`.
- *Causa:* `Resultado.jsx:28-30,44` rotula cada faixa com o intervalo do escore, mas a posição marcada é a categoria final, depois de agravantes e LDL.
- *Impacto:* a pessoa idosa lê duas afirmações incompatíveis ("7%" e "20% ou mais") na mesma tela. A frase de reclassificação vem depois e em tipo menor. Fagerlin, Zikmund-Fisher e Ubel (2011) pedem que as representações de um mesmo risco sejam consistentes entre si.
- *Correção:* quando reclassificado, marcar na escala a posição do escore ("Seu cálculo: 7,1%") e indicar separadamente "Categoria pela diretriz: Alto, por história familiar". Outra saída é tirar os intervalos percentuais dos rótulos e explicá-los em texto. A frase de reclassificação deve vir antes da escala.

### Maiores

**P4. Foco invisível no modo de cores forçadas (Alto Contraste do Windows).**
- *Evidência:* `cen-13-forced-colors-foco-opcao.png` e `cen-14-forced-colors-foco-botao.png` (foco em "Masculino" e depois em "Continuar": as duas capturas são indistinguíveis). O log registra "outline = none | box-shadow = none".
- *Causa:* `base.css:65-67` remove o `outline` e desenha o foco só com `box-shadow`, que o navegador descarta em `forced-colors`. O mesmo vale para `.opcao:focus-within` (`campos.css`).
- *Critério:* WCAG 2.4.7 (Foco visível), relevante para pessoas com baixa visão, que são o público da fonte escolhida.
- *Correção:* `outline: 3px solid transparent` junto com o `box-shadow` (fica visível em cores forçadas) ou `@media (forced-colors: active) { :focus-visible { outline: 3px solid CanvasText } }`.

**P5. Reflow a 320 px quebra na pergunta renal (WCAG 1.4.10).**
- *Evidência:* `cen-11-renal-320px.png`: o cartão "TFG estimada" é cortado à direita e a unidade "mL/min/1,73 m²" quebra ao lado do campo. O log registra `scrollWidth 346 > 320`. Com o espaçamento de texto do WCAG 1.4.12 aplicado, a medida sobe para 370 px no renal e 360 px no resultado (`espacamento-resultado.txt`).
- *Causa:* recuo de `.revelado` (margem + padding) somado à largura fixa do campo (`Campos.jsx:55`) e à unidade longa.
- *Observação:* com texto a 200% num celular de 390 px (`cen-10-resultado-390px-texto200.png`), o "6,4%" sai do cartão e a escala transborda (588 px). O 1.4.4 não exige esse cenário, mas é o uso real de um idoso com a fonte do sistema aumentada.
- *Correção:* em telas estreitas, unidade abaixo do campo e recuo menor. Na escala, usar uma coluna em telas estreitas e `clamp()` com limite em `rem`.

**P6. Fronteiras de arredondamento geram incoerência entre o número, o pictograma e a categoria.**
- *Evidência (API, `bordas-api-resultado.txt`):*
  - homem de 40 anos, PAS 196: exibe **"5,0%"** e 5 figuras, mas a categoria é **Baixo — "menos de 5%"**;
  - homem de 76 anos, fumante, PAS 190: **"20,0%"** e 20 figuras, mas **Intermediário — "5% a menos de 20%"**;
  - 19,6% dá 20 figuras em "Intermediário";
  - 4,6% dá 5 figuras em "Baixo".
- *Causa:* `gabarito.py:30` arredonda o percentual para uma casa decimal e `avaliacao.py:100` usa `round()` com arredondamento bancário, enquanto a categoria usa o valor bruto (`sbc.py:42-47`). Pelo arredondamento bancário, 2,5% vira 2 figuras e 3,5% vira 4 figuras, e 0,5% vira "menos de 1" com a grade vazia. `TelaResultado.jsx:35` recalcula a categoria com outro valor, o já arredondado, criando uma terceira fonte de verdade.
- *Correção:* definir uma regra única (categoria, pictograma e texto calculados do mesmo valor arredondado, ou nunca mostrar "5,0%" em "Baixo") e arredondar meios para cima, de forma documentada. Para riscos abaixo de 1%, usar denominador de 1.000 ou texto explícito em vez de uma grade vazia, que sugere risco zero (Trevena et al., 2013).

**P7. Becos sem saída para valores reais fora da faixa de derivação.**
- *Evidência:* `cen-03-colesterol-340-beco.png` e `cen-04-pressao-12.png`. Colesterol 340, PAS 85 ou HDL 110 só geram "Digite um valor entre…". A pessoa não tem como seguir, a não ser mentindo.
- *Contraste com o próprio projeto:* idade, DCV e diabetes têm tela própria de fora do escopo (`perguntas.js:13-34`), mas os limites numéricos da equação, igualmente de escopo, não têm.
- *Microcopy:* "Confira o valor no exame" não serve para a pressão, que não vem do exame de sangue. "12" (o formato "12 por 8" que a própria dica ensina) poderia gerar a sugestão "Você quis dizer 120?". A idade 15 recebe "Confira o valor digitado." em vez da tela 30–79.
- *Correção:* após a confirmação do valor, uma tela "Seu valor está fora da faixa em que a equação foi testada", com orientação. Conversões assistidas para "12/8" e "12".

**P8. Perda de respostas sem aviso.**
- *Evidência:* clicar na marca no meio do fluxo leva a `#/` e apaga tudo (`App.jsx:107` chama `recomecar()`), sem pedir confirmação (`cenarios-log.txt`). Recarregar a página também perde tudo, e `#/revisao` volta ao início sem explicação.
- *Impacto:* para idosos, que tocam em áreas grandes por engano, é uma violação da heurística de prevenção de erros (Nielsen).
- *Correção:* o link da marca só navega, sem apagar (apagar fica para "Fazer nova avaliação"), ou pede confirmação quando há respostas. Opcionalmente, `sessionStorage` com consentimento. Isso exige ajustar o texto "não guarda".

**P9. As figuras do denominador no pictograma têm contraste insuficiente.**
- *Evidência:* `--sem-evento` (#C4BCAD) sobre o cartão (#FFFDF9) mede **1,85:1** (`contraste-resultado.txt`), abaixo dos 3:1 do WCAG 1.4.11. O documento só mede evento contra sem-evento (4,33:1, que confere).
- *Por que importa:* o valor do pictograma está justamente em mostrar o denominador, o que reduz a negligência do denominador (Garcia-Retamero, Galesic e Gigerenzer, 2010). Para leitores com catarata ou presbiopia, as 93 figuras "apagadas" somem.
- *Correção:* escurecer `--sem-evento` (mínimo de 3:1 contra o cartão), mantendo pelo menos 3:1 contra `--evento`, ou usar figuras vazadas com contorno de 3:1. Diferenciar as duas classes também pela forma (cheia × contorno), não só pela luminosidade.

**P10. "O que mais pesou" é difícil de interpretar para leigos.**
- *Evidência:* `desk-08-resultado.png`:
  - "HDL (colesterol bom) 44 mg/dL" aparece em "Aumentaram o seu risco";
  - "Colesterol não-HDL" é um valor que a pessoa nunca informou (derivado de 210 − 44);
  - as barras não têm escala nem unidade;
  - a "pessoa de referência", que muda o sentido de tudo, fica recolhida num `details` **depois** das barras (`Resultado.jsx:87-100`);
  - o `summary` perdeu o marcador de expansão (`display: flex`, `resultado.css:234-240`; `tec-09`), então parece um link;
  - "Pouco influenciaram" usa a cor de "diminuiu" (`Resultado.jsx:78`).
- *Literatura:* explicações contrastivas funcionam quando o termo de comparação é natural para a pessoa (Miller, 2019). "Uma pessoa de 55 anos com PAS 130" é arbitrária para ela. Trevena et al. (2013) recomendam apresentar a comparação de forma explícita, e não deixá-la implícita.
- *Correção:*
  - dizer em uma frase, antes das barras, com quem ela é comparada;
  - explicar "não-HDL = total − HDL";
  - trocar "HDL (colesterol bom)" por "HDL de 44 (abaixo de 50, o que aumenta o risco)";
  - dar cor neutra ao grupo "pouco influenciou";
  - restaurar o marcador do `summary`;
  - testar a seção com usuários (seção 7) ou movê-la para "Detalhes".

**P11. A impressão para "levar ao médico" perde informação.**
- *Evidência:* `impressao-pag-1.png` e `impressao-pag-2.png` (PDF A4 com o padrão do Chrome, sem gráficos de fundo). Os quadrados da legenda do pictograma somem ("teriam infarto ou AVC" e "não teriam" ficam sem chave de cor), a escala perde as cores (só sobra o contorno da faixa atual), as barras de fatores desaparecem e "Como ler" não é impresso (`pdftotext` não o encontra). A regra `.como-ler > p {display:block}` (`resultado.css:305+`) não abre um `details` fechado.
- *Correção:* `print-color-adjust: exact` nos elementos gráficos ou legenda em SVG em vez de `background`. Em `@media print`, trocar as barras por texto (por exemplo, "aumentou muito") e renderizar "Como ler" fora do `details`. Incluir no impresso a data e os valores informados.

**P12. Envio automático ao serviço de IA, sem escolha, e texto de dados incompleto.**
- *Evidência:* `TelaResultado.jsx:29-31` chama `explicar()` ao abrir o resultado, sem ação da pessoa. O texto da tela inicial é verdadeiro, mas é lido antes de a pessoa saber o que será enviado, não oferece recusa e não diz que o serviço pode estar fora do Brasil ou reter dados. Dados de saúde são **dados pessoais sensíveis** (LGPD, art. 5º, II), e a transferência internacional tem regras próprias (art. 33).
- *Observação:* a justificativa de hospedar a fonte localmente ("sem requisição ao Google — privacidade") convive com o envio de dados clínicos a um LLM externo, possivelmente o próprio Google (`llm.py` suporta Gemini). Nos termos da API gratuita do Gemini, o conteúdo pode ser usado para melhorar produtos.
- *Correção:* botão "Gerar explicação em linguagem simples" com uma linha dizendo o que é enviado e para onde; a explicação sai só com consentimento explícito. O documento deve citar os arts. 5º, 11 e 33.

**P13. Justificativas mal atribuídas ou exageradas** (detalhes na seção 6.1).
- *Atribuições erradas:* NN/g não recomenda 7:1; o WCAG 1.4.12 não é atendido "por ter altura de linha 1,5"; o 2.4.11 não trata da aparência do foco.
- *Exageros:* Zipkin et al. não sustentam que frequências naturais superam percentuais; GOV.UK não fala em "formulários de baixa confiança"; o AI Act art. 50 não "exige" rótulo visível neste caso.
- *Escala tipográfica diferente do código:* medido, é 18 → 25,3 → 31,6 → 39,5 px, e não 18 → 22,5 → 28 → 35 px. As notas saem com 18 px, e não com os 16 px do token (`base.css:8`, `html{font-size:112.5%}` multiplica todos os `rem`).
- *Texto sobre a escala:* o documento declara contraste de texto sobre as cores da escala, mas nenhum texto é posto sobre elas no código. A medida pertinente, de cada faixa contra o fundo, dá 1,27:1 para Baixo e 2,08:1 para Intermediário.

### Menores

- **P14. Marca 4 × 4, não 10 × 10.** `Estrutura.jsx:3` (comentário) e o documento §3.2 dizem 10 × 10, mas `Estrutura.jsx:6-7` e `marca.svg` desenham 16 pontos, um deles destacado. Isso comunica "1 em 16", não "1 em 100". A 32 px os pontos têm 4 px, e o cinza #C4BCAD sobre o papel quase some (1,7:1). Na captura com texto a 200% em 390 px, a marca encolhe para cerca de 8 px.
- **P15. Animação de carregamento fora da regra declarada.** `.linhas-fantasma` usa 1,4 s em repetição infinita (`resultado.css:286`), contra o "100–300 ms" do documento §6. Com `reduce` ela para, o que está correto.
- **P16. Microcopy.**
  - A idade "abc" recebe o exemplo "por exemplo 180 ou 1,2". Para "12/8", o exemplo não ajuda.
  - "Alterar hdl" / "Alterar ldl" em minúsculas no nome acessível (`Telas.jsx`, `toLowerCase()`).
  - As metas usam "< 70 mg/dL" (o símbolo "<" é barreira para quem tem baixo letramento numérico; escrever "menos de 70").
  - "LDL-c" e "Não-HDL-c" aparecem sem explicação.
  - "Sua categoria de risco: alto" vem em minúscula, enquanto a escala usa "Alto".
- **P17. Precisão.** "7,1%" em 72 px, seguido de "cerca de 7", passa uma precisão que a equação não tem para a população brasileira, o que é reconhecido em "Limites". Considerar "cerca de 7%" como número principal e o decimal em nota.
- **P18. `aria-label` do pictograma** ("…das quais 7 estão destacadas") não diz o que "destacadas" significa. Com 0 figuras fica "0 estão destacadas", enquanto o texto diz "menos de 1". Sugestão: "7 de 100 pessoas teriam infarto ou AVC".
- **P19. Botão "Calculando…" desabilitado sem estilo próprio**, e o foco se perde ao desabilitar (`Telas.jsx`, `disabled` + `aria-disabled`). Preferir manter o foco e anunciar com `aria-live`.
- **P20. Resumo de erros com `role="alert"` e foco programático ao mesmo tempo** (`Campos.jsx:12`) pode gerar leitura dupla em alguns leitores de tela. A GOV.UK usa só o foco.
- **P21. "13 perguntas curtas, cerca de 3 minutos"** não tem medida que a sustente: é uma afirmação para o usuário sem evidência. Medir no teste da seção 7.
- **P22. A auditoria axe não cobre** as telas de fora do escopo (o script navega até elas mas não as audita), o estado com a explicação carregada nem os resultados "incomplete" (que pedem revisão manual). O documento deveria dizer isso.

## 5. Perguntas da banca

| # | Pergunta | Resposta esperada | O projeto responde hoje? |
|---|---|---|---|
| 1 | Os roteiros de evidência passaram pelo caminho "Nenhuma destas"? Como garantem que o fluxo mais comum funciona? | Reconhecer P1, corrigir e acrescentar testes de caminho (sem agravantes, só LDL, só creatinina) e testes unitários de `validar()`. | **Não**. `percorrer_fluxo.py` e `auditar_axe.py` sempre marcam um agravante. |
| 2 | Por que a escala diz "20% ou mais" para quem tem 7,1%? Um idoso entenderia? | Explicar a reclassificação da SBC e mostrar o redesenho que separa "cálculo" e "categoria pela diretriz". | **Parcial**. Só a frase de reclassificação (`TelaResultado.jsx:67-76`), depois da escala. |
| 3 | O que acontece se a pessoa muda o sexo na revisão? E se passa a fumar, ou muda de TFGe para creatinina? | Regras de dependência entre perguntas e reperguntar antes de voltar à revisão (GOV.UK *Check answers*). | **Não**. Ver P2. |
| 4 | Por que o pictograma mostra 5 figuras para quem é "Baixo, menos de 5%"? E 0 figuras para 0,4%? | Regra única de arredondamento e tratamento de riscos pequenos (denominador de 1.000). | **Não**. Ver P6. |
| 5 | Zikmund-Fisher et al. (2014) mostram vantagem das figuras humanas também para pessoas com baixo letramento numérico? | Não: a melhor correlação entre risco percebido e real apareceu entre os mais numerados. Entre os menos numerados, os ícones de banheiro não foram melhores. A recordação melhorou com ícones antropomórficos. Além disso, o estudo usou figuras do mesmo sexo do participante. | **Parcial**. O documento cita a melhora de recordação, omite a ressalva e usa uma figura única. |
| 6 | Qual a evidência de que frequência natural é melhor que percentual? | Zipkin et al. (2014) consideram inconclusivo o efeito de frequências contra percentuais. A vantagem clara é do risco absoluto sobre o relativo (em reduções de risco) e dos recursos visuais. Justificar a frequência natural por Gigerenzer e Hoffrage (1995) e Trevena et al. (2013), com a ressalva. | **Parcial**. A citação está superestimada (P13). |
| 7 | Como uma pessoa com baixa visão que usa o Alto Contraste do Windows vê o foco? | Mostrar o teste em `forced-colors` e a correção com `outline` transparente. | **Não**. Ver P4. |
| 8 | O que a pessoa leva ao médico quando imprime? | Uma folha com número, frequência, categoria, meta, fatores legíveis sem cor, valores informados e data. | **Parcial**. O impresso perde a legenda, a escala e as barras (P11). |
| 9 | Os dados de saúde saem do país? A pessoa pode recusar? Qual a base legal? | Identificar o provedor e onde fica, as bases legais (LGPD, arts. 11 e 33) e oferecer a explicação como opção. | **Parcial**. O texto é verdadeiro, mas não há escolha nem menção a dados sensíveis ou transferência (P12). |
| 10 | Como uma pessoa leiga interpreta "HDL (colesterol bom) aumentou seu risco" e "remédio de pressão aumentou"? | Descrever o teste de compreensão (seção 7) e o texto contrastivo revisado. | **Parcial**. O "Como ler" explica o remédio, mas fica recolhido e depois das barras, e não explica o HDL (P10). |
| 11 | Por que o AI Act, se o produto é brasileiro? O art. 50 exige exatamente o quê? | O AI Act não se aplica aqui. O art. 50(2) exige do provedor uma marcação legível por máquina. O 50(4) exige divulgação de texto sobre assuntos de interesse público. O rótulo é boa prática inspirada nele e no PL 2338/2023 (Brasil). | **Não**. O documento fala em "exigência" (§5.6). |
| 12 | Houve teste com pessoas de 60+? Quanto tempo leva de fato? Quantas erram a pressão? | Resultados do protocolo mínimo da seção 7 (taxa de sucesso, tempo, SUS, compreensão). | **Não**. O documento reconhece a lacuna (§8) e o "3 minutos" não tem medida. |
| 13 | A marca é "1 em 100". Por que o desenho tem 16 pontos? | Corrigir o desenho ou a descrição. | **Não**. Ver P14. |
| 14 | O que acontece com colesterol total de 340? | Tela de fora do escopo com orientação, e não um erro de digitação. | **Não**. Ver P7. |

## 6. Verificações executadas

Ambiente: Chrome do sistema (`channel="chrome"`) com Playwright, frontend em `vite preview` (:4173, build de 29/09 01:47, posterior ao último arquivo de `src`) e gateway em :8000 sem LLM configurado (a explicação cai no estado de erro, que também foi avaliado). O estado "explicação carregada" **não** pôde ser observado. Todos os artefatos estão em `tcc/05-banca/anexos/ihc/`.

### 6.1 Justificativas contra as fontes

| Afirmação no `interface-design.md` | O que a fonte diz | Situação |
|---|---|---|
| §1 e §3.3: texto pequeno, baixo contraste e alvos pequenos são os problemas recorrentes dos idosos (NN/g) | Kane (NN/g, 2019): texto pequeno e claro demais, alvos pequenos e legibilidade como problema persistente. | **Confere** |
| §3.4: 7:1 AAA "recomendado para idosos [NN/g]" | O artigo da NN/g não recomenda razão de contraste nem nível AAA. O 7:1 vem do WCAG 1.4.6 (AAA). | **Mal atribuída** |
| §1 e §4: uma pergunta por tela (GOV.UK) | A página *Form structure* confirma "start with one thing per page" e cita benefícios em celular e na recuperação de erros. | **Confere** |
| §2: "o padrão validado para formulários de baixa confiança" | As páginas da GOV.UK não falam em "baixa confiança" nem apresentam validação, e dizem que a pesquisa com usuários indica quando juntar páginas. | **Exagerada** |
| §4: revisão com "Alterar" (GOV.UK *Check answers*) | O padrão manda perguntar de novo antes de voltar à revisão quando a resposta alterada exige isso. | **Citada, mas não seguida** (P2) |
| §3.3: GOV.UK usa 19 px "em telas grandes" | A escala tipográfica atual (GOV.UK Frontend v6) usa 19 px no corpo **também** em telas pequenas. | Desatualizada. O projeto usa 18 px, um pouco abaixo. |
| §3.3: altura de linha 1,5 "atende ao 1.4.12" | O 1.4.12 exige que o conteúdo **suporte** o espaçamento definido pelo usuário, sem perda. Não exige que o autor defina 1,5. Testado: a 320 px o conteúdo transborda (P5). | **Mal atribuída** |
| §8: foco de 3 px "WCAG 2.4.11/2.4.13" | No WCAG 2.2, o 2.4.11 é *Focus Not Obscured (Minimum)*. A aparência do foco é o 2.4.13 (AAA), e o anel de 3 px com 7,24:1 de contraste o atende em modo normal. | **2.4.11 mal citado** |
| §8: alvos ≥ 48 px, acima dos 24 px do 2.5.8 | Correto. Medido: 48 px nos botões e 49,5 px em "Alterar". | **Confere** |
| §5: risco absoluto e frequências naturais melhoram a compreensão "em relação a percentuais isolados" (Zipkin 2014) | Zipkin et al.: recursos visuais e formatos absolutos melhoram a compreensão, NNT a piora, e **frequência contra percentual é inconclusivo**. A comparação absoluto × relativo trata de reduções de risco. | **Exagerada** |
| §1 e §5: pictogramas ajudam pessoas com baixo letramento numérico (Galesic et al. 2009) | O estudo mostra que *icon arrays* melhoraram a compreensão de reduções de risco entre os menos numerados, inclusive em adultos mais velhos. | **Confere** (o contexto é tratamento, não risco basal) |
| §3.5: figuras humanas, 1.502 pessoas de 35–75 anos, calculadora cardiovascular, melhor memorização e preferência (Zikmund-Fisher 2014) | Números e achados conferem, mas o resumo diz que, entre os menos numerados ou com pouco letramento gráfico, os ícones de banheiro **não foram melhores**. Os ícones eram do mesmo sexo do participante. | **Confere com omissão relevante** |
| §3.4: escala sequencial de um só matiz para dados ordinais, segura para daltonismo (Harrower e Brewer 2003) | É o princípio do ColorBrewer. Mas as cores do projeto **não** são uma paleta do ColorBrewer, apesar do comentário "ColorBrewer" em `tokens.css:19`. A distância entre Baixo e Intermediário é de 1,64:1. | **Princípio confere, citação imprecisa** |
| §3.3: Atkinson Hyperlegible Next, Braille Institute 2025, 150+ idiomas, OFL | Lançada em fevereiro de 2025, 7 pesos, variável e 150+ idiomas (Braille Institute). | **Confere** |
| §5.6: transparência sobre IA é "exigência do AI Act, art. 50" | O art. 50 aplica-se desde 2/8/2026, na UE. O 50(2) impõe ao **provedor** uma marcação legível por máquina. O 50(4) impõe ao implantador a divulgação de texto publicado para informar o público sobre assuntos de interesse público. Não se aplica a um protótipo brasileiro e não "exige" o rótulo visível deste caso. | **Exagerada**. Reformular como boa prática, citando também o PL 2338/2023. |
| §2 e §7: LGPD art. 6º, III (necessidade) e VI (transparência) | Correto. Faltam o art. 5º, II e o art. 11 (dado sensível de saúde) e o art. 33 (transferência internacional). | **Confere, incompleta** |
| §6: 100–300 ms; acima de ~500 ms atrapalha (NN/g) | Laubheimer (NN/g, 2020): de 100 a 500 ms, cerca de 100 ms para retorno simples, 200 a 300 ms para mudanças grandes, e em 500 ms a animação "começa a arrastar". | **Confere** (o autor e o título corretos estão nas referências) |
| §2: placeholders prejudiciais; ícones só com rótulo (NN/g) | Sherwin (2014) e Harley (2014) confirmam. | **Confere** |
| §8: 5 usuários (Nielsen 2000) | Confere, mas a literatura mostra grande variância com 5 usuários (Faulkner, 2003) e o público aqui tem dois perfis distintos. | **Confere com ressalva** |

### 6.2 Contrastes (fórmula de luminância relativa do WCAG 2.x)
Script: `anexos/ihc/contraste.py`. Saída: `contraste-resultado.txt`. Resumo:

- **Texto (todos ≥ 4,5:1; os valores declarados conferem):** tinta/papel 14,66; tinta-suave/papel 7,51; acento/papel 7,24; branco/acento 7,95; acento-escuro/papel 9,50; erro/papel 6,75. Nos estados: acento sobre acento-claro (secundário em *hover*) 6,75; branco sobre acento-escuro (primário em *hover*) 10,43; erro sobre erro-claro (links do resumo) 6,28; tinta-suave sobre acento-claro (dica de opção marcada) 7,01.
- **Componentes (1.4.11):** borda do campo 3,33 (papel) e 3,60 (cartão); borda em *hover* 8,11; borda de erro 7,29; borda da opção marcada 7,82; anel de foco 7,24. **Todos passam.**
- **Objetos gráficos:**
  - barra de progresso contra o trilho: 5,87 (passa; o trilho contra o papel dá 1,23, aceitável porque o progresso também está em texto);
  - pictograma, evento contra sem-evento: 4,33 (confere);
  - **sem-evento contra o cartão: 1,85 (falha, P9)**;
  - escala, Baixo contra o papel: **1,27**; Intermediário contra o papel: **2,08**; Baixo contra Intermediário: **1,64**. A informação também está em texto, então o 1.4.11 fica atendido pelo texto, mas as cores quase não contribuem;
  - barra "aumentou" contra "diminuiu": 1,59 (distinguem-se pelo título do grupo, não pela cor).
- **Desabilitado:** não há estilo próprio (P19).

### 6.3 Uso real (Playwright)

| Verificação | Resultado | Evidência |
|---|---|---|
| Fluxo completo só por teclado (Tab, Shift+Tab, setas, Espaço, Enter) | Completo; anel visível em todo controle; foco no `h1` a cada tela | `teclado.py`, `teclado-log.txt`, `tec-01`…`tec-10` |
| Erros: vazio, "abc", "58,5", 15, 150 | Mensagens e foco no resumo corretos; 15 e 150 dão "Confira o valor digitado" | `cen-01-erro-idade-15.png` |
| Idade 25 e `#/fora/diabetes` | Telas corretas, sem tom de erro; "Alterar minha resposta" volta à pergunta com o valor preservado | `cen-02`, `cen-05` |
| Colesterol 340, PAS 12 / "12/8" / 85 | Beco sem saída | `cen-03`, `cen-04` (P7) |
| Voltar e Avançar do navegador | Funcionam e preservam os valores | `cenarios-log.txt` |
| Recarregar / marca no cabeçalho | Tudo é perdido sem aviso | `cenarios-log.txt` (P8) |
| Revisão e "Alterar sexo" | Retorno direto à revisão; agravante incompatível mantido e resultado errado | `cen-06`, `cen-07`, `cen-08` (P2) |
| "Nenhuma destas" | Bloqueia o fluxo | `bug-nenhuma-destas-*.png`, `nenhuma.py` (P1) |
| Reflow 320 px | Revisão e resultado sem transbordo; **renal com 346 px** | `cen-09/10/11-*-320px.png` (P5) |
| 640 px com zoom de 200% (DPR 2) | Sem transbordo | `cen-09/10/11-*-640px.png` |
| Texto a 200% em 1280 px | Sem transbordo | `cen-*-1280px-texto200.png` |
| Texto a 200% em 390 px | Transborda (443, 588 e 689 px) | `cen-*-390px-texto200.png` |
| Espaçamento de texto (1.4.12) | Sem transbordo em 390 px; renal com 370 px e resultado com 360 px em 320 px | `espacamento.py`, `esp-*.png` |
| `prefers-reduced-motion` | Todas as animações passam a 0,01 ms. Sem a preferência, 60 ms após a troca de tela a opacidade está em 0,41, o que confirma a animação de 200 ms | `cenarios-log.txt`, `cen-12` |
| `forced-colors: active` | Foco invisível | `cen-13`, `cen-14`, `cen-15` (P4) |
| Impressão (PDF A4, sem fundo) | Legenda, escala e barras somem; "Como ler" ausente | `impressao-resultado.pdf`, `impressao-pag-*.png` (P11) |
| Tamanhos computados | html/body 18 px; h1 39,5; h2 25,3; `.nota` 18; selo 15,75 | `cenarios-log.txt` (P13) |
| Fronteiras da API (≈ 4.000 combinações) | 5,0% "Baixo"; 20,0% "Intermediário"; arredondamento bancário | `bordas_api.py`, `bordas-api-resultado.txt` (P6) |

### 6.4 Leitura de código relevante
- `validacao.js:66` × `Campos.jsx:80` × `perguntas.js:174`: P1.
- `App.jsx:43-54`: retorno à revisão sem tratar dependências (P2). `App.jsx:95-96`: `ir()` chamado durante a renderização (efeito colateral no render; funciona, mas é frágil).
- `TelaResultado.jsx:35`: limiares de categoria duplicados no frontend (P6).
- `base.css:65-67` e `campos.css:131`: foco só com `box-shadow` (P4).
- `resultado.css:53-68, 110-112, 221-222`: cores como `background`, que não são impressas (P11).
- `backend-gateway/app/main.py`: os *endpoints* legados `/predict` ainda registram em log os dados do paciente (`logger.info(f"Enviando dados…")`). A nova interface não os usa, mas convém removê-los para que o "não guarda" continue verdadeiro no sistema inteiro.

## 7. Lacuna: protocolo mínimo de teste de usabilidade (adequado a um TCC)

**Objetivo.** Verificar se adultos de 30 a 79 anos (a) completam a avaliação sem ajuda, (b) entendem corretamente o resultado e (c) acham o sistema usável.

**Participantes.** De 8 a 10 pessoas em duas rodadas iterativas (5 + 5, corrigindo entre elas), estratificadas: pelo menos metade com 60 anos ou mais, e pelo menos 3 com escolaridade até o ensino médio. Cinco participantes por rodada seguem Nielsen (2000). A estratificação e a segunda rodada respondem à variância mostrada por Faulkner (2003). O letramento numérico é medido com a Escala Subjetiva de Numeracia (Fagerlin et al., 2007), de 3 itens na forma curta, para relatar os resultados por estrato.

**Material.** Três laudos **fictícios** impressos, um por tarefa, para não coletar dados reais de saúde. Celular e computador, pois o participante escolhe o que costuma usar.

**Tarefas** (moderadas, com pensamento em voz alta concorrente):
1. Com o laudo A (colesterol, HDL, TFGe, sem agravantes), descobrir o risco. É o caminho do P1.
2. Com o laudo B (só creatinina, pressão anotada "13 por 9", LDL 170), descobrir o risco.
3. Depois de ver o resultado, corrigir uma resposta digitada errada (fumante) e ver o novo resultado.
4. Com o laudo C (colesterol total 340), perceber a limitação e dizer o que fazer.
5. Preparar o resultado para levar ao médico (imprimir ou salvar).

**Compreensão** (após a tarefa 1 ou 2, sem olhar a tela, e depois olhando):
- literal: "Quantas pessoas em 100?", "Qual é a sua categoria?";
- essência: "Seu risco é baixo, médio ou alto?";
- inferência: "Por que a categoria é Alto se o número é 7%?", "O remédio de pressão faz mal?", "O texto da IA é confiável?".

A pontuação é certo/errado, e o *teach-back* ("explique com suas palavras") é registrado.

**Métricas.**
- taxa de sucesso por tarefa (sem ajuda, com ajuda, falha);
- tempo na tarefa (para verificar a afirmação dos "3 minutos");
- número de erros de validação por campo, sobretudo a pressão;
- acertos de compreensão;
- **SUS** na versão brasileira validada (Lourenço, Carmona e Lopes, 2022), interpretada com a escala de adjetivos de Bangor, Kortum e Miller (2009); abaixo de 68 fica abaixo da média de referência;
- problemas classificados por gravidade (0–4).

**Critérios de sucesso sugeridos.** ≥ 80% de sucesso sem ajuda nas tarefas 1 a 3; ≥ 80% de acerto em "quantas em 100" e na categoria; SUS ≥ 68.

**Ética.** O estudo envolve seres humanos e coleta dados sobre compreensão de informação de saúde. Deve ser submetido ao CEP pela Plataforma Brasil (Resoluções CNS 466/2012 e 510/2016), com TCLE. Os dados dos laudos são fictícios. A gravação é só de tela e áudio, com consentimento; os dados são anonimizados e tratados conforme a LGPD. Se o prazo do TCC não comportar o CEP, o texto deve **declarar isso como limitação** e restringir-se a uma avaliação heurística por especialistas (3 avaliadores, heurísticas de Nielsen, mais um percurso cognitivo para as tarefas 1–5). Mesmo sem teste com usuários, ela é executável e documentável.

## 8. Referências (verificadas em 29/09/2026)

- Ancker JS, Senathirajah Y, Kukafka R, Starren JB. Design features of graphs in health risk communication: a systematic review. *J Am Med Inform Assoc*. 2006;13(6):608-618. https://doi.org/10.1197/jamia.M2115
- Bangor A, Kortum P, Miller J. Determining what individual SUS scores mean: adding an adjective rating scale. *J Usability Stud*. 2009;4(3):114-123. https://uxpajournal.org/determining-what-individual-sus-scores-mean-adding-an-adjective-rating-scale/
- Braille Institute. Atkinson Hyperlegible Font / Atkinson Hyperlegible Next (2025). https://www.brailleinstitute.org/freefont/ ; https://www.brailleinstitute.org/about-us/news/braille-institute-launches-enhanced-atkinson-hyperlegible-font-to-make-reading-easier/
- Brasil. Conselho Nacional de Saúde. Resolução nº 466/2012. https://conselho.saude.gov.br/resolucoes/2012/Reso466.pdf ; Resolução nº 510/2016. https://conselho.saude.gov.br/resolucoes/2016/Reso510.pdf
- Brasil. Lei nº 13.709/2018 (LGPD), arts. 5º, 6º, 11 e 33. https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- Brasil. Senado Federal. PL 2338/2023 (marco da inteligência artificial). https://www25.senado.leg.br/web/atividade/materias/-/materia/157233
- Brooke J. SUS: a "quick and dirty" usability scale. In: Jordan PW et al. (eds.). *Usability Evaluation in Industry*. London: Taylor & Francis; 1996. p. 189-194.
- Fagerlin A, Zikmund-Fisher BJ, Ubel PA et al. Measuring numeracy without a math test: development of the Subjective Numeracy Scale. *Med Decis Making*. 2007;27(5):672-680. https://doi.org/10.1177/0272989X07304449
- Fagerlin A, Zikmund-Fisher BJ, Ubel PA. Helping patients decide: ten steps to better risk communication. *J Natl Cancer Inst*. 2011;103(19):1436-1443. https://pubmed.ncbi.nlm.nih.gov/21931068/
- Faulkner L. Beyond the five-user assumption: benefits of increased sample sizes in usability testing. *Behav Res Methods Instrum Comput*. 2003;35(3):379-383. https://doi.org/10.3758/BF03195514
- Galesic M, Garcia-Retamero R, Gigerenzer G. Using icon arrays to communicate medical risks: overcoming low numeracy. *Health Psychol*. 2009;28(2):210-216. https://pure.mpg.de/view/item_2099767
- Garcia-Retamero R, Galesic M, Gigerenzer G. Do icon arrays help reduce denominator neglect? *Med Decis Making*. 2010;30(6):672-684. https://journals.sagepub.com/doi/10.1177/0272989X10369000
- Gigerenzer G, Hoffrage U. How to improve Bayesian reasoning without instruction: frequency formats. *Psychol Rev*. 1995;102(4):684-704. https://doi.org/10.1037/0033-295X.102.4.684
- GOV.UK Design System. *Question pages*. https://design-system.service.gov.uk/patterns/question-pages/ ; *Check answers*. https://design-system.service.gov.uk/patterns/check-answers/ ; *Error summary*. https://design-system.service.gov.uk/components/error-summary/ ; *Type scale*. https://design-system.service.gov.uk/styles/type-scale/
- GOV.UK Service Manual. *Structuring forms — Start with one thing per page*. https://www.gov.uk/service-manual/design/form-structure
- Harrower M, Brewer CA. ColorBrewer.org: an online tool for selecting colour schemes for maps. *Cartogr J*. 2003;40(1):27-37. https://colorbrewer2.org
- Kane L. Usability for Older Adults: Challenges and Changes. Nielsen Norman Group, 2019. https://www.nngroup.com/articles/usability-for-senior-citizens/
- Laubheimer P. Executing UX Animations: Duration and Motion Characteristics. Nielsen Norman Group, 2020. https://www.nngroup.com/articles/animation-duration/
- Lourenço DF, Carmona EV, Lopes MHBM. Tradução e adaptação transcultural da System Usability Scale para o português do Brasil. *Aquichan*. 2022;22(2):e2228. http://www.scielo.org.co/scielo.php?pid=S1657-59972022000202228&script=sci_abstract&tlng=pt
- MDN Web Docs. `forced-colors` media feature. https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors
- Miller T. Explanation in artificial intelligence: insights from the social sciences. *Artif Intell*. 2019;267:1-38. https://doi.org/10.1016/j.artint.2018.07.007
- Nielsen J. Why You Only Need to Test with 5 Users. Nielsen Norman Group, 2000. https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/
- Nielsen J. 10 Usability Heuristics for User Interface Design. Nielsen Norman Group, 1994 (atual. 2024). https://www.nngroup.com/articles/ten-usability-heuristics/
- Sherwin K. Placeholders in Form Fields Are Harmful. Nielsen Norman Group, 2014. https://www.nngroup.com/articles/form-design-placeholders/
- Harley A. Icon Usability. Nielsen Norman Group, 2014. https://www.nngroup.com/articles/icon-usability/
- Trevena LJ, Zikmund-Fisher BJ, Edwards A et al. Presenting quantitative information about decision outcomes: a risk communication primer for patient decision aid developers. *BMC Med Inform Decis Mak*. 2013;13(Suppl 2):S7. https://doi.org/10.1186/1472-6947-13-S2-S7
- União Europeia. Regulamento (UE) 2024/1689 (AI Act), art. 50. https://eur-lex.europa.eu/eli/reg/2024/1689/oj ; texto do artigo: https://artificialintelligenceact.eu/article/50/
- W3C. Web Content Accessibility Guidelines (WCAG) 2.2. 2023. https://www.w3.org/TR/WCAG22/ ; *Understanding 1.4.10 Reflow*: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html ; *1.4.11 Non-text Contrast*: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html ; *1.4.12 Text Spacing*: https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html ; *2.4.11 Focus Not Obscured (Minimum)*: https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html ; *2.4.13 Focus Appearance*: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html
- Zikmund-Fisher BJ, Witteman HO, Dickson M et al. Blocks, ovals, or people? Icon type affects risk perceptions and recall of pictographs. *Med Decis Making*. 2014;34(4):443-453. https://doi.org/10.1177/0272989X13511706
- Zipkin DA, Umscheid CA, Keating NL et al. Evidence-based risk communication: a systematic review. *Ann Intern Med*. 2014;161(4):270-280. https://doi.org/10.7326/M14-0295
