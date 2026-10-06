---
titulo: Parecer da banca — ética, proteção de dados e regulação
status: vigente
atualizado: 2026-09-29
resumo: Auditoria dos aspectos éticos, legais e de proteção de dados do HeartPredict (LGPD, CEP/Conep, ANVISA, AI Act/PL 2338, termos dos provedores de LLM), com notas, problemas classificados, textos sugeridos e perguntas da banca.
---

# Parecer de ética, proteção de dados e regulação — HeartPredict

**Avaliador(a):** membro da banca (Ética em Pesquisa, Direito Digital e Regulação de IA em Saúde)
**Objeto:** repositório `HEARTPREDICT` no estado de 29/09/2026 (árvore de trabalho, com alterações não commitadas), documentação em `tcc/` e código em `frontend/`, `backend-gateway/`, `experimentos/piloto/` e `jade-agents/`.
**Anexos:** [trechos normativos e contratuais transcritos](anexos/etica/trechos-normativos.md) · [script de verificação do gateway](anexos/etica/verificacao-gateway.py) · [saída da verificação](anexos/etica/verificacao-gateway-saida.txt)

> Aviso de método: este parecer foi feito para uma banca acadêmica e não é consultoria jurídica. As normas foram lidas nas fontes oficiais em 29/09/2026 (seção 7). Os termos de serviço dos provedores mudam com frequência e precisam ser conferidos de novo antes da defesa.

---

## 1. Parecer resumido e veredito

O projeto demonstra **sensibilidade ética acima da média** para um TCC de graduação. Ele não pede o nome do usuário, marca o texto como gerado por IA e "não verificado", tem uma seção de limites honesta e uma [auditoria de decisões](../02-argumentacao/auditoria-decisoes-autorais.md) que admite os próprios erros. O **núcleo experimental** (vinhetas sintéticas, NHANES e anotação da fidelidade de textos de LLM) **não precisa de CEP**. Também não expõe pessoas a risco.

O problema está na **demonstração com dados reais de usuários**. O código confirma a afirmação da interface de que o sistema não guarda as respostas **no fluxo novo**, mas o aviso **omite o que importa**. Os valores de saúde vão, sem escolha do usuário, para um provedor nos EUA. No **plano gratuito do Gemini**, esse provedor **usa o conteúdo para treinar modelos, pode submetê-lo a revisores humanos e pede que não se enviem dados pessoais ou sensíveis**. Os termos do **Gemini** proíbem o uso "to provide medical advice", e os do **Groq** dizem que o serviço "is not for consumer use" e não deve servir para aconselhamento médico. Faltam ainda base legal declarada (LGPD, art. 11), aviso de privacidade (art. 9º) e informação sobre a transferência internacional (art. 33). O endpoint legado `/predict` continua exposto e registra em log o nome e os dados de saúde. A avaliação opcional por médicos e o teste de usabilidade planejado estão enquadrados na **resolução errada** (CNS 510/2016, que é de Ciências Humanas e Sociais), e a Res. CNS 674/2022 diz expressamente que TCCs não se beneficiam da dispensa para atividades de ensino. Por fim, vários textos atribuem ao **AI Act** e ao **PL 2338/2023** "exigências" que não se aplicam ao projeto.

**Veredito: APROVADO COM RESSALVAS OBRIGATÓRIAS.**
- O **trabalho de pesquisa** (experimento *in silico*) é eticamente adequado, desde que corrija as citações normativas (M1, M4).
- A **demonstração pública com dados reais** **não deve ser aberta a terceiros** enquanto os problemas **C1, C2 e M2** não forem resolvidos. Na defesa, recomenda-se usar **perfis fictícios** e um provedor que não treine com os dados.
- A **avaliação por médicos** e o **teste com usuários** só podem acontecer depois de submissão ao CEP ou de dispensa formal **por escrito** do CEP da instituição (M1).

---

## 2. Notas por critério (0–10)

| Critério | Nota | Justificativa |
|---|---|---|
| **Veracidade das declarações de privacidade** | **5** | "O sistema não guarda as suas respostas" é **literalmente verdadeiro no fluxo novo**. Verificado: `avaliacao.py` não registra nem persiste nada, e o frontend não usa `localStorage` nem cookies (`App.jsx:10`). "Sem identificação" também se sustenta: o provedor recebe só idade, sexo e valores clínicos, a partir do IP do servidor. Mas a declaração é **incompleta a ponto de induzir erro**: não diz que o provedor pode **reter** os dados (Groq: até 30 dias; Gemini gratuito: uso para treino e revisão humana), não diz que vão para outro país e que o envio é **automático**. Além disso, o próprio gateway expõe o `/predict` legado, que registra o nome e os dados de saúde (`main.py:120,138,237`). |
| **Conformidade com a LGPD** | **3** | São dados sensíveis de saúde (art. 5º, II), e nenhum documento identifica a base legal (art. 11). Não há aviso com controlador, contato, finalidade, compartilhamento e direitos (art. 9º, I–VII), nem consentimento específico e destacado (art. 11, I) ou para a transferência internacional (art. 33, VIII). O usuário não pode recusar o envio ao LLM (`TelaResultado.jsx:19-31`). O ponto positivo é a **minimização** exemplar: não pede nome e usa só as variáveis do cálculo (art. 6º, III). |
| **Adequação ética da pesquisa** | **6** | O núcleo (sintético + NHANES + anotação de textos) está corretamente fora do sistema CEP/Conep. Mas D015 cita a Res. 510/2016 (Ciências Humanas e Sociais) em vez da **Res. 674/2022, art. 26**, e ignora a **Lei 14.874/2024** e o **Decreto 12.651/2025**. A avaliação por médicos (n ≈ 7–12, recrutados por contato do orientador) dificilmente é "opinião pública com participantes não identificáveis". O **teste de usabilidade com ~5 pessoas** (`interface-design.md:122`) não aparece em nenhuma análise de CEP. |
| **Enquadramento regulatório (ANVISA / termos de uso)** | **4** | O tema **não é discutido** em nenhum documento do TCC (não há uma única menção à ANVISA). A finalidade expressa ("Calcule o seu risco", categoria, meta de LDL, "se for preciso tratar...") encaixa-se em "prevenção" (RDC 751/2022, art. 2º, X, a) e **não** na exclusão de bem-estar (RDC 657/2022, art. 2º, IX). O aviso de protótipo existe, mas **some na impressão** (`resultado.css:305-311`). O uso previsto contraria os termos do Gemini e do Groq. |
| **Transparência de IA** | **7** | Selo "Texto gerado por inteligência artificial", nome do modelo, aviso "não passa pelo verificador" e a regra "se divergir, considere os números" (`Resultado.jsx:105-135`) formam uma prática **exemplar**. O que desconta: a transparência é atribuída a uma "exigência do AI Act, art. 50", que não se aplica ao projeto (art. 2º, n.º 1 e n.º 6). Quando se aplica, o art. 50, n.º 2 exige **marcação legível por máquina**, e isso não existe aqui. O art. 13 e o PL 2338 são citados como "exigência regulatória". A página inicial não diz **qual** provedor nem **em que país**. |
| **Honestidade das limitações** | **7** | A seção "Limites deste resultado" (`TelaResultado.jsx:110-118`), a decisão D025 (risco declarado) e a auditoria E1–E9 mostram honestidade rara. Descontos: a manchete "Em 100 pessoas com os mesmos dados, cerca de N teriam..." (`TelaResultado.jsx:8-12`) apresenta como frequência populacional brasileira o que a própria auditoria E5 diz valer só para a calibração nos EUA. "Exigência regulatória de explicabilidade" (`defesa-valor.md:16`) é um exagero. A OMS 2024 e Chan 2025 sustentam argumentos, mas só o resumo foi lido. "O resultado acima [...] continua válido" (`Resultado.jsx:120`) afirma validade que o trabalho não demonstra. |

