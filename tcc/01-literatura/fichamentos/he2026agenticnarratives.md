---
chave: he2026agenticnarratives
titulo: An Agentic Approach to Generating XAI-Narratives
autores: [Yifan He, David Martens]
ano: 2026
veiculo: arXiv preprint arXiv:2603.20003
tipo_bib: misc
url: https://arxiv.org/abs/2603.20003
temas: [xai-shap, llm-explicacao, fidelidade, verificador, multiagente, trabalho-mais-proximo]
leitura: parcial
lido_em: 2026-10-06
relevancia: central
---

# Abordagem agêntica para gerar narrativas de XAI (He & Martens, 2026)

> **Profundidade de leitura:** li na íntegra o resumo, a introdução, a metodologia (seções 2.1–2.4), a nota da Tabela 2 e a conclusão. As seções de resultados (3.1–3.5) foram lidas só nos trechos citados abaixo. *Preprint*, sem revisão por pares na data da leitura. Texto: `textos/he2026agenticnarratives.txt`. Trabalho apontado pelo parecer de IA da banca simulada (`05-banca/parecer-ia.md`).

## Referência
HE, Y.; MARTENS, D. An Agentic Approach to Generating XAI-Narratives. arXiv:2603.20003, 2026. Código: https://github.com/ADMAntwerp/SHAPnarrative-agents

## Problema
Narrativas de SHAP escritas por LLM podem contradizer a tabela SHAP. Os trabalhos anteriores avaliam a narrativa só depois de gerada, sem refinamento automático.

## Método
- **Agentes:** *Narrator* (gera e revisa); *Faithful Evaluator* (um LLM extrai, de cada variável citada, posto, sinal e valor; **uma regra, sem LLM,** compara com a tabela SHAP); *Faithful Critic* (transforma os erros em instruções de correção; há uma variante só por regras); *Coherence Agent* (qualidade linguística).
- **Cinco desenhos em comparação:** Basic, Critic, Critic-Rule, Coherent, Coherent-Rule.
- **Dados:** 5 bases tabulares binárias (Student, Fifa, German Credit, **Diabetes**, **Stroke**), 20 instâncias cada (100 no total). Modelo: Random Forest com hiperparâmetros padrão; SHAP TreeExplainer; narrativa limitada às **4 variáveis mais importantes**.
- **LLMs:** Claude Sonnet 4.5, GPT-5, DeepSeek-V3.2-Exp, Mistral Medium 3.1, Llama 3.3 70B. Temperatura 0. Máximo de 3 rodadas (10 em experimento adicional).
- **Ponto de partida:** narrativas geradas por DeepSeek-V3-0324 em 4 execuções; **foi escolhida a pior execução** "para dar mais espaço de melhora".
- **Métricas:** Rank/Sign/Value Accuracy, adaptadas de Ichmoukhamedov et al. (2024), calculadas **pelo próprio Faithful Evaluator**.

## Resultados (trechos lidos)
- Linha de base: acurácias de posto/sinal/valor de 0,900/0,958/0,990; **31 de 100 narrativas** com algum erro de fidelidade.
- Basic, Critic e Critic-Rule melhoram a fidelidade nos 5 LLMs; nenhum desenho vence sempre. Critic e Critic-Rule têm desempenho comparável, o que favorece o crítico por regras.
- Melhor combinação: Claude Sonnet 4.5 no desenho Basic (redução de 90% das narrativas infiéis em 3 rodadas, segundo o resumo), sem chegar a 100%.
- **O Coherence Agent melhora o texto, mas piora a fidelidade.**
- Mais rodadas não melhoram necessariamente; a qualidade da narrativa inicial pesa mais.

## Limitações (declaradas e observadas)
1. **Erros de extração são o problema recorrente** em todos os experimentos; o voto de 5 LLMs atenua, mas não elimina.
2. **Falsos positivos (narrativa infiel julgada fiel) ficam fora do estudo:** "we intentionally exclude false positive cases from this study", por ser inviável conferir manualmente.
3. A fidelidade é sempre "reportada": **quem mede o resultado final é o mesmo avaliador que atua no ciclo**. Não há anotação humana independente do desfecho.
4. A verdade de referência é o SHAP de um Random Forest, tomado como fiel ao modelo por hipótese ("with the assumption that the explanation itself is fully faithful to the prediction model").
5. Mede só posto, sinal e valor das 4 variáveis principais. Não mede variáveis fora do modelo, afirmações sem sustentação nem regras de domínio.
6. Ponto de partida enviesado para baixo (pior de 4 execuções).

## Leitura crítica
É o trabalho mais próximo do TCC e **invalida a frase "nenhum trabalho combina verificador da explicação + sinal/valor + ablação"**. O que ele não tem é exatamente o que as limitações 2 a 5 descrevem.

## Relação com o meu TCC
O TCC passa a ser **replicação com extensão** (D030): testa se o efeito do ciclo de crítica se mantém quando (a) a atribuição de referência é exata (escore clínico publicado, sem aproximação), (b) há regras de uma diretriz clínica (categoria, reclassificação, meta), (c) variáveis plausíveis que não entram no modelo são tratadas como erro, e (d) o desfecho é decidido por anotação humana cega, independente do verificador.

## Dados citáveis
- [C1] Na linha de base, 31 de 100 narrativas continham algum erro de fidelidade; acurácias médias de posto, sinal e valor de 0,900, 0,958 e 0,990 (Seção 3.1, texto após a Tabela 2).
- [C2] O avaliador de fidelidade extrai posto, sinal e valor com um LLM e compara com a tabela SHAP por regra, sem LLM (Seção 2.1, "The Faithful Evaluator").
- [C3] Os autores excluem do estudo os falsos positivos da extração, por ser impraticável verificá-los manualmente (Seção 2.4, nota 8).
- [C4] Os erros de extração de um único LLM são o principal problema recorrente em todos os experimentos (Conclusão).
- [C5] O desenho com crítico por regras tem desempenho comparável ao do crítico com LLM e é mais eficiente (Conclusão).
- [C6] O agente de coerência melhora a qualidade linguística, mas prejudica a fidelidade das narrativas (Conclusão).
- [C7] As narrativas iniciais vieram da pior de quatro execuções do modelo gerador (Seção 2.4, "Baseline Experiment").
