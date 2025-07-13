from fastapi import HTTPException
from app.schemas import PatientData
import logging

logger = logging.getLogger(__name__)

def validate_patient_data(patient: PatientData):
    """
    Validações clínicas dos dados do paciente
    """
    # Pressão sistólica maior que diastólica
    if patient.ap_hi <= patient.ap_lo:
        raise HTTPException(
            status_code=400,
            detail="Pressão sistólica deve ser maior que diastólica"
        )
    # IMC extremo
    bmi = patient.weight / ((patient.height / 100) ** 2)
    if bmi < 15 or bmi > 50:
        logger.warning(f"IMC extremo detectado: {bmi:.2f} para usuário {patient.user_id}")
    # Pressão sistólica plausível
    if patient.ap_hi < 70 or patient.ap_hi > 250:
        raise HTTPException(
            status_code=400,
            detail="Pressão sistólica fora da faixa plausível (70-250 mmHg)"
        )
    # Pressão diastólica plausível
    if patient.ap_lo < 40 or patient.ap_lo > 150:
        raise HTTPException(
            status_code=400,
            detail="Pressão diastólica fora da faixa plausível (40-150 mmHg)"
        )
