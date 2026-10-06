---
titulo: Parecer da banca — engenharia do repositório
status: vigente
atualizado: 2026-09-29
resumo: Auditoria de engenharia de software do HEARTPREDICT (arquitetura, código, testes, reprodutibilidade, segurança, coerência doc × código, versionamento), com bugs confirmados por testes em anexos/engenharia/.
---

# Parecer de engenharia de software — HEARTPREDICT

**Avaliador(a):** Prof.(a) Dr.(a) em Engenharia de Software (qualidade, testes, arquitetura, reprodutibilidade de software de pesquisa)
**Objeto:** repositório `HEARTPREDICT` no estado de 29/09/2026, **com todas as mudanças ainda não commitadas** (HEAD = `3fdcc20`, de 19/07/2025).
**Material de apoio:** testes e saídas em [`anexos/engenharia/`](anexos/engenharia/).

---

## 1. Parecer resumido e veredito

O núcleo científico (`experimentos/piloto/prevent.py`, `sbc.py`, `renal.py`) é pequeno, legível, sem dependências externas, determinístico e **correto nas propriedades que importam**: reproduz os 6 valores publicados do PREVENT, e a atribuição de Shapley satisfaz eficiência e jogador nulo em 300 entradas aleatórias. Além disso, coincide com uma implementação independente por permutações (9! ordens) até 10⁻¹⁰ (anexo). A nova interface compila sem avisos de lint, e a documentação em `tcc/` é incomumente honesta sobre o que é transitório.

A engenharia *em volta* do núcleo, porém, ainda não está no nível de uma defesa:

1. **Nada do trabalho atual está versionado.** São 58 caminhos alterados, o último commit é de julho de 2025 e o piloto grava como "commit" um hash que não contém o código que gerou o resultado.
2. **Há bugs reais nas bordas**, todos reproduzidos por teste:
   - inconsistência de categoria no corte de 5% (a tela mostra "5,0% → baixo");
   - HTTP 500 com creatinina ≤ 0;
   - agravante feminino aplicado a homem;
   - LDL sem validação;
   - no endpoint antigo, o 408 é convertido em 500;
   - explicação do fluxo JADE injetável sem autenticação.
3. **A reprodutibilidade tem lacunas.** A versão de Python é contraditória, o `requirements.txt` do serviço antigo não instala no Python do ambiente, o README exige Node incompatível com o Vite instalado, `frontend/public/` é ignorado pelo `.gitignore` e não há script único.
4. **A segurança é básica demais para dados de saúde**: CORS `*`, dados clínicos em log, chave do Gemini na URL e envio a provedores gratuitos cujos termos permitem uso dos dados.

**Veredito:** **aprovável com ressalvas (correções obrigatórias antes da defesa).** Os problemas Críticos da seção 4 (C1–C4) precisam ser resolvidos e demonstrados. Nenhum deles invalida o núcleo de cálculo. Juntos, porém, impedem hoje que a banca reproduza os resultados do piloto a partir do repositório.

---

## 2. Notas por critério (0–10)

