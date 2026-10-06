---
titulo: Parecer de banca — metodologia de pesquisa
status: vigente
atualizado: 2026-09-29
resumo: Auditoria do desenho científico (pergunta, hipóteses, DSR, desenho experimental, métricas, estatística, piloto D023, viabilidade), com notas, problemas classificados, perguntas da banca, verificações executadas e cálculo de poder para McNemar.
---

# Parecer de banca — Metodologia de Pesquisa

**Avaliador(a):** membro de banca, área de Metodologia de Pesquisa em Computação
**Objeto:** projeto de TCC "Verificação de fidelidade em explicações geradas por LLM para estratificação de risco cardiovascular" (estado do repositório em 29/09/2026)
**Anexos:** `tcc/05-banca/anexos/metodologia/` (scripts `v1_verificar_piloto.py` e `v2_poder_mcnemar.py`, saídas `v1_saida.txt` e `v2_saida.txt`, figuras `fig1_n_mcnemar.png` e `fig2_regra_piloto.png`)

---

## 1. Parecer resumido e veredito

O projeto tem uma pergunta de pesquisa estreita, refutável e bem situada na literatura. O registro de decisões (D001–D025), a marcação [P]/[S]/[A] de cada escolha e a autocrítica (brechas B1–B7, auditoria C1–C9) estão acima do que se costuma ver na graduação. Mas o **desenho de avaliação de H2**, que é a contribuição central, ainda não está fechado. Faltam o tamanho de amostra e o plano de análise: unidade de análise, agregação das repetições, multiplicidade e o que fazer quando os 2 LLMs discordam. A circularidade entre o verificador e as métricas (B1) está reconhecida, mas não resolvida. Também não há regra para as explicações **bloqueadas** nem controle para o custo computacional extra do ciclo de correção. A regra de decisão do piloto (D023) tem baixo poder discriminante, é aplicada a uma amostra enriquecida de armadilhas (20/24) e está implementada com uma unidade de análise diferente da que ela mesma declara.

**Veredito: aprovaria com ressalvas** — como **projeto/qualificação**. Os três problemas críticos (seção 4.1) precisam ser resolvidos e registrados como decisões **antes** de rodar o experimento. Um TCC final entregue com o desenho no estado atual não conseguiria sustentar uma conclusão sobre H2, fosse ela positiva ou negativa.

---

## 2. Notas por critério (0–10)

| Critério | Nota | Justificativa |
|---|---|---|
| Clareza da pergunta | **7,5** | A pergunta é comparativa, tem um contraste explícito e pode ser refutada (`proposta.md:25`). Perde pontos por incluir o "LLM para coerência semântica" (nível 2), que D020 tirou do núcleo (`escopo-e-arquitetura.md:55`, `decisoes.md:137`). Do jeito que está escrita, a pergunta não é respondida pelo núcleo. |
| Hipóteses | **6,0** | H2 tem mecanismo (feedback externo e específico, sustentado por Huang 2024 e CRITIC) e um desfecho definido ("totalmente fiel"). Faltam o tamanho de efeito mínimo de interesse e o critério para os 2 LLMs. H1 é quase tautológica em C-ferramenta, porque a categoria é entregue ao LLM (`prompt.py:46`). H3 depende de uma checagem (variável fora do modelo) que não está na especificação do verificador de nível 1 (`proposta.md:58`) e, por ser evento raro, fica sem poder estatístico (seção 6). |
| Desenho experimental | **5,0** | A ablação por composição (C-ferramenta × C-verificador) é o ponto certo. Porém: o bloqueio não tem tratamento no desfecho; não há controle de "mais tentativas sem feedback"; o baseline forte (B2) está em aberto (`pendencias.md:95`); a anotação é feita pelo próprio autor sem cegamento; e não há uma seção de ameaças à validade no formato de Wohlin et al. |
| Métricas | **6,5** | As definições operacionais em `metricas-fidelidade.md` são o melhor artefato metodológico do projeto: unidade atômica, gabarito R(v), ε com sensibilidade, tolerâncias com fonte. Mas: a validação ainda não foi feita (seção 7 do documento); top-k e "consistência", citadas em H2 (`proposta.md:29,95`), não estão definidas; o nome do construto ("fidelidade", no sentido de Jacovi & Goldberg) está deslocado; e a circularidade B1 continua. |
| Estatística | **4,0** | McNemar e bootstrap são escolhas adequadas, e a agregação por vinheta está prevista (`metricas-fidelidade.md:174`). Não há cálculo de n (`proposta.md:104`, `pendencias.md:52`), regra de agregação das repetições, variante do teste (assintótico/exato/mid-p), correção para multiplicidade, tratamento dos dados agrupados nem efeito mínimo detectável. |
| Viabilidade | **6,0** | O núcleo × extensões (D020) foi uma boa decisão, e o piloto está pronto e testado (7 testes passam). O núcleo ainda soma a reescrita do JADE com FIPA, o NHANES, 2 LLMs × 3 configurações × repetições, um extrator independente (que também precisa ser validado) e anotação dupla. Isso dá 1.800–3.600 textos para 100–200 vinhetas (seção 6, item e). |
| Coerência geral | **6,5** | A rastreabilidade problema → decisão → fonte é exemplar. Mas há deriva entre documentos: TRIPOD+AI, calibração e *leakage* na proposta sem modelo treinado no núcleo; "português" ainda como lacuna; a justificativa do JADE pelo MAST retratada em um lugar e mantida em outro; ✔ em viés demográfico na tabela de trabalhos relacionados, sendo que H3 é extensão. |

