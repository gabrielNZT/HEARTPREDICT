---
chave: khan2024prevent
titulo: Development and Validation of the American Heart Association's PREVENT Equations
autores: [Sadiya S. Khan, Kunihiro Matsushita, Yingying Sang, Shoshana H. Ballew, Morgan E. Grams, Aditya Surapaneni, Michael J. Blaha, April P. Carson, Alexander R. Chang, Elizabeth Ciemins, Alan S. Go, Orlando M. Gutierrez, Shih-Jen Hwang, Simerjot K. Jassal, Csaba P. Kovesdy, Donald M. Lloyd-Jones, Michael G. Shlipak, Latha P. Palaniappan, Laurence Sperling, Salim S. Virani, Katherine Tuttle, Ian J. Neeland, Sheryl L. Chow, Janani Rangaswami, Michael J. Pencina, Chiadi E. Ndumele, Josef Coresh]
ano: 2024
veiculo: Circulation
volume: 149
paginas: 430-449
tipo_bib: article
doi: 10.1161/CIRCULATIONAHA.123.067626
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC10910659/
temas: [risco-cardiovascular, escores-clinicos]
leitura: completa
lido_em: 2026-09-29
relevancia: central
---

# PREVENT (Khan et al., 2024)

> **Leitura:** texto completo (manuscrito do autor no PMC, PMC10910659), incluindo as tabelas 1–4. **O suplemento (Tabela S12 com os coeficientes) não pôde ser baixado automaticamente** — ver "Implementação" e [pendências](../../00-projeto/pendencias.md).
>
> **Correção:** a versão anterior deste fichamento listava Coresh, Pencina, Ndumele, Rangaswami e Chow como primeiros autores. Essa é a autoria da *declaração científica* de 2023 (Khan et al., Circulation 2023;148:1982–2004), que é outro documento. A lista acima vem do XML do PMC e confere com a citação da diretriz SBC (ref. 110).

## Referência
KHAN, S. S. et al. Development and Validation of the American Heart Association's PREVENT Equations. **Circulation**, v. 149, n. 6, p. 430–449, 2024. DOI: 10.1161/CIRCULATIONAHA.123.067626. PMCID: PMC10910659.

Documento complementar (não lido): KHAN, S. S. et al. Novel Prediction Equations for Absolute Risk Assessment of Total Cardiovascular Disease Incorporating Cardiovascular-Kidney-Metabolic Health: A Scientific Statement From the AHA. **Circulation**, v. 148, n. 24, p. 1982–2004, 2023. DOI: 10.1161/CIR.0000000000001191.

## Problema
As Pooled Cohort Equations (PCE, 2013) usam raça como preditor, não incluem insuficiência cardíaca, não refletem a prevalência atual de fatores de risco e **superestimam o risco em cerca de 50%** nas coortes contemporâneas.

## Método
- **Derivação:** 25 bases, 3.281.919 adultos dos EUA (1992–2017). **Validação externa:** 21 bases, 3.330.085 adultos. Idade 30–79 anos, **sem DCVA nem IC** no início.
- Bases: coortes de pesquisa (ARIC, CARDIA, CHS, Framingham, JHS, MESA, REGARDS, CRIC, Rancho Bernardo) + prontuários/claims (Geisinger, Optum Labs).
- **Exclusões por valores extremos:** PAS < 90 ou > 200 mmHg; CT < 130 ou > 320 mg/dL; HDL < 20 ou > 100 mg/dL; IMC < 18,5 ou ≥ 40 kg/m².
- **Modelo:** Cox específico por sexo, **sem raça**, com idade como escala de tempo, ajustado para **risco competitivo de morte não cardiovascular**; meta-análise por coorte (efeitos aleatórios).
- **Preditores do modelo base:** não-HDL-c, HDL-c, PAS (spline com nó em 110), diabetes, tabagismo atual, TFGe (CKD-EPI 2021, spline com nó em 60), uso de anti-hipertensivo, uso de estatina, interações tratamento × fator e **interações idade × fator**.
- **IMC entra apenas nos modelos de IC e de morte, não no de DCVA; colesterol não entra no modelo de IC** (Statistical Analysis).
- Desfechos: DCV total (DCVA + IC), **PREVENT-ASCVD** (IAM, morte coronária e AVC; revascularização não incluída) e PREVENT-HF. Horizontes de 10 e 30 anos.
- Modelos opcionais: + razão albumina/creatinina urinária (UACR), + HbA1c, + índice de privação social (SDI), com indicador de dado ausente.
- **Implementação clínica:** "aproximações de regressão simplificadas" (Tabela S12 A–J, **R² ≥ 0,99** em relação ao modelo completo para 10 anos), usadas na calculadora online da AHA.

