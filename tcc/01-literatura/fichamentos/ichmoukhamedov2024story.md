---
chave: ichmoukhamedov2024story
titulo: "How good is my story? Towards quantitative metrics for evaluating LLM-generated XAI narratives"
autores: [Timour Ichmoukhamedov, James Hinns, David Martens]
ano: 2024
veiculo: arXiv preprint arXiv:2412.10220
tipo_bib: misc
url: https://arxiv.org/abs/2412.10220
temas: [xai-shap, llm-explicacao, fidelidade, metricas]
leitura: parcial
lido_em: 2026-10-06
relevancia: alta
---

# Métricas quantitativas para narrativas de XAI (Ichmoukhamedov, Hinns & Martens, 2024)

> **Profundidade de leitura:** li a definição das métricas de fidelidade, a validação do extrator (Seção III) e a discussão das narrativas manipuladas (Seção IV.2). O restante foi lido só pelo resumo. *Preprint*. Texto: `textos/ichmoukhamedov2024story.txt`.

## Referência
ICHMOUKHAMEDOV, T.; HINNS, J.; MARTENS, D. How good is my story? Towards quantitative metrics for evaluating LLM-generated XAI narratives. arXiv:2412.10220, 2024.

## Método (parte lida)
- Um LLM extrator (GPT-4o) lê a narrativa e devolve, por variável, posto, sinal e valor. As métricas **Rank Agreement, Sign Agreement e Value Agreement** comparam o extraído com a tabela SHAP.
- **Validação do extrator:** 60 narrativas com a tabela permutada foram todas sinalizadas; em 60 narrativas humanas, 1 de 53 corretas foi sinalizada por engano.
- **Narrativas manipuladas:** o LLM recebe uma tabela SHAP com a ordem invertida e os sinais trocados, e a avaliação segue contra a tabela original.

## Resultado central para o TCC
Com a tabela manipulada, a acurácia de sinal medida contra a tabela **original** chega a 30%, quando o esperado seria cerca de 4%. Ou seja: o LLM **"corrige" de volta** até cerca de 30% dos sinais que lhe foram entregues trocados. Os autores interpretam como preferência pelo conhecimento interno em vez do contexto que o contradiz.

## Leitura crítica
- **Cuidado com a leitura do número.** O parecer de IA da banca escreveu que "a concordância de sinal cai para cerca de 30%". O texto diz o contrário em relação à tabela fornecida: a fidelidade à tabela entregue cai de cerca de 96% para cerca de 70%, porque 30% dos sinais voltam ao valor "intuitivo". O argumento continua valendo, com o número correto.
- A manipulação inverte tudo, o que produz afirmações absurdas. As atribuições do TCC são contraintuitivas, mas verdadeiras (remédio como marcador de doença; idade abaixo da referência), cenário que este trabalho não testa.

## Relação com o meu TCC
- **Métricas:** polaridade e exatidão numérica do TCC correspondem a Sign/Value Agreement. O TCC deve citá-las como origem e declarar o que acrescenta: unidade de afirmação atômica, tolerância ε, distinção entre alvo "risco" e alvo "categoria", variáveis fora do modelo.
- **Efeito teto (R2):** é a melhor evidência de que os erros de sinal aparecem quando a atribuição contraria o senso comum. Justifica as vinhetas-armadilha e a estratificação do piloto.

## Dados citáveis
- [C1] As métricas Rank, Sign e Value Agreement comparam o posto, o sinal e o valor extraídos da narrativa com os da tabela SHAP (Seção III).
- [C2] Quando o LLM recebe uma tabela SHAP com os sinais invertidos, até cerca de 30% dos sinais aparecem na narrativa "corrigidos" para o valor original, contra cerca de 4% esperados (Seção IV.2).
- [C3] Os autores relacionam o fenômeno à preferência dos LLMs pelo conhecimento paramétrico em vez do contexto que o contradiz (Seção IV.2).
- [C4] Na validação, o extrator sinalizou as 60 narrativas manipuladas e errou em 1 de 53 narrativas humanas corretas (Seção III).
