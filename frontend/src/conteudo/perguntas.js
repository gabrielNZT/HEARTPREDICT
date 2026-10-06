/*
 * Perguntas, uma por tela (GOV.UK, "one thing per page").
 * Faixas numéricas = faixas de derivação do PREVENT (Khan et al. 2024, Methods).
 * Critérios de escopo = D011 / Diretriz SBC 2025, seção 4.1.
 * Justificativas: tcc/03-metodologia/interface-design.md.
 */

/** Valor interno da opção exclusiva "Nenhuma destas" (o rótulo vem de `pergunta.nenhuma`). */
export const NENHUMA = 'nenhuma';

/** Opções que não são agravantes, mas critérios que classificam direto como alto (SBC 2025, Tabela 4.1). */
export const CRITERIOS_ALTO = ['lpa_muito_elevada'];

const SIM_NAO = [
  { valor: 'sim', rotulo: 'Sim' },
  { valor: 'nao', rotulo: 'Não' },
];

export const MOTIVOS_FORA_DO_ESCOPO = {
  idade: {
    titulo: 'Esta calculadora é para pessoas de 30 a 79 anos',
    texto: [
      'A equação PREVENT foi desenvolvida e testada em pessoas de 30 a 79 anos. Fora dessa faixa, o resultado não seria confiável.',
      'Converse com seu médico sobre os seus fatores de risco, como pressão, colesterol e tabagismo.',
    ],
  },
  dcv_previa: {
    titulo: 'Esta calculadora não se aplica a quem já teve doença cardiovascular',
    texto: [
      'Quem já teve infarto, AVC ou outra doença cardiovascular já é considerado de risco muito alto pela Diretriz Brasileira de Dislipidemias 2025. Nesses casos, não é preciso estimar o risco: o acompanhamento e as metas são definidos com o médico.',
    ],
  },
  aterosclerose_subclinica: {
    titulo: 'Esta calculadora não se aplica a quem já tem placa nas artérias em exame',
    texto: [
      'Pela Diretriz Brasileira de Dislipidemias 2025, quem tem placa de aterosclerose identificada em exame de imagem, como escore de cálcio coronário acima de 100 ou placa na carótida, já é classificado como risco alto ou muito alto. Nesses casos, a equação não é usada.',
      'Converse com seu médico sobre a sua categoria e as metas de colesterol.',
    ],
  },
  diabetes: {
    titulo: 'Esta versão ainda não avalia pessoas com diabetes',
    texto: [
      'Para quem tem diabetes, a Diretriz Brasileira de Dislipidemias 2025 usa outros critérios, que levam em conta, por exemplo, a idade, o tempo de diagnóstico e complicações nos rins e nos olhos.',
      'Esses critérios ainda não estão implementados neste protótipo. Converse com seu médico sobre a sua classificação de risco.',
    ],
  },
};