**Média simples: 5,3/10.** A nota é puxada para baixo pela demonstração com dados reais e sobe muito quando se consideram só o experimento e a documentação.

---

## 3. Pontos fortes

1. **Minimização de dados de verdade.** A interface anterior pedia o nome (`git show HEAD:frontend/src/components/ConversationalForm.jsx:250`, `user_id: updatedValues.nome`). A remoção foi justificada pelo art. 6º, III da LGPD (`interface-design.md:27`). O contrato novo (`avaliacao.py:292-306`) só tem as variáveis do cálculo.
2. **Nada persiste no fluxo novo.** `avaliacao.py` não tem `logger`, não grava arquivo nem guarda estado global. O frontend guarda as respostas só na memória da página (`App.jsx:10`; `grep` sem ocorrências de `localStorage`, `sessionStorage` ou `cookie`). As fontes são hospedadas localmente, sem requisição ao Google Fonts (`interface-design.md:42`).
3. **Separação entre cálculo e linguagem (D002).** O número vem de ferramenta determinística, e o LLM "não faz o cálculo" (`Telas.jsx:44`). É a principal salvaguarda de segurança do paciente no desenho.
4. **Rotulagem da IA** clara, acessível e colocada no ponto de exposição: selo, nome do modelo, "ainda não passa pelo verificador" e "considere os números" (`Resultado.jsx:110,129-133`). A explicação carrega depois do número, então a falha do LLM não bloqueia o resultado.
5. **Recusa em vez de suposição.** Idade fora de 30–79 anos, doença cardiovascular prévia e diabetes têm telas próprias que encaminham ao médico (`perguntas.js:13-34`; `avaliacao.py:57-85`).
6. **Aviso sobre medicamentos** ("Não pare nenhum remédio sem falar com seu médico", `Resultado.jsx:96-98`), com explicação do motivo pelo qual o anti-hipertensivo aparece como fator que "aumentou" o risco. O cuidado é raro e pertinente, embora o aviso fique escondido (ver M3).
7. **Equação renal sem raça** (CKD-EPI 2021, `renal.py:2`) e **PREVENT sem raça**. São escolhas coerentes com a equidade.
8. **Cultura de auditoria.** `auditoria-decisoes-autorais.md` classifica as afirmações como defensáveis, condicionais ou erros e as corrige. É o tipo de integridade que a banca procura.

---

## 4. Problemas encontrados

Legenda: **Crítico** impede a demonstração com dados reais ou compromete a legalidade. **Maior** precisa ser corrigido antes da defesa. **Menor** é melhoria recomendada.

### C1 — [Crítico] Dados de saúde de usuários reais enviados a um plano gratuito cujos termos proíbem esse uso
**Evidência**
- `experimentos/piloto/llm.py:16,20,62-71`: os provedores são Groq (`api.groq.com`) e Gemini (`generativelanguage.googleapis.com`). D024 (`decisoes.md:158-163`) escolhe os **planos gratuitos** de ambos.
- `backend-gateway/app/avaliacao.py:120-134`: `/api/avaliacao/explicacao` envia `prompt.construir(g)` ao provedor configurado. O [conteúdo real enviado](anexos/etica/verificacao-gateway-saida.txt) inclui idade, sexo, colesterol total, HDL, não-HDL, LDL, PAS, uso de anti-hipertensivo e estatina, tabagismo, TFGe e **agravantes** ("doença inflamatória crônica", que na interface inclui HIV, `perguntas.js:164`, e "fator de risco específico da mulher", que inclui abortos espontâneos, `perguntas.js:167-170`).
- **Termos do Gemini API (vigência 23/03/2026):** "When you use Unpaid Services [...] Google uses the content you submit [...] to provide, improve, and develop Google products and services and machine learning technologies"; "human reviewers may read, annotate, and process your API input and output"; "**Do not submit sensitive, confidential, or personal information to the Unpaid Services.**" A exceção que aplica as regras do plano pago vale só para EEE, Suíça e Reino Unido, **não para o Brasil**. Restrição de uso: "You may not use the Services [...] **to provide medical advice**".
- **Termos do Groq (22/06/2026):** "Cloud Services and the AI Model Services under this Agreement are **not for consumer use**"; §4.3: "should not be used for medical, legal, financial, or other professional advice". Pontos favoráveis: o Groq não treina com os dados e, por padrão, só retém até 30 dias para confiabilidade e abuso, com opção de ZDR.
- **LGPD, art. 11, § 4º**: veda o compartilhamento entre controladores de dados de saúde "com objetivo de obter vantagem econômica". Quando o dado é usado pelo Google para desenvolver produtos próprios, o Google passa a atuar como controlador, e a contrapartida é a cota gratuita. Existe, portanto, **risco interpretativo relevante** de enquadramento nessa vedação.

