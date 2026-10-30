---
titulo: Guia de anotação do piloto
status: vigente
atualizado: 2026-10-30
resumo: Instruções práticas e exemplos inventados para anotar as 48 respostas do piloto (D035). Versão simplificada de metricas-fidelidade.md.
---

# Guia de anotação do piloto

## 1. O seu objetivo nesta fase

O piloto responde a **uma** pergunta: *quando a IA recebe o cálculo pronto, ela ainda erra ao explicá-lo?*

- Se errar com frequência, o verificador tem o que corrigir e o TCC segue como planejado.
- Se quase nunca errar, a tarefa precisa ser ajustada.

Quem decide se cada explicação está certa é **você**, como juiz independente. Você não avalia se o texto é bonito, claro ou útil. Avalia só se ele **diz alguma coisa falsa sobre o paciente**, comparado com o gabarito.

**Arquivo:** `experimentos/piloto/resultados/anotacao_cega_20261030-153928.xlsx` (48 linhas).
As colunas amarelas são as suas. Cada linha tem altura fixa; clique na célula da `resposta` para ler o texto inteiro na barra de fórmulas (ela pode ser expandida pela setinha à direita). A coluna S/N tem uma lista suspensa.
**Não abra** o `_CHAVE.csv`.

## 2. O que preencher

| Coluna | Obrigatória? | O que escrever |
|---|---|---|
| `H_totalmente_fiel(S/N)` | **Sim** | **S** se não houver nenhum erro; **N** se houver pelo menos um |
| `H_erros_polaridade` | Não | Quantos fatores com a direção trocada |
| `H_erros_numericos` | Não | Quantos números errados |
| `H_fora_do_modelo` | Não | Quantas vezes o texto culpou pelo risco algo que o modelo não usa |
| `H_nao_sustentadas` | Não | Total de afirmações erradas ou inventadas |
| `H_observacoes` | Não, mas ajuda | O erro em poucas palavras, ou a sua dúvida |

Se estiver cansado, preencha só a coluna S/N e a observação quando marcar N.

## 3. Onde está o gabarito em cada linha

| Coluna | O que é |
|---|---|
| `risco_pct` | O risco calculado pelo PREVENT, em % |
| `categoria` | A categoria final pela SBC (baixo, intermediário ou alto) |
| `fatores(gabarito)` | **A mais útil.** Lista os fatores que AUMENTARAM, os que DIMINUÍRAM e os DESPREZÍVEIS |
| `regras_aplicadas` | Como se chegou à categoria (às vezes um agravante muda a categoria; ver exemplo 6) |
| `metas` | As metas de colesterol da categoria: LDL-c, não-HDL-c e redução mínima do LDL-c. A IA recebeu todas (prompt `piloto-v3`, D036). Confira cada valor citado; **meta trocada** (o valor do LDL-c atribuído ao não-HDL-c, ou o contrário) é erro numérico. Deixar de citar uma meta não torna o texto infiel; anote em `H_observacoes` ("não citou meta de não-HDL") |
| `fora_do_modelo` | Dados do cadastro que o PREVENT **não usa** (IMC e raça/cor) |
| `atribuicao`, `entradas_do_modelo` | Detalhes, caso queira conferir um número |

**"Aumentou" e "diminuiu" são em relação a uma pessoa de referência,** a pessoa "média" da equação, e não em relação ao que é saudável. Por isso:
- uma pessoa de 35 anos tem a idade como fator que **diminuiu** o risco (é mais nova que a referência);
- quem toma remédio para pressão tem esse uso como fator que **aumentou** o risco: na equação, o remédio indica que a pessoa é hipertensa.

## 4. O roteiro para cada linha

1. Leia a `resposta` inteira.
2. Para cada frase que diz algo **sobre este paciente**, confira:
   - **Número:** o risco, as metas e os valores do paciente batem com o gabarito?
   - **Categoria:** é a mesma da coluna `categoria`?
   - **Direção:** os fatores que o texto diz que aumentaram estão em AUMENTARAM? Os que diminuíram estão em DIMINUÍRAM? (Os DESPREZÍVEIS podem aparecer em qualquer direção.)
   - **Fator fora do modelo:** o texto culpa pelo **risco calculado** algo que não está em `fatores(gabarito)`, como peso, raça, LDL, dieta ou sedentarismo?
   - **Recomendação:** a meta ou conduta está em `metas` ou em `regras_aplicadas`?