---

## 3. Pontos fortes (com evidência)

1. **Pergunta estreita e contribuição reposicionada com honestidade.** D003 (`decisoes.md:24-28`) e D018 (`decisoes.md:124-127`) abandonam a novidade genérica ("LLM explica SHAP") e o idioma como diferencial, depois da leitura de Santos 2026. Isso é maturidade científica.
2. **Gabarito determinístico e exato.** O PREVENT, com Shapley exato em log-odds (D012), dá uma referência sem aproximação. **Verifiquei** a propriedade de eficiência: Σφ = L(x) − L(ref) com erro máximo de 4,4·10⁻¹⁵ nas 24 vinhetas (`v1_saida.txt`, item 1). Os 7 testes unitários passam e reproduzem os valores publicados.
3. **Separação cálculo × linguagem bem fundamentada** (D002), com evidência primária lida na íntegra (Roeschl 2026, AgentMD, MedCalc-Bench).
4. **Métricas com definição operacional e níveis de fundamento.** `metricas-fidelidade.md` define a unidade atômica, os tipos de afirmação, o alvo (risco × categoria, §5.2), ε com análise de sensibilidade (§3.3, §9) e um critério de uso condicionado a κ ≥ 0,60 (§7.6).
5. **Consciência explícita das ameaças.** B1 (circularidade), B2 (espantalho), B3 (contrafactual de sexo inválido) e B6 (texto × JSON) estão identificadas por escrito (`fundamentacao-por-parte.md:104-131`). A brecha B3 foi incorporada ao desenho (D017).
6. **Piloto de viabilidade antes da implementação (D023).** Testar o risco de efeito teto (R2) antes de investir no JADE e no NHANES é gestão de risco de pesquisa correta. A limitação central do piloto está declarada no README (`experimentos/piloto/README.md:56`).
7. **Reprodutibilidade planejada.** O piloto registra modelo, temperatura, *hash* do prompt e *commit* (`rodar_piloto.py:63-71`). Há um *checklist* de reprodutibilidade (`tecnologias.md:50-57`).
8. **Escopo alinhado à diretriz.** D011 transcreve o domínio exato em que a SBC 2025 manda usar o escore (seção 4.1).

---

## 4. Problemas

### 4.1 Críticos (impedem conclusão válida sobre H2)

#### CR1 — Não há tamanho de amostra nem plano de análise estatística pré-especificado
- **Descrição.** O experimento principal não tem n. Também faltam: a regra de agregação das N repetições em um desfecho binário por vinheta (qualquer erro? maioria? proporção?); a variante do McNemar; a correção para múltiplas comparações (3 pares de configurações × 2 LLMs × 4 métricas × análises de sensibilidade); o critério de H2 quando só um LLM mostra efeito; e o efeito mínimo de interesse.
- **Evidência.** `proposta.md:104` ("Definir o tamanho da amostra antes de rodar"); `pendencias.md:52` ("C5: cálculo de tamanho de amostra após piloto"); `auditoria-decisoes-autorais.md:48` (C5 "Ainda não calculado"); `metricas-fidelidade.md:174` diz que as repetições são "agregadas por vinheta", sem dizer como.
- **Cálculo da banca** (`v2_poder_mcnemar.py`, Connor 1987, conferido por simulação com o teste mid-p). Considere pA = taxa de explicações não totalmente fiéis em C-ferramenta, r = fração corrigida pelo verificador e q = fração de erros novos introduzidos. Com poder de 80% e α = 0,025 (Bonferroni para 2 LLMs):

  | pA | r | q | n de vinhetas |
  |---|---|---|---|
  | 0,10 | 0,5 | 0,03 | **1.381** |
  | 0,10 | 0,8 | 0,03 | 360 |
  | 0,20 | 0,5 | 0,03 | 202 |
  | 0,20 | 0,8 | 0,03 | 92 |
  | 0,30 | 0,5 | 0,03 | 96 |
  | 0,30 | 0,8 | 0,03 | 50 |
  | 0,50 | 0,8 | 0,01 | 22 |

  O poder simulado no n calculado ficou entre 0,81 e 0,90 (`v2_saida.txt`, item a), o que confirma que a fórmula é adequada/conservadora. **Figura 1** (`anexos/metodologia/fig1_n_mcnemar.png`): n cresce de forma explosiva quando pA < 15%.