**Por que é crítico:** o usuário recebe a informação de que os dados "são enviados a um serviço de IA externo" (`Telas.jsx:51-52`), mas não de que esse serviço pode **reter, ler por humanos e usar para treinar** os dados. Pelo art. 9º, § 1º, um consentimento dado com informação incompleta sobre o compartilhamento é **nulo**. Além disso, o uso contraria os termos contratuais dos dois provedores.

**Correção**
1. **Nunca** enviar dados de usuários reais ao **Gemini gratuito**. Para a demonstração, usar o Groq com **Zero Data Retention ativado** (Console → *Data Controls*), um modelo local ou um plano pago com cláusula de não treinamento. Registrar a escolha em uma nova decisão (D026).
2. Para o **experimento** (vinhetas sintéticas e NHANES), o Gemini gratuito **continua aceitável**, porque não há titular vivo identificável nas vinhetas e o NHANES é público e desidentificado. Declarar isso na Metodologia.
3. Dizer no aviso **qual** provedor é usado, **onde** ele está e **o que faz** com os dados (texto sugerido no quadro após C2).
4. Na defesa, preferir **perfis fictícios pré-carregados** (por exemplo, o caso publicado da mulher de 50 anos, D009) em vez de dados de pessoas da plateia.

### C2 — [Crítico] Sem base legal, sem aviso de privacidade e sem escolha sobre o envio ao provedor estrangeiro
**Evidência**
- Nenhum documento do TCC identifica a **base legal** do tratamento. `grep` por "base legal", "consentimento" e "art. 11" em `tcc/` não encontra nada aplicado à interface. A única referência à LGPD é o art. 6º (`interface-design.md:27,109,139`).
- `Telas.jsx:48-54`: a seção "Seus dados" tem duas frases e não traz controlador, contato, finalidade específica, prazo, compartilhamento ou direitos (art. 9º, I–VII).
- `TelaResultado.jsx:19-31`: `pedirExplicacao()` é chamada automaticamente em `useEffect` quando o resultado aparece. **Não há como recusar** o envio ao LLM mantendo o cálculo, que é local ao servidor e não precisa do provedor.
- **LGPD, art. 4º, II, b:** mesmo que o tratamento seja considerado "exclusivamente acadêmico", os **arts. 7º e 11 continuam aplicáveis**. A base do art. 11, II, "c" (estudos por **órgão de pesquisa**) não serve: o controlador é um estudante, não um "órgão de pesquisa" no sentido do art. 5º, XVIII, e a demonstração não é um "estudo". Na prática, **a única base viável é o consentimento específico e destacado (art. 11, I)**.
- **Art. 33:** para os EUA não existe decisão de adequação (inciso I), e o projeto não tem cláusulas-padrão da ANPD (Res. CD/ANPD 19/2024). Resta o **consentimento específico e em destaque para a transferência, "com informação prévia sobre o caráter internacional da operação"** (inciso VIII). Se a banca aceitar a tese do art. 4º, II, b (fim exclusivamente acadêmico), o art. 33 não se aplicaria em sentido estrito. Mesmo assim, recomendo não depender dessa tese: uma demonstração aberta a qualquer pessoa dificilmente é "exclusivamente" acadêmica, e o custo de cumprir é baixo.

**Correção:** (a) tornar a explicação por IA **opcional e ativada pelo usuário** (botão "Gerar explicação por IA", com o aviso ao lado); (b) incluir um aviso de privacidade completo; (c) registrar a base legal numa decisão D026; (d) indicar um contato (e-mail institucional do orientando ou do orientador).

> **Texto sugerido — seção "Seus dados" (tela inicial)**
> **Como tratamos os seus dados**
> Este é um protótipo de um Trabalho de Conclusão de Curso de Engenharia de Computação da [instituição], feito por [nome do estudante] e orientado por [nome]. Contato: [e-mail institucional].
> - **O que usamos:** só as respostas deste questionário (idade, sexo, exames e condições de saúde). Não pedimos nome, documento, e-mail ou localização.
> - **Para quê:** apenas para calcular e explicar o seu risco nesta tela. As respostas não são usadas na pesquisa, não são vendidas e não são guardadas pelo nosso sistema: somem quando você fecha a página.
> - **Cálculo:** feito no nosso servidor, sem inteligência artificial.
> - **Explicação por IA (opcional):** se você pedir, os valores informados, sem nome, são enviados à empresa [Groq Inc.], nos **Estados Unidos**, que gera o texto. [A empresa se compromete a não usar os dados para treinar modelos e está configurada para não guardá-los.] Se você não quiser, veja o resultado sem a explicação.
> - **Seus direitos:** você pode tirar dúvidas ou fazer pedidos pelo contato acima (LGPD, art. 18).
>
> **Texto sugerido — botão de consentimento (tela de resultado, antes de gerar o texto)**
> ☐ Quero uma explicação escrita por inteligência artificial. Entendo que os valores que informei (sem meu nome) serão enviados à empresa [Groq Inc.], nos Estados Unidos, só para gerar este texto.
> [Gerar explicação]  ·  [Não, obrigado]

