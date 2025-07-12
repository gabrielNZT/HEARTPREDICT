import requests
import json

# --- DADOS DO PACIENTE E IA ---
AI_SERVICE_URL = "http://127.0.0.1:8000/predict_risk"
AGENT_GATEWAY_URL = "http://127.0.0.1:8888/registrar" # A nova URL do nosso agente!

patient_data = {
        "user_id": "guilherme", "age": 60, "gender": 2, "height": 190, "weight": 80,
        "ap_hi": 140, "ap_lo": 90, "cholesterol": 2, "gluc": 1, "smoke": 0, "alco": 0, "active": 0
}

def main():
    # --- ETAPA 1: CHAMAR O SERVIÇO DE IA ---
    print("1. Chamando o serviço de IA...")
    try:
        response_ia = requests.post(AI_SERVICE_URL, json=patient_data)
        response_ia.raise_for_status()
        risk_data = response_ia.json()
        print(f"   => SUCESSO! Dados da IA: {risk_data}")
    except Exception as e:
        print(f"   => ERRO na chamada da IA: {e}")
        return

    # --- ETAPA 2: ENVIAR DADOS PARA O NOSSO NOVO GATEWAY NO AGENTE JADE ---
    print("\n2. Enviando dados para o Gateway HTTP do Agente...")
    try:
        # Enviamos os dados que recebemos da IA como um JSON simples.
        # O agente agora espera JSON, não mais a string ACL complexa.
        headers = {'Content-Type': 'application/json'}
        response_jade = requests.post(AGENT_GATEWAY_URL, data=json.dumps(risk_data), headers=headers)
        
        response_jade.raise_for_status()
        
        print(f"   => SUCESSO! Agente respondeu com status {response_jade.status_code}")
        print(f"   => Resposta do agente: '{response_jade.text}'")

    except Exception as e:
        print(f"   => ERRO ao contatar o Gateway do Agente: {e}")
        return

if __name__ == "__main__":
    main()
