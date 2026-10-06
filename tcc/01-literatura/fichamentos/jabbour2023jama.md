---
chave: jabbour2023jama
titulo: Measuring the Impact of AI in the Diagnosis of Hospitalized Patients: A Randomized Clinical Vignette Survey Study
autores: [Sarah Jabbour, David Fouhey, Stephanie Shepard, Thomas S. Valley, Ella A. Kazerooni, Nikola Banovic, Jenna Wiens, Michael W. Sjoding]
ano: 2023
veiculo: JAMA
volume: 330
paginas: 2275-2284
tipo_bib: article
doi: 10.1001/jama.2023.22295
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC10731487/
temas: [vies-de-automacao, xai-clinica, fatores-humanos]
leitura: parcial
lido_em: 2026-09-29
relevancia: alta
---

# Jabbour et al. (JAMA, 2023)

> **Status da leitura: parcial.** O PMC não permite baixar o texto completo em XML (restrição do editor), e o acesso direto à página foi bloqueado para download automático. Li Key Points, Abstract completo, desenho da intervenção, números com IC 95%, Discussão e Limitações a partir da página do PMC por meio de uma ferramenta de extração. **Antes de citar, abra o PDF e confira os números abaixo.**
>
> **Autores:** a lista no front-matter foi montada a partir do bloco de contribuições do PMC (Jabbour, Fouhey, Shepard, Valley, Kazerooni, Banovic, Wiens, Sjoding). Confira a lista e a ordem completas no PDF — podem existir coautores omitidos.

## Referência
JABBOUR, S. et al. Measuring the Impact of AI in the Diagnosis of Hospitalized Patients: A Randomized Clinical Vignette Survey Study. **JAMA**, v. 330, n. 23, p. 2275–2284, 2023. DOI: 10.1001/jama.2023.22295. PMCID: PMC10731487. PMID: 38112814.

## Problema
Diretrizes regulatórias recomendam que sistemas de IA forneçam explicações, mas não se sabe se explicações ajudam clínicos a perceber quando um modelo está **sistematicamente enviesado**.

## Método
- Estudo **randomizado** com vinhetas clínicas, via survey web, abr/2022–jan/2023, 13 estados dos EUA.
- 457 participantes: médicos hospitalistas, enfermeiros de prática avançada e assistentes médicos.
- 9 vinhetas de insuficiência respiratória aguda; diagnósticos: pneumonia, insuficiência cardíaca, DPOC. 2 vinhetas sem IA (baseline), 6 com IA (randomizados para receber ou não explicações), 3 com modelo padrão e 3 com modelo **sistematicamente enviesado**; 1 vinheta de consulta clínica.
- Vieses introduzidos: idade ≥80 → pneumonia; IMC ≥30 → insuficiência cardíaca; radiografia borrada → DPOC.
- **Explicações = mapas de calor Grad-CAM sobre a radiografia** (baseadas em imagem, não em texto). Nos modelos enviesados, os mapas destacavam regiões clinicamente irrelevantes.

## Resultados
- Acurácia baseline: 73,0% (IC95% 68,3–77,8).
- Modelo padrão: +2,9 p.p. (IC95% 0,5–5,2); com explicações: +4,4 p.p. (IC95% 2,0–6,9).
- **Modelo enviesado: −11,3 p.p. (IC95% 7,2–15,5)**; com explicações: −9,1 p.p. (IC95% 4,9–13,2). Diferença entre enviesado com e sem explicação: 2,3 p.p. (IC95% −2,7 a 7,2), **não significativa**.
- 66,7% dos participantes não sabiam que modelos de IA podem ser sistematicamente enviesados.

## Interpretação dos autores
Explicações baseadas em imagem são apenas aproximações do comportamento do modelo e exigem que o clínico construa um modelo mental; a literacia em IA dos clínicos é limitada; houve pouco treinamento com explicações.

## Limitações declaradas
Ambiente de survey web (não clínico real); amostra mais jovem e mais feminina que a população nacional de hospitalistas; radiologistas excluídos; não foi possível coletar dados de não respondentes.

## Leitura crítica
- Evidência forte (JAMA, randomizado, n=457), mas as explicações eram **visuais (Grad-CAM)**, não **narrativas textuais**. **Não generalize sem ressalva:** o argumento para meu TCC é por **analogia** — se explicações visuais não protegeram clínicos de um modelo enviesado, não há razão para supor que explicações textuais, que soam ainda mais convincentes, protejam contra uma explicação infiel.
- Diagnóstico agudo em internação, não risco cardiovascular preventivo.

## Relação com o meu TCC
- Sustenta o argumento central de **por que a verificação deve ser automática e anterior ao usuário**: o ser humano não é um filtro confiável para erros da IA, mesmo com explicação.
- Sustenta a relevância de **medir viés** (H3): modelos enviesados reduzem o acerto clínico de forma significativa.
- Na defesa, apresente como **analogia fundamentada**, deixando claro que o estudo usou explicações visuais.

## Dados citáveis
- [C1] Em estudo randomizado com 457 clínicos, um modelo sistematicamente enviesado reduziu a acurácia diagnóstica em 11,3 p.p. (IC95% 7,2–15,5) em relação ao baseline de 73,0% (Abstract, Results).
- [C2] Explicações do modelo enviesado não recuperaram significativamente o desempenho: diferença de 2,3 p.p. (IC95% −2,7 a 7,2) (Abstract, Results).
- [C3] As explicações avaliadas eram mapas de calor baseados em imagem (Grad-CAM), não narrativas textuais (Methods).
- [C4] 66,7% dos participantes não sabiam que modelos de IA podem ser sistematicamente enviesados (Discussion).