- **Impacto.** O n depende criticamente de pA, e pA é exatamente o que o piloto deveria estimar. Com pA ≈ 10% (valor que o próprio limiar do piloto considera "suficiente"), seriam necessárias **centenas a milhares** de vinhetas. Isso é inviável com a anotação humana planejada. Existe, portanto, uma **inconsistência interna**: o limiar de viabilidade do piloto (10%) fica abaixo da taxa que torna o experimento principal factível.
- **Recomendação.** (1) Registrar uma decisão D0xx com: desfecho primário único ("totalmente fiel", C-ferramenta × C-verificador); unidade = vinheta; agregação pré-definida (sugestão: uma repetição pré-escolhida para o teste primário e as demais em análise de sensibilidade, ou um modelo logístico misto com intercepto aleatório por vinheta); teste mid-p (Fagerland et al. 2013); Holm entre os 2 LLMs; e H2 "confirmada" só se ambos os LLMs mostrarem efeito na mesma direção (ou análise estratificada pré-declarada). (2) Recalcular o n com pA, r e q **medidos no piloto** (ver CR3). (3) Declarar o **efeito mínimo de interesse** (ex.: redução absoluta ≥ 10 p.p.) e reportar sempre a diferença pareada com IC, não só o p-valor. (4) Para análises no nível da resposta, usar erros-padrão agrupados por vinheta (Miller 2024) ou McNemar para dados agrupados (Obuchowski 1998).

#### CR2 — H2 pode ser "vencida por construção": circularidade (B1), bloqueios sem regra e confundimento por custo
- **Descrição.** Há três mecanismos que tornam C-verificador melhor sem que o verificador seja o que se quer demonstrar.
  1. **Circularidade.** O verificador de nível 1 checa números, sinal e categoria (`proposta.md:58`), e as métricas 1, 2 e 4 medem exatamente essas coisas. Mesmo com um "extrator diferente" (`metricas-fidelidade.md:162`), o **construto** é o mesmo. O ganho nas dimensões checadas é esperado *a priori* (lei de Goodhart, que o próprio projeto cita em `fundamentacao-por-parte.md:105`). A pergunta informativa é outra: (a) quanto o verificador **deixa passar** (sensibilidade da extração em texto livre) e (b) se a reescrita **introduz** erros ou omissões nas dimensões não checadas.
  2. **Bloqueio.** Após N ciclos a explicação é bloqueada (`proposta.md:60`, `decisoes.md:37`). Nenhum documento diz como o bloqueio entra no desfecho. Se o bloqueio for excluído, ou contado como "sem afirmação infiel", C-verificador ganha por abstenção.
  3. **Custo computacional e número de tentativas.** C-verificador faz até N+1 chamadas; C-ferramenta faz 1. Sem um controle do tipo "C-ferramenta com N tentativas e seleção sem feedback específico" (*best-of-N*), ou "autocrítica sem ferramenta" (Huang et al. 2024), não dá para atribuir o ganho ao **feedback específico** — que é o mecanismo alegado (`auditoria-decisoes-autorais.md:27`, A6).
- **Evidência.** `pendencias.md:94` (B1 não resolvida); busca por "bloque" em `tcc/00-projeto`, `02-argumentacao` e `03-metodologia`: nenhuma regra de análise, só a descrição do mecanismo (`justificativa-jade.md:24,37`).
- **Impacto.** Ameaça à **validade interna** e **de construto** do resultado central. Um resultado positivo em H2 seria contestado por qualquer banca.
- **Recomendação.** (1) Regra de **intenção de tratar**: explicação bloqueada = "não entregue", reportada como **terceiro desfecho** (fiel / infiel / bloqueada), com análise primária conservadora (bloqueio = falha) e sensibilidade. (2) Acrescentar ao núcleo uma medida que o verificador **não** checa: **cobertura** (top-k presente, que já está em H2 mas não definida) e **omissões**, para detectar o verificador que vence porque a explicação passa a dizer menos. Reportar o número de afirmações por texto. (3) Desfecho primário decidido por **anotação humana cega** à configuração no contraste primário, não pelo extrator automático. (4) Se o orçamento permitir, uma 4ª condição barata: C-ferramenta com regeneração até N vezes, sem feedback. Se não permitir, declarar a limitação e não afirmar que "o feedback específico é a causa". (5) Reportar a matriz de confusão do verificador contra o padrão humano (sensibilidade/especificidade), como já previsto em `proposta.md:98`.

