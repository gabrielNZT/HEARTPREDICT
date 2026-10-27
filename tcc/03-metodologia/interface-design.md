---
titulo: Interface — identidade visual, UX e justificativas
status: vigente
atualizado: 2026-10-06
resumo: Especificação da nova interface (público-alvo, identidade, tipografia, cores com contraste medido, fluxo, apresentação do risco, animação, conteúdo, acessibilidade), com a justificativa e a fonte de cada decisão.
---

# Interface: especificação e justificativas

> **Atualização de 06/10/2026 (após o [parecer de IHC](../05-banca/parecer-ihc.md)).** Correções de atribuição feitas no texto: 7:1 (é do WCAG, não da NN/g), WCAG 1.4.12 e 2.4.11, Zipkin sobre frequências, GOV.UK, AI Act, escala tipográfica, ColorBrewer e a marca. Mudanças na interface registradas em D026 e D028:
> - a opção "Nenhuma destas" impedia concluir a avaliação (corrigido; os roteiros de evidência não passavam por esse caminho);
> - trocar o sexo na revisão refaz a pergunta dos agravantes, como manda o padrão *Check answers* do GOV.UK;
> - a escala marca separadamente a faixa do número e a categoria da diretriz;
> - pictograma: figuras sem evento em contorno, 3,3:1 contra o fundo (antes, 1,85:1);
> - uso de remédio aparece como a condição tratada, com aviso visível para não parar o remédio;
> - explicação por IA só com consentimento; nova pergunta de exclusão (placa em exame de imagem), total de 14 perguntas;
> - impressão mantém avisos, cores e o "Como ler"; foco visível em cores forçadas; pergunta renal cabe em 320 px.
>
> **Ressalvas que continuam:** Zikmund-Fisher et al. (2014) mostram melhor memorização com figuras humanas, mas **não** vantagem entre pessoas com baixo letramento numérico, e usaram figuras do mesmo sexo do participante. "Cerca de 3 minutos" não foi medido. A animação de carregamento dura 1,4 s em repetição, fora da faixa de 100–300 ms, que vale para transições. **Não houve teste com usuários** (depende de CEP — D031); o protocolo mínimo está no parecer de IHC, §7. A auditoria axe-core não substitui esse teste e não cobre lógica de fluxo.


Regra deste documento: **cada decisão tem uma justificativa** — uma fonte [F], uma medida [M] ou uma decisão de projeto do TCC [D]. Nada é escolhido "porque fica bonito".

## 1. Público-alvo
- **Quem usa:** adultos de **30 a 79 anos**, leigos em medicina, com os resultados de um exame de sangue recente — a faixa em que o PREVENT é válido e a diretriz o recomenda [D011; SBC 2025 §4.1]. Parte relevante tem **60 anos ou mais**.
- **Consequências de desenho:**
  - texto grande, contraste alto e alvos de toque amplos — os problemas mais recorrentes de idosos em interfaces são texto pequeno, baixo contraste e alvos pequenos [F: NN/g, *Usability for Older Adults*];
  - **baixo letramento numérico** é comum: risco em frequência natural + pictograma [F: Zipkin et al. 2014; Galesic, Garcia-Retamero e Gigerenzer 2009];
  - uso em celular: layout de coluna única e uma pergunta por tela [F: GOV.UK, *one thing per page*].
- **Usuário secundário:** a banca e o orientador, que precisam ver no próprio produto as decisões do TCC (fonte do cálculo, regras aplicadas, texto de IA não verificado).

