from pydantic import BaseModel, Field
from typing import Dict, Any

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
