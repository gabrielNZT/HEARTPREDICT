import { useEffect, useRef, useState } from 'react';
import { Botao, Progresso } from '../componentes/Estrutura';
import { CampoNumero, GrupoOpcoes, ResumoErros } from '../componentes/Campos';
import { MOTIVOS_FORA_DO_ESCOPO, NENHUMA, opcoesVisiveis, rotuloDaOpcao } from '../conteudo/perguntas';
import { validar } from '../validacao';
import { useTituloDaTela } from '../utilitarios/useTituloDaTela';
import './telas.css';


export function TelaInicio({ aoComecar, temRespostas, aoRecomecar }) {
  useTituloDaTela('Risco cardiovascular em 10 anos');
  return (
    <div className="entrar inicio">
      <h1 tabIndex={-1} data-titulo-tela="">Calcule o seu risco de infarto e AVC nos próximos 10 anos</h1>
      <p className="inicio__lead">
        Use os resultados do seu último exame de sangue e a sua pressão. São 14 perguntas curtas,
        cerca de 3 minutos.
      </p>
      {temRespostas ? (
        <div className="acoes">
          <Botao onClick={aoComecar}>Continuar de onde parei</Botao>
          <Botao variante="texto" onClick={aoRecomecar}>Começar de novo</Botao>
        </div>
      ) : (
        <Botao onClick={aoComecar}>Começar</Botao>
      )}

      <section className="inicio__secao">
        <h2>Para quem é</h2>
        <ul>
          <li>Pessoas de 30 a 79 anos.</li>
          <li>Que nunca tiveram infarto, AVC ou outra doença cardiovascular, nem placa nas artérias em exame de imagem.</li>
          <li>Que não têm diabetes. Nesta versão, quem tem diabetes ainda não é avaliado.</li>
        </ul>
      </section>

      <section className="inicio__secao">
        <h2>O que ter em mãos</h2>
        <ul>
          <li>Colesterol total e HDL. O LDL também ajuda, mas é opcional.</li>
          <li>Uma medida recente da pressão arterial.</li>
          <li>TFG estimada ou creatinina, do mesmo exame de sangue.</li>
        </ul>
      </section>

      <section className="inicio__secao">
        <h2>Como o resultado é produzido</h2>
        <ol className="passos">
          <li><strong>A equação PREVENT</strong>, da American Heart Association, calcula o risco de infarto ou AVC em 10 anos.</li>
          <li><strong>A Diretriz Brasileira de Dislipidemias 2025</strong> define a sua categoria de risco e a meta de colesterol LDL.</li>
          <li><strong>Um modelo de inteligência artificial</strong> escreve uma explicação em linguagem simples a partir desses números. Ele não faz o cálculo.</li>
        </ol>
      </section>

      <section className="inicio__secao">
        <h2>Seus dados</h2>
        <p>
          Não pedimos nome nem documento, e este sistema não guarda as suas respostas: o cálculo é feito e
          descartado. A explicação em linguagem simples é opcional. Ela só é gerada se você pedir, na tela de
          resultado, e aí os valores informados, sem identificação, são enviados a um serviço de inteligência
          artificial externo, que pode ficar fora do Brasil e tem as próprias regras de uso de dados.
        </p>
      </section>

      <p className="nota">
        Este é um protótipo de pesquisa. O resultado é uma estimativa e não substitui a avaliação de um
        profissional de saúde.
      </p>
    </div>
  );
}