## 2. Diagnóstico da interface anterior (o que foi removido e por quê)
| Problema | Por que é problema |
|---|---|
| Emojis em todos os rótulos (👋 🩺 🧪 🍷 🏃 🎂) | Ícones sem função reduzem a clareza e a credibilidade; ícones só ajudam quando o significado é inequívoco ou acompanha texto [F: NN/g, *Icon Usability*; *Trustworthiness in Web Design*] |
| Metáfora de chat para um formulário médico | Esconde o progresso, mistura perguntas e respostas no mesmo fluxo visual e dificulta revisar respostas; o padrão recomendado pelo GOV.UK é começar com uma pergunta por página, com revisão final [F: GOV.UK, *Structuring forms*]. *(A expressão anterior, "padrão validado para formulários de baixa confiança", não está na fonte e foi retirada.)* |
| "Tecnologia IA de Ponta", texto em degradê, bolhas flutuantes | Linguagem de marketing e decoração competem com a informação; texto em degradê tem contraste variável |
| Rótulos dentro dos campos (placeholders) | Somem ao digitar e têm baixo contraste [F: NN/g, *Placeholders in Form Fields Are Harmful*] |
| Pergunta o nome | Dado desnecessário ao cálculo; viola o princípio da necessidade [F: LGPD, art. 6º, III] |
| Campos do dataset do Kaggle | Fora do novo escopo (PREVENT/SBC) [D009, D016] |
| `lang="en"`, título "Vite + React" | Leitores de tela pronunciam o português com regras do inglês; título não identifica a página |
| Ant Design | Impõe a identidade visual da biblioteca e aumenta o pacote; a interface precisa de identidade própria e controle fino de acessibilidade |

## 3. Identidade visual

### 3.1 Conceito: "laudo claro"
A interface se inspira em um **laudo bem diagramado**: papel claro, tinta escura, uma única cor de ação e números em destaque. É o gênero de documento que o público já associa a resultados de saúde, sem recorrer aos clichês do setor (coração, eletrocardiograma, estetoscópio, azul "tecnológico" em degradê). A autenticidade vem de a identidade **nascer da função principal do produto** — comunicar "quantas pessoas em 100".

### 3.2 Marca
- **Símbolo:** uma grade de pontos com um ponto destacado, que remete ao pictograma. **Divergência apontada pela banca:** o arquivo `marca.svg` desenha 4 × 4 pontos (1 em 16), não 10 × 10 como este documento dizia. A 32 px uma grade de 100 pontos não seria legível; a marca é uma alusão, não uma representação de "1 em 100". — a síntese do pictograma de 100 pessoas que é o coração da tela de resultado. A marca e a forma de comunicar o risco são a mesma ideia.
- **Nome:** "HeartPredict" composto só em tipografia, com o descritor em português "Risco cardiovascular em 10 anos". O descritor existe porque o público é brasileiro e o nome do projeto está em inglês.

### 3.3 Tipografia
- **Atkinson Hyperlegible Next** (Braille Institute, 2025): projetada para distinguir letras e números parecidos (I/l/1, O/0) em leitores com baixa visão; suporta mais de 150 idiomas, com os diacríticos do português; licença OFL [F: Braille Institute, 2025]. Hospedada no próprio projeto (pacote `@fontsource-variable`), sem requisição ao Google — privacidade e funcionamento offline.
- **Corpo 18 px** (1,125 rem): texto pequeno é o problema de leitura mais persistente entre idosos [F: NN/g]; a GOV.UK usa 19 px no corpo em telas grandes.
- **Escala 1,25**. Tamanhos **medidos pela banca** no navegador: 18 → 25,3 → 31,6 → 39,5 px (o `html{font-size:112.5%}` multiplica todos os `rem`; os valores 22,5/28/35 que constavam aqui estavam errados, e as notas saem com 18 px, não 16). Altura de linha 1,5. *(Correção: a altura de linha não "atende" ao WCAG 1.4.12; esse critério exige que o conteúdo suporte o espaçamento definido pelo usuário, o que é verificado por teste.)* e **linha de no máximo ~65 caracteres** para leitura confortável.
- **Algarismos tabulares** nos números do resultado, para que valores e unidades fiquem alinhados.
- **Zero com traço ("0" distinto de "O")**: característica de desenho da fonte para leitores com baixa visão; mantido de propósito, pois números de exame são o conteúdo principal.

