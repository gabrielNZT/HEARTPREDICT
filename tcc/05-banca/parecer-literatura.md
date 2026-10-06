---
titulo: Parecer da banca: revisão de literatura e integridade das citações
avaliador: Prof.(a) Dr.(a), especialista em revisão de literatura e integridade científica (banca simulada)
data: 2026-09-29
escopo: tcc/01-literatura (fichamentos, textos, referencias.bib, INDEX), tcc/02-argumentacao, tcc/00-projeto/proposta.md, tcc/03-metodologia
anexos: tcc/05-banca/anexos/literatura/
---

# Parecer: revisão de literatura e integridade científica

## 1. Parecer resumido e veredito

A base de conhecimento do TCC é **acima da média para a graduação**. Há fichamentos com front-matter, dados citáveis [C#] localizados no texto original, textos completos arquivados, um BibTeX gerado e, principalmente, um registro honesto dos próprios erros (auditoria E1–E9). Conferi, contra os textos completos, **57 dados citáveis dos 9 fichamentos com `leitura: completa`, ou seja, todos os [C#] desses fichamentos**. Todos foram encontrados no original: 55 estão corretos e 2 estão imprecisos por omissão de escopo. Nenhum está errado. Os metadados dos artigos centrais conferem com Crossref e arXiv, inclusive autores, volume e número do artigo.

Os problemas aparecem **depois** do fichamento, quando os dados são usados na argumentação. Os principais são estes:

1. **A lacuna declarada não tem busca reprodutível** (C8 continua aberta). Um trabalho cuja tese é "ninguém fez X" precisa de protocolo de busca documentado.
2. **O rótulo de profundidade de leitura é aplicado de forma inconsistente.** Fontes marcadas como "a fichar" ou lidas só no resumo recebem o rótulo [P] ("lido na íntegra"). A tabela da lacuna em `defesa-valor.md` diz "todas lidas", mas inclui três fontes que não foram lidas na íntegra.
3. **Algumas afirmações vão além do que as fontes permitem.** Exemplos: "o pipeline agêntico **reduziu** a fidelidade", apoiado em n=14 com ICs sobrepostos; "LLMs acertaram em 42,5% dos **casos**", quando o estudo usou um único LLM e a unidade eram gerações.
4. **Falta cobertura em frentes óbvias.** Faltam validações externas do PREVENT (há uma validação multinacional na *Nature Medicine* 2026 que pode mudar a limitação E5), revisões sistemáticas de LLM em cardiologia e a literatura de fidelidade de explicações em linguagem natural posterior a 2020.
5. **Duas correções registradas na auditoria não foram propagadas** para todos os documentos: E4 (MAST e FIPA) e E9 (Isern).

**Veredito: APROVADO COM RESSALVAS (revisões maiores antes da qualificação).** Os problemas são corrigíveis em 2 a 3 semanas de trabalho e não comprometem a pergunta de pesquisa. Mas a afirmação de lacuna, hoje, **não é defensável diante de uma banca exigente** sem a busca estruturada (seção 6.3).

## 2. Notas por critério (0–10)

| Critério | Nota | Justificativa |
|---|---|---|
| Exatidão das citações | **8,5** | 57/57 [C#] encontrados, 55 corretos e 2 imprecisos por omissão de escopo (tabela na seção 6.1). Perde pontos na **reutilização**: generalizações em `defesa-valor.md` e `sintese-leitura.md` que o [C#] original não sustenta (problemas M3 e M4). |
| Qualidade dos metadados | **7,0** | Os artigos centrais estão corretos (Crossref: autores, volume, nº do artigo, DOI). Mas 6 de 38 entradas estão sem DOI, e 3 desses DOIs existem e eu os encontrei (Isern, Tang, Chan). Petrova tem 4 autores, não "et al.". Entradas NeurIPS usam o DOI do *preprint* arXiv. Faltam páginas do ColaCare. O validador não checa nada disso. |
| Honestidade sobre profundidade de leitura | **7,5** | O sistema `leitura:` é exemplar e há avisos "ler antes de citar". Porém o rótulo [P] vai para fontes "a fichar" ou só com resumo (`fundamentacao-por-parte.md`:41, 68, 69, 77, 98; `metricas-fidelidade.md`:17, 37, 132, 154, 160). O título da tabela da lacuna diz "todas lidas" (`defesa-valor.md`:19). |
| Rastreabilidade das afirmações | **6,5** | Muitas afirmações não se ligam a fichamento: Huang, CRITIC, FActScore, revisão LLM-como-juiz (κ 0,59–0,88), Wolfrath, Lundberg & Lee, Kusner, AI Act e toda a base de IHC em `interface-design.md`. Há também estatísticas sem fonte ainda presentes no texto (`defesa-valor.md`:13, 15). Isso viola a regra declarada (`auditoria-decisoes-autorais.md`:72–78). |
| Cobertura da literatura | **6,0** | É boa no núcleo (LLM + ferramenta + SHAP + multiagente). É fraca em validação do PREVENT fora dos EUA, revisões sistemáticas de LLM em cardiologia, fidelidade de explicações em linguagem natural (pós-2020), epidemiologia brasileira primária e metodologia de busca. |
| Reprodutibilidade da busca | **3,0** | Não há protocolo nem registro de bases, strings, datas, critérios ou fluxo. A própria auditoria reconhece isso: "~35 trabalhos encontrados por busca não sistemática" (`auditoria-decisoes-autorais.md`:51). |

**Média simples: 6,4.**

## 3. Pontos fortes

1. **Exatidão dos [C#] de leitura completa.** Todos os 57 foram localizados com a seção ou tabela indicada, inclusive números de tabela, como o MedCalc Tab. 4 "GPT-4 0.35 (57%)" e o PREVENT Tab. 4 "0.774 (0.743, 0.788)". Isso é raro em TCC.
2. **Leitura crítica real, não só transcrição.** Três exemplos:
   - o fichamento de Lee percebeu que a "fidelidade 0,783" mede só a presença das variáveis. Confere com o original: "Fidelity (scored as 1/0.66/0.33 for 3/2/1 correct features)" (`textos/lee2025shapllm.txt`:49);
   - o fichamento do ColaCare notou que o ganho sobre o ensemble fica dentro do desvio-padrão (54,05±4,88 vs 53,59±4,52);
   - o fichamento do PREVENT registrou os valores de centralização (idade 55, não-HDL 3,5, HDL 1,3, PAS 130), que conferem com a nota da tabela (`textos/khan2024prevent.txt`:210).
3. **Registro público de erros próprios** (E1–E9) e decisões nunca apagadas. É uma boa prática de integridade.
4. **Metadados centrais corretos.** A lista de 27 autores do PREVENT confere com o Crossref, com Khan como primeira autora e Coresh como último autor nominal; o erro antigo foi mesmo corrigido. AgentMD (Nat Commun 16:9377), Lee (BMC MIDM 25:430), Roeschl (EHJ-DH 7(7):ztag124) e Santos (EHJ-DH 7(5):ztag073) também conferem.
5. **Veículos de conferência confirmados** (OpenReview): MAST (NeurIPS 2025 D&B, spotlight), MedAgentBoard (NeurIPS 2025 D&B), MedCalc-Bench (NeurIPS 2024 D&B, oral), MDAgents (NeurIPS 2024, oral). ColaCare está em WWW'25, pp. 2250–2261.
6. **Transcrições literais verificáveis.** Exemplos: percentuais do MAST em `justificativa-jade.md`:27 (12,4%, 15,7%, 2,8%, 6,2%, 8,2%, 9,1%, 6,8%, todos conferem com `textos/cemri2025mast.txt`:328–356) e CKD-EPI 2021 na derivação do PREVENT (`textos/khan2024prevent.txt`:34).

## 4. Problemas

### Críticos

**K1. A lacuna ("nenhum trabalho reúne verificador + polaridade/exatidão + ablação em PREVENT/SBC") depende de busca não sistemática.**
- Evidências: `auditoria-decisoes-autorais.md`:51 ("~35 trabalhos encontrados por busca não sistemática"); `trabalhos-relacionados.md`:27 ("busca ainda não estruturada"); `sintese-leitura.md`:45 ("não aparecem em nenhum trabalho lido"); `defesa-valor.md`:31 ("ninguém avaliou…").
- Risco: a primeira pergunta de uma banca de metodologia será "como você sabe?". A própria base mostra que o campo muda depressa (Zhu 2026, NEURON 2026, PROVE 2026 foram achados tarde).
- Correção: executar o protocolo da seção 6.3, reescrever como "nos N estudos incluídos pela busca de DD/MM/AAAA" e anexar o fluxo PRISMA e a planilha de triagem.

**K2. O rótulo [P] ("lido na íntegra") é atribuído a fontes não fichadas ou lidas só no resumo, contra a regra declarada.**
- Evidências:
  - `fundamentacao-por-parte.md`:11 define [P] como "lido na íntegra", mas marca [P] em :41 (Lundberg & Lee, "a fichar"), :68 (Huang, "a fichar"), :69 (CRITIC, "a fichar"), :77 (Diao e Anderson, "(resumos)") e :98 (Kusner, "a fichar");
  - `metricas-fidelidade.md`:17 e :132 marcam Jacovi & Goldberg como [P], mas o fichamento está com `leitura: resumo`;
  - `metricas-fidelidade.md`:37 e :154 fazem o mesmo com FActScore ("a fichar");
  - `metricas-fidelidade.md`:160 faz o mesmo com a "revisão de LLM-como-juiz em saúde, 2026", sem fichamento;
  - `defesa-valor.md`:19 diz "cadeia de evidências (todas lidas)", mas as linhas 24 e 27 usam turpin2023unfaithful e jacovi2020faithfulness (`leitura: resumo`) e jabbour2023jama (`leitura: parcial`).
- Correção: reclassificar como [S] ou "[P-pendente]" até ler; fichar Huang, CRITIC, FActScore, Jacovi, Turpin e Lundberg & Lee (todos de acesso aberto); corrigir o título da tabela para "lidas na íntegra, exceto 3 e 6".

### Maiores

**M1. Asgari 2025 e a revisão LLM-como-juiz sustentam parâmetros da métrica sem terem sido lidas.**
- `metricas-fidelidade.md`:163 usa "κ < 0,60… limite inferior da faixa relatada na revisão de 2026" como critério de corte.
- `auditoria-decisoes-autorais.md`:45 cita "κ 0,59–0,88".
- A fonte (arXiv 2605.25273) não tem fichamento (`pendencias.md`: "Fichar a revisão…").
- Correção: fichar, ou justificar κ ≥ 0,60 pela convenção de Landis & Koch (1977) ou de McHugh (2012).

**M2. Santos 2026 (`leitura: resumo`) sustenta uma decisão "defensável" (A1) e uma correção de erro (E1).**
- Os números κw 0,69 e 0,85–0,90 **estão no resumo**, que eu conferi pelo Europe PMC. Mesmo assim:
  - "McNemar usado no piloto de Santos" (`auditoria-decisoes-autorais.md`:35) vem de um piloto não fichado (PMC12794879);
  - E1 declara "Falso" que o português seja lacuna, mas a pendência "confirmar se o português é europeu" (`pendencias.md`:57) segue aberta. Os autores são portugueses (Ferreira Santos, Dores). Se as vinhetas estão em português europeu, a correção E1 fica certa quanto ao idioma, mas errada quanto ao **PT-BR**.
- Correção: ler o texto completo (disponível no PMC) antes da qualificação e reescrever E1 com a variante do idioma.

**M3. Afirmação mais forte que a evidência: "Pipeline agêntico reduziu a fidelidade ao SHAP".**
- Aparece em `defesa-valor.md`:26 e `sintese-leitura.md`:35.
- O original mostra n=14 e ICs sobrepostos: Jaccard 0,077 (IC95% 0,018–0,143) vs 0,171 (0,075–0,279); direção 78,6% (57,1–100,0) vs 92,9% (78,6–100,0) (`textos/zhu2026agenticexpl.txt`:172, 184–188).
- A "consistência de direção" de Zhu é **com o rótulo previsto**, não com o sinal do SHAP (`textos/zhu2026agenticexpl.txt`:144, "direction consistency with the model-predicted risk label"). O projeto reconhece isso em `metricas-fidelidade.md`:86, mas não em `defesa-valor.md`.
- Correção: "num preprint com 14 casos e um modelo de 3B, o pipeline agêntico teve alinhamento com o SHAP numericamente menor (ICs sobrepostos)".

**M4. "LLMs recuperaram as três variáveis SHAP em apenas 42,5% dos casos".**
- Aparece em `defesa-valor.md`:40 (e :25).
- No original, um único LLM (GPT-4) teve *exact match accuracy* média de 0,425 sobre 10 gerações por caso em 40 casos (`textos/lee2025shapllm.txt`:55, 63).
- Correção: "o GPT-4 acertou o trio completo em 42,5% das gerações". O [C1] do fichamento já está certo; o erro é só na reutilização.

**M5. A correção E4 (MAST não recomenda FIPA) não foi propagada.**
- `sintese-leitura.md`:60 ainda diz: "MAST (Apêndice G) recomenda protocolos de comunicação padronizados… **FIPA-ACL (JADE) é exatamente isso**. Isso transforma o JADE… em decisão de projeto justificada". Isso contradiz `auditoria-decisoes-autorais.md`:63 e `fundamentacao-por-parte.md`:59.
- O MAST diz, além disso, que padronizar o formato (MCP e A2A) **não evita** os erros de desalinhamento observados: "the errors we observe in FC2 occur even when agents within the same framework communicate…" (`textos/cemri2025mast.txt`:346). Isso enfraquece o argumento de que o FIPA resolve essas falhas "por construção" (`justificativa-jade.md`:27).
- Correção: reescrever `sintese-leitura.md` §3.5 e incluir essa ressalva do MAST em `justificativa-jade.md`.

**M6. A limitação E5 ("calibração em brasileiros desconhecida") pode estar desatualizada.**
- Neuen et al. (*Nat Med* 2026;32:2629–2638, doi:10.1038/s41591-026-04437-z) validaram PREVENT e SCORE2 em 44 coortes e 18 ensaios (6,4 milhões de pessoas), com boa discriminação e calibração em várias regiões.
- Investigadores do ELSA-Brasil (Mill JG, Bensenor I, Giatti L, da Fonseca MJM) estão entre os coautores e colaboradores. Por isso é provável, mas **não verifiquei no texto completo**, que haja uma coorte brasileira.
- Correção: ler Neuen 2026 e, se houver dados brasileiros, citar o resultado específico. Se não houver, dizer que a validação multinacional não incluiu o Brasil.

**M7. Afirmações factuais sem fonte rastreável nos documentos pedidos.**
- `defesa-valor.md`:
  - :13 "~30% dos óbitos" (fonte ainda não substituída; E7 está aberta). Fonte primária disponível: Oliveira et al., Estatística Cardiovascular – Brasil 2023, *Arq Bras Cardiol* 2024;121(2):e20240079;
  - :15 "20–30% dos médicos já usam LLMs" (E6 aberta), e a mesma ideia sem fonte em :40 ("já são usados por parte dos médicos");
  - :16 "AI Act, Art. 13; PL 2338/2023", sem referência formal;
  - :31 "não há trabalho em português alinhado à SBC 2025", afirmação negativa sem busca.
- `justificativa-jade.md`:
  - :28 "CRITIC; Huang et al. 2024", não fichados;
  - :33 "Zhu 2026 recomenda expor a ausência de dados", que é paráfrase livre: o original diz "should be surfaced rather than hidden" sobre incerteza e ausência (`textos/zhu2026agenticexpl.txt`:229), então é aceitável, mas precisa de [C#];
  - :60 "a indústria migrou para A2A/MCP", apoiada em dois *surveys* lidos só no resumo;
  - :61 "API atual 4.6.0", sem fonte.
- `fundamentacao-por-parte.md`:
  - :92 "revisão de LLM-como-juiz em saúde";
  - :112 "Wolfrath et al., 2024";
  - :47 "Sundararajan & Najmi, ICML 2020".
  Nenhuma dessas três tem fichamento.
- `interface-design.md`: as fontes existem e têm referência completa (§10), mas **nenhuma está na base** (`fichamentos/`). Os itens NN/g e GOV.UK não têm URL nem data de acesso. Harrower & Brewer 2003 está sem volume e páginas (*Cartogr J* 40(1):27–37).
- `interface-design.md`:67: Zikmund-Fisher 2014 está **correto** (1.502 pessoas de 35–75 anos, ícones "restroom" melhores na memorização e preferidos, conferido no PubMed 24246564). Mas omite que esses ícones "performed no better than other icon types among less numerate" participants. Isso qualifica o uso do pictograma "especialmente para baixo letramento" em :16 e :91.
- `metricas-fidelidade.md`: :37, :154 e :160 (ver K2 e M1). Positivo: a tolerância de 5% do MedCalc-Bench está correta, mas só vale para calculadoras por equação de exames laboratoriais e físicos e de conversão de dose (`textos/khandekar2024medcalc.txt`:216); o texto em :103 deveria dizer isso.

**M8. Metadados e BibTeX (detalhe no anexo `verificar_metadados-saida.txt`).**

| Chave | Problema | Correção verificada |
|---|---|---|
| isern2016agents | Sem DOI; `url` aponta para a página da revista, não do artigo. E9 diz "já corrigido". | doi:10.1007/s10916-015-0376-2; J Med Syst 40(2):43 (online em 2015-11-21) |
| tang2024medagents | Sem DOI nem páginas | doi:10.18653/v1/2024.findings-acl.33; pp. 599–621 |
| chan2025vies | Sem DOI e volume (pendência aberta) | doi:10.3389/fdgth.2025.1710594; *Front Digit Health* 7:1710594 |
| asgari2025hallucination | "et al." e sem volume/artigo | *npj Digit Med* 8:274; 7 autores (Crossref) |
| petrova2025webofagents | "et al." gera `and others`, mas o arXiv lista só 4 autores | Remover "et al." |
| wang2025colacare | Sem páginas; `url` aponta para o arXiv | pp. 2250–2261; usar https://doi.org/10.1145/3696410.3714877 |
| cemri, zhu2025medagentboard, khandekar, kim2024mdagents | `@inproceedings` NeurIPS com `doi` do **preprint** arXiv (10.48550) | Trocar o DOI por `url` dos anais (proceedings.neurips.cc) e `eprint`/`archivePrefix` para o arXiv |
| turpin2023unfaithful | Sem volume e páginas | Preencher pelos anais do NeurIPS 36 |
| hevner2004dsr | Páginas 75–105; Crossref registra 75–106 | Divergência menor; manter 75–105 (forma usual) ou alinhar ao DOI |
| kapoor2023leakage | `url` aponta para cópia de terceiros (hbiostat.org) | Usar o DOI |
| who2024lmm | Sem ISBN | Acrescentar o ISBN da publicação da OMS |
| khan2024prevent | Omite o autor coletivo "for the CKD Prognosis Consortium and the AHA CKM Science Advisory Group" | Opcional (ABNT/Vancouver aceitam omitir) |
| todos | Páginas com hífen simples (`963-970`) | Usar `--` no gerador |

- O BibTeX é **sintaticamente válido**: 38 entradas, chaves balanceadas, tipos article/inproceedings/misc, títulos protegidos com `{{…}}`.
- Os *preprints* estão marcados em `howpublished` ("arXiv preprint", "medRxiv (preprint)"). Mas o `indexar.py validar` sai com código 0 sem apontar nenhum dos problemas acima: não verifica a presença de DOI para `relevancia: central/alta`, nem "et al." em `autores`.

### Menores

- **m1.** `jin2025agentmd` [C5] é impreciso. "91,6% dos testes unitários" refere-se a 500 cálculos num subconjunto de 100 calculadoras ("only 8.4% (42/500)", `textos/jin2025agentmd.txt`:160), não às 2.164. A autoverificação em 6 critérios, essa sim, vale para as 2.164 (:386).
- **m2.** `zhu2025medagentboard` [C7] é impreciso. A Tabela 13 cobre **só a Tarefa 1** (QA e VQA), e o próprio texto diz que o LLM único com CoT-SC foi o método mais caro nas tarefas textuais (`textos/zhu2025medagentboard.txt`, Apêndice D).
- **m3.** `sintese-leitura.md`:49 ainda lista "em **português**" entre os elementos inéditos, e `defesa-valor.md`:31 ainda afirma "não há trabalho em português…". Isso é compatível com a correção E1 só se ficar claro que o diferencial é a **diretriz**, não o idioma (D018).
- **m4.** `sintese-leitura.md`:53 diz que a falta de SHAP no prompt é a "causa provável do Jaccard baixíssimo em Zhu 2026". É hipótese do autor, pois o LLM isolado também não recebia o SHAP e teve Jaccard maior. Marcar como conjectura.
- **m5.** `perguntas-banca.md`:43–44 mantém a "Resposta anterior" ("O MAST recomenda… FIPA-ACL é um padrão consolidado… → cemri2025mast [C7]"). Está rotulada como antiga, mas pode vazar para o texto final; mover para o histórico.
- **m6.** `jabbour2023jama` [C4] (66,7%) é atribuído à Discussion, mas a leitura foi parcial via extrator. Conferir no PDF, como a pendência já pede.
- **m7.** `INDEX.md` e os fichamentos listam 38 fontes, das quais 27 (71%) só foram lidas no resumo. É aceitável para o contexto, mas o capítulo de revisão deve citar essas fontes só por afirmações que estejam no resumo.

## 5. Perguntas da banca

| # | Pergunta | Resposta esperada | O projeto responde hoje? |
|---|---|---|---|
| 1 | Como você sabe que ninguém combinou verificador + polaridade + ablação? | Busca estruturada documentada (bases, strings, data, critérios, fluxo PRISMA) com N estudos incluídos e tabela comparativa | **Não.** C8 aberta (`auditoria…`:51) |
| 2 | Quantas das fontes que você cita foram lidas na íntegra? | 9 completas, 2 parciais, 27 resumos; só as completas sustentam números | **Parcial.** Está em `INDEX.md`, mas a argumentação mistura níveis (K2) |
| 3 | O "Zhu 2026 mostra que agentes reduzem a fidelidade" é estatisticamente sustentado? | Não: n=14, ICs sobrepostos, modelo de 3B, preprint. É um indício, não um resultado | **Parcial.** `perguntas-banca.md` lista as limitações, mas `defesa-valor.md`:26 afirma "reduziu" |
| 4 | O que exatamente Lee et al. mediram como "fidelidade"? | Presença das top-3 por pontuação 1/0,66/0,33; não mede sinal nem magnitude | **Sim.** `lee2025shapllm` [C3]; `sintese-leitura.md`:18 |
| 5 | O PREVENT é válido no Brasil? | A SBC adota; o PREVENT foi derivado nos EUA; a validação multinacional (Neuen 2026) deve ser discutida; a calibração local é incerta | **Parcial.** A limitação está declarada (E5), mas falta a literatura de validação externa (M6) |
| 6 | Santos 2026 usou português do Brasil? | Verificar no texto completo; se for europeu, o PT-BR continua sem estudo específico | **Não.** Pendência aberta (`pendencias.md`:57) |
| 7 | De onde vem o limiar κ ≥ 0,60? | Convenção de Landis & Koch ou McHugh, ou revisão fichada | **Não.** Fonte não fichada (M1) |
| 8 | Por que a tolerância numérica de 5%? | MedCalc-Bench usa 5% para calculadoras por equação (lab/físicas/dose); risco em % derivado de equação é análogo | **Parcial.** A fonte está correta, mas o escopo não é declarado (`metricas-fidelidade.md`:103) |
| 9 | O MAST justifica usar FIPA/JADE? | Não diretamente: recomenda protocolos padronizados, cita MCP e A2A, e observa que padronizar o formato não elimina o desalinhamento | **Parcial.** Correto em `fundamentacao-por-parte.md`:59; contraditório em `sintese-leitura.md`:60 (M5) |
| 10 | Os percentuais de falha do MAST citados na justificativa do JADE são de qual amostra? | MAST-Data (210 traços na Fig. 4, 7 frameworks); os percentuais são proporções de modos de falha, não taxas por sistema | **Parcial.** Números corretos (`justificativa-jade.md`:27), mas sem a unidade |
| 11 | AgentMD já tem verificador; qual a diferença? | A autoverificação acontece na curadoria das calculadoras; não há verificação da explicação na inferência | **Sim.** `sintese-leitura.md`:21; `perguntas-banca.md` |
| 12 | Há revisões sistemáticas de LLM em cardiologia? O que dizem sobre explicabilidade? | Citar ao menos Gendler et al., JMIR Cardio 2026 | **Não.** Ausente da base |
| 13 | Pictogramas ajudam pessoas com baixo letramento numérico? | Galesic 2009: sim. Zikmund-Fisher 2014: ícones humanos melhoram a memorização em geral, mas **não** superam outros tipos entre os menos numéricos | **Parcial.** A nuance foi omitida (M7) |
| 14 | Por que fidelidade e não só plausibilidade? Qual a definição operacional na literatura de NLP? | Jacovi & Goldberg 2020; Lyu et al. 2024 (*survey*); Parcalabescu & Frank 2024 | **Parcial.** Jacovi está só no resumo; o restante está ausente |
| 15 | Os dados de mortalidade cardiovascular são de fonte primária? | Estatística Cardiovascular – Brasil 2023 (ABC) ou GBD | **Não.** E7 está aberta; `defesa-valor.md`:13 |

## 6. Verificações executadas

### 6.1 Checagem dos [C#] de leitura completa

Método: para cada [C#], busquei no texto completo (`tcc/01-literatura/textos/<chave>.txt`) as expressões que sustentam o número ou a afirmação. O veredito foi dado pela leitura do trecho. O processo pode ser reproduzido com `python3 tcc/05-banca/anexos/literatura/verificar_citaveis.py`; a saída está em `anexos/literatura/verificar_citaveis-saida.txt`, com linha e trecho.

**Resultado: 57 checados, 57 encontrados (100%), 55 corretos (96,5%), 2 imprecisos, 0 errados, 0 não encontrados.**

| Fichamento | [C#] | Trecho do original (linha no .txt) | Veredito |
|---|---|---|---|
| jin2025agentmd | C1 | "114.4% (0.877 vs. 0.409, Fig. 3c)" (L189) | correto |
| jin2025agentmd | C2 | "AgentMD with GPT-3.5 even outperforms CoT with GPT-4 (0.546 vs. 0.409)" (L190) | correto |
| jin2025agentmd | C3 | "correct (52.3%) or partially correct (28.5%)" (L204) | correto |
| jin2025agentmd | C4 | "HEART Score and Canadian C-Spine Rule… scored low due to incorrect assumptions" (L217) | correto |
| jin2025agentmd | C5 | "six criteria… final set of 2164" (L386); "only 8.4% (42/500)… 91.6%" (L160) | **impreciso** (os 91,6% referem-se a 500 testes em 100 calculadoras) |
| jin2025agentmd | C6 | "reused the 350 manually validated sets… used GPT-4 to expand them into a clinical vignette" (L479) | correto |
| jin2025agentmd | C7 | "further and more comprehensive evaluations are required before…" (L280) | correto |
| khandekar2024medcalc | C1 | "one-shot demonstration further increases its accuracy to 50.91%" (L257); 1047 instâncias (L254) | correto |
| khandekar2024medcalc | C2 | Tab. 2, GPT-4 one-shot, Risk = 33.75 (L250) | correto |
| khandekar2024medcalc | C3 | Tab. 15: "Overall 23.69% 30.29% 37.92% 48.51%" (L1477) | correto |
| khandekar2024medcalc | C4 | Tab. 4: "GPT-4 0.35 (57%)" zero-shot CoT (L333) | correto |
| khandekar2024medcalc | C5 | "drop is much more drastic as the parameter count increases" (L1496) | correto |
| khandekar2024medcalc | C6 | "necessary (but not sufficient) condition" (L417) | correto |
| zhu2025medagentboard | C1 | "do not consistently outperform the best-performing single LLMs" (L433) | correto |
| zhu2025medagentboard | C2 | "ColaCare's 82.91% AUROC versus DeepSeek-V3's 76.86%"; GPT-4o 85.99; AdaCare 94.28 (L425–465) | correto |
| zhu2025medagentboard | C3 | "largely driven by the power of the underlying base LLM" (L435) | correto |
| zhu2025medagentboard | C4 | "Exploring hybrid architectures that synergize…" (L567) | correto |
| zhu2025medagentboard | C5 | "fail to elicit genuine domain-specific knowledge" (L2346) | correto |
| zhu2025medagentboard | C6 | "frequent JSON parsing errors… getting stuck in loops" (L2349) | correto |
| zhu2025medagentboard | C7 | "Table 13: Estimated cost… for Task 1"; "CoT-SC… most expensive method overall" | **impreciso** (escopo: só Tarefa 1; omite que o CoT-SC único custa mais) |
| wang2025colacare | C1 | "SHAP strategy to obtain feature importance weights" (Eq. 3, L219) | correto |
| wang2025colacare | C2 | Tab. 3 "w/o Expert Models 27.73±3.38" vs "ColaCare 54.05±4.88" (L472–474) | correto |
| wang2025colacare | C3 | "54.05±4.88" vs "Ensemble Mean 53.59±4.52" (L342, L356) | correto |
| wang2025colacare | C4 | Seção 4.3 Multimodal Fusion Network; nenhuma métrica de fidelidade no texto | correto (inferência por ausência) |
| wang2025colacare | C5 | "$0.013 USD per patient"; "# API Requests 8.56 8.37 10.39 11.86" (L539–547) | correto (8,4–11,9 ≈ "8–12") |
| wang2025colacare | C6 | "mechanisms for confidence estimation and continuous learning" (L711) | correto |
| cemri2025mast | C1 | "41% to 86.7% failure rate on 7… MAS" (L130) | correto |
| cemri2025mast | C2 | "κ=0.88… 14 unique modes, clustered into 3 categories" (L106) | correto |
| cemri2025mast | C3 | "(FM-3.2, 8.20%)… (FM-3.3, 9.10%)" (L355) | correto |
| cemri2025mast | C4 | "many existing verifiers perform only superficial checks" (L360) | correto |
| cemri2025mast | C5 | "+15.6% improvement in task success on ProgramDev" (L363) | correto |
| cemri2025mast | C6 | "improvements in the base model capabilities will be insufficient" (L397) | correto |
| cemri2025mast | C7 | "standardized communication protocol"; "symbolic validation" (Apêndice G, L831–834) | correto |
| lee2025shapllm | C1 | "overall fidelity of 0.783… exact match accuracy was 0.425" (L63) | correto |
| lee2025shapllm | C2 | Tab. 3 "SHAP Polarity Error 3… Interpreted negative SHAP values as increasing risk" (L71) | correto |
| lee2025shapllm | C3 | "Fidelity (scored as 1/0.66/0.33 for 3/2/1 correct features)" (L49) | correto |
| lee2025shapllm | C4 | "safety: 3.45 vs. 4.79" (L10, L66) | correto |
| lee2025shapllm | C5 | "performs all calculations outside the LLM… monitoring layer that flags or blocks" (L99) | correto |
| lee2025shapllm | C6 | Tab. 1 "TN 0.3591 0.2 0.70" (L55) | correto |
| lee2025shapllm | C7 | "lack of a direct baseline comparison against standard SHAP explanations" (L95) | correto |
| roeschl2026pipeline | C1 | "mean Krippendorff's α: 0.78 vs. 0.32 vs. 0.39 vs. 0.31" (L11, L68) | correto |
| roeschl2026pipeline | C2 | "exact agreement ranging from 0.0% to 15.8% for five of six models" (L65) | correto |
| roeschl2026pipeline | C3 | "knowledge conflict… assigned a point for 'Hypertension' in the HAS-BLED" (L64) | correto |
| roeschl2026pipeline | C4 | "expert-curated prompting performs better than retrieval-based knowledge augmentation" (L17) | correto |
| roeschl2026pipeline | C5 | "treating physicians tended to underestimate patient risk" (L68) | correto |
| zhu2026agenticexpl | C1 | "mean Jaccard 0.171 versus 0.077… (92.9% versus 78.6%)" (L54, L172) | correto (a "direção" é em relação ao rótulo previsto) |
| zhu2026agenticexpl | C2 | "guideline grounding (0.762 versus 0.143)" (L54) | correto |
| zhu2026agenticexpl | C3 | "paired with attribution-based checks before use in high-stakes risk explanation" (L56) | correto |
| zhu2026agenticexpl | C4 | "same local ollama-served llama3.2:3b"; entrada = dados + probabilidade prevista (L262–268) | correto |
| zhu2026agenticexpl | C5 | "Only 14 generated cases overlapped…" (L229) | correto |
| khan2024prevent | C1 | "25 datasets (N=3,281,919)"; "3,330,085 participants from 21" (L7) | correto |
| khan2024prevent | C2 | "0.774 (0.743, 0.788)… 0.736 (0.710, 0.755)" (L65) | correto |
| khan2024prevent | C3 | "0.54 [0.47, 0.61] and 0.50 [0.39, 0.52]"; "overestimation of risk by about 50%" (L77, L81); PREVENT 1.09/1.04 (L66) | correto |
| khan2024prevent | C4 | Tab. 2: IMC com "*" nas colunas de DCV e DCVA, valores só na de IC (L191) | correto (parte "morte" não conferida) |
| khan2024prevent | C5 | "5.4%, 3.6%, and 2.5%… 9.3%, 6.0%, and 4.7%" (L74) | correto |
| khan2024prevent | C6 | "R2 ≥ 0.99 for 10-year risk estimates" (L74) | correto |
| khan2024prevent | C7 | "sex-specific, race-free… adjusted for competing risk of non-CVD death" (L7) | correto |

Checagens adicionais fora dos [C#], todas **corretas**:
- percentuais do MAST em `justificativa-jade.md`:27 e :33 (FM-1.3 15,7%, FM-1.4 2,8%, FM-1.5 12,4%, FM-2.2 6,8%);
- valores de centralização do PREVENT (`fundamentacao-por-parte.md`:20);
- "PREVENT FORTE/ALTA" na SBC (`textos/sbc2025dislipidemias.txt`:363);
- CKD-EPI 2021 (`interface-design.md`:85);
- tolerância de 5% do MedCalc-Bench;
- "valores alucinados nas primeiras versões" de Lee (`textos/lee2025shapllm.txt`:37);
- Zikmund-Fisher 2014 (PubMed 24246564);
- κw de Santos 2026, no resumo (Europe PMC).

### 6.2 Metadados

Consultei o Crossref para 21 DOIs e o arXiv API para 14 preprints (script `anexos/literatura/verificar_metadados.py`, saída em `verificar_metadados-saida.txt`), além do OpenReview para os veículos NeurIPS. Todos os fichamentos `central` e `alta` com DOI conferem em título, veículo, ano e autores; as exceções estão na tabela de M8. O `python3 tcc/tools/indexar.py validar` roda sem erros, mas **não detecta** DOI ausente, "et al." indevido nem DOI de preprint em `inproceedings`. Sugiro acrescentar essas três regras.

Observação: zhu2026agenticexpl tem ID arXiv 2608.26109 com v1 datada de 21/05/2026. O arXiv API confirma essa data, então não é erro do projeto.

### 6.3 Protocolo de busca estruturada proposto (para fechar a pendência C8)

Base metodológica: Kitchenham & Charters (2007), que dá o protocolo de revisão em engenharia de software; PRISMA 2020 (Page et al., 2021) e PRISMA-S (Rethlefsen et al., 2021), para relatar a busca; e Wohlin (2014), para o *snowballing*. É adequado a um TCC como **revisão sistemática rápida/mapeamento** com um revisor principal e checagem por amostra.

1. **Pergunta (PICOC):**
   - *Population:* explicações em linguagem natural geradas por LLM sobre saídas de modelos de risco clínico;
   - *Intervention:* verificação ou checagem automática da explicação (determinística ou por LLM);
   - *Comparison:* sem verificação, ou LLM isolado;
   - *Outcome:* fidelidade (sinal/direção, números, top-k, afirmações não sustentadas);
   - *Context:* predição de risco clínico, com ênfase cardiovascular.
2. **Bases:** PubMed/MEDLINE; Scopus ou Web of Science (via Portal de Periódicos CAPES); IEEE Xplore; ACM Digital Library; ACL Anthology; arXiv e medRxiv (preprints, sinalizados como tal); SciELO e LILACS (produção brasileira). Complemento: Google Scholar (primeiros 100 resultados, ordenados por relevância).
3. **Período:** 01/2020 até a data da busca (era dos LLMs pós-GPT-3), com a data registrada. Repetir antes da qualificação e da defesa, como `sintese-leitura.md` §4 já prevê.
4. **String (blocos A AND B AND C, adaptada a cada base):**
   - A (LLM): `"large language model*" OR LLM* OR GPT* OR "generative AI" OR "language agent*"`
   - B (explicação e verificação): `explanation* OR explainab* OR "natural language explanation*" OR narrative* OR SHAP OR "feature attribution" OR faithful* OR verif* OR "self-correct*" OR hallucinat*`
   - C (risco clínico): `"risk prediction" OR "risk score*" OR "risk calculator*" OR "clinical prediction model*" OR cardiovascular OR "clinical decision support"`
   - Exemplo PubMed: `("large language model*"[tiab] OR LLM[tiab] OR GPT*[tiab]) AND (explanation*[tiab] OR SHAP[tiab] OR faithful*[tiab] OR verif*[tiab]) AND ("risk prediction"[tiab] OR "risk score*"[tiab] OR cardiovascular[tiab] OR "clinical decision support"[tiab]) AND 2020:2026[dp]`
   - arXiv: `abs:("large language model" AND (SHAP OR faithfulness OR explanation) AND (clinical OR medical))`, categorias cs.CL, cs.AI, cs.LG.
5. **Critérios de inclusão:**
   - (I1) um LLM gera explicação ou justificativa sobre a saída de um modelo ou escore de risco, ou sobre um cálculo clínico;
   - (I2) há avaliação empírica da qualidade da explicação ou do cálculo;
   - (I3) texto completo em inglês, português ou espanhol.
6. **Critérios de exclusão:**
   - (E1) só QA médico sem modelo de risco;
   - (E2) só imagem (Grad-CAM etc.) sem texto;
   - (E3) editoriais e opinião;
   - (E4) duplicatas ou versões anteriores (manter a versão publicada).
7. **Triagem:**
   - título e resumo, depois texto completo;
   - o orientador (ou um colega) triará de forma independente uma amostra aleatória de 20%, e o κ será reportado;
   - os conflitos serão resolvidos por discussão.
8. **Extração:** uma planilha com as mesmas colunas de `trabalhos-relacionados.md` (verificador? top-k? polaridade? números? ablação? domínio? revisão por pares?). Ela passa a ser a fonte da tabela comparativa.
9. **Snowballing:** uma iteração para trás e uma para frente (Wohlin, 2014) a partir dos artigos centrais (Lee 2025, Zhu 2026, ColaCare, AgentMD, Roeschl 2026).
10. **Fluxo PRISMA simplificado:** identificados por base, depois duplicatas removidas, triados, excluídos (com motivos), avaliados no texto completo, excluídos (com motivos) e incluídos, somando os adicionados por *snowballing*.
11. **Registro:** um arquivo `tcc/01-literatura/busca/protocolo.md` com as strings exatas por base, a data e o nº de resultados, mais o CSV exportado e o diagrama. A frase da lacuna passa a ser: "Nos N estudos incluídos (busca de DD/MM/2026), nenhum…".

Esforço estimado: de 25 a 40 horas, o que é compatível com um TCC.

### 6.4 Correções já registradas: foram propagadas?

| Correção | Estado | Evidência |
|---|---|---|
| E9 PREVENT (Coresh como 1º autor) | **Corrigida** | O único "Coresh" fora da lista de autores é a nota de correção (`khan2024prevent.md`:22); o Crossref confirma Khan como 1ª autora |
| E9 "fidelidade 0,783" genérica | **Corrigida** | Todas as ocorrências vêm qualificadas (`lee2025shapllm.md`:52, 64; `sintese-leitura.md`:18) |
| E9 link de Isern | **Parcial** | Tirou o link errado, mas o `url` atual é a página da revista e não há DOI (`isern2016agents.md`:9; `referencias.bib`); a pendência continua aberta |
| E1 "português é lacuna" | **Parcial** | Corrigido em `fundamentacao-por-parte.md`:136 e `trabalhos-relacionados.md`:30. Ainda há resquícios em `defesa-valor.md`:31 e `sintese-leitura.md`:49, e a própria correção depende de uma leitura de resumo (M2) |
| E4 "JADE justificado pelo MAST" | **Não propagada** | `sintese-leitura.md`:60 ("FIPA-ACL (JADE) é exatamente isso"); `perguntas-banca.md`:43–44 ("Resposta anterior") |
| E6 "20–30% dos médicos" | **Pendente** | Continua em `defesa-valor.md`:15 (com aviso) |
| E7 "30% das mortes" | **Pendente** | Continua em `defesa-valor.md`:13 (com aviso); a fonte primária existe (ref. 7) |
| E8 Jabbour como analogia | **Corrigida** | `defesa-valor.md`:27 e `proposta.md`:21 dizem "por analogia" |
| E3 teto do `cardio_train` | **Corrigida** | Nenhuma ocorrência de "73%" na argumentação |

## 7. Referências

### 7.1 Sugeridas para entrar na base (10, todas verificadas)

1. **Neuen BL, Major RW, Grams ME, et al.** Multinational validation of the PREVENT and SCORE2 cardiovascular risk equations across 6.4 million individuals. *Nat Med*. 2026;32:2629–2638. https://doi.org/10.1038/s41591-026-04437-z
   *Por quê:* é a validação externa mais ampla do PREVENT fora dos EUA, com investigadores do ELSA-Brasil. Afeta diretamente a limitação E5 e a pergunta 5 da banca.
2. **Ambrosio M, Alebna PL, Lee T, et al.** Performance of PREVENT and pooled cohort equations for predicting 10-year ASCVD risk in the UK Biobank. *Am J Prev Cardiol*. 2025;22:101009. https://doi.org/10.1016/j.ajpc.2025.101009
   *Por quê:* validação do PREVENT-**ASCVD** em 10 anos (o desfecho exato do TCC) numa coorte não americana.
3. **Li H, et al.** Validation and Recalibration of PCE, China-PAR, and PREVENT Models for Estimating ASCVD Risk in China. *JACC Asia*. 2026;6:602–616. https://doi.org/10.1016/j.jacasi.2025.12.015
   *Por quê:* mostra a necessidade de **recalibração** local, o que fundamenta a ressalva sobre o uso do PREVENT no Brasil.
4. **Oliveira GMM, Brant LCC, Polanczyk CA, et al.** Estatística Cardiovascular – Brasil 2023. *Arq Bras Cardiol*. 2024;121(2):e20240079. https://doi.org/10.36660/abc.20240079
   *Por quê:* fonte primária brasileira para a carga da doença (resolve E7 e `defesa-valor.md`:13).
5. **Gendler M, Nadkarni GN, Sudri K, et al.** Large Language Models in Cardiology: Systematic Review. *JMIR Cardio*. 2026;10:e76734. https://doi.org/10.2196/76734
   *Por quê:* frente ausente, que mapeia o estado da arte de LLM na cardiologia e dá contexto à relevância.
6. **Mishra N, Abu-Hanna A, Calixto I.** Explainability of decoder-only clinical large language models: A scoping review. *Artif Intell Med*. 2026;181:103501. https://doi.org/10.1016/j.artmed.2026.103501
   *Por quê:* revisão de escopo sobre explicabilidade de LLM clínico, diretamente ligada à lacuna. Útil para o K1 (mostra o que já foi mapeado).
7. **Lyu Q, Apidianaki M, Callison-Burch C.** Towards Faithful Model Explanation in NLP: A Survey. *Computational Linguistics*. 2024;50:657–723. https://doi.org/10.1162/coli_a_00511
   *Por quê:* referência consolidada sobre fidelidade após Jacovi & Goldberg; sustenta as definições de `metricas-fidelidade.md`.
8. **Parcalabescu L, Frank A.** On Measuring Faithfulness or Self-consistency of Natural Language Explanations. *ACL 2024*, pp. 6048–6089. https://doi.org/10.18653/v1/2024.acl-long.329
   *Por quê:* argumenta que muitas "métricas de fidelidade" medem autoconsistência. É a crítica mais provável às métricas do TCC, que precisam declarar que medem fidelidade **ao sistema de cálculo**, não aos processos internos do LLM.
9. **Page MJ, McKenzie JE, Bossuyt PM, et al.** The PRISMA 2020 statement. *BMJ*. 2021;372:n71. https://doi.org/10.1136/bmj.n71 · com **Rethlefsen ML, et al.** PRISMA-S. *Syst Rev*. 2021;10:39. https://doi.org/10.1186/s13643-020-01542-z
   *Por quê:* relato da busca estruturada (C8).
10. **Kitchenham B, Charters S.** *Guidelines for performing Systematic Literature Reviews in Software Engineering*. EBSE Technical Report EBSE-2007-01, Keele University & Durham University, 2007. https://www.elsevier.com/__data/promis_misc/525444systematicreviewsguide.pdf · com **Wohlin C.** Guidelines for snowballing in systematic literature studies. *EASE 2014*, pp. 1–10. https://doi.org/10.1145/2601248.2601268
    *Por quê:* protocolo de revisão adequado a Engenharia de Computação e *snowballing* documentado.

Já previstas na pendência "Fichar" e que devem ser fichadas antes da qualificação (verifiquei que existem): Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet*, ICLR 2024 (https://arxiv.org/abs/2310.01798); Gou et al., *CRITIC*, ICLR 2024 (https://arxiv.org/abs/2305.11738); Min et al., *FActScore*, EMNLP 2023, pp. 12076–12100 (https://doi.org/10.18653/v1/2023.emnlp-main.741).

### 7.2 Fontes usadas neste parecer
- Textos completos em `tcc/01-literatura/textos/` (9 fichamentos de leitura completa).
- Crossref REST API (https://api.crossref.org), arXiv API (https://export.arxiv.org/api), OpenReview API (https://api2.openreview.net), PubMed E-utilities (PMID 24246564, 42086979, 40510258, 41718513, 41989882, 42594748, 38896747) e Europe PMC (resumo de Santos 2026, doi:10.1093/ehjdh/ztag073).
- Isern D, Moreno A. *J Med Syst*. 2016;40(2):43. https://doi.org/10.1007/s10916-015-0376-2
- Tang X, et al. MedAgents. *Findings of ACL 2024*, pp. 599–621. https://doi.org/10.18653/v1/2024.findings-acl.33
- Chan JTN, Kwek RK. *Front Digit Health*. 2025;7:1710594. https://doi.org/10.3389/fdgth.2025.1710594
- Zikmund-Fisher BJ, et al. Blocks, ovals, or people? *Med Decis Making*. 2014;34(4):443–453. https://doi.org/10.1177/0272989X13511706

### 7.3 Anexos
- `tcc/05-banca/anexos/literatura/verificar_citaveis.py`: checagem reproduzível dos 57 [C#]; a saída está em `verificar_citaveis-saida.txt`.
- `tcc/05-banca/anexos/literatura/verificar_metadados.py`: consulta ao Crossref e ao arXiv; a saída está em `verificar_metadados-saida.txt`.
