import './estrutura.css';

/** Símbolo: grade 10 × 10 com um ponto destacado — síntese do pictograma "1 em 100" (interface-design.md §3.2). */
export function Marca({ tamanho = 32 }) {
  const pontos = [];
  for (let l = 0; l < 4; l++) {
    for (let c = 0; c < 4; c++) {
      const destaque = l === 1 && c === 1;
      pontos.push(
        <circle key={`${l}-${c}`} cx={8 + c * 8} cy={8 + l * 8} r={destaque ? 3 : 2}
          fill={destaque ? 'var(--acento)' : 'var(--sem-evento)'} />,
      );
    }
  }
  return (
    <svg width={tamanho} height={tamanho} viewBox="0 0 40 40" aria-hidden="true" focusable="false">
      {pontos}
    </svg>
  );
}

export function Cabecalho({ aoIrParaInicio }) {
  return (
    <header className="cabecalho">
      <div className="cabecalho__interno">
        <a href="#/" className="cabecalho__marca" onClick={aoIrParaInicio}>
          <Marca />
          <span>
            <span className="cabecalho__nome">HeartPredict</span>
            <span className="cabecalho__descritor">Risco cardiovascular em 10 anos</span>
          </span>
        </a>
        <span className="cabecalho__selo">Protótipo acadêmico</span>
      </div>
    </header>
  );
}

export function Rodape() {
  return (
    <footer className="rodape">
      <div className="rodape__interno">
        <p>
          Protótipo desenvolvido em um Trabalho de Conclusão de Curso de Engenharia de Computação.
          Não substitui a avaliação de um profissional de saúde.
        </p>
        <p>
          Cálculo: equação PREVENT (American Heart Association, 2024). Categorias e metas: Diretriz
          Brasileira de Dislipidemias e Prevenção da Aterosclerose (SBC, 2025).
        </p>
      </div>
    </footer>
  );
}

export function Progresso({ atual, total }) {
  return (
    <div className="progresso">
      <p className="progresso__texto">Pergunta {atual} de {total}</p>
      <div className="progresso__trilho" aria-hidden="true">
        <div className="progresso__barra" style={{ width: `${(atual / total) * 100}%` }} />
      </div>
    </div>
  );
}

export function Botao({ variante = 'primario', ...props }) {
  return <button className={`botao botao--${variante}`} {...props} />;
}