### 3.4 Cores (contraste medido pela fórmula do WCAG) [M]
| Token | Cor | Uso | Contraste |
|---|---|---|---|
| `--papel` | #F7F4EE | Fundo | — (quente e levemente escuro, reduz o ofuscamento do branco puro) |
| `--superficie` | #FFFDF9 | Cartões e campos | — |
| `--tinta` | #17222E | Texto principal | **14,7:1** sobre papel (acima do 7:1 do nível AAA, WCAG 1.4.6; a NN/g aponta texto pequeno e de baixo contraste como problema para idosos, mas **não** recomenda uma razão de contraste) |
| `--tinta-suave` | #44505C | Texto secundário | **7,5:1** |
| `--acento` | #0E5A5E | Botões, links, foco, progresso | **7,2:1** sobre papel; texto branco sobre ele **7,95:1** |
| `--erro` | #A4231B | Mensagens de erro | **6,8:1** |
| `--linha` | #8C8579 | Borda de campos | **3,3:1** (≥ 3:1 exigido para componentes, WCAG 1.4.11) |
| `--risco-baixo` / `--risco-intermediario` / `--risco-alto` | #EAD9B5 / #D9A15F / #8E2F1F | Escala de categoria | Texto sobre cada uma: 11,6:1 / 7,1:1 / branco 8,2:1 |
| `--evento` / `--sem-evento` | #8E2F1F / #C4BCAD | Pictograma | **4,3:1** entre si (≥ 3:1) |

Justificativas:
- **Ação em verde-petróleo, não em vermelho nem em azul-tecnologia:** separa "o que clicar" de "o que é risco" e evita o tom de alarme. O vermelho fica reservado a erros.
- **Categoria em escala sequencial de um só matiz quente (claro → escuro)**, e não em semáforo verde-amarelo-vermelho: dados ordinais pedem escala sequencial por luminosidade, que também é segura para daltonismo [F: Harrower e Brewer 2003, princípio do ColorBrewer; as cores usadas aqui **não** são uma paleta do ColorBrewer]. O semáforo depende da distinção vermelho/verde, a mais afetada pelo daltonismo.
- **A cor nunca é o único sinal:** cada categoria tem rótulo em texto e posição na escala (WCAG 1.4.1).

### 3.5 Ícones
- **Única exceção — o pictograma de 100 pessoas:** figuras humanas simples (estilo "placa de banheiro"). Numa calculadora de risco cardiovascular com 1.502 pessoas de 35 a 75 anos, ícones antropomórficos melhoraram a memorização do risco em relação a blocos e ovais, e foram os preferidos [F: Zikmund-Fisher et al. 2014]. É um ícone com **função demonstrada**, não decoração.
- **Nenhum outro ícone.** Botões, estados e avisos usam texto. Setas de "voltar" são a palavra "Voltar".

## 4. Estrutura e fluxo
1. **Início:** o que a ferramenta faz, para quem é, o que ter em mãos, como o resultado é produzido e como os dados são tratados.
2. **Perguntas, uma por tela** [F: GOV.UK]: idade → sexo → doença cardiovascular prévia → diabetes → colesterol total → HDL → LDL (opcional) → pressão sistólica → anti-hipertensivo → estatina → tabagismo → função renal → agravantes.
   - Critérios de exclusão logo no início (idade fora de 30–79, doença cardiovascular prévia, diabetes): quem está fora do escopo descobre antes de digitar exames [D011].
3. **Revisão** ("Confira suas respostas"), com "Alterar" em cada item [F: padrão *check answers* da GOV.UK].
4. **Resultado.**
5. **Telas de fora do escopo** explicam o motivo e o que fazer, sem tom de erro.

Detalhes de interação:
- Progresso em **texto e barra** ("Pergunta 5 de 13").
- **Botão "Voltar" do navegador funciona** (cada etapa tem um endereço `#/...`): voltar é uma das ações mais usadas na web e quebrá-lo desorienta.
- Rótulo acima do campo, dica abaixo do rótulo, unidade fora do campo [F: NN/g, placeholders].
- Campos numéricos com `inputmode="decimal"` (teclado numérico no celular) e aceitação de vírgula decimal.
- **Erros:** resumo no topo com link para o campo + mensagem junto ao campo, dizendo o que fazer ("Digite um valor entre 90 e 200 mmHg") [F: padrão *error summary* da GOV.UK].
- **Dica de pressão em linguagem brasileira:** "Se sua pressão foi 12 por 8, digite 120."
- **Creatinina como alternativa à TFGe:** muitos laudos trazem só a creatinina; o sistema calcula a TFGe pela CKD-EPI 2021, a mesma equação usada na derivação do PREVENT [F: Inker et al. 2021; Khan et al. 2024].
- **Foco movido para o título** a cada nova tela, para leitores de tela anunciarem a pergunta; título da aba atualizado.

