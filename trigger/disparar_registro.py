import requests
import json

# --- DADOS DO PACIENTE ---
# Agora enviamos apenas os dados do paciente, sem fazer chamada prévia para IA
AGENT_GATEWAY_URL = "http://127.0.0.1:8888/registrar" # URL do agente gerenciador

patient_data = {
        "user_id": "guilherme", "age": 25, "gender": 2, "height": 190, "weight": 80.0,
        "ap_hi": 130, "ap_lo": 90, "cholesterol": 0, "gluc": 1, "smoke": 0, "alco": 1, "active": 1
}

def main():
    # --- ENVIAR DADOS DIRETAMENTE PARA O AGENTE GERENCIADOR ---
    print("Enviando dados do paciente para o AgenteGerenciadorPacientes...")
    try:
        # Enviamos apenas os dados do paciente como JSON
        # O AgenteClassificador irá fazer a chamada para o serviço de IA
        headers = {'Content-Type': 'application/json'}
        response_jade = requests.post(AGENT_GATEWAY_URL, data=json.dumps(patient_data), headers=headers)
        
        response_jade.raise_for_status()
        
        print(f"   => SUCESSO! Agente respondeu com status {response_jade.status_code}")
        print(f"   => Resposta do agente: '{response_jade.text}'")

    except Exception as e:
        print(f"   => ERRO ao contatar o Gateway do Agente: {e}")
        return

if __name__ == "__main__":
    main()