#### CR3 — A regra de decisão do piloto (D023) não discrimina, é enviesada pela amostra e está implementada de forma inconsistente
- **Descrição e evidência.**
  1. **Baixo poder discriminante.** Com 24 vinhetas × 3 repetições e a regra "taxa ≥ 10% → segue", a probabilidade de "SEGUE" é **0,44** quando a taxa real é 10%, **0,17–0,24** quando é 7,5% e **0,64–0,87** quando é 12,5–15% (`v2_saida.txt`, item b; **Figura 2**, `fig2_regra_piloto.png`). O IC95% de Wilson para 7/72 vai de **4,8% a 18,7%**. Com correlação intra-vinheta de 0,3, o n efetivo cai de 72 para ≈ 45.
  2. **Amostra enriquecida.** Pelos critérios que o próprio `vinhetas.py:4-9` declara, **20 de 24 vinhetas** têm ao menos um gatilho de erro (`v1_saida.txt`, item 4). A categoria de 6 delas foi alterada por regra e só 2 têm risco ≥ 20% (item 3). O README reconhece que a taxa "não estima a taxa em uso real" (`README.md:56`), **mas a regra de decisão trata essa taxa como se estimasse**. No cenário ilustrativo p_armadilha = 15% e p_típica = 3%, o piloto marcaria 13% (SEGUE), enquanto uma população com 20–40% de armadilhas teria 5–8% (AJUSTA) (`v2_saida.txt`, item c).
  3. **Unidade inconsistente (defeito no código).** `resumir.py:5` declara que "a unidade de análise é a vinheta", mas a regra usa a taxa por resposta (`resumir.py:40,44`). Teste com um CSV sintético em que 7 de 24 vinhetas (29%) têm erro em 1 de 3 repetições: a saída é "7/72 respostas com erro (**10%**) … 7/24 vinhetas com ≥1 erro → **AJUSTAR**". Além de usar a unidade errada, o valor exibido arredondado (10%) contradiz a decisão (9,7% < 10%).
  4. **Ramo "AJUSTAR" = caminhos que se bifurcam.** Entre as saídas previstas estão trocar para "modelos menores/abertos" e para cenários onde o problema aparece (`proximos-passos.md:38`). Escolher a condição **depois** de ver onde o verificador ajuda é seleção pós-hoc que infla a validade aparente.
  5. O piloto roda a 0,7 de temperatura (`README.md:52`), mas a temperatura do experimento não está definida (`pendencias.md:71`). As taxas podem não se transferir.
  6. O piloto só mede C-ferramenta, então **não estima r nem q**, que são necessários para o n (CR1).
- **Impacto.** A decisão de rumo mais importante do TCC depende de algo próximo de um cara-ou-coroa perto do limiar, calculado sobre uma amostra que infla a taxa e com um defeito de implementação.
- **Recomendação.** (1) Separar o piloto em dois estratos, **típico** e **armadilha**, e aplicar a regra ao estrato típico (ou ponderar pela composição prevista do NHANES). (2) Trocar a regra pontual por uma regra com **zona de indiferença**: segue se o limite inferior do IC95% for > 5%; ajusta se o limite superior for < 10%; senão, amplia o piloto. (3) Corrigir `resumir.py` para decidir pela unidade declarada, ou declarar a unidade correta. (4) Rodar **offline o verificador determinístico** sobre as respostas do piloto para estimar r (detecção). (5) Pré-registrar (D0xx) **qual** ajuste de tarefa será feito se der "AJUSTA", antes de rodar. (6) Definir a regra de combinação dos 2 LLMs (ambos? qualquer um?). (7) Usar no piloto a mesma temperatura do experimento.

### 4.2 Maiores

#### M1 — Baseline isolado forte (B2) indefinido e H1 quase tautológica
- **Evidência.** `pendencias.md:95` (B2 aberto); `proposta.md:71` ("LLM recebe dados do paciente, calcula risco e explica sozinho"). Em C-ferramenta a categoria é entregue pronta (`prompt.py:46`), então a concordância de categoria tende a 100% por construção.
- **Impacto.** H1 compara "copiar a categoria" com "calcular sem a equação", o que é espantalho (Wolfrath 2024, citado pelo próprio projeto).
- **Recomendação.** Definir C-isolado com a equação no prompt ou com interpretador de código (A12). Rebaixar H1 formalmente a "replicação/verificação de sanidade" com um n pequeno (é efeito grande). Priorizar recursos em H2.

