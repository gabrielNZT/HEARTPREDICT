"""
API FastAPI usando o modelo aprimorado de risco cardíaco
Integra o pipeline completo desenvolvido com metodologia científica rigorosa
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import uvicorn
from typing import Optional, Dict, Any
import os
import logging
import threading
import time
from contextlib import asynccontextmanager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir a estrutura de dados completa do paciente
class PatientData(BaseModel):
    user_id: str = Field(..., description="ID único do usuário")
    age: int = Field(..., description="Idade em anos", ge=18, le=100)
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
        json_schema_extra = {
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

class EnhancedPredictionResponse(BaseModel):
    user_id: str
    chronic_risk_score: float
    risk_prediction: int
    risk_level: str
    processing_time_ms: float
    model_info: Dict[str, Any]
    clinical_features: Dict[str, Any]
    interpretation: Dict[str, str]

    class Config:
        protected_namespaces = ()

class ModelManager:
    """
    Gerenciador thread-safe para o modelo aprimorado
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock: 
                if cls._instance is None:
                    cls._instance = super(ModelManager, cls).__new__(cls)
                    cls._instance._model = None
                    cls._instance._metadata = None
                    cls._instance._model_lock = threading.RLock()
        return cls._instance
    
    def load_model(self, model_path: str = "models/cardiac_risck_model_v2.joblib"):
        """
        Carrega o modelo aprimorado de forma thread-safe
        """
        with self._model_lock:
            if self._model is None:
                if not os.path.exists(model_path):
                    raise FileNotFoundError(f"Modelo aprimorado não encontrado em: {model_path}")
                
                try:
                    self._model = joblib.load(model_path)
                    
                    # Carregar metadados
                    metadata_path = model_path.replace('cardiac_risck_model_v2.joblib', 'model_metadata.joblib')
                    if os.path.exists(metadata_path):
                        self._metadata = joblib.load(metadata_path)
                    
                    logger.info(f"Modelo aprimorado carregado com sucesso de: {model_path}")
                    if self._metadata:
                        logger.info(f"Modelo: {self._metadata['model_name']}, ROC-AUC: {self._metadata['final_metrics']['roc_auc']:.4f}")
                        
                except Exception as e:
                    logger.error(f"Erro ao carregar modelo aprimorado: {e}")
                    raise
    
    def preprocess_patient_data(self, patient_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Preprocessa dados do paciente usando as mesmas transformações do treinamento
        """
        # Converter para DataFrame
        df = pd.DataFrame([patient_data])
        
        # Calcular BMI
        df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
        
        # Categorias de BMI
        def categorize_bmi(bmi):
            if bmi < 18.5:
                return 'Underweight'
            elif bmi < 25:
                return 'Normal'
            elif bmi < 30:
                return 'Overweight'
            else:
                return 'Obese'
        
        df['bmi_category'] = df['bmi'].apply(categorize_bmi)
        
        # Categorias de Pressão Arterial
        def categorize_blood_pressure(systolic, diastolic):
            if systolic < 120 and diastolic < 80:
                return 'Normal'
            elif systolic < 130 and diastolic < 80:
                return 'Elevated'
            elif (systolic >= 130 and systolic < 140) or (diastolic >= 80 and diastolic < 90):
                return 'Stage1_Hypertension'
            elif systolic >= 140 or diastolic >= 90:
                return 'Stage2_Hypertension'
            else:
                return 'Hypertensive_Crisis'
        
        df['bp_category'] = df.apply(lambda x: categorize_blood_pressure(x['ap_hi'], x['ap_lo']), axis=1)
        
        # Features de interação
        df['age_cholesterol_interaction'] = df['age'] * df['cholesterol']
        df['bmi_age_interaction'] = df['bmi'] * df['age']
        df['pressure_pulse'] = df['ap_hi'] - df['ap_lo']
        
        # Lifestyle score
        df['lifestyle_score'] = df['smoke'] + df['alco'] - df['active']
        
        # Categorização de idade
        def categorize_age(age):
            if age < 40:
                return 'Young'
            elif age < 55:
                return 'Middle_aged'
            else:
                return 'Senior'
        
        df['age_category'] = df['age'].apply(categorize_age)
        
        return df
    
    def predict(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz previsão usando o modelo aprimorado
        """
        with self._model_lock:
            if self._model is None:
                raise RuntimeError("Modelo não carregado")
            
            # Preprocessar dados
            df = self.preprocess_patient_data(patient_data)
            
            # Fazer previsão
            risk_proba = self._model.predict_proba(df)[0][1]
            risk_prediction = self._model.predict(df)[0]
            
            return {
                'risk_probability': risk_proba,
                'risk_prediction': int(risk_prediction),
                'processed_features': df.iloc[0].to_dict()
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Retorna informações do modelo aprimorado
        """
        with self._model_lock:
            if self._model is None:
                raise RuntimeError("Modelo não carregado")
            
            info = {
                "model_type": "Enhanced Pipeline with LightGBM",
                "version": "2.0",
                "pipeline_stages": [
                    "Data Cleaning",
                    "Feature Engineering", 
                    "Preprocessing Pipeline",
                    "Model Comparison",
                    "Hyperparameter Optimization",
                    "Cross-Validation"
                ]
            }
            
            if self._metadata:
                info.update({
                    "model_name": self._metadata['model_name'],
                    "training_date": self._metadata['training_date'],
                    "final_metrics": self._metadata['final_metrics'],
                    "data_shape": self._metadata['data_shape'],
                    "features_count": self._metadata['features_count']
                })
            
            return info
    
    def is_loaded(self) -> bool:
        """
        Verifica se o modelo está carregado
        """
        with self._model_lock:
            return self._model is not None

# Instância global do gerenciador
model_manager = ModelManager()

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

def get_clinical_interpretation(features: Dict, risk_score: float) -> Dict[str, str]:
    """
    Gera interpretação clínica baseada nas features
    """
    interpretation = {}
    
    # Interpretação do BMI
    bmi_cat = features.get('bmi_category', 'Normal')
    if bmi_cat == 'Obese':
        interpretation['bmi'] = "Obesidade é um fator de risco cardiovascular significativo"
    elif bmi_cat == 'Overweight':
        interpretation['bmi'] = "Sobrepeso pode contribuir para risco cardiovascular"
    else:
        interpretation['bmi'] = "IMC dentro da faixa considerada saudável"
    
    # Interpretação da pressão arterial
    bp_cat = features.get('bp_category', 'Normal')
    if 'Hypertension' in bp_cat:
        interpretation['blood_pressure'] = "Hipertensão é um dos principais fatores de risco cardiovascular"
    elif bp_cat == 'Elevated':
        interpretation['blood_pressure'] = "Pressão elevada requer monitoramento"
    else:
        interpretation['blood_pressure'] = "Pressão arterial dentro da faixa normal"
    
    # Interpretação do estilo de vida
    lifestyle_score = features.get('lifestyle_score', 0)
    if lifestyle_score > 0:
        interpretation['lifestyle'] = "Estilo de vida com fatores de risco (fumo/álcool sem atividade física)"
    elif lifestyle_score < 0:
        interpretation['lifestyle'] = "Estilo de vida favorável (ativo, sem fumo/álcool excessivo)"
    else:
        interpretation['lifestyle'] = "Estilo de vida neutro em termos de risco cardiovascular"
    
    # Interpretação geral
    if risk_score > 0.7:
        interpretation['overall'] = "Alto risco detectado. Recomenda-se avaliação médica urgente."
    elif risk_score > 0.4:
        interpretation['overall'] = "Risco moderado. Considerar modificações no estilo de vida."
    else:
        interpretation['overall'] = "Baixo risco cardiovascular com base nos fatores analisados."
    
    return interpretation

def validate_patient_data(patient: PatientData):
    """
    Validações clínicas dos dados do paciente
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
    
    # Validar pressão arterial plausível
    if patient.ap_hi < 70 or patient.ap_hi > 250:
        raise HTTPException(
            status_code=400,
            detail="Pressão sistólica fora da faixa plausível (70-250 mmHg)"
        )
    
    if patient.ap_lo < 40 or patient.ap_lo > 150:
        raise HTTPException(
            status_code=400,
            detail="Pressão diastólica fora da faixa plausível (40-150 mmHg)"
        )

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação
    """
    # Startup
    logger.info("Iniciando API com modelo aprimorado...")
    try:
        model_manager.load_model()
        logger.info("Modelo aprimorado carregado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao carregar modelo aprimorado: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Finalizando API...")

# Criar instância da aplicação FastAPI
app = FastAPI(
    title="Enhanced Cardiac Risk Prediction API",
    description="API aprimorada para previsão de risco cardíaco usando pipeline científico com LightGBM",
    version="2.0.0",
    lifespan=lifespan
)

def get_model_manager() -> ModelManager:
    """
    Dependency injection para o model manager
    """
    return model_manager

@app.get("/")
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

@app.get("/health")
async def health_check():
    """
    Endpoint de health check aprimorado
    """
    model_info = {}
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

@app.post("/debug_predict")
async def debug_predict(request: Request):
    """
    Endpoint de debug para ver exatamente o que está sendo enviado
    """
    try:
        # Capturar raw body
        body = await request.body()
        logger.info(f"=== DEBUG RAW REQUEST ===")
        logger.info(f"Method: {request.method}")
        logger.info(f"URL: {request.url}")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Raw Body: {body}")
        logger.info(f"Body as string: {body.decode('utf-8') if body else 'Empty'}")
        logger.info(f"========================")
        
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

@app.post("/predict_risk", response_model=EnhancedPredictionResponse)
async def predict_risk(
    patient: PatientData,
    manager: ModelManager = Depends(get_model_manager)
):
    """
    Endpoint principal para previsão de risco cardíaco aprimorado
    """
    start_time = time.time()
    
    try:
        logger.info(f"=========================")
        
        # Log detalhado dos dados recebidos
        logger.info(f"=== DADOS RECEBIDOS ===")
        logger.info(f"User ID: {patient.user_id}")
        logger.info(f"Age: {patient.age} (type: {type(patient.age)})")
        logger.info(f"Gender: {patient.gender} (type: {type(patient.gender)})")
        logger.info(f"Height: {patient.height} (type: {type(patient.height)})")
        logger.info(f"Weight: {patient.weight} (type: {type(patient.weight)})")
        logger.info(f"AP Hi: {patient.ap_hi} (type: {type(patient.ap_hi)})")
        logger.info(f"AP Lo: {patient.ap_lo} (type: {type(patient.ap_lo)})")
        logger.info(f"========================")
        
        # Verificar se o modelo está carregado
        if not manager.is_loaded():
            raise HTTPException(
                status_code=500, 
                detail="Modelo aprimorado não carregado. Verifique os logs do servidor."
            )
        
        logger.info(f"Recebendo dados para previsão - Usuário: {patient.user_id}")
        
        # Validar dados do paciente
        validate_patient_data(patient)
        
        # Converter para dict
        patient_dict = patient.model_dump()
        
        # Fazer previsão
        prediction_result = manager.predict(patient_dict)
        
        risk_score = prediction_result['risk_probability']
        risk_prediction = prediction_result['risk_prediction']
        processed_features = prediction_result['processed_features']
        
        # Determinar nível de risco
        risk_level = get_risk_level(risk_score)
        
        # Calcular tempo de processamento
        processing_time = (time.time() - start_time) * 1000
        
        # Obter informações do modelo
        model_info = manager.get_model_info()
        
        # Criar features clínicas para resposta
        clinical_features = {
            "bmi": round(processed_features['bmi'], 2),
            "bmi_category": processed_features['bmi_category'],
            "blood_pressure_category": processed_features['bp_category'],
            "age_category": processed_features['age_category'],
            "lifestyle_score": processed_features['lifestyle_score'],
            "pressure_pulse": processed_features['pressure_pulse']
        }
        
        # Gerar interpretação clínica
        interpretation = get_clinical_interpretation(processed_features, risk_score)
        
        # Criar resposta
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

@app.get("/model_info")
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

@app.get("/compare_models")
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

if __name__ == "__main__":
    # Configurar e executar o servidor
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8002,  # Porta diferente
        log_level="info",
        reload=False
    )
