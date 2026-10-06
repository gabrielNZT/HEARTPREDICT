# Base de conhecimento do TCC

Tudo o que é construído sobre o TCC (leituras, decisões, argumentos) fica aqui, em Markdown versionado com o código.

**Comece por [INDEX.md](INDEX.md)**, gerado automaticamente com o índice de tudo, a lista de leituras e as evidências citáveis.

## Estrutura

```
tcc/
├── INDEX.md                  ← gerado; não editar à mão
├── 00-projeto/
│   ├── proposta.md           ← documento-mestre (tese, hipóteses, método, escopo)
│   ├── decisoes.md           ← registro de decisões (D###) e pendentes (P###)
│   └── pendencias.md         ← verificações e leituras a fazer
├── 01-literatura/
│   ├── fichamentos/<chave>.md  ← um arquivo por fonte
│   ├── sintese-leitura.md      ← o que a leitura mudou no projeto
│   ├── referencias.bib         ← gerado a partir dos fichamentos
│   └── textos/                 ← textos completos baixados (fora do git)
├── 02-argumentacao/
│   ├── defesa-valor.md
│   ├── perguntas-banca.md
│   └── trabalhos-relacionados.md
└── tools/indexar.py
```

## Comandos

```bash
python3 tcc/tools/indexar.py              # regenera INDEX.md e referencias.bib
python3 tcc/tools/indexar.py validar      # só valida os fichamentos
python3 tcc/tools/indexar.py buscar PREVENT   # busca em toda a base (ignora acentos e maiúsculas)
```

## Como adicionar um fichamento

1. Crie `01-literatura/fichamentos/<chave>.md`. A chave segue `sobrenomeAAAApalavra` (ex.: `jin2025agentmd`) e **o nome do arquivo deve ser igual à chave**.
2. Front-matter obrigatório:

```yaml
---
chave: sobrenome2025palavra
titulo: Título completo
autores: [Nome Sobrenome, Nome Sobrenome, et al.]
ano: 2025
veiculo: Nome da revista ou evento
tipo_bib: article          # article | inproceedings | misc
doi: 10.xxxx/yyyy           # opcional
volume: 16                  # opcional
paginas: 100-110            # opcional
url: https://...
temas: [tema-a, tema-b]
leitura: completa          # completa | parcial | resumo | pendente
lido_em: 2026-09-29
relevancia: alta           # central | alta | media | baixa
---
```

3. Seções recomendadas: Referência · Problema · Método · Resultados · Limitações declaradas · Leitura crítica · Relação com o meu TCC · **Dados citáveis**.
4. Na seção `## Dados citáveis`, cada item deve seguir o formato `- [C1] afirmação (localização no texto: seção, tabela, figura)`. Esses itens aparecem no INDEX como evidências prontas para citar.
5. Rode `python3 tcc/tools/indexar.py`.

## Regras de honestidade da base
- `leitura: completa` só quando o texto integral foi lido. Resumo lido = `resumo`.
- Metadados que vieram de memória ou de fonte secundária levam **(verificar)** e entram em `pendencias.md`.
- Nunca cite um número de um fichamento com `leitura: resumo` sem conferir o original.
- Decisões nunca são apagadas: marque como substituídas em `decisoes.md`.

## Textos completos
`01-literatura/textos/` guarda os textos baixados para consulta local e **não é versionado** (direitos autorais variam por artigo).