| Critério | Nota | Justificativa |
|---|---:|---|
| **Arquitetura e acoplamento** | **5,5** | O núcleo puro e sem estado é uma boa decisão, e o gateway fino também. Pesam contra: a importação por `sys.path.insert` de módulos com nomes genéricos (`prompt`, `llm`, `sbc`) em `avaliacao.py:20`; dois fluxos paralelos com contratos incompatíveis (`/predict` + JADE + XGBoost × `/api/avaliacao`); regra de categoria duplicada no cliente (`TelaResultado.jsx:35`); o gateway só sobe a partir de `app/` (`main.py:18`). A transição está documentada (D025), o que atenua. |
| **Qualidade de código** | **6,5** | O núcleo é enxuto (734 linhas no piloto), com docstrings que apontam a decisão (D009–D012) e sem dependências. Bugs de borda confirmados: B1–B8 (seção 4). O tratamento de erros mistura códigos (`ValueError` genérico em `renal.py:8`; erro de programação mascarado como 503 em `avaliacao.py:131-134`). O código legado (`main.py`) tem `except Exception` que engole `HTTPException`. |
| **Testes** | **5,0** | Existem 13 testes (7 no núcleo e 6 na API), todos passando e bem escolhidos (caso publicado, eficiência, recusas). Faltam: regras SBC (nenhum teste direto de `sbc.py`), `renal.py` contra valores de referência, `/explicacao`, `prompt.py`, `resumir.py` (IC de Wilson), `preanotar.py`, frontend (zero testes), JADE (zero testes, `pom.xml` declara JUnit sem nenhum teste). Não há CI nem medição de cobertura. |
| **Reprodutibilidade** | **4,0** | Pontos positivos: piloto determinístico (`--seco` idempotente, hashes iguais antes/depois), versões fixadas no gateway, `package-lock.json` presente, metadados de execução gravados. Pontos negativos: registro de commit sem valor (C1); Python 3.11 × 3.8 (M5); `requirements.txt` de 91 linhas que não instala em 3.8 (M6); Node ≥ 18 × Vite 7 (M7); `public/` ignorado (C3); sem script único; temperatura 0,7 fixa no código. |
| **Segurança básica** | **4,5** | `.env` e `tcc/01-literatura/textos/` estão corretamente ignorados, a interface não coleta identificação e o texto do LLM é renderizado como texto (sem XSS). Pesam contra: CORS `*`; dados de saúde em log (`main.py:138,237`); chave na URL (`llm.py:242`, `GeminiClient.java:350`); endpoint de injeção e endpoint de depuração expostos; bind em `0.0.0.0` no fluxo antigo; envio de dados de saúde a planos gratuitos sem registro de base legal. |
| **Coerência documentação × código** | **6,0** | Na maior parte, o README e `tcc/` descrevem honestamente a transição. Divergências: "4 agentes: Gerenciador, Classificador, Julgador, Explicador" × D019 (Entrada, Classificador, Explicador, Verificador); "Funcional" × `pendencias.md:67` ("ainda não verificado"); Ant Design 5.26 listado em `tecnologias.md:48`, mas removido do `package.json`; React 19.1/Vite 7.0 declarados × 19.3/7.3.6 instalados; Node ≥ 18 × Vite 7; `trigger/` descrito como teste, mas só exercita o fluxo antigo. |
| **Versionamento** | **2,0** | O último commit é de 19/07/2025. Todo o trabalho de 29/09/2026 está fora do git: 11 caminhos não rastreados (incluindo `experimentos/`, `tcc/` e `avaliacao.py`), 14 modificados e 33 removidos/renomeados, com área de preparação parcial (D/RM *staged* misturados com M *unstaged*). Artefatos de execução versionados (`jade-agents/APDescription.txt` com IP privado e hostname, `.deps_installed`, `jade_cert.cer`, modelos `.joblib`, CSV de 2,9 MB). Não há tags nem LICENSE. |

**Média simples: 4,8/10.** O núcleo mereceria nota maior; a média é puxada pelo versionamento e pela reprodutibilidade, que são corrigíveis em poucos dias.

---

## 3. Pontos fortes

- **Núcleo correto e verificável.**
  - `test_prevent.py` reproduz os 6 valores do artigo (DCVA, DCV total e IC, com e sem tabagismo).
  - Meus testes de propriedade confirmaram eficiência, jogador nulo e equivalência com Shapley por permutações ([`test_nucleo_propriedades.py`](anexos/engenharia/test_nucleo_propriedades.py)).
- **Recusa em vez de suposição.** O núcleo e a API recusam fora da faixa de derivação, fora do escopo (DCV prévia, diabetes) e dado ausente, com códigos estáveis (`fora_da_faixa`, `fora_do_escopo`, `dado_ausente`), conforme `avaliacao.py:52-84`.
- **Validação por faixa correta nos limites.** A varredura dos limites inclusivos e de ±1 passo das 5 variáveis retornou 200/422 como esperado ([`test_api_varredura.py::test_limites`](anexos/engenharia/test_api_varredura.py)). NaN em variável do modelo é recusado.
- **Piloto bem instrumentado para um TCC.** Grava modelo, temperatura, `max_tokens`, versão e hash do prompt e carimbo de tempo por chamada (`rodar_piloto.py:63-71`), além de manter `resultados/gabarito.json` e `prompt_exemplo.txt` versionáveis. O modo `--seco` é determinístico.
- **Zero dependências no núcleo.** O cliente LLM usa só `urllib`, o que elimina uma classe inteira de problemas de ambiente.
- **Frontend limpo.** Sem biblioteca de componentes, lint sem avisos, build de 254 kB (80 kB gzip). A vírgula decimal é tratada (`validacao.js:7-12`), e o estado fica só na memória, sem `localStorage` (App.jsx:10).
- **Documentação do raciocínio.** O registro de decisões (D001–D025), as pendências com data e o critério de detalhamento das tecnologias (D022) são práticas de nível acima do esperado para graduação.
- **Honestidade na interface.** A explicação é rotulada como IA e "ainda não verificada" (`Resultado.jsx:127-131`), coerente com D025.

---

## 4. Problemas

Legenda: **C** = Crítico (bloqueia a defesa ou a reprodutibilidade dos resultados), **M** = Maior, **m** = Menor. As entradas com teste marcadas **[confirmado]** foram reproduzidas em `anexos/engenharia/`.

### Críticos

**C1 — Trabalho não versionado e commit do piloto sem valor.**