#### M2 — A pergunta de pesquisa não é respondível pelo núcleo
- **Evidência.** A pergunta inclui "com LLM para coerência semântica" (`proposta.md:25`); o núcleo tem "Verificador só de nível 1" (`escopo-e-arquitetura.md:55`); o nível 2 é extensão (`escopo-e-arquitetura.md:63`).
- **Recomendação.** Reescrever a pergunta para o verificador **determinístico** e deixar o nível 2 como pergunta secundária condicional.

#### M3 — H3: mecanismo depende de checagem não especificada e o poder é inviável
- **Evidência.** H3 (`proposta.md:30`) supõe que o verificador barra menções a raça/etnia. O nível 1 especificado checa números, sinais e categoria (`proposta.md:58`), não variáveis fora do modelo. O prompt atual nem inclui raça (`prompt.py:30-42`). Se raça for incluída e o verificador barrar variáveis fora do modelo, H3 vira **tautologia**. Com evento raro, o n necessário é 455–1.064 pares para uma taxa-base de 1–2% (`v2_saida.txt`, item d).
- **Recomendação.** Manter H3 como **análise exploratória descritiva** (como D020 já sugere), sem teste confirmatório. Declarar explicitamente se a checagem de "variável fora do modelo" faz parte do nível 1.

#### M4 — Anotação pelo próprio autor, sem cegamento
- **Evidência.** D015 (`decisoes.md:108`): "você + um colega"; o piloto é anotado "por uma pessoa, sem κ" (`README.md:57`). Não há menção a cegamento em `metricas-fidelidade.md` §7.
- **Impacto.** Viés do experimentador (o autor tem interesse em H2) — ameaça à validade de construto (Wohlin et al. 2012).
- **Recomendação.** Cegar a configuração (IDs aleatórios, remover marcas de formato, ordem embaralhada) e fazer com que o colega anote o contraste primário. Com 100 textos em dobro e κ real de 0,70, 95% dos κ amostrais caem entre **0,52 e 0,85**; com 200, entre 0,58 e 0,81 (`v2_saida.txt`, item f; ver Sim & Wright 2005). Portanto, **< 100 textos** não permite afirmar κ ≥ 0,60 com segurança.

#### M5 — Construto "fidelidade" mal nomeado e não comparável entre configurações
- **Evidência.** `metricas-fidelidade.md:17` define "fidelidade ao sistema de cálculo" citando Jacovi & Goldberg, para quem *faithfulness* é refletir o **processo de raciocínio do próprio modelo que explica**. Aqui, o LLM explica **outro** modelo (PREVENT). Em C-isolado, o LLM não recebe R(v), e "fidelidade a R(v)" é, na verdade, **correção**.
- **Recomendação.** Nomear o construto com precisão ("fidelidade ao modelo explicado" / "*groundedness* no pacote de referência") e aplicar as métricas de fidelidade só aos contrastes em que o LLM recebe R(v), ou seja, C-ferramenta × C-verificador.

#### M6 — Métricas citadas em H2 sem definição operacional
- **Evidência.** H2 cita "top-k SHAP" (`proposta.md:29`) e "Consistência: entropia/variação" (`proposta.md:95`). `metricas-fidelidade.md` define só as 4 métricas novas.
- **Recomendação.** Definir top-k (k, empates, sinônimos → glossário) e consistência, ou retirar essas métricas de H2. O top-k é necessário para o controle de omissão de CR2.

#### M7 — Enquadramento em DSR superficial e ameaças à validade não sistematizadas
- **Evidência.** DSR aparece em uma linha (`proposta.md:41`). O fichamento de Hevner é "leitura: resumo… Citado de memória" (`hevner2004dsr.md`). Não há requisitos de projeto do artefato com critérios mensuráveis (atividade 2 de Peffers et al. 2007), nem estratégia de avaliação (FEDS). As "Limitações" têm 5 itens (`proposta.md:111`), sem a classificação em validade de construto, interna, externa e de conclusão (Wohlin et al. 2012).
- **Recomendação.** Uma seção de método com: (a) DSRM de Peffers (problema → objetivos → projeto → demonstração → avaliação → comunicação), mapeada nas decisões D###; (b) avaliação **artificial e somativa** (FEDS) por **experimento controlado**; (c) tabela de ameaças em 4 classes, com mitigação. Ler Hevner 2004 na íntegra.

#### M8 — Afirmações sobre o JADE que o desenho não avalia
- **Evidência.** `justificativa-jade.md:27`: o protocolo "ataca essas falhas por construção", citando taxas do MAST. Não há medição planejada de falhas de término/repetição com e sem FIPA. `sintese-leitura.md:60` mantém que "FIPA-ACL (JADE) é exatamente isso", o que a própria auditoria classificou como exagero (E4, `auditoria-decisoes-autorais.md:63`).
- **Recomendação.** Tratar os benefícios do JADE como **propriedades de engenharia** (término garantido, rastro), demonstradas por testes. Retirar qualquer afirmação causal sem avaliação e corrigir `sintese-leitura.md` §3.5.

