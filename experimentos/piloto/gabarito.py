"""Pacote de referência R(v) de cada vinheta (metricas-fidelidade.md, seção 1)."""

import prevent
import sbc

NOMES = {
    "idade": "idade",
    "nao_hdl": "colesterol não-HDL",
    "hdl": "HDL (colesterol bom)",
    "pas": "pressão arterial sistólica",
    "anti_hipertensivo": "uso de anti-hipertensivo",
    "estatina": "uso de estatina",
    "diabetes": "diabetes",
    "tabagismo": "tabagismo",
    "tfge": "função renal (TFGe)",
}

AGRAVANTES_PT = sbc.AGRAVANTES_PT


def montar(vinheta):
    p = vinheta["paciente"]
    r = prevent.risco(p)
    cat, regras = sbc.categoria(r, p)
    phi = prevent.shapley(p)
    ordenadas = sorted(phi.items(), key=lambda kv: -abs(kv[1]))
    return {
        "id": vinheta["id"],
        "entradas": p,
        "risco_pct": round(r * 100, 1),
        "categoria": cat,
        "regras_aplicadas": regras,
        "metas": sbc.METAS[cat],
        "atribuicao": {k: round(v, 4) for k, v in phi.items()},
        "ranking": [k for k, v in ordenadas if abs(v) > 1e-9],
    }
