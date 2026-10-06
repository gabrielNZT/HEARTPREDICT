import { useEffect, useState } from 'react';
import { avaliar } from './api';
import { Cabecalho, Rodape } from './componentes/Estrutura';
import { MOTIVOS_FORA_DO_ESCOPO, NENHUMA, PERGUNTAS, opcoesVisiveis } from './conteudo/perguntas';
import { TelaForaDoEscopo, TelaInicio, TelaPergunta, TelaRevisao } from './telas/Telas';
import { TelaResultado } from './telas/TelaResultado';

/*
 * Cada etapa tem um endereço (#/p/idade, #/revisao...), para o botão "Voltar" do navegador funcionar.
 * As respostas ficam só na memória da página: nada é salvo no navegador (interface-design.md §7).
 */
function lerRota() {
  const partes = window.location.hash.replace(/^#\/?/, '').split('/');
  return { tela: partes[0] || 'inicio', parametro: partes[1] };
}

function ir(caminho) {
  window.location.hash = `#/${caminho}`;
}

const indiceDe = (id) => PERGUNTAS.findIndex((p) => p.id === id);

export default function App() {
  const [rota, setRota] = useState(lerRota);
  const [respostas, setRespostas] = useState({});
  const [voltarParaRevisao, setVoltarParaRevisao] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [enviando, setEnviando] = useState(false);
  const [erroEnvio, setErroEnvio] = useState(null);

  useEffect(() => {
    const aoMudar = () => setRota(lerRota());
    window.addEventListener('hashchange', aoMudar);
    return () => window.removeEventListener('hashchange', aoMudar);
  }, []);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [rota]);

  const primeiraSemResposta = PERGUNTAS.find(
    (p) => (!p.opcional || p.obrigatorioSe?.(respostas)) && respostas[p.id] == null,
  );

  function responder(pergunta, valor) {
    const novas = { ...respostas, [pergunta.id]: valor };
    const invalidada = revalidarDependentes(novas);
    setRespostas(novas);
    setResultado(null);
    if (pergunta.foraDoEscopo?.(valor)) return ir(`fora/${pergunta.id}`);
    if (invalidada) return ir(`p/${invalidada}`); // pede de novo a resposta que deixou de valer
    if (voltarParaRevisao) {
      setVoltarParaRevisao(false);
      return ir('revisao');
    }
    const proxima = PERGUNTAS[indiceDe(pergunta.id) + 1];
    ir(proxima ? `p/${proxima.id}` : 'revisao');
  }

  function recomecar() {
    setRespostas({});
    setResultado(null);
    setErroEnvio(null);
    setVoltarParaRevisao(false);
    ir('');
  }

  async function confirmar() {
    setEnviando(true);
    setErroEnvio(null);
    try {
      setResultado(await avaliar(respostas));
      ir('resultado');
    } catch (e) {
      setErroEnvio(e.message);
    } finally {
      setEnviando(false);
    }
  }

  let tela;
  if (rota.tela === 'p' && indiceDe(rota.parametro) >= 0) {
    const i = indiceDe(rota.parametro);
    const pergunta = PERGUNTAS[i];
    tela = (
      <TelaPergunta key={pergunta.id} pergunta={pergunta} indice={i + 1} total={PERGUNTAS.length}
        respostas={respostas} aoResponder={(v) => responder(pergunta, v)}
        aoVoltar={() => ir(i === 0 ? '' : `p/${PERGUNTAS[i - 1].id}`)} />
    );
  } else if (rota.tela === 'fora' && motivoValido(rota.parametro)) {
    tela = <TelaForaDoEscopo motivo={rota.parametro} aoAlterar={() => ir(`p/${rota.parametro}`)} aoRecomecar={recomecar} />;
  } else if (rota.tela === 'revisao' && !primeiraSemResposta) {
    tela = (
      <TelaRevisao perguntas={PERGUNTAS} respostas={respostas} enviando={enviando} erro={erroEnvio}
        aoAlterar={(id) => { setVoltarParaRevisao(true); ir(`p/${id}`); }} aoConfirmar={confirmar} />
    );
  } else if (rota.tela === 'resultado' && resultado) {
    tela = <TelaResultado resultado={resultado} respostas={respostas} aoRecomecar={recomecar} />;
  } else if (rota.tela === 'revisao' && primeiraSemResposta && Object.keys(respostas).length) {
    ir(`p/${primeiraSemResposta.id}`);
  } else {
    tela = (
      <TelaInicio aoComecar={() => ir(primeiraSemResposta ? `p/${primeiraSemResposta.id}` : 'revisao')}
        temRespostas={Object.keys(respostas).length > 0} aoRecomecar={recomecar} />
    );
  }

  return (
    <>
      <a href="#conteudo" className="pular" onClick={(e) => {
        e.preventDefault();
        document.getElementById('conteudo')?.focus();
      }}>Pular para o conteúdo</a>
      <Cabecalho aoIrParaInicio={(e) => { e.preventDefault(); ir(''); }} />
      <main id="conteudo" className="conteudo" tabIndex={-1}>{tela}</main>
      <Rodape />
    </>
  );
}

/**
 * Remove opções que deixaram de valer após uma mudança (ex.: "situações da saúde da mulher" quando o
 * sexo muda para masculino). Se a resposta ficar vazia, apaga-a e devolve o id da pergunta para
 * ser respondida de novo (padrão "check answers" da GOV.UK: mudanças que afetam outras respostas).
 */
function revalidarDependentes(respostas) {
  for (const p of PERGUNTAS) {
    if (p.tipo !== 'multipla' || !Array.isArray(respostas[p.id])) continue;
    const validos = new Set(opcoesVisiveis(p, respostas).map((o) => o.valor).concat([NENHUMA]));
    const filtrada = respostas[p.id].filter((v) => validos.has(v));
    if (filtrada.length === respostas[p.id].length) continue;
    if (filtrada.length) {
      respostas[p.id] = filtrada;
    } else {
      delete respostas[p.id];
      return p.id;
    }
  }
  return null;
}

function motivoValido(id) {
  return Object.keys(MOTIVOS_FORA_DO_ESCOPO).includes(id);
}
