import logging
import time
import pandas as pd
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Dict, Any

from app.schemas import PatientData, EnhancedPredictionResponse
from app.core.model_manager import model_manager, get_model_manager, ModelManager
from app.validation import validate_patient_data
from app.services import get_risk_level, get_clinical_interpretation

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
async def root():
    """
    Endpoint raiz
    """
    return {
        "message": "Enhanced Cardiac Risk Prediction API", 
        "status": "ativo",
        "version": "2.0.0",
        "model_loaded": model_manager.is_loaded(),
        "pipeline": "Scientific methodology with LightGBM"
    }

@router.get("/health")
async def health_check():
    """
    Endpoint de health check aprimorado
    """
    model_info: Dict[str, Any] = {}
    if model_manager.is_loaded():
        try:
            model_info = model_manager.get_model_info()
        except Exception:
            pass
    return {
        "status": "healthy",
        "model_loaded": model_manager.is_loaded(),
        "timestamp": pd.Timestamp.now().isoformat(),
        "model_info": model_info
    }

@router.post("/debug_predict")
async def debug_predict(request: Request):
    """
    Endpoint de debug para ver exatamente o que está sendo enviado
    """
    try:
        body = await request.body()
        logger.info("=== DEBUG RAW REQUEST ===")
        logger.info(f"Method: {request.method}")
        logger.info(f"URL: {request.url}")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Raw Body: {body}")
        logger.info(f"Body as string: {body.decode('utf-8') if body else 'Empty'}")
        logger.info("========================")
        return {
            "status": "debug_received",
            "method": request.method,
            "headers": dict(request.headers),
            "body_length": len(body) if body else 0,
            "body": body.decode('utf-8') if body else "Empty"
        }
    except Exception as e:
        logger.error(f"Erro no debug: {e}")
        return {"error": str(e)}

@router.post("/predict_risk", response_model=EnhancedPredictionResponse)
async def predict_risk(
    patient: PatientData,
    manager: ModelManager = Depends(get_model_manager)
):
    """
    Endpoint principal para previsão de risco cardíaco aprimorado
    """
    start_time = time.time()
    try:
        logger.info("=========================")
        logger.info("=== DADOS RECEBIDOS ===")
        logger.info(f"User ID: {patient.user_id}")
        logger.info(f"Age: {patient.age} (type: {type(patient.age)})")
        logger.info(f"Gender: {patient.gender} (type: {type(patient.gender)})")
        logger.info(f"Height: {patient.height} (type: {type(patient.height)})")
        logger.info(f"Weight: {patient.weight} (type: {type(patient.weight)})")
        logger.info(f"AP Hi: {patient.ap_hi} (type: {type(patient.ap_hi)})")
        logger.info(f"AP Lo: {patient.ap_lo} (type: {type(patient.ap_lo)})")
        logger.info("========================")
        if not manager.is_loaded():
            raise HTTPException(
                status_code=500, 
                detail="Modelo aprimorado não carregado. Verifique os logs do servidor."
            )
        validate_patient_data(patient)
        patient_dict = patient.model_dump()
        prediction_result = manager.predict(patient_dict)
        risk_score = prediction_result['risk_probability']
        risk_prediction = prediction_result['risk_prediction']
        processed_features = prediction_result['processed_features']
        risk_level = get_risk_level(risk_score)
        processing_time = (time.time() - start_time) * 1000
        model_info = manager.get_model_info()
        clinical_features: Dict[str, Any] = {
            "bmi": round(processed_features['bmi'], 2),
            "bmi_category": processed_features['bmi_category'],
            "blood_pressure_category": processed_features['bp_category'],
            "age_category": processed_features['age_category'],
            "lifestyle_score": processed_features['lifestyle_score'],
            "pressure_pulse": processed_features['pressure_pulse']
        }
        interpretation = get_clinical_interpretation(processed_features, risk_score)
        response = EnhancedPredictionResponse(
            user_id=patient.user_id,
            chronic_risk_score=round(risk_score, 4),
            risk_prediction=risk_prediction,
            risk_level=risk_level,
            processing_time_ms=round(processing_time, 2),
            model_info={
                "model_name": model_info.get('model_name', 'Enhanced LightGBM'),
                "version": model_info.get('version', '2.0'),
                "roc_auc": model_info.get('final_metrics', {}).get('roc_auc', 0),
                "training_date": model_info.get('training_date', 'Unknown')
            },
            clinical_features=clinical_features,
            interpretation=interpretation
        )
        logger.info(f"Previsão calculada - Usuário: {patient.user_id}, Risco: {risk_score:.4f}, Nível: {risk_level}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro durante previsão para usuário {patient.user_id}: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno do servidor durante a previsão: {str(e)}"
        )

@router.get("/model_info")
async def get_model_info(manager: ModelManager = Depends(get_model_manager)):
    """
    Endpoint para obter informações detalhadas do modelo aprimorado
    """
    try:
        return manager.get_model_info()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao obter informações do modelo: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter informações do modelo")

@router.get("/compare_models")
async def compare_models():
    """
    Endpoint para comparar modelo original vs aprimorado
    """
    try:
        model_info = model_manager.get_model_info()
        comparison = {
            "original_model": {
                "type": "Mock/Fixed",
                "risk_score": 0.78,
                "features": 7,
                "validation": "None",
                "interpretability": "Limited"
            },
            "enhanced_model": {
                "type": model_info.get('model_name', 'LightGBM'),
                "roc_auc": model_info.get('final_metrics', {}).get('roc_auc', 0),
                "features": model_info.get('features_count', 0),
                "validation": "5-Fold Cross-Validation",
                "interpretability": "SHAP Analysis",
                "improvements": [
                    "Data cleaning with medical criteria",
                    "Advanced feature engineering", 
                    "Cross-validation",
                    "Hyperparameter optimization",
                    "Multiple model comparison",
                    "Clinical interpretability"
                ]
            }
        }
        return comparison
    except Exception as e:
        logger.error(f"Erro na comparação: {e}")
        raise HTTPException(status_code=500, detail="Erro ao comparar modelos")
