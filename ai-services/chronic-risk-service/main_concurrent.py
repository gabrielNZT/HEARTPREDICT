"""
Versão melhorada da API com melhor tratamento de concorrência
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import uvicorn
import os
import logging
import threading
from contextlib import asynccontextmanager
from functools import lru_cache

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

class PredictionResponse(BaseModel):
    user_id: str
    chronic_risk_score: float
    features_used: dict
    processing_time_ms: float

class ModelManager:
    """
    Gerenciador thread-safe para o modelo XGBoost
    """
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ModelManager, cls).__new__(cls)
                    cls._instance._model = None
                    cls._instance._model_lock = threading.RLock()
        return cls._instance
    
    def load_model(self, model_path: str = "models/cardiac_risk_model.joblib"):
        """
        Carrega o modelo de forma thread-safe
        """
        with self._model_lock:
            if self._model is None:
                if not os.path.exists(model_path):
                    raise FileNotFoundError(f"Modelo não encontrado em: {model_path}")
                
                try:
                    self._model = joblib.load(model_path)
                    logger.info(f"Modelo carregado com sucesso de: {model_path}")
                except Exception as e:
                    logger.error(f"Erro ao carregar modelo: {e}")
                    raise
    
    def predict(self, input_data: pd.DataFrame) -> np.ndarray:
        """
        Faz previsão de forma thread-safe
        """
        with self._model_lock:
            if self._model is None:
                raise RuntimeError("Modelo não carregado")
            
            # XGBoost é thread-safe para predição
            return self._model.predict_proba(input_data)
    
    def get_model_info(self) -> dict:
        """
        Retorna informações do modelo de forma thread-safe
        """
        with self._model_lock:
            if self._model is None:
                raise RuntimeError("Modelo não carregado")
            
            return {
                "model_type": "XGBoost Classifier",
                "n_estimators": self._model.n_estimators,
                "max_depth": self._model.max_depth,
                "learning_rate": self._model.learning_rate,
                "n_features": getattr(self._model, 'n_features_in_', "Unknown"),
                "feature_names": [
                    "age", "gender", "height", "weight", "ap_hi", "ap_lo",
                    "cholesterol", "gluc", "smoke", "alco", "active", "bmi"
                ]
            }
    
    def is_loaded(self) -> bool:
        """
        Verifica se o modelo está carregado
        """
        with self._model_lock:
            return self._model is not None

# Instância global do gerenciador
model_manager = ModelManager()

@lru_cache(maxsize=1000)
def preprocess_patient_data_cached(
    age: int, gender: int, height: int, weight: float,
    ap_hi: int, ap_lo: int, cholesterol: int, gluc: int,
    smoke: int, alco: int, active: int
) -> pd.DataFrame:
    """
    Versão cached do preprocessamento para melhor performance
    """
    # Criar dicionário com os dados do paciente
    patient_dict = {
        'age': age,
        'gender': gender,
        'height': height,
        'weight': weight,
        'ap_hi': ap_hi,
        'ap_lo': ap_lo,
        'cholesterol': cholesterol,
        'gluc': gluc,
        'smoke': smoke,
        'alco': alco,
        'active': active
    }
    
    # Calcular BMI
    bmi = weight / ((height / 100) ** 2)
    patient_dict['bmi'] = bmi
    
    # Criar DataFrame
    df = pd.DataFrame([patient_dict])
    
    # Garantir ordem das colunas
    expected_columns = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 
                       'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'bmi']
    
    return df[expected_columns]

def preprocess_patient_data(patient: PatientData) -> pd.DataFrame:
    """
    Wrapper para a função cached
    """
    return preprocess_patient_data_cached(
        patient.age, patient.gender, patient.height, patient.weight,
        patient.ap_hi, patient.ap_lo, patient.cholesterol, patient.gluc,
        patient.smoke, patient.alco, patient.active
    )

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação
    """
    # Startup
    logger.info("Iniciando aplicação...")
    try:
        model_manager.load_model()
        logger.info("Modelo carregado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao carregar modelo: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Finalizando aplicação...")

# Criar instância da aplicação FastAPI
app = FastAPI(
    title="Cardiac Risk Prediction API",
    description="API para previsão de risco cardíaco usando XGBoost com suporte a concorrência",
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
    Endpoint raiz para verificar se a API está funcionando
    """
    return {
        "message": "Cardiac Risk Prediction API", 
        "status": "ativo",
        "model_loaded": model_manager.is_loaded(),
        "version": "2.0.0"
    }

@app.get("/health")
async def health_check():
    """
    Endpoint de health check
    """
    return {
        "status": "healthy",
        "model_loaded": model_manager.is_loaded(),
        "timestamp": pd.Timestamp.now().isoformat(),
        "thread_id": threading.get_ident()
    }

@app.post("/predict_risk", response_model=PredictionResponse)
async def predict_risk(
    patient: PatientData,
    manager: ModelManager = Depends(get_model_manager)
):
    """
    Endpoint principal para previsão de risco cardíaco
    """
    import time
    start_time = time.time()
    
    try:
        # Verificar se o modelo está carregado
        if not manager.is_loaded():
            raise HTTPException(
                status_code=500, 
                detail="Modelo não carregado. Verifique os logs do servidor."
            )
        
        logger.info(f"Recebendo dados para previsão - Usuário: {patient.user_id}")
        
        # Validar dados do paciente
        validate_patient_data(patient)
        
        # Preprocessar dados
        input_df = preprocess_patient_data(patient)
        
        # Fazer previsão usando o manager thread-safe
        risk_probabilities = manager.predict(input_df)
        risk_score = float(risk_probabilities[0][1])  # Probabilidade da classe 1
        
        
        # Calcular tempo de processamento
        processing_time = (time.time() - start_time) * 1000  # em ms
        
        # Criar resposta
        response = PredictionResponse(
            user_id=patient.user_id,
            chronic_risk_score=round(risk_score, 4),
            processing_time_ms=round(processing_time, 2),
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
        
        logger.info(f"Previsão calculada - Usuário: {patient.user_id}, Risco: {risk_score:.4f}, risck-score: {round(risk_score, 4)}, Tempo: {processing_time:.2f}ms")
        
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
    Endpoint para obter informações sobre o modelo
    """
    try:
        return manager.get_model_info()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao obter informações do modelo: {e}")
        raise HTTPException(status_code=500, detail="Erro ao obter informações do modelo")

@app.get("/stats")
async def get_stats():
    """
    Endpoint para estatísticas de performance
    """
    return {
        "model_loaded": model_manager.is_loaded(),
        "thread_id": threading.get_ident(),
        "cache_info": preprocess_patient_data_cached.cache_info()._asdict(),
        "active_threads": threading.active_count()
    }

if __name__ == "__main__":
    # Configurar e executar o servidor
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8000,  # Porta diferente para não conflitar
        log_level="info",
        reload=False,
        workers=1  # Para desenvolvimento, em produção use mais workers
    )