### M1 — [Maior] Enquadramento ético (CEP) com a resolução errada e atividades com participantes sem previsão de submissão
**Evidência**
- `decisoes.md:110`: "confirmar com o CEP [...] se ela se enquadra como pesquisa de opinião com participantes não identificados (**Res. CNS 510/2016, art. 1º, parágrafo único**)". A 510/2016 regula pesquisas em **Ciências Humanas e Sociais** (art. 1º, caput). A avaliação, por médicos, da utilidade e segurança de explicações clínicas geradas por software, num TCC de Engenharia, não é pesquisa de Ciências Humanas e Sociais. A norma de tramitação aplicável a qualquer área é a **Res. CNS 674/2022**, cujo **art. 26** tem lista de dispensas parecida.
- **Res. 674/2022, art. 26, VIII, "a"**: "**não se enquadram** no inciso antecedente os **Trabalhos de Conclusão de Curso de Graduação** [...], devendo-se, nesses casos, apresentar o protocolo de pesquisa ao Sistema CEP/Conep". Ou seja, o TCC **não** pode alegar que é "atividade de ensino".
- **Res. 674/2022, art. 2º, XXVI**: pesquisa de opinião pública exige "**sem possibilidade de identificação do participante**". Com 7 a 12 médicos recrutados pelo orientador (`decisoes.md:175`, O003), numa comunidade pequena e provavelmente por formulário com e-mail, a não identificabilidade é **difícil de garantir**. Uma escala Likert aplicada a um grupo escolhido é "coleta dirigida de dados" (art. 2º, III).
- **Lei 14.874/2024**, art. 2º, XXXIV: pesquisa com seres humanos inclui envolver o ser humano "de forma direta ou indireta, incluído o manejo de seus dados". Art. 63: vale "em todas as áreas do conhecimento". **Decreto 12.651/2025, art. 39**: as normas do CNS **continuam válidas** até a Instância Nacional publicar as suas. Nenhum documento do TCC menciona a Lei ou o Decreto.
- **Teste de usabilidade** com ~5 pessoas do público-alvo (`interface-design.md:122`; `pendencias.md:81`): envolve participantes, possivelmente idosos (público-alvo com ≥ 60 anos, `interface-design.md:13`) e potencialmente os **dados de saúde deles**. Não aparece em D015 nem em O002.
- `decisoes.md:87` diz "NHANES (público, sem necessidade de comitê de ética)". A conclusão está **correta**, mas falta o fundamento normativo (674/2022, art. 26, II/III) e a menção às restrições de uso do NCHS, que proíbem tentar reidentificar participantes. Estas últimas devem ser conferidas no site do NCHS e citadas.

**Enquadramento correto, atividade por atividade**

| Atividade | Participante humano? | Enquadramento | Precisa de CEP? |
|---|---|---|---|
| Vinhetas sintéticas → LLM → métricas | Não | Não é pesquisa com seres humanos (Lei 14.874, art. 2º, XXXIV, a contrario) | **Não** |
| Perfis do NHANES (arquivos públicos desidentificados) | Indireto, com dados públicos | Res. 674/2022, art. 26, II e III | **Não** (declarar e respeitar as restrições de uso do NCHS) |
| Anotação de textos pelo autor e por um colega (κ) | O colega atua como **membro da equipe**, e os dados analisados são os textos, não a pessoa | Não é coleta de dados sobre o anotador | **Não**, se o colega constar formalmente como integrante da equipe e nenhum dado sobre ele for analisado. Documentar |
| Avaliação Likert por médicos (D015, opcional) | **Sim** (coleta dirigida, n pequeno, identificável) | Res. 674/2022; Res. 466/2012; Lei 14.874/2024 | **Sim**, salvo dispensa **por escrito** do CEP local. Tramitação provavelmente simplificada |
| Teste de usabilidade com ~5 usuários | **Sim** | Idem | **Sim**, salvo dispensa escrita. Usar **dados fictícios** fornecidos pelo pesquisador, nunca os exames do participante |
| Demonstração pública (sem coleta para pesquisa) | Não é pesquisa | LGPD (C2), não CEP | Não, **desde que** nenhum dado ou log da demonstração seja usado como dado de pesquisa |

**Correção:** reescrever D015 com o quadro acima, citando a 674/2022, a Lei 14.874/2024 e o Decreto 12.651/2025. Consultar o CEP **antes** de qualquer contato com médicos ou usuários e guardar a resposta como anexo do TCC. Se não houver tempo para o CEP, **retirar** a avaliação por médicos e o teste de usabilidade e declará-los como trabalho futuro.

### M2 — [Maior] O gateway ainda expõe o fluxo legado, que registra nome e dados de saúde em log, com endpoints sem autenticação e CORS aberto
**Evidência** (verificação executada; ver [saída](anexos/etica/verificacao-gateway-saida.txt))
- `main.py:18-20` inclui o roteador novo **no mesmo app** que mantém `/predict`, `/explanation/{user_id}` e `/pending` (rotas listadas na verificação).
- A interface antiga enviava o **nome** como `user_id` (`git show HEAD:frontend/src/components/ConversationalForm.jsx:250`). O gateway registra em nível INFO:
  - `main.py:120` `Recebendo dados do paciente: {user_id}`
  - `main.py:138` `Enviando dados para JADE Agent: {...}` (dicionário completo com pressão, colesterol, glicose, tabagismo e álcool). Na verificação, apareceu no log `maria.silva@email.com` com todos os dados;
  - `main.py:237` registra o texto completo da explicação, que no fluxo legado contém `patientName` = `user_id`.
- No fluxo legado, o `AgenteExplicador.java:147,162` coloca `userId` (o nome) **no prompt enviado ao Gemini** ("• Paciente: ..."). Os agentes também imprimem os dados no stdout (`AgenteClassificador.java:59,87,103`).
- `main.py:23,192-195`: `pending_explanations` guarda `user_id` em memória por até 60 s. `main.py:248-253`: `/pending` **lista os `user_id`** sem autenticação.
- `main.py:232-246`: `/explanation/{user_id}` aceita **qualquer** POST sem autenticação. Um terceiro pode **injetar uma "explicação" falsa** para um usuário que está aguardando, o que é um risco de desinformação em saúde (art. 46 da LGPD e princípio da segurança, art. 6º, VII).
- `main.py:26-32`: `allow_origins=["*"]`, com o servidor ouvindo em `0.0.0.0` (`main.py:257`). Qualquer site pode usar o gateway e esgotar a cota gratuita do LLM (negação de serviço) ou abusar do `/explanation`. Verificado: um preflight de `https://site-qualquer.example` recebe `access-control-allow-origin: *`.
- O `README.md` ainda documenta o fluxo legado como executável ("3. Agentes JADE (fluxo antigo /predict)").

