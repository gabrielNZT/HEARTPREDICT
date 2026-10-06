import { useEffect } from 'react';

/** Move o foco para o título ao abrir a tela e atualiza o título da aba (leitores de tela anunciam a mudança). */
export function useTituloDaTela(titulo) {
  useEffect(() => {
    document.title = `${titulo} — HeartPredict`;
    document.querySelector('[data-titulo-tela]')?.focus();
  }, [titulo]);
}