- *Evidência:*
  - `git status`: 11 `??`, 31 `D`, 14 `M`, 2 `RM`.
  - `git log -1` = `3fdcc20` (2025-07-19).
  - `rodar_piloto.py:24-29` grava `git rev-parse --short HEAD` sem checar árvore suja.
- *Impacto:* qualquer execução do piloto hoje gravaria `commit: 3fdcc20`, um commit em que `experimentos/` **não existe**. A rastreabilidade prometida no checklist (`tecnologias.md:52`) fica falsa, e uma perda de disco apaga todo o TCC.
- *Correção:*
  1. Commits atômicos imediatos (núcleo, gateway, frontend, `tcc/`).
  2. Em `commit_atual()`, usar `git describe --always --dirty` e **recusar** a execução com árvore suja (ou gravar também o `git diff` junto ao `.jsonl`).
  3. Criar uma tag por execução do experimento.

**C2 — Inconsistência de categoria no corte de 5% (e 20%) [confirmado].**

- *Evidência:*
  - `sbc.py:42` compara o risco **não arredondado**; `gabarito.py:26` e a regra em `sbc.py:48` exibem 1 casa.
  - Para homem de 55 anos, CT 256, HDL 44, PAS 140, TFGe 95, o risco é 4,951%. A API retorna `risco_pct: 5.0`, `categoria: "baixo"` e a regra literal `"escore PREVENT 5,0% → baixo (Tabela 4.1)"`. O caso foi confirmado também no servidor em execução (127.0.0.1:8000).
  - Com um agravante, o frontend (`TelaResultado.jsx:35`) recalcula a categoria do escore com o valor arredondado e diz "Pelo cálculo, o risco seria **intermediário**", enquanto o servidor registra "baixo → intermediário".
- *Impacto:*
  - A tela contradiz a própria escala ("baixo = menos de 5%").
  - **O prompt do experimento contém a contradição** "5,0% → baixo", o que pode *induzir* no LLM exatamente o erro de exatidão ou categoria que o TCC mede e contaminar H2.
  - A vinheta V06 ("logo abaixo do corte", 4,9%) está a 0,05 p.p. desse efeito.
- *Correção:*
  - Definir uma única política: classificar sobre o valor exibido **ou** exibir com precisão suficiente (ex.: "4,95%") perto do corte.
  - Enviar `categoria_do_escore` pronta do servidor e remover a duplicação no cliente.
  - Adicionar teste de regressão (o do anexo serve).

**C3 — `frontend/public/` está ignorado pelo git.**

- *Evidência:* `git check-ignore -v frontend/public/marca.svg` → `.gitignore:233:public`, regra herdada do Gatsby. `index.html:8` referencia `/marca.svg`.
- *Impacto:* um clone limpo perde o ícone/marca. Outros arquivos colocados em `public/` também sumiriam silenciosamente.
- *Correção:* adicionar `!frontend/public/` ou remover a regra `public`. Revisar as demais regras genéricas do `.gitignore` (`lib/`, `dist`, `*.json` em `*/data/`) herdadas de modelos.

**C4 — Não há como reproduzir o ambiente a partir do README.**

- *Evidência:*
  - O README pede Python ≥ 3.11 (`README.md:32`), mas o piloto diz 3.8+ (`experimentos/piloto/README.md:22`) e todos os testes foram rodados em 3.8.11 (pyenv); `tecnologias.md:40` diz "confirmar a usada".
  - O `requirements.txt` do serviço antigo fixa `matplotlib==3.10.3` e `scikit-image==0.25.2`, que exigem Python ≥ 3.10, e `numpy==1.25.2`/`pandas==2.1.4`, que exigem ≥ 3.9 (metadados *Requires-Python* no PyPI). Logo, não instala no 3.8 do ambiente.
  - O Vite 7.3.6 instalado exige `node ^20.19.0 || >=22.12.0` (`node_modules/vite/package.json`), mas o README diz Node ≥ 18.
  - O JADE exige Java 17, e o ambiente tem OpenJDK 11.0.21 e nenhum Maven. `pendencias.md:67` admite que nunca foi compilado.
  - Não há script único (`pendencias.md:70`).
- *Impacto:* a banca não consegue subir o sistema nem rodar o piloto de forma determinística.
- *Correção:*
  - Fixar uma versão (sugiro 3.11), `.python-version` e `engines` no `package.json`.
  - Criar `requirements.txt` mínimo por componente.
  - Oferecer `Makefile` ou `scripts/reproduzir.sh` com alvos `teste`, `piloto-seco`, `api` e `interface`.
  - Adicionar `.env.example` com as variáveis (`LLM_PROVEDOR`, `LLM_MODELO`, `GROQ_API_KEY`, `GEMINI_API_KEY`, `GEMINI_MODEL`).

### Maiores

**M1 — Creatinina ≤ 0 gera HTTP 500 [confirmado].**

