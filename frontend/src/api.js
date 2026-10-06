import { CRITERIOS_ALTO, NENHUMA } from './conteudo/perguntas';

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/** Converte as respostas da interface no contrato de POST /api/avaliacao (gateway). */
export function montarEntrada(r) {
  const renal = r.renal || {};
  return {
    idade: r.idade,
    sexo: r.sexo,
    dcv_previa: r.dcv_previa === 'sim',
    aterosclerose_subclinica: r.aterosclerose_subclinica === 'sim',
    diabetes: r.diabetes === 'sim',
    colesterol_total: r.colesterol_total,
    hdl: r.hdl,
    ldl: r.ldl ?? null,
    pas: r.pas,
    anti_hipertensivo: r.anti_hipertensivo === 'sim',
    estatina: r.estatina === 'sim',
    tabagismo: r.tabagismo === 'sim',
    tfge: renal.tipo === 'tfge' ? renal.valor : null,
    creatinina: renal.tipo === 'creatinina' ? renal.valor : null,
    agravantes: (r.agravantes || []).filter((a) => a !== NENHUMA && !CRITERIOS_ALTO.includes(a)),
    criterios_alto: (r.agravantes || []).filter((a) => CRITERIOS_ALTO.includes(a)),
  };
}

async function postar(caminho, corpo) {
  let resposta;
  try {
    resposta = await fetch(`${BASE}${caminho}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(corpo),
    });
  } catch {
    throw new Error('Não foi possível conectar ao servidor. Verifique se o gateway está em execução.');
  }
  const dados = await resposta.json().catch(() => ({}));
  if (!resposta.ok) {
    const d = dados.detail;
    const mensagem = typeof d === 'string' ? d : (d?.mensagens || []).join(' ') || `Erro ${resposta.status}.`;
    const erro = new Error(mensagem);
    erro.codigo = d?.codigo;
    throw erro;
  }
  return dados;
}

export const avaliar = (respostas) => postar('/api/avaliacao', montarEntrada(respostas));
/** Só chamada depois do consentimento explícito na tela de resultado (parecer de Ética, C1/C2). */
export const explicar = (respostas) =>
  postar('/api/avaliacao/explicacao', { ...montarEntrada(respostas), consentimento_envio_llm: true });