**Correção:** remover `/predict`, `/explanation` e `/pending` do app que serve a interface, ou montá-los só com uma variável `MODO_LEGADO=1`. Rebaixar os logs a DEBUG e nunca registrar corpo de requisição. Restringir o CORS à origem do frontend. Limitar a taxa de chamadas do `/api/avaliacao/explicacao`. Adicionar um teste automatizado que confirme que nenhum log contém valores clínicos.

### M3 — [Maior] O enquadramento sanitário (SaMD) não foi analisado, e os avisos de protótipo desaparecem no PDF que o usuário leva ao médico
**Evidência**
- Não há nenhuma menção a ANVISA, SaMD ou RDC em `tcc/` (`grep` sem resultados).
- **Finalidade pretendida** declarada pelo próprio produto: "Calcule o seu risco de infarto e AVC nos próximos 10 anos" (`Telas.jsx:14`). Categoria, **meta de LDL** e "Se for preciso tratar, a diretriz recomenda reduzir o LDL em pelo menos 50%" (`TelaResultado.jsx:79-97`). A finalidade é de **prevenção de doença** individual.
- **RDC 751/2022, art. 2º, X, "a"**: dispositivo médico é o software destinado a "diagnóstico, **prevenção**, monitoramento, tratamento" de doença. **RDC 657/2022, art. 2º, VII** inclui o SaaS. O **art. 2º, IX** exclui dos softwares de bem-estar os que se destinam a "prevenção". O **art. 2º, XII** cita "**previsão de risco**" como função de SaMD. Pela **Regra 11** (RDC 751/2022), software que presta informações para decisões terapêuticas seria classe II no mínimo.
- **Leitura da banca:** um protótipo acadêmico **não comercializado** e sem "fabricante" que peça regularização não precisa de registro na ANVISA enquanto for pesquisa e demonstração restrita. A RDC 657 trata de *regularização* para colocação no mercado. Porém, **o aviso "protótipo, não substitui avaliação médica" não muda a finalidade pretendida**, que decorre do que o software faz e diz. Se o sistema for disponibilizado **publicamente** para o público leigo estimar o próprio risco, entra numa zona cinzenta regulatória. O TCC precisa **dizer isso** e restringir o acesso.
- **Impressão:** `resultado.css:305-311` esconde no `@media print` o `.cabecalho__selo` ("Protótipo acadêmico", `Estrutura.jsx:33`) e o `.rodape` ("Não substitui a avaliação de um profissional de saúde", `Estrutura.jsx:44-45`). O PDF que a interface sugere levar ao médico (`TelaResultado.jsx:121`) **perde a identificação de protótipo** e não traz data nem versão do cálculo.
- **Medicamentos:** o aviso "Não pare nenhum remédio sem falar com seu médico" fica dentro de um `<details>` fechado (`Resultado.jsx:87-100`). Na tela, o usuário vê "Aumentaram o seu risco: uso de anti-hipertensivo" **sem** o aviso aberto. Ele aparece expandido só na impressão (`resultado.css:312-314`). O prompt proíbe "diagnóstico", mas **não proíbe** o LLM de sugerir iniciar, parar ou mudar medicamentos (`prompt.py:14-19`), e a temperatura é 0,7 (`avaliacao.py:132`), sem verificador (D025).

**Correção:** incluir no TCC uma subseção "Enquadramento regulatório" com a leitura acima. Tornar o aviso sobre medicamentos **visível sem clique**, logo abaixo da lista de fatores. Manter o selo, o rodapé, a data, a versão e "gerado por protótipo acadêmico, não é laudo" na impressão. Acrescentar ao prompt: "Não sugira iniciar, suspender ou alterar medicamentos; não recomende doses; não use tom de urgência". Não publicar a interface em URL aberta, ou colocá-la atrás de senha para a banca.

### M4 — [Maior] Citações normativas imprecisas: AI Act, PL 2338/2023 e OMS apresentados como "exigências"
**Evidência**
- `interface-design.md:95` e `Resultado.jsx:105`: "Transparência sobre conteúdo gerado por IA é **exigência do AI Act, art. 50**". O AI Act aplica-se a sistemas colocados no mercado ou em serviço **na União** (art. 2º, n.º 1, a) e **não** se aplica a sistemas desenvolvidos só para pesquisa científica ou antes de sua colocação no mercado (art. 2º, n.º 6 e n.º 8). Além disso, o art. 50 **não exige** um selo visível nesse caso. O n.º 2 exige **marcação legível por máquina** a cargo do *prestador* do sistema gerador, e o n.º 4 exige a divulgação para texto publicado "with the purpose of informing the public on matters of public interest", o que não é o caso de uma explicação individual. O n.º 1 (informar que a pessoa interage com IA) é o paralelo mais próximo. O selo é **boa prática inspirada no art. 50**, e não cumprimento de uma exigência.
- `defesa-valor.md:16`: "**Exigência regulatória de explicabilidade:** OMS 2024; AI Act, Art. 13; PL 2338/2023". A OMS publica **orientação**, não regulação. O art. 13 do AI Act trata da transparência do **prestador para o responsável pela implantação** em sistemas de **alto risco**. O PL 2338/2023 **não é lei**: a situação na Câmara em 02/09/2026 é "Aguardando Parecer".
- `justificativa-jade.md:41`: "atende à exigência de **auditabilidade** do AI Act (**Art. 13**)". O registro de eventos (*logs*) está no **art. 12**, também só para alto risco. `perguntas-banca.md:23` repete: "OMS e AI Act exigem inteligibilidade".
- A OMS 2024 (`who2024lmm.md`, "leitura: resumo") fundamenta a Justificativa sem que o texto tenha sido lido.

**Correção:** trocar "exigência" por "**orientação** (OMS 2024) e **tendência regulatória** (AI Act, que só se aplica na UE; PL 2338/2023, em tramitação)". Citar o art. 50 como **referência de boa prática**, e, se quiser, dizer que num lançamento na UE ele exigiria também marcação legível por máquina (art. 50, n.º 2). Corrigir art. 13 → art. 12 para registros. Ler o texto completo da OMS antes de citá-la.

