from typing import Dict, Any


def get_risk_level(risk_score: float) -> str:
    """
    Categoriza o nível de risco baseado no score
    """
    if risk_score < 0.3:
        return "Baixo"
    elif risk_score < 0.6:
        return "Moderado"
    elif risk_score < 0.8:
        return "Alto"
    else:
        return "Muito Alto"


def get_clinical_interpretation(features: Dict[str, Any], risk_score: float) -> Dict[str, str]:
    """
    Gera interpretação clínica baseada nas features
    """
    interpretation: Dict[str, str] = {}

    # BMI
    bmi_cat = features.get('bmi_category', 'Normal')
    if bmi_cat == 'Obese':
        interpretation['bmi'] = "Obesidade é um fator de risco cardiovascular significativo"
    elif bmi_cat == 'Overweight':
        interpretation['bmi'] = "Sobrepeso pode contribuir para risco cardiovascular"
    else:
        interpretation['bmi'] = "IMC dentro da faixa considerada saudável"

    # Blood pressure
    bp_cat = features.get('bp_category', 'Normal')
    if 'Hypertension' in bp_cat:
        interpretation['blood_pressure'] = "Hipertensão é um dos principais fatores de risco cardiovascular"
    elif bp_cat == 'Elevated':
        interpretation['blood_pressure'] = "Pressão elevada requer monitoramento"
    else:
        interpretation['blood_pressure'] = "Pressão arterial dentro da faixa normal"

    # Lifestyle
    lifestyle_score = features.get('lifestyle_score', 0)
    if lifestyle_score > 0:
        interpretation['lifestyle'] = "Estilo de vida com fatores de risco (fumo/álcool sem atividade física)"
    elif lifestyle_score < 0:
        interpretation['lifestyle'] = "Estilo de vida favorável (ativo, sem fumo/álcool excessivo)"
    else:
        interpretation['lifestyle'] = "Estilo de vida neutro em termos de risco cardiovascular"

    # Overall recommendations
    if risk_score > 0.7:
        interpretation['overall'] = "Alto risco detectado. Recomenda-se avaliação médica urgente."
    elif risk_score > 0.4:
        interpretation['overall'] = "Risco moderado. Considerar modificações no estilo de vida."
    else:
        interpretation['overall'] = "Baixo risco cardiovascular com base nos fatores analisados."

    return interpretation
