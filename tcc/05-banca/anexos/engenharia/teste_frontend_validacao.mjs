/*
 * Testes da banca (engenharia) para a lógica pura do frontend. NÃO fazem parte do projeto.
 * Empacotar com o esbuild do próprio frontend e rodar com node (sem instalar nada):
 *
 *   cd frontend
 *   npx esbuild ../tcc/05-banca/anexos/engenharia/teste_frontend_validacao.mjs --bundle \
 *       --platform=node --format=esm --define:import.meta.env={} --outfile=<scratchpad>/teste.mjs && node <scratchpad>/teste.mjs
 */
import assert from 'node:assert/strict';
import { lerNumero, validar } from '../../../../frontend/src/validacao.js';
import { montarEntrada } from '../../../../frontend/src/api.js';
import { PERGUNTAS } from '../../../../frontend/src/conteudo/perguntas.js';

const P = Object.fromEntries(PERGUNTAS.map((p) => [p.id, p]));
let ok = 0;
const achados = [];
function caso(nome, fn) {
  try { fn(); ok++; console.log('ok  ', nome); } catch (e) { console.log('FALHA', nome, '\n   ', e.message); process.exitCode = 1; }
}

// ---------- lerNumero: vírgula decimal e entradas estranhas ----------
caso('vírgula e ponto decimais', () => {
  assert.equal(lerNumero('1,2'), 1.2);
  assert.equal(lerNumero('1.2'), 1.2);
  assert.equal(lerNumero(' 1 , 2 '), 1.2); // espaços internos removidos
});
caso('vazio → null; lixo → NaN', () => {
  assert.equal(lerNumero(''), null);
  assert.equal(lerNumero(undefined), null);
  for (const s of ['-5', '1e3', '.5', '5.', 'abc', '1,2,3', '0x10']) assert.ok(Number.isNaN(lerNumero(s)), s);
});
caso('separador de milhar "1.234,5" é recusado (NaN), não lido como 1,234', () => {
  assert.ok(Number.isNaN(lerNumero('1.234,5')));
});

// ---------- validar: faixas-limite ----------
caso('colesterol total: 130 e 320 aceitos; 129,9 e 320,1 recusados', () => {
  assert.equal(validar(P.colesterol_total, '130', {}).erros.length, 0);
  assert.equal(validar(P.colesterol_total, '320', {}).erros.length, 0);
  assert.equal(validar(P.colesterol_total, '129,9', {}).erros.length, 1);
  assert.equal(validar(P.colesterol_total, '320,1', {}).erros.length, 1);
});
caso('idade 29 passa na validação (vai para "fora do escopo" pela pergunta), 17 pede conferência', () => {
  assert.equal(validar(P.idade, '29', {}).erros.length, 0);
  assert.ok(P.idade.foraDoEscopo(29));
  assert.equal(validar(P.idade, '17', {}).erros[0].mensagem, 'Confira o valor digitado.');
});
caso('LDL opcional: vazio vira null e é enviado como null', () => {
  const v = validar(P.ldl, '', {});
  assert.deepEqual(v, { valor: null, erros: [] });
  assert.equal(montarEntrada({ ldl: null }).ldl, null);
  assert.equal(montarEntrada({}).ldl, null);
});
caso('LDL maior que colesterol total é aceito no cliente (sem validação cruzada)', () => {
  const v = validar(P.ldl, '300', { colesterol_total: 180, hdl: 50 });
  assert.equal(v.erros.length, 0);
  achados.push('LDL 300 com CT 180 aceito no cliente (e no servidor).');
});
caso('creatinina 0 é barrada no cliente (faixa 0,3–15), mas o servidor devolve 500 se chamado direto', () => {
  const v = validar(P.renal, { tipo: 'creatinina', valor: '0' }, {});
  assert.equal(v.erros.length, 1);
});

// ---------- sexo alterado depois de marcar o agravante feminino ----------
caso('BUG: resposta antiga "fator_especifico_mulher" sobrevive à troca de sexo e é enviada', () => {
  // 1) usuária responde sexo=feminino e marca o agravante
  const r1 = { sexo: 'feminino' };
  const ag = validar(P.agravantes, ['fator_especifico_mulher'], r1);
  assert.deepEqual(ag.valor, ['fator_especifico_mulher']);
  // 2) na revisão, troca sexo para masculino (App.responder só grava o novo sexo e volta para a revisão)
  const respostas = { ...r1, agravantes: ag.valor, sexo: 'masculino' };
  // 3) montarEntrada envia o agravante feminino para um homem
  const corpo = montarEntrada(respostas);
  assert.equal(corpo.sexo, 'masculino');
  assert.deepEqual(corpo.agravantes, ['fator_especifico_mulher']);
  achados.push('Agravante feminino enviado com sexo=masculino após troca na revisão.');
});

// ---------- categoria "pelo cálculo" recomputada no cliente ----------
caso('BUG: categoria do escore recomputada com o risco ARREDONDADO diverge do servidor', () => {
  // TelaResultado.jsx:35 usa r.risco_pct (1 casa); o servidor usa o valor não arredondado (sbc.py:42)
  const r = { risco_pct: 5.0 }; // servidor: 4,951% → "baixo"
  const categoriaDoEscore = r.risco_pct < 5 ? 'baixo' : r.risco_pct < 20 ? 'intermediário' : 'alto';
  assert.equal(categoriaDoEscore, 'intermediário');
  achados.push('Com agravante, a tela diria "pelo cálculo seria intermediário" e a categoria final também intermediário (servidor: baixo→intermediário).');
});

console.log(`\n${ok} casos ok.`);
console.log('Achados:\n- ' + achados.join('\n- '));