- *Evidência:* `renal.py:8-9` levanta `ValueError` genérico, e `avaliacao.py:70` não o captura. `curl` no servidor vivo retornou `Internal Server Error`, HTTP 500.
- *Impacto:* quebra o contrato de erros (`{codigo, mensagens}`). O cliente só se protege porque valida a faixa 0,3–15 (`perguntas.js:150`), e o servidor não tem essa faixa.
- *Correção:* `creatinina: Optional[confloat(gt=0)]`, faixa no servidor e captura com `_recusar("fora_da_faixa", ...)`.

**M2 — Agravante feminino aplicado a homem [confirmado em 3 camadas].**

- *Evidência:*
  - Na interface, após marcar "Situações da saúde da mulher" e trocar o sexo pela revisão, `App.jsx:165-176` grava só o novo sexo. `montarEntrada` (`api.js:20`) envia `fator_especifico_mulher`, e a revisão exibe a opção feminina para um homem.
  - O servidor (`avaliacao.py:76`) e o núcleo (`sbc.py:50`) aceitam o agravante: homem de 35 anos vai de baixo para intermediário.
- *Impacto:* classificação clínica errada, silenciosa.
- *Correção:*
  - No servidor, rejeitar (422) `fator_especifico_mulher` quando `sexo == "masculino"`.
  - No cliente, ao mudar o sexo, refiltrar `agravantes` com `opcoesVisiveis` ou invalidar a resposta e reperguntar.
  - Adicionar teste em ambas as camadas.

**M3 — LDL sem validação no servidor [confirmado].**

- *Evidência:* `EntradaAvaliacao.ldl: Optional[float]` (`avaliacao.py:48`). LDL −50, 0, 5000 e 239 (com CT 240 e HDL 55, impossível) retornam 200; LDL 5000 classifica como "alto". `ldl: NaN` é aceito em `/api/avaliacao` (200) e em `/explicacao` vira 503 "cannot convert float NaN to integer" (`prompt.py:39`).
- *Impacto:* dados impossíveis alteram a categoria. Um erro de programação é reportado como "LLM indisponível".
- *Correção:*
  - Faixa 20–400 no servidor, igual ao cliente.
  - Checagens cruzadas LDL < CT − HDL e HDL < CT.
  - Construir o prompt **fora** do `try` que converte exceções em 503.

**M4 — Agravantes desconhecidos descartados em silêncio [confirmado].** `avaliacao.py:76` e `sbc.py:50` filtram, então um erro de digitação do cliente (`historia_familiar_PREMATURA`) retorna 200 sem o agravante. No núcleo, `prompt.py:52` faz `AGRAVANTES_PT[a]` sem filtro, e um agravante inválido gera `KeyError` (teste no anexo). *Correção:* `List[Literal[...]]` no modelo Pydantic e um único ponto de filtragem.

**M5 — Versão de Python contraditória e `typing_extensions` implícito.** `avaliacao.py:18` importa `typing_extensions`, que não está no `requirements.txt` do gateway (chega como dependência transitiva do Pydantic). O Python 3.8 está fora de suporte desde outubro de 2024 (devguide). *Correção:* adotar 3.11, usar `typing.Literal` e declarar tudo o que é importado.

**M6 — `ai-services/chronic-risk-service/requirements.txt` é um `pip freeze` (91 linhas).** Inclui `matplotlib`, `scikit-image` e outros que o código não importa (imports reais: fastapi, pydantic, joblib, numpy, pandas, uvicorn, e xgboost/sklearn via modelo). `trigger/requirements.txt` também traz `slixmpp`, `pyjabber`, `SQLAlchemy`, `alembic` e outros para um script que só usa `requests`. É exatamente o que `tecnologias.md:62` diz para não fazer. *Correção:* enxugar agora, e não "junto com a troca para o PREVENT".

**M7 — Acoplamento por `sys.path` e módulo de pesquisa servindo produção.**

- *Evidência:*
  - `avaliacao.py:20` insere `experimentos/piloto` na **posição 0** do `sys.path`. Os nomes `prompt`, `llm`, `sbc`, `renal` e `gabarito` passam a sombrear qualquer pacote homônimo instalado.
  - `main.py:18` usa `from avaliacao import ...`, então `uvicorn app.main:app` a partir de `backend-gateway/` falha, e o gateway só roda com cwd/argv em `app/`.
  - O mesmo `prompt.VERSAO = "piloto-v1"` e a temperatura 0,7 (`avaliacao.py:132`) servem à interface e ao experimento. Se o prompt mudar para o experimento, a interface muda junto, sem registro.
- *Correção:*
  - Criar um pacote `heartpredict_nucleo/` (layout `src/`, com `pyproject.toml`) instalado em modo editável nos dois consumidores.
  - Configurar temperatura e versão do prompt por variável de ambiente e devolvê-las na resposta de `/explicacao`.

