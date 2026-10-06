import { useCallback, useEffect, useState } from 'react';
import { explicar } from '../api';
import { Botao } from '../componentes/Estrutura';
import { EscalaCategoria, Explicacao, ListaFatores, Pictograma } from '../componentes/Resultado';
import { fmtNumero as fmt, fmtPct } from '../utilitarios/formato';
import { useTituloDaTela } from '../utilitarios/useTituloDaTela';

function fraseFrequencia(n, pct) {
  if (n === 0) return 'Em 100 pessoas com os mesmos dados, menos de 1 teria um infarto ou AVC em 10 anos.';
  // Evita "cerca de 5" ao lado de "menos de 5%" (e 20 × "menos de 20%"): parecer de Cardiologia, m1
  const quase = (n === 5 && pct < 5) || (n === 20 && pct < 20) ? 'pouco menos de' : 'cerca de';
  if (n === 1) return `Em 100 pessoas com os mesmos dados, ${quase} 1 teria um infarto ou AVC em 10 anos.`;
  return `Em 100 pessoas com os mesmos dados, ${quase} ${n} teriam um infarto ou AVC em 10 anos.`;
}

/** Tela de resultado em pirâmide invertida (interface-design.md §5). */
export function TelaResultado({ resultado, respostas, aoRecomecar }) {
  useTituloDaTela('Seu resultado');
  const [explicacao, setExplicacao] = useState({ tipo: 'aguardando' });

  const pedirExplicacao = useCallback(() => {
    setExplicacao({ tipo: 'carregando' });
    explicar(respostas)
      .then((dados) => setExplicacao({ tipo: 'ok', dados }))
      .catch((e) => {
        console.warn('Explicação indisponível:', e.message);
        setExplicacao({ tipo: 'erro', mensagem: 'Não foi possível gerar a explicação agora.' });
      });
  }, [respostas]);

  // Na impressão, abre o "Como ler" para que a explicação das barras vá junto (parecer de IHC).
  useEffect(() => {
    const abrir = () => document.querySelectorAll('details').forEach((d) => { d.open = true; });
    window.addEventListener('beforeprint', abrir);
    return () => window.removeEventListener('beforeprint', abrir);
  }, []);

  const r = resultado;
  const reclassificado = r.regras_aplicadas.length > 1;
  const categoriaDoEscore = r.risco_pct < 5 ? 'baixo' : r.risco_pct < 20 ? 'intermediário' : 'alto';

  const valorDe = (variavel) => ({
    idade: `${respostas.idade} anos`,
    nao_hdl: `${fmt(respostas.colesterol_total - respostas.hdl)} mg/dL`,
    hdl: `${fmt(respostas.hdl)} mg/dL`,
    pas: `${respostas.pas} mmHg`,
    anti_hipertensivo: respostas.anti_hipertensivo === 'sim' ? 'usa remédio' : 'não usa remédio',
    estatina: respostas.estatina === 'sim' ? 'usa estatina' : 'não usa estatina',
    tabagismo: respostas.tabagismo === 'sim' ? 'fuma' : 'não fuma',
    tfge: `${r.tfge_usada} mL/min/1,73 m²`,
    diabetes: 'não',
  }[variavel]);

  return (
    <div className="entrar">
      <section className="destaque" aria-labelledby="titulo-resultado">
        <h1 id="titulo-resultado" tabIndex={-1} data-titulo-tela="" className="visualmente-oculto">Seu resultado</h1>
        <p className="nota">Risco estimado de infarto ou AVC nos próximos 10 anos</p>
        <p className="destaque__numero numero">{fmtPct(r.risco_pct)}</p>
        <p className="destaque__frase">{fraseFrequencia(r.em_100_pessoas, r.risco_pct)}</p>
        <Pictograma eventos={r.em_100_pessoas}
          descricao={`Grade de 100 pessoas, das quais ${r.em_100_pessoas} estão destacadas.`} />
        <p className="legenda-pictograma">
          <span className="com">teriam infarto ou AVC</span>
          <span className="sem">não teriam</span>
        </p>
      </section>

      <section className="bloco" aria-labelledby="titulo-categoria">
        <h2 id="titulo-categoria">Sua categoria de risco: {r.categoria}</h2>
        <EscalaCategoria categoria={r.categoria} categoriaDoCalculo={categoriaDoEscore} />
        {reclassificado ? (
          <p className="reclassificacao">
            Pelo cálculo, o risco seria <strong>{categoriaDoEscore}</strong>.
            {r.agravantes.length > 0 && <> A diretriz eleva a categoria quando há {r.agravantes.join('; ')}.</>}
            {respostas.ldl >= 160 && <> O LDL de {fmt(respostas.ldl)} mg/dL também é considerado pela diretriz.</>}
            {r.criterios_alto?.length > 0 && <> A diretriz classifica como risco alto quem tem {r.criterios_alto.join('; ')}.</>}
            {' '}Por isso, a sua categoria é <strong>{r.categoria}</strong>.
          </p>
        ) : (
          <p>A categoria segue a Diretriz Brasileira de Dislipidemias e Prevenção da Aterosclerose (SBC, 2025).</p>
        )}
      </section>

      <section className="bloco" aria-labelledby="titulo-meta">
        <h2 id="titulo-meta">Meta de colesterol para a sua categoria</h2>
        <div className="metas">
          <div className="meta">
            <p className="meta__rotulo">LDL-c</p>
            <p className="meta__valor numero">{r.metas.ldl} mg/dL</p>
          </div>
          <div className="meta">
            <p className="meta__rotulo">Não-HDL-c</p>
            <p className="meta__valor numero">{r.metas.nao_hdl} mg/dL</p>
          </div>
        </div>
        <p>
          {respostas.ldl != null
            ? <>Seu LDL informado é <strong className="numero">{fmt(respostas.ldl)} mg/dL</strong>. </>
            : null}
          {r.categoria === 'baixo'
            ? <>No risco baixo, a diretriz indica remédio só se o LDL continuar em 145 mg/dL ou mais depois de mudanças no estilo de vida. </>
            : <>Se for preciso tratar, a diretriz recomenda reduzir o LDL em pelo menos {r.metas.reducao_ldl.replace('≥ ', '')}. </>}
          {respostas.estatina === 'sim' && <>Como você já usa estatina, o LDL informado é o valor durante o tratamento. </>}
          A decisão sobre tratamento é sempre do seu médico.
        </p>
      </section>

      <section className="bloco" aria-labelledby="titulo-fatores">
        <h2 id="titulo-fatores">O que mais pesou no seu resultado</h2>
        <ListaFatores fatores={r.fatores} valorDe={valorDe} />
        {r.origem_tfge !== 'informada' && (
          <p className="nota">A TFG estimada ({r.tfge_usada} mL/min/1,73 m²) foi {r.origem_tfge}.</p>
        )}
      </section>

      <Explicacao estado={explicacao} aoPedir={pedirExplicacao} aoTentarDeNovo={pedirExplicacao} />

      <section className="bloco limites" aria-labelledby="titulo-limites">
        <h2 id="titulo-limites">Limites deste resultado</h2>
        <ul>
          <li>É uma estimativa para um grupo de pessoas com dados parecidos com os seus, não uma previsão sobre você.</li>
          <li>A equação PREVENT foi desenvolvida com dados de adultos dos Estados Unidos. Num estudo com cerca de 11 mil brasileiros (ELSA-Brasil), ela separou bem quem teve e quem não teve eventos, mas estimou riscos em média um pouco mais altos que os observados (cerca de 20%). Perto de 5% ou de 20%, a categoria pode mudar.</li>
          <li>Não considera histórico completo, outros exames nem o exame clínico. Não é um diagnóstico.</li>
          <li>Leve este resultado ao seu médico para decidir os próximos passos.</li>
        </ul>
      </section>

      <div className="acoes">
        <Botao onClick={() => window.print()}>Imprimir ou salvar em PDF</Botao>
        <Botao variante="secundario" onClick={aoRecomecar}>Fazer nova avaliação</Botao>
      </div>
    </div>
  );
}