## 5. Tela de resultado (pirâmide invertida)
Ordem = ordem de importância para o usuário.
1. **Frase-resumo** com o risco absoluto: "Seu risco estimado de infarto ou AVC nos próximos 10 anos é de 6%."
2. **Frequência natural + pictograma de 100 pessoas**, com os eventos agrupados no início da grade: "Em 100 pessoas com os mesmos dados, cerca de 6 teriam um infarto ou AVC em 10 anos." Formatos de risco absoluto e recursos visuais melhoram a compreensão [F: Zipkin 2014]. **Ressalva:** a mesma revisão considera **inconclusiva** a comparação entre frequência e percentual; por isso a tela mostra os dois. A vantagem das frequências naturais é sustentada por Gigerenzer e Hoffrage (1995) e Trevena et al. (2013), ainda não lidos por mim. *(Redação anterior, mais forte que a fonte:)* ~~Risco absoluto e frequências naturais melhoram a compreensão em relação a percentuais isolados ou riscos relativos~~, e pictogramas ajudam especialmente pessoas com baixo letramento numérico [F: Zipkin et al. 2014; Galesic et al. 2009].
3. **Categoria da Diretriz SBC 2025** em escala de três faixas iguais (a escala é ordinal, não proporcional) com marcador. Se um agravante reclassificou, a tela diz "O cálculo indica baixo; a história familiar eleva para intermediário" [D010].
4. **Meta de LDL-c** da categoria.
5. **O que mais pesou**, em palavras ("aumentou", "diminuiu", "pouco influenciou") e barras proporcionais à contribuição, com "Como ler" recolhível explicando a pessoa de referência [D012]. O limiar de "pouco influenciou" é o mesmo da métrica de polaridade (5%).
6. **Explicação em linguagem simples**, marcada como **"Texto gerado por inteligência artificial"** e com o aviso de que **ainda não passa pelo verificador** do projeto. Rotular o conteúdo gerado por IA é **boa prática**, inspirada no art. 50 do AI Act. O regulamento não se aplica a este protótipo (não é colocado no mercado da União Europeia e é pesquisa) e, quando se aplica, exige do fornecedor marcação legível por máquina; declarar a ausência do verificador é coerente com o próprio TCC. Carrega **depois** do cálculo, para o número aparecer imediatamente.
7. **Limites do resultado:** calibrado na população dos EUA, não é diagnóstico, conversar com o médico [khan2024prevent; SBC 2025 §4.2].
8. **Ações:** "Imprimir ou salvar em PDF" (para levar ao médico) e "Fazer nova avaliação".

## 6. Movimento
- Durações entre **100 e 300 ms**: ~120 ms para retorno de interação, ~200 ms para troca de tela, ~300 ms para revelar dados (barras e pictograma); acima de ~500 ms a animação passa a atrapalhar [F: NN/g, *Executing UX Animations*].
- Movimento **curto e na direção da leitura** (entrar de baixo, 8 px): indica continuidade sem chamar atenção.
- **Sem contagem progressiva do número de risco:** animar o número sugere precisão e dramatiza o resultado.
- **`prefers-reduced-motion`:** todas as animações são desativadas para quem pede menos movimento no sistema.

## 7. Conteúdo e tom
- Segunda pessoa ("você"), frases curtas, termos técnicos acompanhados de explicação ("HDL, o colesterol 'bom'").
- Sem promessas nem alarme: "risco estimado", nunca "você vai ter".
- Honestidade sobre o que o sistema é: protótipo acadêmico; não substitui avaliação médica; explicação de IA não verificada.
- **Privacidade (texto verdadeiro):** não pedimos nome nem documento e o sistema não armazena as respostas; **para gerar a explicação, os valores são enviados a um serviço de IA externo**. Quem usa precisa saber disso [F: LGPD, art. 6º, VI — transparência].

