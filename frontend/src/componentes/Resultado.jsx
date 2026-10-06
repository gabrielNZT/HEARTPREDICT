import './resultado.css';

/**
 * Pictograma de 100 pessoas, eventos agrupados no início.
 * Figuras humanas simples: melhor memorização do risco que blocos ou ovais numa calculadora
 * cardiovascular (Zikmund-Fisher et al. 2014). Único uso de ícone na interface (interface-design.md §3.5).
 */
export function Pictograma({ eventos, descricao }) {
  const n = Math.max(0, Math.min(100, eventos));
  return (
    <div className="pictograma" role="img" aria-label={descricao}>
      <svg width="0" height="0" aria-hidden="true" style={{ position: 'absolute' }}>
        <symbol id="pessoa" viewBox="0 0 12 16">
          <circle cx="6" cy="3" r="2.6" />
          <path d="M1.6 15.2V9.4a3.4 3.4 0 0 1 3.4-3.4h2a3.4 3.4 0 0 1 3.4 3.4v5.8z" />
        </symbol>
      </svg>
      {Array.from({ length: 100 }, (_, i) => (
        <svg key={i} viewBox="0 0 12 16" className={i < n ? 'pessoa pessoa--evento' : 'pessoa'} aria-hidden="true">
          <use href="#pessoa" />
        </svg>
      ))}
    </div>
  );
}

const CATEGORIAS = [
  { id: 'baixo', rotulo: 'Baixo', faixa: 'menos de 5%' },
  { id: 'intermediário', rotulo: 'Intermediário', faixa: '5% a menos de 20%' },
  { id: 'alto', rotulo: 'Alto', faixa: '20% ou mais' },
];

/**
 * Escala ordinal de faixas iguais (ordinal, não proporcional); cor sequencial + texto + posição (WCAG 1.4.1).
 * Quando a diretriz reclassifica, marca as duas coisas: a faixa em que o número calculado cai e a
 * categoria final. Antes só a final era marcada, e 7,1% aparecia ao lado de "20% ou mais" (parecer de IHC).
 */
export function EscalaCategoria({ categoria, categoriaDoCalculo }) {
  const reclassificado = categoriaDoCalculo && categoriaDoCalculo !== categoria;
  return (
    <ol className="escala" aria-label="Categorias de risco da Diretriz SBC 2025">
      {CATEGORIAS.map((c, i) => {
        const atual = c.id === categoria;
        const doCalculo = reclassificado && c.id === categoriaDoCalculo;
        return (
          <li key={c.id} className={`escala__faixa escala__faixa--${i} ${atual ? 'escala__faixa--atual' : ''} ${doCalculo ? 'escala__faixa--calculo' : ''}`}
            aria-current={atual ? 'true' : undefined}>
            <span className="escala__cor" aria-hidden="true" />
            <span className="escala__rotulo">{c.rotulo}</span>
            <span className="escala__intervalo">pelo cálculo: {c.faixa}</span>
            {doCalculo && <span className="escala__marcador escala__marcador--calculo">Seu número cai aqui</span>}
            {atual && <span className="escala__marcador">{reclassificado ? 'Sua categoria pela diretriz' : 'Sua categoria'}</span>}
          </li>
        );
      })}
    </ol>
  );
}

const GRUPOS = [
  { direcao: 'aumentou', titulo: 'Aumentaram o seu risco' },
  { direcao: 'diminuiu', titulo: 'Diminuíram o seu risco' },
  { direcao: 'pouco influenciou', titulo: 'Pouco influenciaram' },
];

/** Remédio aparece como a condição tratada (parecer de Cardiologia, C1): o coeficiente capta a indicação. */
const NOMES_NA_TELA = {
  anti_hipertensivo: 'pressão alta em tratamento',
  estatina: 'colesterol alto em tratamento com estatina',
};

const REMEDIOS = {
  anti_hipertensivo: { remedio: 'remédio para pressão', condicao: 'pressão alta' },
  estatina: { remedio: 'remédio para colesterol', condicao: 'colesterol alto' },
};