### M5 — [Maior] H3 (raça/etnia) não é operacionalizável com o prompt atual, e a discussão de equidade é estreita
**Evidência**
- H3 (`proposta.md:30`; D017) prevê pares contrafactuais que só diferem em raça/etnia (`proposta.md:79`). Mas `prompt.py:26-53` **não tem campo de raça/etnia**, e `grep` por "raça" em `experimentos/piloto/*.py` só encontra a regex de pré-anotação (`preanotar.py:18`) e o comentário de `renal.py`. Com o prompt atual, o par contrafactual gera **prompts idênticos**, e H3 fica trivialmente confirmada ou sem objeto.
- Para testar H3, raça/etnia precisa **entrar no prompt** como dado irrelevante ao modelo. Isso é legítimo nas vinhetas sintéticas, mas no NHANES trata-se de dado sensível (LGPD, art. 5º, II), mesmo que público nos EUA. É preciso declarar o objetivo e **não** levar esse campo para a interface.
- A **equidade para o usuário brasileiro** não é discutida além da calibração. O PREVENT não foi validado na população brasileira (reconhecido em `TelaResultado.jsx:114`). As categorias raciais do NHANES não correspondem às de cor/raça do IBGE. A pergunta de sexo é binária, sem orientação para pessoas trans ou intersexo (`perguntas.js:48-58`). A base de Chan 2025 (`chan2025vies.md`) foi lida só no resumo e tem DOI "(verificar)".

**Correção:** acrescentar ao prompt da configuração experimental um campo "Raça/etnia autodeclarada" (só nas vinhetas de H3) e documentar esse campo. Escrever uma subseção "Equidade" que cubra calibração, representatividade, sexo e letramento (este já tratado na interface). Ler Chan 2025 na íntegra.

### m1 — [Menor] A manchete de frequência natural omite a ressalva de calibração
`TelaResultado.jsx:8-12`: "Em 100 pessoas com os mesmos dados, cerca de N teriam...". A auditoria E5 (`auditoria-decisoes-autorais.md:64`) corrigiu isso nos textos do TCC, mas não na interface. **Sugestão:** "Pelo modelo PREVENT, calibrado em adultos dos EUA, em 100 pessoas com dados como os seus, cerca de N teriam...".

### m2 — [Menor] "O resultado acima [...] continua válido"
`Resultado.jsx:120`. Sugerir "O cálculo acima não depende deste texto" (afirmação verdadeira), em vez de "válido".

### m3 — [Menor] Detalhes de segurança da informação
- `llm.py:69`: a chave do Gemini vai na *query string* (`?key=`). Se houver log de URL em proxy, a chave vaza. Usar o cabeçalho `x-goog-api-key`.
- `avaliacao.py:134`: devolve ao cliente até 200 caracteres da mensagem de erro do provedor. Trocar por uma mensagem genérica e registrar o detalhe só no servidor.
- O `uvicorn` padrão registra IP, porta, método e rota de cada acesso (sem corpo). Isso é compatível com "não guarda as respostas", mas o aviso de privacidade deve mencionar esses registros técnicos, se forem mantidos.

### m4 — [Menor] A página inicial não identifica provedor, país nem responsável
`Telas.jsx:51-52` diz "serviço de inteligência artificial externo". O LGPD, art. 9º, V–VI pede que se informe o uso compartilhado e os agentes envolvidos. Resolvido pelo texto sugerido em C2.

### m5 — [Menor] Revisão humana de decisões automatizadas
A categoria de risco é um perfil de saúde produzido de forma automatizada. Mesmo que se discuta se o art. 20 da LGPD se aplica, o texto "Leve este resultado ao seu médico" já funciona como a via de revisão humana. Vale **nomear isso** no TCC.

### m6 — [Menor] Responsabilidade por texto de IA errado
O TCC não discute quem responde se o texto do LLM induzir dano. A responsabilidade não passa ao provedor, porque os termos de ambos excluem o uso para aconselhamento médico: fica com quem **disponibiliza** o sistema (o autor e, eventualmente, a instituição), pelo regime geral de responsabilidade civil (Código Civil, arts. 186 e 927). O aviso reduz, mas **não elimina**, essa responsabilidade. É mais um argumento a favor de explicação opcional, demonstração restrita e verificador.

---

## 5. Perguntas da banca