export function TelaPergunta({ pergunta, indice, total, respostas, aoResponder, aoVoltar }) {
  const inicial = pergunta.tipo === 'numero' && respostas[pergunta.id] != null
    ? String(respostas[pergunta.id]).replace('.', ',')
    : pergunta.tipo === 'renal' && respostas.renal
      ? { tipo: respostas.renal.tipo, valor: String(respostas.renal.valor ?? '').replace('.', ',') }
      : respostas[pergunta.id];
  const [bruto, setBruto] = useState(inicial);
  const [erros, setErros] = useState([]);
  useTituloDaTela(`Pergunta ${indice} de ${total}`);

  function enviar(e) {
    e.preventDefault();
    const { valor, erros: novos } = validar(pergunta, bruto, respostas);
    setErros(novos);
    if (!novos.length) aoResponder(valor);
  }

  const erroDe = (campo) => erros.find((x) => x.campo === campo)?.mensagem;

  let corpo;
  if (pergunta.tipo === 'numero') {
    corpo = (
      <CampoNumero id={pergunta.id} rotulo={pergunta.titulo} rotuloComoTitulo dica={pergunta.dica}
        unidade={pergunta.unidade} valor={bruto} aoMudar={setBruto} erro={erroDe(pergunta.id)} />
    );
  } else if (pergunta.tipo === 'escolha' || pergunta.tipo === 'multipla') {
    corpo = (
      <GrupoOpcoes id={pergunta.id} titulo={pergunta.titulo} dica={pergunta.dica}
        opcoes={opcoesVisiveis(pergunta, respostas)} valor={bruto} aoMudar={setBruto}
        erro={erroDe(pergunta.id)} multipla={pergunta.tipo === 'multipla'} exclusiva={pergunta.nenhuma} />
    );
  } else if (pergunta.tipo === 'renal') {
    const atual = bruto || {};
    corpo = (
      <GrupoOpcoes id={pergunta.id} titulo={pergunta.titulo} dica={pergunta.dica} opcoes={pergunta.opcoes}
        valor={atual.tipo} aoMudar={(tipo) => setBruto({ tipo, valor: '' })} erro={erroDe(pergunta.id)}
        filhos={(o) => (
          <div className="revelado">
            <CampoNumero id={`${pergunta.id}-valor`} rotulo={o.campo} unidade={o.unidade}
              valor={atual.valor} aoMudar={(valor) => setBruto({ ...atual, valor })}
              erro={erroDe(`${pergunta.id}-valor`)} />
          </div>
        )}
      />
    );
  }

  return (
    <form className="entrar" onSubmit={enviar} noValidate key={pergunta.id}>
      <Progresso atual={indice} total={total} />
      <ResumoErros erros={erros} />
      {corpo}
      <div className="acoes">
        <Botao type="submit">Continuar</Botao>
        <Botao type="button" variante="texto" onClick={aoVoltar}>Voltar</Botao>
      </div>
    </form>
  );
}

export function TelaForaDoEscopo({ motivo, aoAlterar, aoRecomecar }) {
  const m = MOTIVOS_FORA_DO_ESCOPO[motivo];
  useTituloDaTela(m.titulo);
  return (
    <div className="entrar">
      <h1 tabIndex={-1} data-titulo-tela="">{m.titulo}</h1>
      {m.texto.map((t) => <p key={t}>{t}</p>)}
      <div className="acoes">
        <Botao variante="secundario" onClick={aoAlterar}>Alterar minha resposta</Botao>
        <Botao variante="texto" onClick={aoRecomecar}>Voltar ao início</Botao>
      </div>
    </div>
  );
}

function formatarResposta(pergunta, valor) {
  if (pergunta.tipo === 'numero') return pergunta.formatar(valor == null ? null : String(valor).replace('.', ','));
  if (pergunta.tipo === 'escolha') return rotuloDaOpcao(pergunta, valor);
  if (pergunta.tipo === 'renal') {
    const o = pergunta.opcoes.find((x) => x.valor === valor?.tipo);
    return o ? `${o.rotuloRevisao}: ${String(valor.valor).replace('.', ',')} ${o.unidade}` : '';
  }
  if (pergunta.tipo === 'multipla') {
    if (!valor?.length || valor.includes(NENHUMA)) return pergunta.nenhuma;
    return valor.map((v) => rotuloDaOpcao(pergunta, v)).join('; ');
  }
  return String(valor);
}

/** Revisão antes de enviar (padrão "check answers" da GOV.UK). */
export function TelaRevisao({ perguntas, respostas, aoAlterar, aoConfirmar, enviando, erro }) {
  useTituloDaTela('Confira suas respostas');
  const ref = useRef(null);
  useEffect(() => {
    if (erro) ref.current?.focus();
  }, [erro]);
  return (
    <div className="entrar">
      <h1 tabIndex={-1} data-titulo-tela="">Confira suas respostas</h1>
      <p>Se algo estiver errado, use “Alterar”. O resultado é calculado quando você confirmar.</p>
      {erro && (
        <div className="resumo-erros" role="alert" tabIndex={-1} ref={ref}>
          <h2 className="resumo-erros__titulo">Não foi possível calcular</h2>
          <p>{erro}</p>
        </div>
      )}
      <dl className="revisao">
        {perguntas.map((p) => (
          <div key={p.id} className="revisao__linha">
            <dt>{p.rotuloRevisao}</dt>
            <dd className="numero">{formatarResposta(p, respostas[p.id])}</dd>
            <dd className="revisao__acao">
              <button type="button" className="botao botao--texto" onClick={() => aoAlterar(p.id)}>
                Alterar<span className="visualmente-oculto"> {p.rotuloRevisao.toLowerCase()}</span>
              </button>
            </dd>
          </div>
        ))}
      </dl>
      <div className="acoes">
        <Botao onClick={aoConfirmar} disabled={enviando} aria-disabled={enviando}>
          {enviando ? 'Calculando…' : 'Confirmar e ver o resultado'}
        </Botao>
      </div>
    </div>
  );
}
