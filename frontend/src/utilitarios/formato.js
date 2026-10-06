export const fmtNumero = (v) => String(v).replace('.', ',');
export const fmtPct = (v) => `${fmtNumero(v)}%`;