**M8 — Endpoint antigo `/predict` com defeitos de controle e de segurança [confirmado].**

- *Evidência:*
  - `main.py:178` (`except Exception`) captura a `HTTPException(408)` lançada em `main.py:160` e devolve **500** "Erro interno do servidor: 408: Timeout...".
  - `POST /explanation/{user_id}` (`main.py:232`) aceita qualquer texto sem autenticação e o entrega ao usuário que está aguardando. O teste injetou "forjado".
  - `GET /pending` (`main.py:248`) lista IDs aguardando.
  - `uvicorn.run(host="0.0.0.0")` (`main.py:257`).
  - `pending_explanations` indexado por `user_id` colide com requisições concorrentes do mesmo usuário.
- *Correção:* se `/predict` segue vivo até a migração, adicionar `except HTTPException: raise`, segredo compartilhado com o JADE, `conversation-id` por requisição (D021), remover `/pending` e fazer bind em 127.0.0.1. Melhor ainda, removê-lo já (`pendencias.md:84`).

**M9 — Dados de saúde em log e enviados a terceiros sem registro de base legal.**

- *Evidência:*
  - `main.py:120,138` registram dados do paciente em INFO, e `main.py:237` registra a explicação completa.
  - `GeminiClient.java:363-365` imprime corpos de erro.
  - `/explicacao` envia idade, sexo, lipídios, PA, tabagismo e TFGe a Groq/Gemini. `TelaInicio` informa isso ao usuário (bom), mas os termos do Gemini API para serviços **não pagos** permitem o uso do conteúdo para melhorar produtos.
- *Impacto:* dado de saúde é **dado pessoal sensível** (LGPD, art. 5º, II), ainda que sem identificação direta. A combinação idade + sexo + exames reduz o anonimato. Em teste com pessoas (interface-design §8), isso precisa passar pelo CEP.
- *Correção:*
  - Registrar só IDs e códigos de erro.
  - Documentar no TCC os termos de cada provedor na data de uso.
  - No teste de usabilidade, usar só dados fictícios.

**M10 — CORS `allow_origins=["*"]` com `allow_methods=["*"]`.**

- *Evidência:* `main.py:26-32`. O preflight de `Origin: https://evil.example` retornou `access-control-allow-origin: *`.
- *Impacto:* qualquer site aberto no navegador do avaliador pode consumir a API local, incluindo `/explicacao`, que gasta a cota do LLM.
- *Correção:* lista explícita de origens (`http://localhost:5173` e `http://localhost:4173`) via variável de ambiente, e métodos `GET`/`POST`.

**M11 — Chave de API do Gemini na query string.** `llm.py:242` e `GeminiClient.java:350` usam `?key=`. URLs aparecem em logs de proxy, histórico e rastreamentos de erro. A API aceita o cabeçalho `x-goog-api-key`. *Correção:* mover a chave para o cabeçalho.

**M12 — Cobertura de testes ausente onde há lógica de decisão.**

- *Evidência:* nenhum teste para `sbc.categoria` (cortes, agravante em "alto", LDL 160/189/190), `renal.tfge_ckd_epi_2021` (contra valores conhecidos do CKD-EPI 2021), `resumir.wilson`, `preanotar.checar`, `/explicacao`, frontend e JADE.
- *Correção:* ver a lista de testes propostos no fim desta seção.

### Menores