export const PERGUNTAS = [
  {
    id: 'idade',
    tipo: 'numero',
    titulo: 'Qual é a sua idade?',
    unidade: 'anos',
    inteiro: true,
    plausivel: [18, 120],
    foraDoEscopo: (v) => v < 30 || v > 79,
    rotuloRevisao: 'Idade',
    formatar: (v) => `${v} anos`,
  },
  {
    id: 'sexo',
    tipo: 'escolha',
    titulo: 'Qual é o seu sexo?',
    dica: 'A equação usa fórmulas diferentes para mulheres e homens, porque o risco cardiovascular varia entre os sexos.',
    opcoes: [
      { valor: 'feminino', rotulo: 'Feminino' },
      { valor: 'masculino', rotulo: 'Masculino' },
    ],
    rotuloRevisao: 'Sexo',
  },
  {
    id: 'dcv_previa',
    tipo: 'escolha',
    titulo: 'Você já teve infarto, AVC ou outra doença cardiovascular diagnosticada?',
    dica: 'Inclui angina, ponte de safena, angioplastia com stent e entupimento de artérias das pernas.',
    opcoes: SIM_NAO,
    foraDoEscopo: (v) => v === 'sim',
    rotuloRevisao: 'Doença cardiovascular prévia',
  },
  {
    id: 'aterosclerose_subclinica',
    tipo: 'escolha',
    titulo: 'Algum exame de imagem já mostrou placa de gordura nas artérias?',
    dica: 'Por exemplo: escore de cálcio coronário acima de 100, placa na carótida em ultrassom ou placa em angiotomografia das coronárias. Se nunca fez esses exames, responda Não.',
    opcoes: SIM_NAO,
    foraDoEscopo: (v) => v === 'sim',
    rotuloRevisao: 'Placa nas artérias em exame',
  },
  {
    id: 'diabetes',
    tipo: 'escolha',
    titulo: 'Você tem diabetes?',
    dica: 'Responda sim se um médico já diagnosticou diabetes ou se você toma remédio para diabetes.',
    opcoes: SIM_NAO,
    foraDoEscopo: (v) => v === 'sim',
    rotuloRevisao: 'Diabetes',
  },
  {
    id: 'colesterol_total',
    tipo: 'numero',
    titulo: 'Qual é o seu colesterol total?',
    dica: 'Aparece no exame de sangue como “Colesterol total”.',
    unidade: 'mg/dL',
    faixa: [130, 320],
    rotuloRevisao: 'Colesterol total',
    formatar: (v) => `${v} mg/dL`,
  },
  {
    id: 'hdl',
    tipo: 'numero',
    titulo: 'Qual é o seu HDL?',
    dica: 'É o colesterol “bom”. No exame pode aparecer como “HDL-colesterol” ou “Colesterol HDL”.',
    unidade: 'mg/dL',
    faixa: [20, 100],
    rotuloRevisao: 'HDL',
    formatar: (v) => `${v} mg/dL`,
  },
  {
    id: 'ldl',
    tipo: 'numero',
    titulo: 'Qual é o seu LDL? (opcional)',
    dica: 'É o colesterol “ruim”. Ele não entra no cálculo do risco, mas a diretriz o usa para ajustar a categoria e comparar com a meta. Se não souber, deixe em branco. Se você usa remédio para colesterol, este é o valor durante o tratamento.',
    // Obrigatório quando o não-HDL é alto: a equação só vale com LDL < 160 (SBC 2025, seção 4.1)
    obrigatorioSe: (r) => r.colesterol_total - r.hdl >= 190,
    mensagemObrigatorio: 'Com o seu colesterol total e HDL, o LDL precisa ser informado: se ele passar de 160, a diretriz não usa esta equação.',
    unidade: 'mg/dL',
    faixa: [20, 400],
    opcional: true,
    rotuloRevisao: 'LDL',
    formatar: (v) => (v == null ? 'Não informado' : `${v} mg/dL`),
  },
  {
    id: 'pas',
    tipo: 'numero',
    titulo: 'Qual é a sua pressão sistólica?',
    dica: 'É o primeiro número da medida da pressão. Se sua pressão foi 12 por 8, digite 120. Se tiver mais de uma medida recente, feita em repouso, use a média.',
    unidade: 'mmHg',
    inteiro: true,
    faixa: [90, 200],
    rotuloRevisao: 'Pressão sistólica',
    formatar: (v) => `${v} mmHg`,
  },
  {
    id: 'anti_hipertensivo',
    tipo: 'escolha',
    titulo: 'Você toma remédio para pressão alta?',
    opcoes: SIM_NAO,
    rotuloRevisao: 'Remédio para pressão',
  },
  {
    id: 'estatina',
    tipo: 'escolha',
    titulo: 'Você toma estatina, remédio para baixar o colesterol?',
    dica: 'Por exemplo: sinvastatina, atorvastatina, rosuvastatina ou pravastatina. Outros remédios para colesterol, como ezetimiba ou fibrato, não contam aqui.',
    opcoes: SIM_NAO,
    rotuloRevisao: 'Estatina',
  },
  {
    id: 'tabagismo',
    tipo: 'escolha',
    titulo: 'Você fuma atualmente?',
    dica: 'Responda sim mesmo que fume poucos cigarros por dia.',
    opcoes: SIM_NAO,
    rotuloRevisao: 'Fuma atualmente',
  },
  {
    id: 'renal',
    tipo: 'renal',
    titulo: 'O que o seu exame mostra sobre a função dos rins?',
    dica: 'Procure no exame de sangue por “TFG estimada” (às vezes “eGFR”) ou por “Creatinina”.',
    opcoes: [
      { valor: 'tfge', rotulo: 'TFG estimada', unidade: 'mL/min/1,73 m²', faixa: [15, 140], campo: 'Valor da TFG estimada', rotuloRevisao: 'TFG estimada', mensagemVazio: 'Digite o valor da TFG estimada.' },
      {
        valor: 'creatinina', rotulo: 'Só a creatinina', unidade: 'mg/dL', faixa: [0.3, 15], campo: 'Valor da creatinina', rotuloRevisao: 'Creatinina',
        mensagemVazio: 'Digite o valor da creatinina.',
        dica: 'Vamos calcular a TFG estimada com a mesma equação usada pelo PREVENT (CKD-EPI 2021).',
      },
    ],
    rotuloRevisao: 'Função dos rins',
  },
  {
    id: 'agravantes',
    tipo: 'multipla',
    titulo: 'Alguma destas situações se aplica a você?',
    dica: 'A diretriz usa estas condições para ajustar a categoria de risco. Marque todas as que se aplicam.',
    opcoes: [
      { valor: 'historia_familiar_prematura', rotulo: 'Pai, mãe, irmão ou irmã teve infarto ou AVC cedo', dica: 'Homens antes dos 55 anos ou mulheres antes dos 65.' },
      { valor: 'doenca_inflamatoria_cronica', rotulo: 'Doença inflamatória crônica', dica: 'Por exemplo: artrite reumatoide, psoríase, lúpus, doença de Crohn, retocolite ou HIV.' },
      { valor: 'sindrome_metabolica', rotulo: 'Diagnóstico de síndrome metabólica', dica: 'Só marque se um médico já deu esse diagnóstico.' },
      { valor: 'transplante', rotulo: 'Transplante de órgão' },
      {
        valor: 'fator_especifico_mulher', rotulo: 'Situações da saúde da mulher', somente: 'feminino',
        dica: 'Pré-eclâmpsia, pressão alta ou diabetes na gravidez, parto prematuro, bebê com restrição de crescimento na gestação, 3 ou mais abortos espontâneos, menopausa antes dos 40 anos, ou primeira menstruação aos 12 anos ou antes, ou aos 17 anos ou depois.',
      },
      { valor: 'lpa_elevada', rotulo: 'Lipoproteína(a) entre 50 e 180 mg/dL em exame', dica: 'Ou entre 125 e 390 nmol/L.' },
      { valor: 'lpa_muito_elevada', rotulo: 'Lipoproteína(a) acima de 180 mg/dL em exame', dica: 'Ou acima de 390 nmol/L. A diretriz classifica esse valor diretamente como risco alto.' },
      { valor: 'pcr_us_elevada', rotulo: 'PCR ultrassensível elevada em exame', dica: 'Igual ou acima de 2 mg/L, em exame feito sem infecção ou inflamação aguda.' },
    ],
    nenhuma: 'Nenhuma destas',
    rotuloRevisao: 'Situações que ajustam a categoria',
  },
];

export function opcoesVisiveis(pergunta, respostas) {
  return (pergunta.opcoes || []).filter((o) => !o.somente || o.somente === respostas.sexo);
}

export function rotuloDaOpcao(pergunta, valor) {
  const o = (pergunta.opcoes || []).find((x) => x.valor === valor);
  return o ? o.rotulo : valor;
}
