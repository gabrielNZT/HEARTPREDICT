---
titulo: Próximos passos (triagem de pendências)
status: vigente
atualizado: 2026-09-29
resumo: Triagem das 59 pendências em riscos que podem mudar o rumo, bloqueios técnicos e itens que podem esperar; ordem de execução recomendada.
---

# Próximos passos

Triagem das 59 pendências abertas em [pendencias.md](pendencias.md). Critério: **o que pode invalidar ou mudar o trabalho vem antes do que só o completa.**

## A. Riscos que podem mudar o rumo (resolver primeiro)

| # | Risco | Por que pode mudar o rumo | Como resolver |
|---|---|---|---|
| R1 | **O orientador ainda não validou a Opção A** | Todo o desenho (D001–D022) foi construído sem ele; a crítica original era de fundamentação e posicionamento | Reunião com proposta de 1 página + escopo (núcleo × extensões) + justificativa do JADE + decisões de D010 |
| R2 | **Efeito teto: os LLMs atuais podem já explicar sem erro** | Se a configuração com ferramenta (sem verificador) já for ~100% fiel, H2 não tem o que medir. Lee 2025 usou GPT-4 de 2024 e Zhu 2026 um modelo de 3B; Santos 2026 mostrou extração quase perfeita. **Não há evidência de que o problema persista nos modelos de 2026 nesta tarefa específica** | **Piloto** (seção C) antes de implementar o resto |
| R3 | **Novidade:** outro trabalho pode já ter feito verificador + fidelidade em risco cardiovascular | A contribuição (D003, D018) mudaria | Busca estruturada documentada (C8), em paralelo ao piloto |
| R4 | **Prazo e normas do curso** (O001, O002) | Definem se o núcleo cabe e se há exigências formais (qualificação, CEP) | Perguntar na mesma reunião de R1 |
| R5 | **Acesso e custo dos LLMs** | Sem chave/orçamento ou hardware para o modelo aberto, D014 muda | Verificar cota/custo da API do Gemini e opção de modelo aberto via API ou local |

## B. Bloqueios técnicos (nada do núcleo anda sem eles)

| # | Bloqueio | Quem resolve |
|---|---|---|
| T1 | **Tabela S12 do PREVENT** (coeficientes) — download automático bloqueado | **Você**, pelo navegador (link em pendencias.md) |
| T2 | **Compilar e testar de ponta a ponta** após a limpeza (`mvn clean package`) | Você (não há Maven neste ambiente) |
| T3 | **Escolher o modelo Gemini** (`GEMINI_MODEL`) e registrar a versão | Você, na página oficial de depreciações |

## C. Piloto de viabilidade (responde R2) — proposta

**Objetivo:** medir se, **sem verificador**, os LLMs atuais ainda erram ao explicar o PREVENT. Não é o experimento; é um teste para decidir se ele faz sentido.

- **Mínimo necessário:** PREVENT + atribuição em Python (depende de T1), 20–30 vinhetas variadas (incluindo casos-armadilha, como IMC alto com risco baixo), configuração C-ferramenta com os 2 LLMs, 3 repetições.
- **Não precisa** de JADE reescrito, NHANES nem anotação dupla: anotação rápida por você, usando as definições de [metricas-fidelidade](../03-metodologia/metricas-fidelidade.md).
- **Regra de decisão (definir antes de rodar):**
  - **erros frequentes** (ex.: ≥ 10% das explicações com alguma afirmação não sustentada) → segue o desenho atual;
  - **erros raros** → ajustar a tarefa para onde o problema aparece: linguagem para leigos, recomendações de conduta, modelos menores/abertos, casos com agravantes ou dados ausentes — ou reenquadrar a contribuição como *demonstração de que a verificação é necessária só em certos cenários*.
- O limiar de 10% é autoral e deve ser acertado com o orientador.

## C.1 Estado do piloto (29/09/2026)
- **Pronto e testado** em `experimentos/piloto/`: calculadora PREVENT (reproduz os 6 valores publicados), atribuição de Shapley, regras SBC, 24 vinhetas, prompt, cliente de LLM, pré-anotação e resumo com a regra de decisão.
- **Falta:** as chaves de API (`.env`) para rodar os LLMs, e a anotação manual.
- Os coeficientes vêm do pacote `preventr` (provisório); a validação contra o artigo reduz, mas não elimina, a necessidade de T1.
- **Achado de desenho:** na atribuição, o uso de anti-hipertensivo **aumenta** o risco (é um marcador de hipertensão no modelo) e idades abaixo de 55 anos **diminuem**. Por isso o prompt explica a pessoa de referência; sem isso, "erros de polaridade" seriam artefatos do prompt.

## D. Pode esperar (não muda o rumo)
Conferência de metadados (isern, jacovi, hevner, NeurIPS etc.), fichamentos de fundamentação (Huang, CRITIC, Lundberg & Lee, Wooldridge…), H3 e seus itens (B3, chan2025vies, Kusner), B4 e B5, PNS, diretriz ACC/AHA 2026, errata da SBC, licença, script único de execução, requirements do serviço de risco (junto com o PREVENT).

## Ordem recomendada
1. **Agora:** T1, T2, T3 (você) · eu preparo a proposta de 1 página para o orientador e o protocolo do piloto.
2. **Reunião com o orientador:** R1 + R4 (+ limiar do piloto).
3. **Piloto** (R2) + **busca estruturada** (R3) em paralelo.
4. **Decisão:** seguir, ajustar a tarefa ou reenquadrar.
5. Só então: reescrita do JADE (D021), NHANES, protocolo de anotação, cálculo de amostra, experimento.