### 4.3 Menores

| # | Problema | Evidência | Recomendação |
|---|---|---|---|
| m1 | Vinheta fisiologicamente impossível: LDL-c 165 > não-HDL 135 | `vinhetas.py:32` (V18); `v1_saida.txt`, item 2 | Corrigir (ex.: CT 225) e validar a plausibilidade de todas as vinhetas sintéticas (LDL ≤ não-HDL; Friedewald quando houver TG) |
| m2 | Formato decimal misto no prompt: "0,3%" com vírgula e contribuições "-1.567" com ponto | `prompt.py:45,52`; `v1_saida.txt`, item 5 | Padronizar para vírgula; o formato misto pode induzir erros numéricos que seriam atribuídos ao LLM |
| m3 | Rigor declarado com TRIPOD+AI, calibração e *leakage*, sem modelo treinado no núcleo | `proposta.md:41`; `defesa-valor.md:37`; D016 (`decisoes.md:115`) | Mover para a extensão XGBoost |
| m4 | "Não há trabalho em português" persiste como lacuna | `defesa-valor.md:31` × D018 | Alinhar ao D018 |
| m5 | Tabela de trabalhos relacionados marca ✔ "viés demográfico" e ✔ verificador "híbrido" para o TCC | `trabalhos-relacionados.md:24` | Marcar ◐ ou "extensão" |
| m6 | Contribuição C2 inclui "consistência entre execuções + viés contrafactual", fora do núcleo | `proposta.md:36` | Alinhar a D020 |
| m7 | NHANES amostrado de forma estratificada sem mencionar pesos amostrais | `proposta.md:77-78` | Declarar que as taxas são por estrato (não populacionais) ou reponderar |
| m8 | Prompt único, sem variação de redação: resultados podem ser específicos do prompt | `prompt.py:10` (`piloto-v1`) | Declarar como ameaça à validade externa ou testar 2 paráfrases em uma subamostra |
| m9 | D010 afirma que a interpretação da SBC "não favorece nenhuma configuração". Vale para C-ferramenta × C-verificador, mas não para C-isolado (H1), que é penalizado se o LLM interpretar o agravante de outro modo | `decisoes.md:70` | Restringir a afirmação ao contraste de H2 |
| m10 | Trabalho de interface (D025, auditoria axe-core) cresce fora da pergunta de pesquisa | `decisoes.md:165-169` | Manter como apêndice/demonstração; não consumir o cronograma do núcleo |

---

## 5. Perguntas da banca

