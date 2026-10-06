---
chave: khandekar2024medcalc
titulo: MedCalc-Bench: Evaluating Large Language Models for Medical Calculations
autores: [Nikhil Khandekar, Qiao Jin, Guangzhi Xiong, Soren Dunn, Serina S. Applebaum, Zain Anwar, Maame Sarfo-Gyamfi, Conrad W. Safranek, Abid A. Anwar, Andrew Zhang, Aidan Gilson, Maxwell B. Singer, Amisha Dave, Andrew Taylor, Aidong Zhang, Qingyu Chen, Zhiyong Lu]
ano: 2024
veiculo: Advances in Neural Information Processing Systems 37 (NeurIPS 2024) - Datasets and Benchmarks Track
tipo_bib: inproceedings
doi: 10.48550/arXiv.2406.12036
url: https://arxiv.org/abs/2406.12036
temas: [llm-calculo-clinico, benchmarks, llm-ferramentas]
leitura: completa
lido_em: 2026-09-29
relevancia: central
---

# MedCalc-Bench (Khandekar et al., 2024)

## Referência
KHANDEKAR, N. et al. MedCalc-Bench: Evaluating Large Language Models for Medical Calculations. In: **Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Datasets and Benchmarks Track**, 2024. arXiv:2406.12036 (v4 lida). Dados: https://github.com/ncbi-nlp/MedCalc-Bench (licença CC BY-SA 4.0).

## Problema
Benchmarks médicos para LLMs (MedQA, PubMedQA, MedMCQA) avaliam conhecimento e raciocínio **qualitativo**, em múltipla escolha. Não havia benchmark de **cálculo clínico** (regras e equações), que é o que o médico faz com calculadoras.

## Método
- 55 calculadoras "populares" do MDCalc: 19 baseadas em regras (ex.: HEART, CHA2DS2-VASc, Wells) e 36 baseadas em equações (ex.: MDRD, LDL calculado, QTc).
- Notas de pacientes do corpus *Open-Patients* (>180 mil notas públicas); GPT-3.5 filtra elegíveis, GPT-4 extrai atributos, **profissionais de saúde verificam e corrigem**. Para 21 calculadoras sem notas: 10 com notas sintéticas por template e 11 com notas sintetizadas por clínicos.
- **1.047 instâncias** de teste (nota + pergunta + resposta + explicação passo a passo gerada por template). Também um conjunto de treino de 10.053 instâncias.
- 8 LLMs (GPT-4, GPT-3.5, Llama 3 8B/70B, Mistral-7B, Mixtral-8x7B, PMC-LLaMA-13B, MediTron-70B) × 3 estratégias (zero-shot direto, zero-shot CoT, one-shot CoT).
- Critério de acerto: regra → exato; equação → dentro de ±5%; datas → exato.
- Análise de erros: tipo A (conhecimento da fórmula/regra), B (extração de atributos), C (aritmética), D (outros). Classificador de erros = GPT-4, validado em 200 amostras (89% de acerto).

## Resultados
- Melhor resultado: **GPT-4 one-shot CoT = 50,91%**. GPT-4 zero-shot CoT = 37,92%; zero-shot direto = 20,82% (Tabela 2).
- Subcategoria **Risk** (escores de risco baseados em regras): GPT-4 one-shot = 33,75% (Tabela 2).
- Llama 3-70B próximo do GPT-4 em zero-shot; modelos médicos específicos (PMC-LLaMA, MediTron) foram piores que modelos gerais.
- Em zero-shot, a maioria dos erros é de **conhecimento (tipo A)**; com one-shot, crescem os erros de extração (B) e aritmética (C) (Tabela 4).
- **Apêndice D:** dar interpretador de código ao LLM eleva GPT-4 de 37,92% para apenas **48,51%** (zero-shot) — o código resolve a aritmética, mas não a escolha da fórmula nem a extração.
- **Apêndice C:** fine-tuning leva Mistral-7B de 10,79% a 49,19%.
- **Apêndice E:** a acurácia cai conforme aumenta o número de atributos da calculadora.

## Limitações declaradas
- Tamanho limitado (1.047) pela dificuldade de verificação manual.
- Entidades mencionadas várias vezes na nota dificultam a extração.
- Não testaram few-shot com mais exemplos.

## Leitura crítica
- Mede o LLM **fazendo o cálculo sozinho**; não avalia a qualidade da explicação textual além do valor final.
- Explicações de referência são geradas por **template**, não por LLM — o que é um bom modelo para meu verificador determinístico.
- Os próprios autores dizem que passar no benchmark é condição **necessária, mas não suficiente** para uso clínico.
- Modelos avaliados são de 2023–2024; modelos atuais provavelmente vão melhor. **Na banca, não trate 50,9% como "estado atual" — trate como evidência de que o problema é estrutural** (conhecimento + extração + aritmética) e por isso deve ser resolvido por arquitetura, não por "esperar o próximo modelo".

## Relação com o meu TCC
- Justifica a decisão de projeto de **não deixar o LLM calcular**.
- O Apêndice D é argumento importante: **"dar Python ao LLM" não basta** (48,5%); a ferramenta precisa ser a **calculadora validada em si** (implementação determinística do PREVENT), não código gerado pelo LLM na hora. Isso diferencia meu desenho do AgentMD, que gera o código de chamada.
- A queda de acurácia com o número de atributos é relevante: PREVENT tem ~9–10 variáveis.
- As categorias de erro A/B/C podem ser reutilizadas na minha taxonomia de erros.

## Dados citáveis
- [C1] O melhor LLM avaliado (GPT-4 com one-shot chain-of-thought) acertou 50,91% das 1.047 instâncias (Tabela 2; Seção 3.2).
- [C2] Na subcategoria de escores de risco baseados em regras, o GPT-4 one-shot acertou 33,75% (Tabela 2).
- [C3] Com interpretador de código, a acurácia do GPT-4 zero-shot subiu de 37,92% para 48,51% (Apêndice D, Tabela 15).
- [C4] Em zero-shot, a maior parte dos erros do GPT-4 (57%) foi de conhecimento da fórmula ou regra (Tabela 4).
- [C5] A acurácia dos melhores modelos cai de forma acentuada à medida que o número de atributos da calculadora aumenta (Apêndice E.1).
- [C6] Os autores afirmam que passar no MedCalc-Bench é condição necessária, mas não suficiente, para uso em cálculos médicos (Broader Impacts).