/** Fatores em palavras + barras proporcionais à contribuição (atribuição de Shapley, D012). */
export function ListaFatores({ fatores, valorDe }) {
  // Aviso visível, não escondido no "Como ler" (parecer de Cardiologia, C1): uso de remédio aparecendo
  // como fator que aumentou o risco pode levar alguém a parar o tratamento.
  const remediosQueAumentaram = fatores
    .filter((f) => f.direcao === 'aumentou' && REMEDIOS[f.variavel])
    .map((f) => REMEDIOS[f.variavel]);
  const juntar = (campo) => remediosQueAumentaram.map((x) => x[campo]).join(' e ');
  const maximo = Math.max(...fatores.map((f) => Math.abs(f.contribuicao)), 1e-9);
  return (
    <div className="fatores">
      {GRUPOS.map((g) => {
        const itens = fatores.filter((f) => f.direcao === g.direcao);
        if (!itens.length) return null;
        return (
          <section key={g.direcao} className="fatores__grupo">
            <h3 className="fatores__titulo">{g.titulo}</h3>
            <ul className="fatores__lista">
              {itens.map((f) => (
                <li key={f.variavel} className="fator">
                  <div className="fator__texto">
                    <span className="fator__nome">{primeiraMaiuscula(NOMES_NA_TELA[f.variavel] || f.nome)}</span>
                    <span className="fator__valor numero">{valorDe(f.variavel)}</span>
                  </div>
                  <div className="fator__trilho" aria-hidden="true">
                    <div className={`fator__barra fator__barra--${g.direcao === 'aumentou' ? 'mais' : 'menos'}`}
                      style={{ width: `${Math.max(3, (Math.abs(f.contribuicao) / maximo) * 100)}%` }} />
                  </div>
                </li>
              ))}
            </ul>
          </section>
        );
      })}
      {remediosQueAumentaram.length > 0 && (
        <div className="aviso-remedio">
          <p>
            <strong>Não pare nenhum remédio por causa deste resultado.</strong> O uso de {juntar('remedio')}{' '}
            aparece como fator que aumentou o risco porque, na equação, indica que a pessoa tem{' '}
            {juntar('condicao')} em tratamento. O remédio em si não aumenta o risco.
          </p>
        </div>
      )}
      <details className="como-ler">
        <summary>Como ler esta seção</summary>
        <p>
          O cálculo compara você com uma pessoa de referência: 55 anos, colesterol não-HDL de 135 mg/dL,
          HDL de 50 mg/dL, pressão sistólica de 130 mmHg, TFG estimada de 90, que não fuma, não tem diabetes e
          não usa remédios.
          As barras mostram o quanto cada fator puxou o seu risco para cima ou para baixo em relação a essa
          pessoa. Barras maiores pesaram mais.
        </p>
        <p>
          Por isso, ter menos de 55 anos aparece como fator que diminuiu o risco. E usar remédio para pressão ou
          para colesterol pode aparecer como fator que aumentou: no cálculo, ele indica que a pessoa tem pressão
          alta ou colesterol alto em tratamento. Isso não significa que o remédio faça mal. Não pare nenhum
          remédio sem falar com seu médico.
        </p>
      </details>
    </div>
  );
}

/**
 * Explicação do LLM: só é pedida depois de a pessoa consentir com o envio (LGPD art. 11, I; parecer de
 * Ética). Rotulada como texto de IA (boa prática de transparência inspirada no AI Act, art. 50, que não
 * se aplica a este protótipo) e como ainda não verificada.
 */
export function Explicacao({ estado, aoPedir, aoTentarDeNovo }) {
  return (
    <section className="explicacao" aria-labelledby="titulo-explicacao" aria-busy={estado.tipo === 'carregando'}>
      <h2 id="titulo-explicacao">Explicação em linguagem simples</h2>
      <p className="explicacao__selo">Texto gerado por inteligência artificial</p>
      {estado.tipo === 'aguardando' && (
        <div className="explicacao__consentimento">
          <p>
            Um modelo de inteligência artificial pode escrever um texto explicando o resultado acima. Para isso,
            os valores que você informou e o resultado do cálculo são enviados, sem nome nem documento, a um
            serviço externo de IA. Esse serviço pode ficar fora do Brasil e tem as próprias regras sobre o uso
            dos dados.
          </p>
          <p>O resultado acima não depende deste texto. Se preferir, não gere a explicação.</p>
          <button className="botao botao--secundario" onClick={aoPedir}>Concordo e quero gerar a explicação</button>
        </div>
      )}
      {estado.tipo === 'carregando' && (
        <div className="explicacao__carregando">
          <p aria-live="polite">Gerando a explicação. Isso pode levar alguns segundos.</p>
          <div className="linhas-fantasma" aria-hidden="true"><span /><span /><span /></div>
        </div>
      )}
      {estado.tipo === 'erro' && (
        <div className="explicacao__erro">
          <p>{estado.mensagem}</p>
          <p>O resultado acima não depende deste texto e continua válido.</p>
          <button className="botao botao--secundario" onClick={aoTentarDeNovo}>Tentar de novo</button>
        </div>
      )}
      {estado.tipo === 'ok' && (
        <>
          <div className="explicacao__texto entrar">
            {estado.dados.texto.split(/\n{2,}/).map((p, i) => <p key={i}>{p}</p>)}
          </div>
          <p className="nota explicacao__aviso">
            Este texto foi escrito por um modelo de linguagem ({estado.dados.modelo}) a partir dos números
            acima. Nesta versão, ele <strong>ainda não passa pelo verificador automático</strong> do projeto.
            Se algo no texto divergir dos números, considere os números.
          </p>
        </>
      )}
    </section>
  );
}

function primeiraMaiuscula(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}
