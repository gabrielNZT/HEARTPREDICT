import { NENHUMA, opcoesVisiveis } from './conteudo/perguntas';

const fmt = (n) => String(n).replace('.', ',');

/** Aceita vírgula ou ponto decimal; retorna número ou null. */
export function lerNumero(texto) {
  const limpo = String(texto ?? '').trim().replace(/\s/g, '').replace(',', '.');
  if (limpo === '') return null;
  if (!/^\d+(\.\d+)?$/.test(limpo)) return NaN;
  return Number(limpo);
}

/**
 * Valida a resposta de uma pergunta.
 * Retorna { valor, erros: [{campo, mensagem}] }. Mensagens dizem o que fazer (GOV.UK, error message).
 */
export function validar(pergunta, bruto, respostas) {
  const erros = [];
  const campo = pergunta.id;

  if (pergunta.tipo === 'numero') {
    const n = lerNumero(bruto);
    if (n === null) {
      if (pergunta.obrigatorioSe?.(respostas)) {
        erros.push({ campo, mensagem: pergunta.mensagemObrigatorio });
        return { valor: null, erros };
      }
      if (pergunta.opcional) return { valor: null, erros };
      erros.push({ campo, mensagem: 'Digite um número.' });
    } else if (Number.isNaN(n)) {
      erros.push({ campo, mensagem: 'Digite só números, por exemplo 180 ou 1,2.' });
    } else if (pergunta.inteiro && !Number.isInteger(n)) {
      erros.push({ campo, mensagem: 'Digite um número inteiro.' });
    } else if (pergunta.faixa && (n < pergunta.faixa[0] || n > pergunta.faixa[1])) {
      const [lo, hi] = pergunta.faixa;
      erros.push({
        campo,
        // Sem beco sem saída (parecer de IHC): diz o que fazer se o valor estiver mesmo fora da faixa.
        mensagem: `Digite um valor entre ${fmt(lo)} e ${fmt(hi)} ${pergunta.unidade}. Se o seu exame mostra mesmo um valor fora dessa faixa, a equação não foi desenvolvida para ele e esta calculadora não se aplica ao seu caso: leve o exame ao seu médico.`,
      });
    } else if (pergunta.plausivel && (n < pergunta.plausivel[0] || n > pergunta.plausivel[1])) {
      erros.push({ campo, mensagem: 'Confira o valor digitado.' });
    }
    return { valor: n, erros };
  }

  if (pergunta.tipo === 'escolha') {
    if (!bruto) erros.push({ campo, mensagem: 'Selecione uma opção.' });
    return { valor: bruto, erros };
  }

  if (pergunta.tipo === 'renal') {
    const { tipo, valor } = bruto || {};
    if (!tipo) {
      erros.push({ campo, mensagem: 'Selecione o que aparece no seu exame.' });
      return { valor: bruto, erros };
    }
    const opcao = pergunta.opcoes.find((o) => o.valor === tipo);
    const n = lerNumero(valor);
    const campoValor = `${campo}-valor`;
    if (n === null) erros.push({ campo: campoValor, mensagem: opcao.mensagemVazio });
    else if (Number.isNaN(n)) erros.push({ campo: campoValor, mensagem: 'Digite só números, por exemplo 90 ou 0,9.' });
    else if (n < opcao.faixa[0] || n > opcao.faixa[1]) {
      erros.push({ campo: campoValor, mensagem: `Digite um valor entre ${fmt(opcao.faixa[0])} e ${fmt(opcao.faixa[1])} ${opcao.unidade}.` });
    }
    return { valor: { tipo, valor: n }, erros };
  }

  if (pergunta.tipo === 'multipla') {
    const lista = bruto || [];
    const validos = new Set(opcoesVisiveis(pergunta, respostas).map((o) => o.valor).concat([NENHUMA]));
    const filtrada = lista.filter((v) => validos.has(v));
    if (filtrada.length === 0) {
      erros.push({ campo, mensagem: `Selecione pelo menos uma opção ou marque “${pergunta.nenhuma}”.` });
    }
    return { valor: filtrada, erros };
  }

  return { valor: bruto, erros };
}