| # | Pergunta | Resposta esperada | O projeto responde hoje? |
|---|---|---|---|
| 1 | "O sistema não guarda as suas respostas." Isso é verdade para **todo** o caminho dos dados? | O nosso código não persiste nada no fluxo novo, mas o provedor recebe os dados e pode retê-los (Groq: até 30 dias, salvo ZDR; Gemini gratuito: uso para treino e revisão humana). O aviso será completado. | **Parcial.** Verdadeiro para `avaliacao.py`/`App.jsx`. Omite a retenção pelo provedor (C1). |
| 2 | Qual é a **base legal** da LGPD para tratar dado de saúde na demonstração? | Consentimento específico e destacado (art. 11, I). O art. 4º, II, b mantém os arts. 7º e 11 mesmo para fins acadêmicos. O art. 11, II, c não serve porque o controlador não é "órgão de pesquisa". | **Não** (C2). |
| 3 | Os dados vão para os EUA. Qual hipótese do art. 33 autoriza isso? | Consentimento específico e em destaque, com informação prévia sobre o caráter internacional (art. 33, VIII), já que não há adequação nem cláusulas-padrão. | **Não.** A interface diz "serviço externo", sem dizer o país (C2). |
| 4 | Você leu os **termos do plano gratuito** do Gemini e do Groq? Eles permitem o seu uso? | O Gemini gratuito usa os dados para treino, prevê revisão humana, pede para não enviar dados sensíveis e proíbe "medical advice". O Groq não treina com os dados, mas não é "for consumer use" e não deve ser usado para aconselhamento médico. Com dados reais, a demonstração deve usar Groq com ZDR, modelo local ou plano pago. | **Não.** D024 (`decisoes.md:158-163`) avalia só custo e cota. |
| 5 | O que exatamente vai no prompt? Há algo que identifique a pessoa? | Idade, sexo, lipídios, PAS, medicamentos, tabagismo, TFGe e agravantes. Não vão nome nem IP do usuário. A combinação é praticamente não reidentificável pelo provedor, mas continua sendo dado de saúde. | **Parcial.** A resposta está no código (`prompt.py:26-53`), mas não no TCC. |
| 6 | O endpoint `/predict` ainda está ativo? O que ele registra? | Sim, ainda está. Ele registra nome e dados de saúde em INFO, e `/explanation` aceita injeção sem autenticação. Será removido ou isolado. | **Não** (M2). |
| 7 | Por que a Res. **510/2016**? Qual resolução rege a tramitação no Sistema CEP/Conep para esta área? | A 510 é de Ciências Humanas e Sociais. A tramitação e as dispensas estão na **674/2022, art. 26**, e o marco legal é a **Lei 14.874/2024**, regulamentada pelo **Decreto 12.651/2025**, cujo art. 39 mantém as normas do CNS em vigor. | **Não** (M1; `decisoes.md:110`). |
| 8 | O que diz o parágrafo único do art. 1º da 510/2016, e ele cobre a avaliação por médicos? | Lista o que não é registrado nem avaliado pelo CEP/Conep: opinião pública com participantes **não identificados**, informação de acesso público ou de domínio público, censos, bases agregadas, revisão de literatura, aprofundamento teórico da prática, atividade exclusivamente de ensino. Um painel pequeno de médicos convidados e identificáveis dificilmente se encaixa, e TCC não é "atividade de ensino" (674/2022, art. 26, VIII, a). | **Parcial.** A dúvida está registrada, mas a conclusão tende ao lado errado. |
| 9 | E o teste de usabilidade com 5 pessoas? | É pesquisa com participantes: precisa de CEP ou de dispensa escrita, com dados fictícios e TCLE. | **Não** (`interface-design.md:122`). |
| 10 | O NHANES precisa de CEP? | Não: são informações públicas desidentificadas (674/2022, art. 26, II/III), respeitadas as restrições de uso do NCHS, que proíbem tentar reidentificar. | **Parcial.** A conclusão está certa, mas sem fundamento normativo (`decisoes.md:87`). |
| 11 | O HeartPredict é um *Software as a Medical Device* pela ANVISA? | Pela finalidade (prevenção, previsão de risco individual, metas terapêuticas), atende à definição (RDC 751/2022, art. 2º, X, a; RDC 657/2022, art. 2º, VII e XII) e não é software de bem-estar (art. 2º, IX). Não precisa de regularização enquanto for protótipo de pesquisa não comercializado e de acesso restrito, mas não deve ser disponibilizado ao público. | **Não.** Não há análise regulatória (M3). |
| 12 | "Protótipo acadêmico, não substitui avaliação médica" basta para uma demonstração pública? | Não: o aviso não muda a finalidade pretendida, some na impressão e não impede a decisão de parar um remédio. É preciso acesso restrito, aviso visível sobre medicamentos e prompt que proíba conduta. | **Parcial** (M3). |
| 13 | Se alguém parar o anti-hipertensivo porque a tela disse que ele "aumentou o risco", quem responde? | Quem disponibiliza o sistema, pelo regime geral de responsabilidade civil. O provedor exclui esse uso nos termos. Por isso o aviso deve estar aberto na tela, e o LLM, proibido de sugerir mudanças em medicamentos. | **Parcial.** O aviso existe, mas escondido (`Resultado.jsx:96-98`). |
| 14 | O AI Act se aplica ao seu sistema? O que o art. 50 exige de fato? | Não se aplica: o sistema não é colocado no mercado da UE e está excluído como pesquisa (art. 2º, n.º 6 e 8). O art. 50 exige informar a interação com IA (n.º 1), marcação legível por máquina pelo prestador (n.º 2) e divulgação de texto de interesse público (n.º 4). O selo é boa prática inspirada nele. | **Não.** O texto diz "exigência do AI Act, art. 50" (M4). |
| 15 | Qual seria a classificação de risco do sistema no AI Act e no PL 2338? | No AI Act, um sistema que é dispositivo médico com avaliação por terceiro seria de alto risco (art. 6º, n.º 1, Anexo I). Para o PL 2338, não há classificação vinculante porque o projeto não é lei (em 02/09/2026, "Aguardando Parecer" na Câmara). | **Não.** |
| 16 | Como a H3 testa a atribuição a raça se o prompt não informa raça? | Hoje não testa. É preciso incluir raça/etnia autodeclarada no prompt das vinhetas de H3 e medir menções causais. | **Não** (M5). |
| 17 | O risco "em 100 pessoas" vale para brasileiros? | Não se sabe: o PREVENT foi calibrado nos EUA, e a SBC reconhece essa limitação. | **Parcial.** Está na seção de limites, mas não na manchete (m1). |
| 18 | Os colegas anotadores são participantes de pesquisa? | Não, se forem membros da equipe e se os dados analisados forem os textos, não eles. Documentar. | **Parcial** (`auditoria-decisoes-autorais.md:34`, A13; falta o enquadramento ético). |

---

## 6. Verificações executadas

1. **Leitura integral** dos arquivos exigidos: `interface-design.md`, `decisoes.md` (D013, D015, D024, D025 e demais), `defesa-valor.md`, `auditoria-decisoes-autorais.md`, `who2024lmm.md`, `chan2025vies.md`, `Telas.jsx`, `TelaResultado.jsx`, `Resultado.jsx`, `perguntas.js`, `avaliacao.py`, `main.py`, `llm.py`, `prompt.py`. Também lidos: `App.jsx`, `api.js`, `index.html`, `Estrutura.jsx`, `resultado.css` (impressão), `sbc.py` (rótulos dos agravantes), `README.md`, `pendencias.md`, `proposta.md` (hipóteses), `justificativa-jade.md`, `perguntas-banca.md`, e os agentes JADE (`grep` de `System.out` e `userId`).
2. **Execução do gateway em processo** com `fastapi.testclient` ([script](anexos/etica/verificacao-gateway.py), [saída](anexos/etica/verificacao-gateway-saida.txt)). `llm.gerar` foi substituída por uma função falsa: **nenhum dado foi enviado a provedor real**. Resultados:
   - `POST /api/avaliacao` e `/api/avaliacao/explicacao` não geram nenhum log da aplicação (só a linha do cliente HTTP de teste);
   - prompt enviado ao provedor capturado literalmente, sem nome, com agravantes;
   - preflight CORS de origem arbitrária → `access-control-allow-origin: *`;
   - `POST /predict` com `user_id` = e-mail fictício → **o e-mail e todos os dados clínicos aparecem no log INFO**;
   - `POST /explanation/qualquer` sem autenticação → aceito (200);
   - rotas expostas: `/api/avaliacao`, `/api/avaliacao/explicacao`, `/predict`, `/explanation/{user_id}`, `/pending`, `/health`, `/docs`, `/redoc`, `/openapi.json`.
