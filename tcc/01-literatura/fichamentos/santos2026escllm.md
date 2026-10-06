---
chave: santos2026escllm
titulo: Large language models approach clinician performance in ESC cardiovascular risk stratification: a vignette-based benchmark study
autores: [José Ferreira Santos, Regina de Brito Duarte, Inês Mota, Rita Carvalheira Santos, José Maria Moreira, Joana Campos, Nuno André Silva, Bernardo Neves, Ricardo Ladeiras-Lopes, Francisca Leite, Hélder Dores]
ano: 2026
veiculo: European Heart Journal - Digital Health
volume: 7
paginas: ztag073
tipo_bib: article
doi: 10.1093/ehjdh/ztag073
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC13215473/
temas: [llm-risco-cv, risco-cardiovascular, portugues, trabalho-mais-proximo]
leitura: resumo
lido_em: 2026-09-29
relevancia: alta
---

# Santos et al. (EHJ Digital Health, 2026) — LLMs na estratificação ESC/SCORE2

> **Leitura: resumo (abstract no PMC).** Texto completo disponível no PMC (≈ 6.900 palavras) — **ler antes de citar números**. Há um estudo-piloto anterior dos mesmos autores (PMC12794879, suplemento da EHJ-DH), com 30 vinhetas em português, Gemini 2.0 Flash × GPT-4o, κ e teste de McNemar.

## O que se sabe (do resumo)
- 11 LLMs, **30 vinhetas simuladas em português e inglês**, estratificação pelo SCORE2 da ESC em três competências: extrair fatores de risco, calcular o escore e aplicar os limiares da diretriz.
- Padrão de referência: comitê de 3 cardiologistas; benchmark humano: 8 clínicos independentes.
- Extração de fatores quase perfeita (micro-F1 0,97–0,99).
- Categoria final com concordância moderada (melhor: GPT-4o, κw 0,69); 10 de 11 modelos **subestimaram** o risco.
- **Recalcular o SCORE2 de forma determinística** com as variáveis extraídas pelo próprio LLM elevou a concordância para **κw 0,85–0,90** em todos os modelos: "computational execution was the primary failure mode".
- Clínicos individuais: κw 0,52.
- Desempenho **semelhante em português e inglês**.

## Relação com o meu TCC
- **Mais uma evidência independente para H1 e D002**, agora **em português** e em estratificação cardiovascular.
- **Derruba a afirmação de que "português é uma lacuna"**: o idioma sozinho não é contribuição (D018).
- Precedente metodológico direto: vinhetas simuladas, comitê como referência, κ ponderado, McNemar.
- Não avalia explicações nem fidelidade → a lacuna central (verificação da explicação) se mantém.
- Diferenças: SCORE2/ESC (Europa) × PREVENT/SBC (Brasil); português provavelmente europeu (autores portugueses) — **verificar**.

## Dados citáveis
- [C1] Em 11 LLMs e 30 vinhetas em português e inglês, a recalculação determinística do SCORE2 com as variáveis extraídas pelos modelos elevou a concordância da categoria para κw 0,85–0,90, indicando que a execução do cálculo era a principal fonte de erro (Abstract).
- [C2] O desempenho foi amplamente consistente entre português e inglês (Abstract).
