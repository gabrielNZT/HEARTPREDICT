from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import json
import asyncio
import logging
from typing import Optional
import uuid
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="HeartPredict Gateway", version="1.0.0")

# Storage temporário para aguardar respostas dos agentes
pending_explanations = {}

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer host
    allow_credentials=False,  # Necessário quando allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    user_id: str
    age: int
    gender: int  # 1=Female, 2=Male, 3=Other
    height: int  # cm
    weight: float  # kg
    ap_hi: int  # systolic blood pressure
    ap_lo: int  # diastolic blood pressure
    cholesterol: int  # 1=normal, 2=above normal, 3=well above normal
    gluc: int  # 1=normal, 2=above normal, 3=well above normal
    smoke: int  # 0=no, 1=yes
    alco: int  # 0=no, 1=yes
    active: int  # 0=no, 1=yes

class ExplanationData(BaseModel):
    explanation: str

class PredictionResponse(BaseModel):
    success: bool
    patient_data: Optional[PatientData] = None
    prediction: Optional[dict] = None
    explanation: Optional[str] = None
    error: Optional[str] = None

# URL do AgenteGerenciadorPacientes
JADE_AGENT_URL = "http://localhost:8888/registrar"

@app.post("/predict", response_model=PredictionResponse)
async def predict_cardiac_risk(patient_data: PatientData):
    """
    Endpoint principal para predição de risco cardíaco
    """
    try:
        logger.info(f"Recebendo dados do paciente: {patient_data.user_id}")
        
        # Converte os dados para o formato esperado pelo chronic-risk-service
        chronic_service_data = {
            "user_id": patient_data.user_id,
            "age": patient_data.age,
            "gender": patient_data.gender,
            "height": patient_data.height,
            "weight": patient_data.weight,
            "ap_hi": patient_data.ap_hi,
            "ap_lo": patient_data.ap_lo,
            "cholesterol": patient_data.cholesterol,
            "gluc": patient_data.gluc,
            "smoke": patient_data.smoke,
            "alco": patient_data.alco,
            "active": patient_data.active
        }
        
        logger.info(f"Enviando dados para JADE Agent: {chronic_service_data}")
        
        # Envia dados para o AgenteGerenciadorPacientes
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                JADE_AGENT_URL,
                json=chronic_service_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro na comunicação com JADE Agent: {response.status_code}"
                )
        
        logger.info("Dados enviados com sucesso para JADE Agent")
        
        # Aguardar resposta real do agente explicador
        explanation = await wait_for_explanation(patient_data.user_id)
        
        if explanation is None:
            raise HTTPException(
                status_code=408,
                detail="Timeout: Não foi possível obter explicação do agente"
            )
        
        return PredictionResponse(
            success=True,
            patient_data=patient_data,
            prediction={"risk_level": "analyzed"},
            explanation=explanation
        )
        
    except httpx.RequestError as e:
        logger.error(f"Erro de conexão com JADE Agent: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Serviço de análise temporariamente indisponível"
        )
    except Exception as e:
        logger.error(f"Erro interno: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno do servidor: {str(e)}"
        )

async def wait_for_explanation(user_id: str, timeout: int = 60) -> Optional[str]:
    """
    Aguarda a explicação do agente explicador via polling
    """
    logger.info(f"Aguardando explicação para usuário {user_id}")
    
    # Registra que estamos aguardando explicação para este usuário
    pending_explanations[user_id] = {
        "timestamp": datetime.now(),
        "explanation": None
    }
    
    # Polling para aguardar a resposta
    start_time = datetime.now()
    while (datetime.now() - start_time).seconds < timeout:
        # Verifica se recebemos a explicação
        if user_id in pending_explanations and pending_explanations[user_id]["explanation"]:
            explanation = pending_explanations[user_id]["explanation"]
            # Remove da lista de pendentes
            del pending_explanations[user_id]
            logger.info(f"Explicação recebida para usuário {user_id}")
            return explanation
        
        # Aguarda um pouco antes de verificar novamente
        await asyncio.sleep(1)
    
    # Timeout - remove da lista de pendentes
    if user_id in pending_explanations:
        del pending_explanations[user_id]
    
    logger.warning(f"Timeout aguardando explicação para usuário {user_id}")
    return None

@app.get("/health")
async def health_check():
    """
    Endpoint de verificação de saúde do serviço
    """
    return {"status": "healthy", "service": "HeartPredict Gateway"}

@app.post("/explanation/{user_id}")
async def receive_explanation(user_id: str, explanation_data: ExplanationData):
    """
    Endpoint para receber explicações do agente explicador
    """
    logger.info(f"Recebendo explicação para usuário {user_id}: {explanation_data.explanation}")
    
    # Armazena a explicação para o usuário correspondente
    if user_id in pending_explanations:
        pending_explanations[user_id]["explanation"] = explanation_data.explanation
        logger.info(f"Explicação armazenada para usuário {user_id}")
    else:
        logger.warning(f"Explicação recebida para usuário {user_id} que não está aguardando")
    
    return {"status": "explanation_received", "user_id": user_id}

@app.get("/pending")
async def get_pending_explanations():
    """
    Endpoint para debug - lista explicações pendentes
    """
    return {"pending_explanations": list(pending_explanations.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