## 8. Acessibilidade (checklist)
- [x] `lang="pt-BR"`; um `h1` por tela; landmarks (`header`, `main`, `footer`).
- [x] Contrastes medidos (seção 3.4).
- [x] Foco visível de 3 px em `--acento` com recuo (WCAG 2.4.7, Foco visível; a aparência do foco é o 2.4.13, nível AAA. O 2.4.11 trata de foco não encoberto e estava citado por engano.) Em cores forçadas, o foco usa `outline`.
- [x] Alvos com no mínimo 48 px de altura (acima dos 24 px do WCAG 2.5.8).
- [x] Opções de resposta como cartões clicáveis inteiros, com `input` nativo por baixo (teclado e leitor de tela funcionam sem código extra).
- [x] Erros ligados ao campo por `aria-describedby`; resumo de erros com foco.
- [x] Pictograma com descrição textual (`role="img"` + `aria-label`); a informação também está em texto.
- [x] `prefers-reduced-motion`.
- [x] **Auditoria automática axe-core 4 (Deque)**, regras WCAG 2.0/2.1/2.2 A e AA + boas práticas, em 7 telas × 2 larguras (1280 px e 390 px): **0 violações** (29 a 44 verificações aprovadas por tela) — [evidência](../04-evidencias/interface/auditoria-axe-core.txt). Ferramentas automáticas cobrem só parte dos critérios; não substituem avaliação manual nem teste com usuários.
- [x] **Fluxo completo percorrido em Chrome automatizado** (Playwright), desktop e celular, com capturas em [04-evidencias/interface](../04-evidencias/interface/).
- [ ] **Teste com usuários reais** (não feito): recomenda-se um teste rápido com cerca de 5 pessoas do público-alvo, suficiente para encontrar a maioria dos problemas de usabilidade [F: Nielsen, 2000, *Why You Only Need to Test with 5 Users*].

## 9. Implementação
- React + Vite, sem biblioteca de componentes; CSS com variáveis (*tokens*) em `frontend/src/estilos/tokens.css`.
- Conteúdo das perguntas separado dos componentes (`frontend/src/conteudo/perguntas.js`), para revisão de texto sem mexer em código.
- API: `POST /api/avaliacao` (cálculo) e `POST /api/avaliacao/explicacao` (texto de IA), no gateway.

## 10. Referências
- Zipkin DA et al. Evidence-based risk communication: a systematic review. *Ann Intern Med*. 2014;161(4):270-280.
- Galesic M, Garcia-Retamero R, Gigerenzer G. Using icon arrays to communicate medical risks: overcoming low numeracy. *Health Psychol*. 2009;28(2):210-216.
- Zikmund-Fisher BJ et al. Blocks, ovals, or people? Icon type affects risk perceptions and recall of pictographs. *Med Decis Making*. 2014;34(4):443-453.
- Harrower M, Brewer CA. ColorBrewer.org: an online tool for selecting colour schemes for maps. *The Cartographic Journal*. 2003.
- W3C. *Web Content Accessibility Guidelines (WCAG) 2.2*. 2023.
- Nielsen Norman Group: *Usability for Older Adults*; *Placeholders in Form Fields Are Harmful*; *Executing UX Animations: Duration and Motion Characteristics*; *Icon Usability*; *Trustworthiness in Web Design*.
- GOV.UK Design System / Service Manual: *One thing per page*; *Question pages*; *Check answers*; *Error summary*.
- Braille Institute. *Atkinson Hyperlegible Next*. 2025.
- Inker LA et al. New creatinine- and cystatin C-based equations to estimate GFR without race. *N Engl J Med*. 2021.
- Brasil. Lei nº 13.709/2018 (LGPD), art. 6º.
- União Europeia. Regulamento (UE) 2024/1689 (AI Act), art. 50.
- Nielsen J. *Why You Only Need to Test with 5 Users*. NN/g, 2000.