- **m1 — Arredondamento bancário no pictograma.** `avaliacao.py:100` usa `round()`: 2,5% vira 2 pessoas e 3,5% vira 4, e 0,5% vira "menos de 1". Usar `decimal` com `ROUND_HALF_UP` ou `math.floor(x + 0.5)`.
- **m2 — `%d` trunca valores decimais no prompt.** `prompt.py:32-39` imprime idade, CT, HDL, PAS, TFGe e LDL com `%d`: HDL 55,9 vira "55", e LDL 189,6 aparece como "189" com a regra "≥ 190 → alto" não disparada (correto, mas confuso). Idade 54,9 vira "54" (teste no anexo).
- **m3 — Formatos de erro inconsistentes.** A validação do Pydantic devolve `detail` como lista, e as recusas de domínio devolvem `{codigo, mensagens}`. `api.js:15` cobre os dois só parcialmente: lista vira "Erro 422.".
- **m4 — `fetch` sem timeout nem cancelamento.** Em `api.js:5`, somado às retentativas de `llm._post` (5 tentativas com espera 5+10+20+40 s e *timeout* de 120 s), uma explicação pode levar ≈ 10 min. Em `TelaResultado.jsx:29-31`, o `StrictMode` duplica a chamada ao LLM em desenvolvimento (efeito sem `AbortController`).
- **m5 — Efeito colateral durante a renderização.** Em `App.jsx:217-218`, `ir()` altera `location.hash` dentro do render.
- **m6 — `llm._post` captura só `HTTPError`.** `URLError` e `socket.timeout` saem sem retentativa (`llm.py:47-55`). Se a resposta do Gemini não trouxer `candidates` (bloqueio), o erro é `KeyError`.
- **m7 — `rodar_piloto.py` frágil.** Sobrescreve `resultados/gabarito.json` a cada execução, inclusive com `--vinhetas` parcial, o que quebra `preanotar.py` para `.jsonl` antigos. `--seco` com filtro vazio gera `IndexError` (`gabs[0]`).
- **m8 — `resumir.py` inconsistente com a própria docstring.** A docstring diz "unidade de análise é a vinheta", mas a regra de decisão usa a taxa **por resposta** (`resumir.py:39`), e o IC de Wilson trata as 3 repetições como independentes. Linhas com erro de API são descartadas sem aviso.
- **m9 — Mistura de idiomas.** O código novo usa PT (`avaliar`, `risco_pct`) e o legado usa EN (`PatientData`, `riskScore`); há chaves do JSON de coeficientes em EN (`female_ascvd`) e o pacote Java se chama `br.com.yourproject` (*placeholder*). É aceitável, mas vale padronizar o código novo em PT e declarar a convenção.
- **m10 — `pom.xml` com resíduos.** O plugin `exec-maven-plugin` aponta para `AgenteHelloWorld`, que não existe, e o *artifactId* é `cardiac-alert-jade`.
- **m11 — Artefatos de execução versionados.** `jade-agents/APDescription.txt` e `MTPs-Main-Container.txt` (IP 172.26.18.120, host `LOQ-Gabriel`), `jade_cert.cer`, `.deps_installed`, `frontend/README.md` (template do Vite).
- **m12 — `indexar.py validar` é silencioso em caso de sucesso.** Imprimir "0 erros em N fichamentos" ajuda na evidência.
- **m13 — Temperatura 0,7 fixa no código.** Está em `avaliacao.py:132` e `GeminiClient.java:69`. D-pendente (`pendencias.md:71`) e está em tensão com a literatura citada no próprio `tecnologias.md:21` (temperatura 0).

### Testes que faltam (propostos)

1. **`sbc.categoria` (tabela de decisão):**
   - risco 4,99 → baixo e 5,00 → intermediário;
   - agravante em "alto" não sobe;
   - LDL 159/160/189/190 × categoria de partida;
   - agravante + LDL ≥ 190 juntos;
   - diabetes → `ForaDoEscopo`.
2. **`renal`:** 3–4 valores de referência do CKD-EPI 2021 (Inker 2021) ou do `preventr::calc_egfr`, por sexo e com creatinina abaixo e acima de κ.
3. **PREVENT contra `preventr`:** uma grade de ≥ 100 perfis exportada do R, com tolerância de 10⁻⁶. O teste atual cobre um único paciente.
4. **Propriedades de Shapley:** já escritas no anexo. Incorporar ao projeto (eficiência, jogador nulo, equivalência com permutações).
5. **API:** a varredura de faixas do anexo mais contrato de erro, `/explicacao` com dublê de LLM (sucesso, erro de rede, sem configuração) e recusa de agravante incompatível com o sexo.
6. **`prompt.construir`:** teste *golden* (snapshot) de `prompt_exemplo.txt`. Mudou o texto, mudou `VERSAO`.
7. **`resumir.wilson`:** valores conhecidos (k=0, k=n, k=5 com n=20).
8. **Frontend:** Vitest para `validacao.js`/`api.js` (o anexo mostra que a lógica é testável) e 1 teste de fluxo com Testing Library ou Playwright, incluindo a troca de sexo após o agravante.
9. **JADE:** ao menos 1 teste de integração do protocolo quando for reescrito (D021).
10. **CI:** um GitHub Actions rodando 1, 3, 5 e 8 em cada *push*.

---

## 5. Perguntas da banca