3. **Armazenamento no navegador:** `grep` por `localStorage|sessionStorage|indexedDB|cookie|analytics|gtag` em `frontend/src` e `index.html` → nenhuma ocorrência. A única chamada de console é `console.warn` com a mensagem de erro (`TelaResultado.jsx:24`), sem dados.
4. **Histórico:** `git grep user_id HEAD -- frontend` confirma que a interface anterior enviava o **nome** como `user_id`.
5. **Impressão:** `resultado.css:305-314` esconde o selo "Protótipo acadêmico" e o rodapé, e expande o "Como ler".
6. **Normas consultadas na fonte oficial** (transcrições no [anexo](anexos/etica/trechos-normativos.md)): LGPD (Planalto, texto compilado, baixado e lido), Res. CNS 510/2016 (BVS/MS), Res. CNS 674/2022 (PDF do CNS, lido na íntegra nos arts. 1º–5º e 26–32), Lei 14.874/2024 e Decreto 12.651/2025 (Planalto), RDC 657/2022 e RDC 751/2022 (AnvisaLegis), AI Act, arts. 2º, 6º e 50 (texto consolidado; o EUR-Lex não respondeu à consulta automatizada, então conferir no EUR-Lex antes de citar), situação do PL 2338/2023 (API de dados abertos da Câmara), Res. CD/ANPD 19/2024 (DOU).
7. **Termos dos provedores:** Gemini API Additional Terms (vigência 23/03/2026, atualizados em 28/04/2026), Groq Services Agreement (22/06/2026) e página "Your Data in GroqCloud".
8. **Não verificado** (por limitação de acesso nesta sessão): os termos de uso de dados do NHANES/NCHS, eventual guia da ANPD sobre tratamento para fins acadêmicos e eventuais normas já publicadas pela nova Instância Nacional de Ética em Pesquisa depois do Decreto 12.651/2025. **Conferir antes da defesa.**

---

## 7. Referências normativas e contratuais

- BRASIL. **Lei nº 13.709, de 14 de agosto de 2018** (LGPD), arts. 4º, 5º, 6º, 9º, 11, 12, 20, 33, 46. https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- BRASIL. **Lei nº 14.874, de 28 de maio de 2024** (pesquisa com seres humanos), arts. 2º, XXXIV, 61, 63. https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2024/lei/l14874.htm
- BRASIL. **Decreto nº 12.651, de 7 de outubro de 2025**, arts. 35, 37, 39. https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/decreto/D12651.htm
- BRASIL. **Lei nº 10.406/2002** (Código Civil), arts. 186 e 927. https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm
- CNS. **Resolução nº 466, de 12 de dezembro de 2012.** https://www.gov.br/conselho-nacional-de-saude/pt-br/atos-normativos/resolucoes/2012/resolucao-no-466.pdf
- CNS. **Resolução nº 510, de 7 de abril de 2016**, art. 1º e parágrafo único; art. 2º. https://bvsms.saude.gov.br/bvs/saudelegis/cns/2016/res0510_07_04_2016.html
- CNS. **Resolução nº 674, de 6 de maio de 2022** (DOU de 25/10/2022), arts. 2º e 26. https://www.gov.br/conselho-nacional-de-saude/pt-br/atos-normativos/resolucoes/2022/resolucao-no-674.pdf
- ANVISA. **RDC nº 657, de 24 de março de 2022** (SaMD), arts. 1º, 2º, 4º. https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&tipo=RDC&numeroAto=00000657&seqAto=000&valorAno=2022&orgao=RDC/DC/ANVISA/MS&codTipo=&desItem=&desItemFim=&cod_menu=1696&cod_modulo=134&pesquisa=true
- ANVISA. **RDC nº 751, de 15 de setembro de 2022** (classificação de dispositivos médicos), art. 2º, X; Anexo, Regra 11. https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&tipo=RDC&numeroAto=00000751&seqAto=000&valorAno=2022&orgao=RDC/DC/ANVISA/MS&codTipo=&desItem=&desItemFim=&cod_menu=1696&cod_modulo=134&pesquisa=true
- ANPD. **Resolução CD/ANPD nº 19, de 23 de agosto de 2024** (transferência internacional). https://www.in.gov.br/en/web/dou/-/resolucao-cd/anpd-n-19-de-23-de-agosto-de-2024-580095396
- UNIÃO EUROPEIA. **Regulamento (UE) 2024/1689** (AI Act), arts. 2º, 6º, 12, 13, 50, 113. https://eur-lex.europa.eu/eli/reg/2024/1689/oj (texto consolidado consultado em https://artificialintelligenceact.eu/article/50/ e https://artificialintelligenceact.eu/article/2/)
- SENADO FEDERAL / CÂMARA DOS DEPUTADOS. **PL 2338/2023**, situação em 02/09/2026: "Aguardando Parecer". https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=2487262
- GOOGLE. **Gemini API Additional Terms of Service** (vigência 23/03/2026). https://ai.google.dev/gemini-api/terms
- GROQ. **Groq Services Agreement** (22/06/2026). https://console.groq.com/docs/legal/services-agreement · **Your Data in GroqCloud.** https://console.groq.com/docs/your-data
- WORLD HEALTH ORGANIZATION. *Ethics and governance of artificial intelligence for health: guidance on large multi-modal models*. 2024. https://www.who.int/publications/b/70584 (orientação, não norma)