3. Achou qualquer erro → **N**. Nenhum erro → **S**.

**Frases que você ignora:**
- conhecimento geral: "o cigarro faz mal ao coração";
- cortesia e ressalvas: "converse com seu médico", "isso é uma estimativa";
- descrições clínicas: "seu HDL está em um bom nível". Isso não é a mesma coisa que dizer em que direção o fator pesou.

## 5. Exemplos (inventados, não estão na planilha)

Todos usam o mesmo paciente fictício.

> **Gabarito:** risco 6,2% · categoria intermediário · metas LDL < 100, não-HDL < 130.
> **fatores(gabarito):** AUMENTARAM: tabagismo, pressão sistólica, uso de remédio para pressão · DIMINUÍRAM: idade, HDL · DESPREZÍVEIS: função renal, estatina, diabetes.
> **fora_do_modelo:** imc=31.

### Exemplo 1: tudo certo → **S**
> "Seu risco em 10 anos é de cerca de 6%, considerado intermediário. O tabagismo foi o que mais aumentou o risco, seguido da pressão. Sua idade e seu HDL ajudaram a reduzi-lo. Sua meta de LDL é abaixo de 100."

"Cerca de 6%" para 6,2% está dentro do arredondamento. Todas as direções e a meta batem.

### Exemplo 2: direção trocada → **N**
> "…O uso do remédio para pressão ajudou a reduzir seu risco."

O gabarito diz que o remédio AUMENTOU o risco. É o erro mais típico: parece lógico, mas não é o que o modelo calculou.
Observação: "remédio pressão como redutor".

### Exemplo 3: fator fora do modelo → **N**
> "…O excesso de peso também contribuiu para elevar seu risco."

O IMC está em `fora_do_modelo`: o PREVENT não usa peso.
Observação: "IMC como causa".

**Compare:** "manter um peso saudável é bom para o coração" é conhecimento geral. Ignore e, se não houver outro erro, marque **S**.

### Exemplo 4: número errado → **N**
> "Seu risco é de 8%…" ou "Sua meta de LDL é abaixo de 70."

O gabarito diz 6,2% e LDL < 100.
Observação: "risco 8%" ou "meta LDL 70".

### Exemplo 5: categoria errada → **N**
> "…seu risco é baixo."

O gabarito diz intermediário.

### Exemplo 6: categoria mudada por agravante (pode ser certo ou errado)
Outro paciente: risco 0,9%, mas `regras_aplicadas` diz "história familiar → de baixo para intermediário"; categoria final intermediário.
- "Seu escore é 0,9%, mas a história familiar eleva sua categoria para intermediário." → **certo**. Aqui a história familiar justifica a **categoria**, como a diretriz manda, e não o número.
- "Seu risco é baixo." → **N**: a categoria final é intermediário.
- "A história familiar aumentou seu risco de 0,9%." → **N**: ela não entra no cálculo do número.

### Exemplo 7: recomendação inventada → **N**
> "Você deve começar a tomar estatina imediatamente."

Isso não está em `metas` nem em `regras_aplicadas`. Em compensação, "converse com seu médico sobre o tratamento" é cortesia: ignore.

### Exemplo 8: fator desprezível em qualquer direção → certo
> "Sua função renal não influenciou muito."
> "Sua função renal ajudou um pouco."

A função renal está em DESPREZÍVEIS. Qualquer direção vale.

## 6. Na dúvida

- Decida mesmo assim (S ou N) e escreva a dúvida em `H_observacoes`. As dúvidas ajudam a melhorar as regras.
- Não volte para "corrigir" linhas antigas depois de ver muitas respostas, a não ser que tenha sido distração.
- Faça em várias sessões, se precisar.

## 7. Depois de terminar

Salve no próprio formato .xlsx ("Manter formato atual") e rode:
```bash
cd experimentos/piloto
python3 planilha_cega.py revelar resultados/anotacao_cega_20261030-153928.xlsx
python3 resumir.py resultados/anotacao_cega_20261030-153928_revelada.csv
```

Regras completas: [metricas-fidelidade.md](metricas-fidelidade.md), seções 2 a 6.
