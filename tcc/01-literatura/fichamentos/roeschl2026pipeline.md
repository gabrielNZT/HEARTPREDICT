---
chave: roeschl2026pipeline
titulo: Development of an LLM pipeline exceeding physician-documented cardiovascular risk scores under routine clinical conditions
autores: [Tobias Roeschl, Marie Hoffmann, Axel Unbehaun, Henryk Dreger, Gerhard Hindricks, Volkmar Falk, Ran Balicer, Radu Tanacli, Felix Hohendanner, Alexander Meyer]
ano: 2026
veiculo: European Heart Journal - Digital Health
volume: 7
paginas: ztag124
tipo_bib: article
doi: 10.1093/ehjdh/ztag124
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC13492338/
temas: [llm-ferramentas, calculadoras-clinicas, risco-cardiovascular, trabalho-mais-proximo]
leitura: completa
lido_em: 2026-09-29
relevancia: central
---

# Pipeline LLM para escores de risco cardiovascular (Roeschl et al., 2026)

## Referência
ROESCHL, T. et al. Development of an LLM pipeline exceeding physician-documented cardiovascular risk scores under routine clinical conditions. **European Heart Journal – Digital Health**, v. 7, n. 7, ztag124, 2026. DOI: 10.1093/ehjdh/ztag124. PMCID: PMC13492338. Código: https://github.com/charite-iaim/mcp-risk-server (GPLv3, implementado como servidor MCP).

> Lista de autores retirada do XML do PMC (10 primeiros contribuidores). Confira se há mais autores no PDF.

## Problema
Escores de risco cardiovascular são essenciais, mas o cálculo manual é trabalhoso e sujeito a erro. LLMs erram cálculo e alucinam. Estudos anteriores usaram vinhetas sintéticas; faltava validação em documentos clínicos reais comparando com médicos.

## Método
- Estudo diagnóstico retrospectivo, centro cardíaco quaternário na Alemanha (Charité), 2020–2023, aprovado por comitê de ética.
- Coortes: 179 pacientes com fibrilação atrial (CHA2DS2-VASc, HAS-BLED) e 76 com estenose aórtica grave (EuroSCORE II).
- **3 configurações × 6 LLMs** (GPT-5.2, Gemini 3.1 Pro, DeepSeek-R1, Qwen3-235B, GPT-OSS 120B, Kimi K2.5), temperatura 0, zero-shot:
  1. **LLM isolado:** calcula o escore de ponta a ponta.
  2. **LLM + RAG:** extração por componente guiada por literatura recuperada, cálculo determinístico.
  3. **Pipeline:** (i) definições dos componentes curadas por especialistas; (ii) LLM extrai **cada componente** em JSON; (iii) **motor determinístico em Python** calcula o escore.
- Padrão-ouro: 2 cardiologistas independentes + 3º para desempate. Métricas: Krippendorff α (concordância por categoria clínica), RMSE, calibração (KDE), acurácia por componente.

## Resultados
- **Pipeline: α médio 0,78** vs LLM isolado 0,32 vs RAG 0,39 vs **médicos assistentes 0,31**. RMSE: 0,89 vs 5,81 vs 1,85 vs 1,34.
- **LLM isolado falha em escores baseados em regressão:** no EuroSCORE II (logístico), a consistência entre o escore que o LLM relatou e o recalculado a partir dos próprios componentes que ele extraiu foi de **0,0% a 15,8%** em 5 dos 6 modelos. Em escores aditivos simples (CHA2DS2-VASc), a consistência passou de 97%.
- **"Knowledge conflict":** o LLM usa sua definição genérica em vez da definição do escore (ex.: marca "hipertensão" no HAS-BLED sem PAS > 160 mmHg).
- LLMs são bons **extratores**, piores **intérpretes** (ex.: classe NYHA) — mas os próprios especialistas também discordam mais nesses itens.
- RAG não substitui instruções curadas por especialistas.
- Médicos tendiam a **subestimar** o risco; HAS-BLED documentado em só 20,1% dos pacientes.

## Limitações declaradas
Retrospectivo, centro único; prompts curados por especialistas (escalabilidade e adaptação local); entrada em alemão com prompts em inglês; padrão-ouro com subjetividade em algumas variáveis.

## Leitura crítica
- Estudo forte, recente, revisado por pares, **em cardiologia** — ótima referência para a banca.
- Avalia só o **número/categoria**; **não gera nem avalia explicação** para o paciente/clínico. A lacuna de fidelidade da explicação continua aberta.
- Não usa multiagentes nem verificador; é um pipeline determinístico fixo.
- Não avalia viés demográfico.

## Relação com o meu TCC
- **Principal evidência para H1 no domínio cardiovascular:** separar extração (LLM) de cálculo (determinístico) supera LLM isolado e até médicos.
- **Argumento decisivo sobre o PREVENT:** o PREVENT é uma equação de regressão (como o EuroSCORE II). Roeschl mostra que LLMs isolados praticamente **não conseguem** calcular escores de regressão de forma consistente (0–15,8%). Logo, o PREVENT **precisa** ser calculado por ferramenta.
- **Design:** extrair e validar **componente a componente**, com definições operacionais explícitas (ex.: o que conta como "diabetes", "tabagismo atual").
- **Checagem de consistência interna** (escore relatado vs recalculado a partir dos componentes) é uma técnica que posso reutilizar no verificador.
- **Diferença:** meu foco é a camada seguinte — a explicação — e o papel de um verificador.

## Dados citáveis
- [C1] O pipeline com extração por LLM e cálculo determinístico obteve Krippendorff α médio de 0,78, contra 0,32 do LLM isolado, 0,39 do LLM com RAG e 0,31 dos escores documentados por médicos (Abstract; Results).
- [C2] No EuroSCORE II, baseado em regressão logística, a concordância entre o escore relatado pelo LLM isolado e o recalculado a partir dos seus próprios componentes foi de 0,0% a 15,8% em 5 de 6 modelos (Results).
- [C3] LLMs isolados aplicaram definições genéricas em vez dos critérios do escore (ex.: hipertensão no HAS-BLED), fenômeno descrito como conflito de conhecimento (Results).
- [C4] Instruções curadas por especialistas superaram o uso de RAG sobre a literatura para extração de componentes (Results; Discussion).
- [C5] Os médicos assistentes tenderam a subestimar o risco em relação ao padrão-ouro (Results; Discussion).
