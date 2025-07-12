"""
API FastAPI para previsão de risco cardíaco usando modelo XGBoost treinado
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import uvicorn
from typing import Optional
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir a estrutura de dados completa do paciente
class PatientData(BaseModel):
    user_id: str = Field(..., description="ID único do usuário")
    age: int = Field(..., description="Idade em anos", ge=0, le=120)
    gender: int = Field(..., description="Gênero (1: mulher, 2: homem)", ge=1, le=2)
    height: int = Field(..., description="Altura em cm", ge=100, le=250)
    weight: float = Field(..., description="Peso em kg", ge=30.0, le=300.0)
    ap_hi: int = Field(..., description="Pressão sistólica", ge=70, le=250)
    ap_lo: int = Field(..., description="Pressão diastólica", ge=40, le=150)
    cholesterol: int = Field(..., description="Colesterol (1: normal, 2: acima normal, 3: muito acima)", ge=1, le=3)
    gluc: int = Field(..., description="Glicose (1: normal, 2: acima normal, 3: muito acima)", ge=1, le=3)
    smoke: int = Field(..., description="Fumante (0: não, 1: sim)", ge=0, le=1)
    alco: int = Field(..., description="Consumo álcool (0: não, 1: sim)", ge=0, le=1)
    active: int = Field(..., description="Atividade física (0: não, 1: sim)", ge=0, le=1)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user123",
                "age": 45,
                "gender": 1,
                "height": 165,
                "weight": 70.5,
                "ap_hi": 120,
                "ap_lo": 80,
                "cholesterol": 1,
                "gluc": 1,
                "smoke": 0,
                "alco": 0,
                "active": 1
            }
        }

class PredictionResponse(BaseModel):
    user_id: str
    chronic_risk_score: float
    risk_level: str
    features_used: dict

# Variável global para armazenar o modelo
model = None

def load_model():
    """
    Carrega o modelo treinado uma única vez na inicialização da aplicação
    """
    global model
    model_path = "models/cardiac_risk_model.joblib"
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo não encontrado em: {model_path}")
    
    try:
        model = joblib.load(model_path)
        logger.info(f"Modelo carregado com sucesso de: {model_path}")
        return model
    except Exception as e:
        logger.error(f"Erro ao carregar modelo: {e}")
        raise

def preprocess_patient_data(patient: PatientData) -> pd.DataFrame:
    """
    Transforma os dados do paciente em um DataFrame com as mesmas features
    usadas no treinamento do modelo
    """
    # Criar dicionário com os dados do paciente
    patient_dict = {
        'age': patient.age,  # Já está em anos
        'gender': patient.gender,
        'height': patient.height,
        'weight': patient.weight,
        'ap_hi': patient.ap_hi,
        'ap_lo': patient.ap_lo,
        'cholesterol': patient.cholesterol,
        'gluc': patient.gluc,
        'smoke': patient.smoke,
        'alco': patient.alco,
        'active': patient.active
    }
    
    # Calcular BMI (mesma lógica do treinamento)
    bmi = patient.weight / ((patient.height / 100) ** 2)
    patient_dict['bmi'] = bmi
    
    # Criar DataFrame com uma linha
    df = pd.DataFrame([patient_dict])
    
    # Garantir que as colunas estão na ordem esperada pelo modelo
    expected_columns = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 
                       'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'bmi']
    
    df = df[expected_columns]
    
    return df

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

def validate_patient_data(patient: PatientData):
    """
    Validações adicionais dos dados do paciente
    """
    # Validar pressão arterial
    if patient.ap_hi <= patient.ap_lo:
        raise HTTPException(
            status_code=400, 
            detail="Pressão sistólica deve ser maior que diastólica"
        )
    
    # Validar IMC extremo
    bmi = patient.weight / ((patient.height / 100) ** 2)
    if bmi < 15 or bmi > 50:
        logger.warning(f"IMC extremo detectado: {bmi:.2f} para usuário {patient.user_id}")

# Criar instância da aplicação FastAPI
app = FastAPI(
    title="Cardiac Risk Prediction API",
    description="API para previsão de risco cardíaco usando XGBoost",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """
    Carrega o modelo quando a aplicação inicia
    """
    try:
        load_model()
        logger.info("Aplicação iniciada com sucesso!")
    except Exception as e:
        logger.error(f"Erro na inicialização: {e}")
        raise

@app.get("/")
async def root():
    """
    Endpoint raiz para verificar se a API está funcionando
    """
    return {
        "message": "Cardiac Risk Prediction API", 
        "status": "ativo",
        "model_loaded": model is not None
    }

@app.get("/health")
async def health_check():
    """
    Endpoint de health check
    """
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": pd.Timestamp.now().isoformat()
    }

@app.post("/predict_risk", response_model=PredictionResponse)
async def predict_risk(patient: PatientData):
    """
    Endpoint principal para previsão de risco cardíaco
    """
    try:
        # Verificar se o modelo está carregado
        if model is None:
            raise HTTPException(
                status_code=500, 
                detail="Modelo não carregado. Verifique os logs do servidor."
            )
        
        logger.info(f"Recebendo dados para previsão - Usuário: {patient.user_id}")
        
        # Validar dados do paciente
        validate_patient_data(patient)
        
        # Preprocessar dados
        input_df = preprocess_patient_data(patient)
        
        # Fazer previsão
        # Usar predict_proba para obter a probabilidade da classe 1 (doença)
        risk_probabilities = model.predict_proba(input_df)
        risk_score = float(risk_probabilities[0][1])  # Probabilidade da classe 1
        
        # Determinar nível de risco
        risk_level = get_risk_level(risk_score)
        
        # Criar resposta
        response = PredictionResponse(
            user_id=patient.user_id,
            chronic_risk_score=round(risk_score, 4),
            risk_level=risk_level,
            features_used={
                "age": patient.age,
                "gender": "Feminino" if patient.gender == 1 else "Masculino",
                "bmi": round(patient.weight / ((patient.height / 100) ** 2), 2),
                "blood_pressure": f"{patient.ap_hi}/{patient.ap_lo}",
                "cholesterol_level": patient.cholesterol,
                "glucose_level": patient.gluc,
                "lifestyle_factors": {
                    "smoking": bool(patient.smoke),
                    "alcohol": bool(patient.alco),
                    "physical_activity": bool(patient.active)
                }
            }
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

@app.get("/model_info")
async def get_model_info():
    """
    Endpoint para obter informações sobre o modelo
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo não carregado")
    
    try:
        # Informações básicas do modelo
        model_info = {
            "model_type": "XGBoost Classifier",
            "n_estimators": model.n_estimators,
            "max_depth": model.max_depth,
            "learning_rate": model.learning_rate,
            "n_features": model.n_features_in_ if hasattr(model, 'n_features_in_') else "Unknown",
            "feature_names": [
                "age", "gender", "height", "weight", "ap_hi", "ap_lo",
                "cholesterol", "gluc", "smoke", "alco", "active", "bmi"
            ]
        }
        
        return model_info
        
    except Exception as e:
        logger.error(f"Erro ao obter informações do modelo: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter informações do modelo")

if __name__ == "__main__":
    # Configurar e executar o servidor
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000,
        log_level="info",
        reload=False  # Desabilitar reload em produção
    )
