# main_mock.py
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Define a estrutura de dados do paciente que esperamos receber
class PatientData(BaseModel):
    user_id: str
    age: int
    gender: int
    ap_hi: int # Pressão sistólica
    ap_lo: int # Pressão diastólica
    cholesterol: int
    gluc: int # Glicose

app = FastAPI()

@app.post("/predict_risk")
def predict_risk(patient: PatientData):
    print(f"Recebi dados para o paciente: {patient.user_id}")

    risk_score = 0.78 

    print(f"Calculando risco (mock)... Risco = {risk_score}")

    return {"user_id": patient.user_id, "chronic_risk_score": risk_score}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)