| # | Pergunta | Resposta esperada | O projeto responde hoje? |
|---|---|---|---|
| 1 | Qual commit gerou os resultados do piloto que serão apresentados? Consigo fazer *checkout* e obter o mesmo `gabarito.json`? | Hash de um commit que contém `experimentos/`, gravado no `.jsonl` e com árvore limpa | **Não.** Nada está commitado, e `commit_atual()` grava `3fdcc20` (C1) |
| 2 | Como você garante que sua implementação do PREVENT está correta além do único caso publicado? | Comparação com `preventr` em grade de perfis, conferência contra a Tabela S12 original | **Parcial.** 6 valores publicados (`test_prevent.py`); coeficientes "PROVISÓRIOS" (`coeficientes...json:_origem.status`; `pendencias.md:15`) |
| 3 | Por que Shapley exato e não amostrado? Como sabe que a implementação está certa? | 9 variáveis → 512 coalizões, custo trivial; testes de eficiência e comparação com definição por permutações | **Parcial.** Eficiência testada (`test_prevent.py:31`); jogador nulo e permutações só no anexo da banca |
| 4 | Um paciente com risco 4,95% é baixo ou intermediário? O que a tela e o prompt mostram? | Política única de arredondamento e categoria, com teste | **Não.** Mostra "5,0% → baixo" (C2) |
| 5 | O que acontece se o usuário marcar um agravante feminino e depois mudar o sexo? | A resposta é invalidada no cliente e recusada no servidor | **Não** (M2) |
| 6 | Por que o gateway importa o núcleo por `sys.path`? Qual é o plano e o prazo? | Transitório (D025); pacote instalável com versão | **Parcial.** Documentado em `pendencias.md:82`, sem prazo |
| 7 | Quais versões exatas de Python, Node, Java e dependências você usou? | Tabela com versões *verificadas* e arquivo de ambiente | **Não.** 3.11 × 3.8; Node ≥ 18 × Vite 7; Java 17 × 11 no ambiente (C4) |
| 8 | Como alguém reproduz o experimento do zero em uma máquina limpa? | Um comando: `make reproduzir` ou script, a partir de `.env.example` | **Não.** `pendencias.md:70` |
| 9 | Que dados de saúde saem do seu sistema, para quem, e com qual base? | Lista de campos, provedores, termos vigentes, ausência de identificação, CEP para testes com pessoas | **Parcial.** Aviso ao usuário em `Telas.jsx` ("Seus dados"); sem análise de termos nem LGPD no `tcc/` |
| 10 | Por que CORS `*`? Quem mais pode chamar sua API? | Origens explícitas; a API é local | **Não** (M10) |
| 11 | Como a temperatura do LLM foi escolhida? Ela é a mesma na interface e no experimento? | Valor justificado, configurável e registrado | **Parcial.** Registrado no piloto (`rodar_piloto.py:63`); fixo em 0,7 no gateway; `pendencias.md:71` em aberto |
| 12 | O README diz que o JADE é "funcional". Você compilou e executou o fluxo de ponta a ponta? Mostre o log | `mvn package` e execução registrados | **Não.** `pendencias.md:67`: "ainda não verificado" |
| 13 | Quantos testes existem e o que eles cobrem? Há CI? | Números por componente, lacunas assumidas | **Parcial.** 7 + 6 testes; sem CI; sem teste de SBC nem de frontend |
| 14 | Se a Groq ou o Gemini desligarem o modelo usado, o que é preservado para auditoria? | ID do modelo, data, prompt e hash, resposta bruta e uso | **Sim** para o piloto (`rodar_piloto.py:63-76`); **não** para a interface (não há registro) |
| 15 | O endpoint antigo `/predict` ainda é necessário? Por que dois fluxos coexistem? | Plano de remoção datado; um só contrato | **Parcial.** `pendencias.md:84` |

---

## 6. Verificações executadas

Ambiente: Linux 6.2, Python 3.8.11 (pyenv; `/usr/bin/python3.11` também disponível), Node 22.17.0, OpenJDK 11.0.21, sem Maven. Os servidores já estavam em 127.0.0.1:8000 (gateway) e 127.0.0.1:4173 (frontend).