## Resultados
- **Discriminação (validação, DCVA):** C = **0,774** (IQI 0,743–0,788) em mulheres e **0,736** (0,710–0,755) em homens (Tabela 4). DCV total: 0,794 e 0,757.
- **Calibração (DCVA):** inclinação 1,09 em mulheres e 1,04 em homens (ideal = 1). **PCE:** 0,54 e 0,50 — ou seja, superestimam cerca de 50% (Tabela 4).
- Calibração semelhante entre grupos raciais/étnicos. Subestimação modesta com IMC > 40 (inclinação 1,30).
- Modelos opcionais trazem ganhos mínimos de discriminação (ΔC ≈ 0,002–0,005); UACR melhora a calibração em albuminúria > 300 mg/g.
- **Caso de teste publicado (Results, "Predicted 10- and 30-Year CVD Risk"):** mulher de 50 anos, CT 240 mg/dL, HDL 55 mg/dL, sem estatina, **PAS tratada 160 mmHg**, sem diabetes, não fumante, IMC 35, TFGe 90 → risco em 10 anos: **DCV total 5,4%, DCVA 3,6%, IC 2,5%**. Se fumante: 9,3%, **6,0%**, 4,7%.
- **Tabela 2 (derivação, DCVA, HR):** diabetes 2,35 (mulheres) / 2,10 (homens); tabagismo 1,67 / 1,53; PAS ≥ 110 por +20 mmHg 1,44 / 1,39; não-HDL por +1 mmol/L 1,12 / 1,17; HDL por +0,3 mmol/L 0,86 / 0,89; TFGe < 60 por −15 1,75 / 1,59; estatina 0,93 / 0,90. Interações idade × fator < 1: **o peso relativo dos fatores diminui com a idade**. Centralização: idade 55, não-HDL 3,5 mmol/L, HDL 1,3 mmol/L, PAS 130 mmHg.

## Limitações declaradas
Dados de prontuário sem adjudicação de desfechos; bases cobrindo mais de 3 décadas; idade como escala de tempo pode superestimar o risco em 30 anos; determinantes sociais individuais ausentes (SDI é por CEP); biomarcadores (troponina, BNP, PCR, CAC) não incluídos; **população dos EUA**.

## Leitura crítica
- Modelo robusto e bem calibrado **nos EUA**. Não há validação em coorte brasileira no artigo; a diretriz SBC o adota mesmo assim, por ausência de escore brasileiro (ver [sbc2025dislipidemias](sbc2025dislipidemias.md)).
- O código oficial em STATA é "disponível sob pedido"; a implementação usual é a da Tabela S12.

## Implementação no TCC
- **Forma da equação de 10 anos** (Tabela S12, conferida no código do pacote R `preventr` v0.12.0, licença MIT, CRAN, 2026): `risco = exp(L) / (1 + exp(L))`, com `L = Σ βᵢ·xᵢ` sobre termos centrados:
  - `idade = (idade − 55)/10`; `não-HDL = (CT − HDL [mmol/L]) − 3,5`; `HDL = (HDL[mmol/L] − 1,3)/0,3`;
  - `PAS<110 = (min(PAS,110) − 110)/20`; `PAS≥110 = (max(PAS,110) − 130)/20`;
  - `TFGe<60 = (min(TFGe,60) − 60)/−15`; `TFGe≥60 = (max(TFGe,60) − 90)/−15`;
  - diabetes, tabagismo, anti-hipertensivo, estatina (0/1);
  - interações: anti-hipertensivo × PAS≥110; estatina × não-HDL; idade × (não-HDL, HDL, PAS≥110, diabetes, tabagismo, IMC≥30, TFGe<60).
  - Conversão: mg/dL ÷ 38,67 = mmol/L (Tabela 1, nota).
- **Os coeficientes não estão no artigo principal**, só na Tabela S12. Fonte primária a obter manualmente; `preventr` serve como verificação cruzada.
- **Testes unitários com fonte primária:** o caso da mulher de 50 anos (DCVA 3,6% e 6,0% se fumante) deve ser reproduzido pela implementação.
- **Validação de entrada:** rejeitar (ou sinalizar) valores fora das faixas de derivação (PAS 90–200, CT 130–320, HDL 20–100, IMC 18,5–39,9, idade 30–79).
- **Atribuição exata:** como o modelo é linear em log-odds com interações, a contribuição de cada variável original pode ser calculada **exatamente** por valores de Shapley (≈ 10 variáveis → 2¹⁰ coalizões), com referência nos valores de centralização. Isso dá um "gabarito" de atribuição **sem aproximação**, ideal para medir fidelidade.
- **Caso de teste para o verificador:** IMC **não** entra no modelo de DCVA. Uma explicação que diga "seu IMC aumentou seu risco aterosclerótico em 10 anos" é **infiel ao modelo**, mesmo sendo clinicamente plausível. Esse é um exemplo concreto da diferença entre fidelidade e plausibilidade ([jacovi2020faithfulness](jacovi2020faithfulness.md)).

## Dados citáveis
- [C1] O PREVENT foi derivado em 3.281.919 adultos de 25 bases e validado externamente em 3.330.085 adultos de 21 bases, com idade de 30 a 79 anos e sem DCV prévia (Abstract; Methods).
- [C2] Na validação, o PREVENT-ASCVD teve C-estatística de 0,774 em mulheres e 0,736 em homens (Tabela 4).
- [C3] As Pooled Cohort Equations tiveram inclinação de calibração de 0,54 (mulheres) e 0,50 (homens) para DCVA, isto é, superestimaram o risco em cerca de 50%, contra 1,09 e 1,04 do PREVENT (Tabela 4; Discussion).
- [C4] O IMC foi incluído apenas nos modelos de insuficiência cardíaca e de morte, e não no de DCVA (Methods, Statistical Analysis).
- [C5] Para uma mulher de 50 anos com CT 240, HDL 55, PAS tratada 160, sem diabetes, não fumante, IMC 35 e TFGe 90, o risco de DCVA em 10 anos foi 3,6% (6,0% se fumante) (Results).
- [C6] As aproximações de regressão simplificadas usadas na implementação reproduzem o modelo completo com R² ≥ 0,99 para 10 anos (Results; Tabela S12).
- [C7] Os modelos são específicos por sexo, não usam raça como preditor e ajustam para o risco competitivo de morte não cardiovascular (Abstract; Methods).
