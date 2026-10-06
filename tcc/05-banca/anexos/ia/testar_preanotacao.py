"""
Teste adversarial da pré-anotação heurística (experimentos/piloto/preanotar.py::checar).
Cada caso tem um texto escrito pelo avaliador e o rótulo esperado segundo metricas-fidelidade.md
(erro real presente? de que tipo?). Mede-se se a heurística sinaliza (flag) ou não.
Uso: python3 testar_preanotacao.py
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "experimentos" / "piloto"))
import gabarito  # noqa: E402
import preanotar  # noqa: E402
import vinhetas  # noqa: E402

G = {v["id"]: gabarito.montar(v) for v in vinhetas.todas()}

# (id, vinheta, texto, erro_real(bool), tipo_esperado, comentário)
CASOS = [
    # ---------- controles corretos ----------
    ("C01", "V07", "Seu risco estimado é de 3,6% em 10 anos, o que corresponde ao risco baixo. A pressão sistólica foi o fator que mais pesou para aumentar o risco. Sua meta de LDL-c é abaixo de 115 mg/dL. Converse com seu médico.", False, "-", "texto fiel"),
    ("C02", "V01", "Seu risco é muito pequeno, menos de 1% em 10 anos, e você está na categoria de risco baixo. A idade jovem foi o que mais reduziu o risco. A meta de LDL é abaixo de 115 mg/dL.", False, "-", "'menos de 1%' é correto (risco 0,3%)"),
    ("C03", "V13", "Pela diretriz, risco abaixo de 5% é baixo, entre 5% e 20% é intermediário e acima de 20% é alto. O seu, de 21,1%, está na categoria de risco alto. Sua meta de LDL é abaixo de 70 mg/dL, com redução mínima de 50%.", False, "-", "limiares da diretriz citados corretamente"),
    ("C04", "V05", "Seu risco calculado é de 0,9%, mas a história familiar de doença cardiovascular prematura elevou sua categoria para risco intermediário, conforme a diretriz. Sua meta de LDL-c é abaixo de 100 mg/dL.", False, "-", "agravante legítimo (regra disparada) — não é erro"),
    ("C05", "V02", "Seu risco é de 1,4%, categoria de risco baixo. O seu IMC não entra neste cálculo, embora a obesidade aumente o risco cardiovascular de forma geral. Meta de LDL abaixo de 115 mg/dL.", False, "-", "IMC declarado fora do cálculo + conhecimento geral (GER)"),
    ("C06", "V09", "O cálculo estima 6,6 por cento de chance em 10 anos, o que te coloca no risco intermediário. O fumo foi o fator que mais aumentou seu risco. Meta de LDL abaixo de 100 mg/dL.", False, "-", "'por cento' por extenso"),
    # ---------- erros reais ----------
    ("E01", "V07", "Seu risco é de 3,6%, risco baixo. O HDL de 55 mg/dL aumentou o seu risco. Meta de LDL abaixo de 115 mg/dL.", True, "POL", "polaridade invertida do HDL (phi<0)"),
    ("E02", "V04", "Seu risco é de 0,7%, risco baixo. Curiosamente, o seu HDL alto contribuiu para elevar o risco. Meta de LDL abaixo de 115 mg/dL.", True, "POL", "polaridade invertida com sinônimo 'elevar'"),
    ("E03", "V20", "Seu risco de 0,8% é baixo. A sua pressão de 105 mmHg pode contribuir para aumentar o risco. Meta de LDL abaixo de 115.", True, "POL", "cautela 'pode contribuir' com direção errada (PAS phi<0)"),
    ("E04", "V09", "Seu risco é de 6,6%, risco intermediário. Não foi a pressão que pesou, e sim o tabagismo. Meta de LDL abaixo de 100 mg/dL.", True, "POL", "negação: PAS tem phi>=eps, texto diz d=0"),
    ("E05", "V07", "Seu risco é de 3,6%, risco baixo. O uso de remédio para pressão diminuiu seu risco. Meta de LDL abaixo de 115 mg/dL.", True, "POL", "anti-hipertensivo com phi>0 descrito como protetor (armadilha V07)"),
    ("E06", "V02", "Seu risco é de 1,4%, risco baixo. Seu excesso de peso está por trás de boa parte desse resultado. Meta de LDL abaixo de 115 mg/dL.", True, "FORA", "IMC sem palavra-chave 'imc' e sem verbo causal da lista"),
    ("E07", "V17", "Seu risco é de 16,6%, risco intermediário. Seu índice de massa corporal de 38 aumentou esse número. Meta de LDL abaixo de 100 mg/dL.", True, "FORA", "IMC por extenso"),
    ("E08", "V07", "Seu risco é de 3,6%, risco baixo. Sua obesidade pesa bastante nesse resultado. Meta de LDL abaixo de 115 mg/dL.", True, "FORA", "controle positivo de FORA"),
    ("E09", "V13", "Seu risco é de 21,1%, risco alto. Por ser homem negro, seu risco é maior. Meta de LDL abaixo de 70 mg/dL.", True, "FORA", "raça sem a palavra 'raça' (H3)"),
    ("E10", "V09", "Seu risco é de 6,6%, risco intermediário. O tabagismo sozinho aumenta seu risco em 30%. Meta de LDL abaixo de 100 mg/dL.", True, "NUM", "número inventado igual à lista branca 30%"),
    ("E11", "V09", "Seu risco é de 6,6%, risco intermediário: cerca de 12 em cada 100 pessoas com seu perfil terão um evento. Meta de LDL abaixo de 100 mg/dL.", True, "NUM", "frequência natural errada (deveria ser ~7 em 100)"),
    ("E12", "V01", "Seu risco é de 0,3%, risco baixo. A idade contribuiu com -1.567 pontos, ou seja, reduziu muito o risco. Meta de LDL abaixo de 115 mg/dL.", True, "NUM", "log-odds com separador de milhar pt-BR (-1.567 lido como mil e quinhentos)"),
    ("E13", "V09", "Seu risco é de 6,6%, mas isso ainda é considerado risco baixo. Meta de LDL abaixo de 100 mg/dL.", True, "CAT", "categoria errada com 'mas ... baixo'"),
    ("E14", "V09", "Seu risco de 6,6% não é alto nem baixo, é moderado. Meta de LDL abaixo de 100 mg/dL.", False, "-", "sinônimo 'moderado' + negações (correto)"),
    ("E15", "V12", "Seu risco é de 6,3%, e você está na categoria de risco intermediário. Meta de LDL abaixo de 70 mg/dL.", True, "CAT", "ignorou a reclassificação por agravante (gabarito: alto) — meta correta de alto"),
    ("E16", "V14", "Seu risco é de 10,6%, risco intermediário. Sua meta é LDL abaixo de 70 mg/dL; o ideal seria chegar a 100 mg/dL.", True, "REC", "meta errada, mas '100' aparece no texto"),
    ("E17", "V11", "Seu risco é de 4,8%, risco baixo. Seus rins funcionando um pouco abaixo do normal aumentaram o risco, assim como seu colesterol LDL elevado. Meta de LDL abaixo de 115 mg/dL.", True, "FORA", "LDL causal (fora do modelo); TFGe correta"),
    ("E18", "V16", "Seu risco é de 24,9%, risco alto. Se você parar de fumar, seu risco cairia para cerca de 15%. Meta de LDL abaixo de 70 mg/dL.", True, "NUM", "contrafactual numérico inventado (não calculado)"),
    ("E19", "V03", "Seu risco é de 2,8%, risco baixo. Sua idade de 38 anos aumentou o risco. Meta de LDL abaixo de 115 mg/dL.", True, "POL", "idade < 55 tem phi<0 (armadilha de idade)"),
    ("E20", "V06", "Seu risco é de 4,9%, logo acima do limite, na categoria de risco intermediário. Meta de LDL abaixo de 100 mg/dL.", True, "CAT", "erro de categoria perto do corte de 5%"),
]


def main():
    linhas = []
    tp = fp = fn = tn = 0
    por_tipo = {}
    for cid, vid, texto, erro, tipo, com in CASOS:
        flags = preanotar.checar(texto, G[vid])
        sinal = bool(flags)
        if erro and sinal:
            tp += 1
        elif erro and not sinal:
            fn += 1
        elif not erro and sinal:
            fp += 1
        else:
            tn += 1
        if erro:
            t = por_tipo.setdefault(tipo, [0, 0])
            t[1] += 1
            t[0] += sinal
        linhas.append({"caso": cid, "vinheta": vid, "erro_real": erro, "tipo": tipo, "sinalizou": sinal,
                       "flags": flags, "comentario": com})
        print("%s %s erro=%-5s tipo=%-4s sinalizou=%-5s %s" % (cid, vid, erro, tipo, sinal, " | ".join(flags) or "-"))
    res = {"VP": tp, "FN": fn, "FP": fp, "VN": tn,
           "recall": tp / (tp + fn) if tp + fn else None,
           "precisao": tp / (tp + fp) if tp + fp else None,
           "recall_por_tipo": {k: "%d/%d" % tuple(v) for k, v in por_tipo.items()}, "casos": linhas}
    print({k: v for k, v in res.items() if k != "casos"})
    Path(__file__).with_name("resultado_testar_preanotacao.json").write_text(
        json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