| Comando | Resultado |
|---|---|
| `cd experimentos/piloto && python3 -m unittest test_prevent -v` | `Ran 7 tests ... OK` (3.8.11; também OK em 3.11) |
| `cd backend-gateway/app && <venv-gw>/bin/python -m unittest discover -s ../tests -v` | `Ran 6 tests ... OK` (fastapi 0.108.0, pydantic 2.5.3, starlette 0.32.0.post1) |
| `cd frontend && npx eslint src` | sem saída, código 0 |
| `npx vite build --outDir <scratchpad>` | `✓ 45 modules transformed`; JS 253,87 kB (79,70 kB gzip); **vite v7.3.6** |
| `python3 tcc/tools/indexar.py validar` | sem saída, código 0 |
| `python3 rodar_piloto.py --seco` | 24 vinhetas (V01 0,3% baixo … V16 24,9% alto); SHA-256 de `gabarito.json` e `prompt_exemplo.txt` **idênticos** antes e depois (determinístico) |
| `git check-ignore -v frontend/public/marca.svg` | `.gitignore:233:public` (C3) |
| `git status --porcelain \| awk '{print $1}' \| sort \| uniq -c` | `11 ??`, `31 D`, `14 M`, `2 RM` (C1) |
| `curl -X POST :8000/api/avaliacao` com `creatinina: 0` | `Internal Server Error`, HTTP 500 (M1) |
| `curl -X OPTIONS` com `Origin: https://evil.example` | `access-control-allow-origin: *` (M10) |
| `curl` com homem, 55 anos, CT 256, HDL 44, PAS 140, TFGe 95 + história familiar | `5.0 intermediário ['escore PREVENT 5,0% → baixo (Tabela 4.1)', 'agravante(s): ... de baixo para intermediário']` (C2) |
| `node -e` (engines) | vite 7.3.6 `{"node":"^20.19.0 \|\| >=22.12.0"}`; react 19.3.0 (M/doc) |
| **Anexo:** `python3 -m unittest discover -s tcc/05-banca/anexos/engenharia -p "test_nucleo_*.py" -v` | `Ran 13 tests in 8.7s OK`. Risco mínimo na faixa ≈ 0,034% e máximo ≈ 41,0%; caso-limite 4,9510% → "5,0" e "baixo". Saída: [`saida_test_nucleo_propriedades.txt`](anexos/engenharia/saida_test_nucleo_propriedades.txt) |
| **Anexo:** `cd backend-gateway/app && <venv-gw>/bin/python -m unittest discover -s ../../tcc/05-banca/anexos/engenharia -p "test_api_*.py" -v` | `Ran 18 tests OK`. Os testes `test_BUG_*` passam *porque o bug existe*: 500 com creatinina 0 e −1; agravante feminino em homem; LDL −50/5000 aceito; ldl NaN → 200 e depois 503 "cannot convert float NaN to integer"; `/predict` 408 → 500; injeção em `/explanation/vitima`. Saída: [`saida_test_api_varredura.txt`](anexos/engenharia/saida_test_api_varredura.txt) |
| **Anexo:** `cd frontend && npx esbuild ../tcc/05-banca/anexos/engenharia/teste_frontend_validacao.mjs --bundle --platform=node --format=esm '--define:import.meta.env={}' --outfile=<scratchpad>/teste.mjs && node <scratchpad>/teste.mjs` | `10 casos ok`. Achados: agravante feminino enviado com `sexo=masculino`; categoria do escore recalculada com valor arredondado; LDL > CT aceito. Saída: [`saida_teste_frontend.txt`](anexos/engenharia/saida_teste_frontend.txt) |

Não foi possível executar: `mvn package` do JADE (sem Maven, Java 11 < 17 exigido) e instalação do `requirements.txt` do serviço antigo (incompatível com Python 3.8, conforme o *Requires-Python* das versões fixadas). Nenhum LLM foi chamado. Nenhum arquivo do projeto foi modificado: `rodar_piloto.py --seco` reescreveu `resultados/` com conteúdo byte a byte idêntico.

---

## 7. Referências

- WILSON, G. et al. **Good enough practices in scientific computing.** *PLOS Computational Biology*, 13(6): e1005510, 2017. https://doi.org/10.1371/journal.pcbi.1005510
- SANDVE, G. K. et al. **Ten simple rules for reproducible computational research.** *PLOS Computational Biology*, 9(10): e1003285, 2013. https://doi.org/10.1371/journal.pcbi.1003285
- THE TURING WAY COMMUNITY. **The Turing Way: a handbook for reproducible, ethical and collaborative research.** https://book.the-turing-way.org/
- WIGGINS, A. **The Twelve-Factor App** — III. Config; II. Dependencies. https://12factor.net/config · https://12factor.net/dependencies
- OWASP. **API Security Top 10 — 2023** (API2 Broken Authentication; API8 Security Misconfiguration). https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- OWASP. **Logging Cheat Sheet** (dados que não devem ser registrados). https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- MDN. **Cross-Origin Resource Sharing (CORS).** https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
- GOOGLE. **Gemini API — Using Gemini API keys** (cabeçalho `x-goog-api-key`). https://ai.google.dev/gemini-api/docs/api-key
- GOOGLE. **Gemini API Additional Terms of Service** (uso de dados em serviços não pagos). https://ai.google.dev/gemini-api/terms
- BRASIL. **Lei nº 13.709/2018 (LGPD)**, art. 5º, II, e art. 11. https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
- PYTHON SOFTWARE FOUNDATION. **Status of Python versions.** https://devguide.python.org/versions/
- PYTHON PACKAGING AUTHORITY. **src layout vs flat layout.** https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
- VITE. **Getting Started** (requisito de versão do Node.js). https://vite.dev/guide/
- REACT. **`<StrictMode>`** (efeitos executados duas vezes em desenvolvimento). https://react.dev/reference/react/StrictMode
- FASTAPI. **Testing.** https://fastapi.tiangolo.com/tutorial/testing/
- GIT. **git-describe** (`--dirty`). https://git-scm.com/docs/git-describe
- LUNDBERG, S. M.; LEE, S.-I. **A unified approach to interpreting model predictions.** NeurIPS 2017. https://arxiv.org/abs/1705.07874
- KHAN, S. S. et al. **Development and validation of the American Heart Association's PREVENT equations.** *Circulation*, 149:430–449, 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC10910659/
