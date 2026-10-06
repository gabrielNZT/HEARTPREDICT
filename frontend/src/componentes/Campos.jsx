import { useEffect, useRef } from 'react';
import { NENHUMA } from '../conteudo/perguntas';
import './campos.css';

/** Resumo de erros no topo, com links para os campos (padrão "error summary" da GOV.UK). */
export function ResumoErros({ erros }) {
  const ref = useRef(null);
  useEffect(() => {
    if (erros.length) ref.current?.focus();
  }, [erros]);
  if (!erros.length) return null;
  return (
    <div className="resumo-erros" role="alert" tabIndex={-1} ref={ref} aria-labelledby="resumo-erros-titulo">
      <h2 id="resumo-erros-titulo" className="resumo-erros__titulo">Corrija para continuar</h2>
      <ul>
        {erros.map((e) => (
          <li key={e.campo + e.mensagem}>
            <a href={`#campo-${e.campo}`} onClick={(ev) => {
              ev.preventDefault();
              document.getElementById(`campo-${e.campo}`)?.focus();
            }}>{e.mensagem}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

/**
 * Campo numérico: rótulo acima, dica abaixo do rótulo, unidade fora do campo (NN/g: sem placeholder).
 * type="text" + inputMode="decimal": teclado numérico no celular e aceita vírgula (GOV.UK desaconselha type="number").
 */
export function CampoNumero({ id, rotulo, rotuloComoTitulo, dica, unidade, valor, aoMudar, erro, largura = '8ch' }) {
  const idDica = dica ? `dica-${id}` : undefined;
  const idErro = erro ? `erro-${id}` : undefined;
  const rotuloEl = <label htmlFor={`campo-${id}`} className="campo__rotulo">{rotulo}</label>;
  return (
    <div className={`campo ${erro ? 'campo--erro' : ''}`}>
      {rotuloComoTitulo
        ? <h1 className="campo__titulo" tabIndex={-1} data-titulo-tela="">{rotuloEl}</h1>
        : <div className="campo__subrotulo">{rotuloEl}</div>}
      {dica && <p id={idDica} className="campo__dica">{dica}</p>}
      {erro && <p id={idErro} className="campo__erro"><span className="visualmente-oculto">Erro: </span>{erro}</p>}
      <div className="campo__linha">
        <input
          id={`campo-${id}`}
          className="campo__entrada numero"
          type="text"
          inputMode="decimal"
          autoComplete="off"
          spellCheck={false}
          value={valor ?? ''}
          onChange={(e) => aoMudar(e.target.value)}
          aria-describedby={[idDica, idErro].filter(Boolean).join(' ') || undefined}
          aria-invalid={erro ? 'true' : undefined}
          style={{ width: `calc(${largura} + 1.5rem)` }}
        />
        {unidade && <span className="campo__unidade">{unidade}</span>}
      </div>
    </div>
  );
}

/**
 * Opções como cartões inteiros clicáveis, com input nativo (teclado e leitor de tela funcionam sem código extra).
 * `multipla`: caixas de seleção; `exclusiva` desmarca as demais (ex.: "Nenhuma destas").
 */
export function GrupoOpcoes({ id, titulo, dica, opcoes, valor, aoMudar, erro, multipla = false, exclusiva, filhos }) {
  const idDica = dica ? `dica-${id}` : undefined;
  const idErro = erro ? `erro-${id}` : undefined;
  const marcado = (v) => (multipla ? (valor || []).includes(v) : valor === v);

  function alternar(v) {
    if (!multipla) return aoMudar(v);
    const atual = valor || [];
    if (v === NENHUMA) return aoMudar(atual.includes(v) ? [] : [v]);
    const sem = atual.filter((x) => x !== NENHUMA);
    aoMudar(sem.includes(v) ? sem.filter((x) => x !== v) : [...sem, v]);
  }

  const todas = exclusiva ? [...opcoes, { valor: NENHUMA, rotulo: exclusiva, separada: true }] : opcoes;

  return (
    <fieldset className={`grupo ${erro ? 'campo--erro' : ''}`} aria-describedby={[idDica, idErro].filter(Boolean).join(' ') || undefined}>
      <legend className="grupo__legenda">
        <h1 className="campo__titulo" tabIndex={-1} data-titulo-tela="">{titulo}</h1>
      </legend>
      {dica && <p id={idDica} className="campo__dica">{dica}</p>}
      {erro && <p id={idErro} className="campo__erro"><span className="visualmente-oculto">Erro: </span>{erro}</p>}
      <div className="grupo__opcoes">
        {todas.map((o, i) => (
          <div key={o.valor}>
            {o.separada && <p className="grupo__ou">ou</p>}
            {/* Rótulo curto como nome acessível; dica ligada por aria-describedby (GOV.UK). O cartão
                inteiro continua clicável porque o ::after do rótulo cobre o cartão. */}
            <div className={`opcao ${marcado(o.valor) ? 'opcao--marcada' : ''}`}>
              <input
                id={i === 0 ? `campo-${id}` : `opcao-${id}-${o.valor}`}
                type={multipla ? 'checkbox' : 'radio'}
                name={id}
                value={o.valor}
                checked={marcado(o.valor)}
                onChange={() => alternar(o.valor)}
                aria-describedby={o.dica ? `dica-${id}-${o.valor}` : undefined}
              />
              <span className="opcao__texto">
                <label className="opcao__rotulo" htmlFor={i === 0 ? `campo-${id}` : `opcao-${id}-${o.valor}`}>{o.rotulo}</label>
                {o.dica && <span id={`dica-${id}-${o.valor}`} className="opcao__dica">{o.dica}</span>}
              </span>
            </div>
            {!multipla && marcado(o.valor) && filhos?.(o)}
          </div>
        ))}
      </div>
    </fieldset>
  );
}