| # | Pergunta | O que uma boa resposta precisa conter | O projeto responde hoje? |
|---|---|---|---|
| 1 | Quantas vinhetas o senhor precisa para detectar o efeito do verificador, e com que poder? | pA, r e q estimados no piloto; fórmula/simulação; α ajustado para 2 LLMs; efeito mínimo de interesse | **Não** (`proposta.md:104`; C5 aberto) |
| 2 | Se o verificador e a métrica checam as mesmas coisas, o resultado de H2 não é garantido por construção? | Admitir o ganho esperado nas dimensões checadas; desfecho primário por anotação humana cega; métricas não checadas (omissão/cobertura); sensibilidade do verificador | **Parcial** (B1 reconhecida em `fundamentacao-por-parte.md:104-109`; sem solução operacional) |
| 3 | Como entram no resultado as explicações bloqueadas pelo verificador? | Intenção de tratar; bloqueio como desfecho próprio; análise conservadora e de sensibilidade | **Não** |
| 4 | O ganho vem do feedback específico ou apenas de o LLM ter mais tentativas? | Controle *best-of-N*/autocrítica sem ferramenta, ou limitação declarada; referência a Huang 2024 e CRITIC | **Parcial** (o mecanismo é citado em A6, sem controle) |
| 5 | Por que um LLM e não um *template* determinístico, que é 100% fiel por construção? | Argumento de valor (linguagem adaptada, perguntas abertas) e, idealmente, um *template* como teto de fidelidade/piso de inteligibilidade | **Parcial** (`perguntas-banca.md:22-23` trata do "para que o LLM", não do *template*) |
| 6 | Como as 3 repetições viram um único dado por vinheta? E por que não um modelo misto? | Regra pré-especificada; justificativa; sensibilidade; dependência intra-vinheta | **Parcial** (`metricas-fidelidade.md:174` diz que agrega, não diz como; o piloto usa "qualquer erro", mas decide por resposta) |
| 7 | Se um LLM confirmar H2 e o outro não, qual é a conclusão? | Critério pré-declarado; análise estratificada; heterogeneidade do efeito como achado | **Não** |
| 8 | A regra de 10% do piloto: qual a chance de ela errar a decisão? | Curva operacional; IC; zona de indiferença; estrato típico × armadilha | **Não** (limiar "autoral", `proximos-passos.md:39`) |
| 9 | Se 20 das 24 vinhetas do piloto são armadilhas, o que a taxa do piloto estima? | Reconhecer que é a taxa condicional às armadilhas; regra aplicada ao estrato típico ou ponderada | **Parcial** (limitação em `README.md:56`, ignorada pela regra) |
| 10 | "Fiel" a quê? A referência do Shapley muda o sinal da contribuição do HDL ou da idade | Definição "sob a referência declarada"; sensibilidade com a média do NHANES (B4); prompt explicando a referência | **Sim, no papel** (`fundamentacao-por-parte.md:47-50`; `prompt.py:17`), com a sensibilidade relegada a extensão |
| 11 | Quem anota, e os anotadores sabem de qual configuração veio o texto? | Cegamento, ordem aleatória, anotador independente, n para κ (≥ 100–200) | **Não** (cegamento ausente; n "a definir") |
| 12 | Por que Design Science? Quais são os requisitos do artefato e o critério de sucesso? | Peffers/FEDS; requisitos mensuráveis; avaliação somativa artificial | **Parcial** (uma linha em `proposta.md:41`; Hevner lido só pelo resumo) |
| 13 | H3 tem poder? Quantas menções à raça o senhor espera observar? | Estimativa da taxa-base; n; decisão de tratar como exploratória | **Não** (sem estimativa; a tabela da seção 6 sugere n ≥ 455 para taxa-base de 2%) |
| 14 | Os resultados valem para outros prompts, outras temperaturas e outros modelos de 2026? | Ameaças à validade externa; prompt fixo; temperatura; ≥ 2 LLMs | **Parcial** (≥ 2 LLMs em D014/D024; temperatura e prompt, não) |
| 15 | O extrator "independente" que avalia todas as explicações: como ele é validado, e não é ele mesmo um segundo verificador? | Precisão/*recall* por tipo contra o padrão humano; diferença de implementação em relação ao verificador | **Parcial** (`metricas-fidelidade.md:161-162`, sem implementação) |

---

## 6. Verificações executadas

Todas as verificações foram feitas sem modificar arquivos do projeto: os módulos do piloto foram importados com `PYTHONDONTWRITEBYTECODE=1`, e o *dry-run* rodou numa cópia no *scratchpad*.

| # | Comando | Resultado |
|---|---|---|
| 1 | `cd experimentos/piloto && python3 -m unittest test_prevent` | `Ran 7 tests … OK` |
| 2 | `python3 rodar_piloto.py --seco` (em cópia) | 24 vinhetas: 9 baixo, 10 intermediário, 5 alto; riscos de 0,3% a 24,9% |
| 3 | `python3 tcc/05-banca/anexos/metodologia/v1_verificar_piloto.py` → `v1_saida.txt` | (i) eficiência do Shapley OK (4,4·10⁻¹⁵); (ii) **V18 impossível** (LDL 165 > não-HDL 135); (iii) 6/24 vinhetas com categoria alterada por regra; 2/24 com risco ≥ 20%; (iv) **20/24 vinhetas com gatilho de erro**; (v) decimais mistos no prompt; (vi) **`resumir.py` decide por resposta, apesar de declarar a vinheta como unidade**; exibe "10%" e decide "AJUSTAR" |
| 4 | `<venv>/bin/python tcc/05-banca/anexos/metodologia/v2_poder_mcnemar.py` → `v2_saida.txt` | (a) tabela de n (36 cenários, 3 níveis de α) e poder simulado mid-p de 0,81–0,90; (b) curva operacional da regra do piloto; (c) viés por enriquecimento de armadilhas; (d) n para H3; (e) carga do núcleo: 1.800 / 3.600 / 5.400 textos para 100 / 200 / 300 vinhetas; (f) precisão do κ |

**Figuras**
- `anexos/metodologia/fig1_n_mcnemar.png` — n de vinhetas × pA para r ∈ {0,3; 0,5; 0,8}, q = 3%, α = 0,025.
- `anexos/metodologia/fig2_regra_piloto.png` — probabilidade de a regra do piloto dizer "SEGUE" em função da taxa real, para ICC de 0; 0,3 e 0,6.

**Premissas do cálculo de poder** (ilustrativas; não são estimativas). p10 = pA·r e p01 = (1−pA)·q. Fórmula de Connor (1987), conferida por Monte Carlo com o teste mid-p (4.000 réplicas, semente 20260929). Os valores de pA, r e q devem ser substituídos pelos medidos no piloto.

**Leitura prática.** Um experimento com **~100–150 vinhetas** por LLM só tem poder se pA ≥ 20–30% **e** o verificador corrigir ≥ 50% das falhas introduzindo poucos erros novos (q ≤ 3%). Se o piloto mostrar pA ≈ 10% no estrato típico, H2 **não é testável** com o orçamento de anotação de um TCC. Nesse caso, o desfecho e a população precisam mudar de forma **pré-registrada**, por exemplo passando a taxa por afirmação ou a um estrato de maior risco de erro declarado como tal.

---

## 7. Referências consultadas (verificadas em 29/09/2026)

**Metodologia e validade**
- WOHLIN, C. et al. *Experimentation in Software Engineering*. Springer, 2012. DOI: [10.1007/978-3-642-29044-2](https://doi.org/10.1007/978-3-642-29044-2) — ameaças à validade (construto, interna, externa, de conclusão).
- HEVNER, A. R.; MARCH, S. T.; PARK, J.; RAM, S. Design Science in Information Systems Research. *MIS Quarterly*, 28(1):75–105, 2004. DOI: [10.2307/25148625](https://doi.org/10.2307/25148625) ([AIS eLibrary](https://aisel.aisnet.org/misq/vol28/iss1/6/)).
- PEFFERS, K.; TUUNANEN, T.; ROTHENBERGER, M.; CHATTERJEE, S. A Design Science Research Methodology for Information Systems Research. *J. Management Information Systems*, 24(3):45–77, 2007. DOI: [10.2753/MIS0742-1222240302](https://doi.org/10.2753/MIS0742-1222240302).
- VENABLE, J.; PRIES-HEJE, J.; BASKERVILLE, R. FEDS: a Framework for Evaluation in Design Science Research. *European Journal of Information Systems*, 25(1):77–89, 2016 ([EconPapers](https://econpapers.repec.org/article/taftjisxx/v_3a25_3ay_3a2016_3ai_3a1_3ap_3a77-89.htm)).

**Estatística**
- CONNOR, R. J. Sample size for testing differences in proportions for the paired-sample design. *Biometrics*, 43(1):207–211, 1987. [PubMed 3567305](https://pubmed.ncbi.nlm.nih.gov/3567305/).
- FAGERLAND, M. W.; LYDERSEN, S.; LAAKE, P. The McNemar test for binary matched-pairs data: mid-p and asymptotic are better than exact conditional. *BMC Med. Res. Methodol.*, 13:91, 2013. [Link](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-91).
- OBUCHOWSKI, N. A. On the comparison of correlated proportions for clustered data. *Statistics in Medicine*, 17:1495–1507, 1998. [Wiley](https://onlinelibrary.wiley.com/doi/10.1002/(SICI)1097-0258(19980715)17:13%3C1495::AID-SIM863%3E3.0.CO;2-I).
- MILLER, E. Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations. arXiv:2411.00640, 2024 (*preprint*). [arXiv](https://arxiv.org/abs/2411.00640).
- DROR, R.; BAUMER, G.; SHLOMOV, S.; REICHART, R. The Hitchhiker's Guide to Testing Statistical Significance in NLP. *ACL 2018*, p. 1383–1392. [ACL Anthology](https://aclanthology.org/P18-1128/).
- SIM, J.; WRIGHT, C. C. The kappa statistic in reliability studies: use, interpretation, and sample size requirements. *Physical Therapy*, 85(3):257–268, 2005. [PubMed 15733050](https://pubmed.ncbi.nlm.nih.gov/15733050/).

**Conteúdo (fidelidade e autocorreção)**
- JACOVI, A.; GOLDBERG, Y. Towards Faithfully Interpretable NLP Systems: How Should We Define and Evaluate Faithfulness? *ACL 2020*, p. 4198–4205. [ACL Anthology](https://aclanthology.org/2020.acl-main.386/). (Confirma as páginas pendentes em `pendencias.md:20`.)
- HUANG, J. et al. Large Language Models Cannot Self-Correct Reasoning Yet. *ICLR 2024*. [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/8b4add8b0aa8749d80a34ca5d941c355-Abstract-Conference.html).

**Observações sobre as referências**
- Os metadados de Hevner 2004 conferem com o fichamento (o item de `pendencias.md:21` pode ser fechado). A página final varia entre as fontes (105 ou 106).
- Não verifiquei o conteúdo integral de Wohlin et al. nem de Peffers et al. Cito apenas a estrutura amplamente documentada (4 classes de validade; 6 atividades do DSRM).
