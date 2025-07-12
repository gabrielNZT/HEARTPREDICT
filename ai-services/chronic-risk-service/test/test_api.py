"""
Script de teste para demonstrar o uso da API de previsão de risco cardíaco
"""

import requests
import json
import time

# URL base da API
API_URL = "http://127.0.0.1:8000"

def test_api_basic():
    """Testa endpoints básicos da API"""
    print("=== TESTANDO ENDPOINTS BÁSICOS ===")
    
    # Testar endpoint raiz
    response = requests.get(f"{API_URL}/")
    print(f"Endpoint raiz: {response.status_code} - {response.json()}")
    
    # Testar health check
    response = requests.get(f"{API_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    
    # Testar informações do modelo
    response = requests.get(f"{API_URL}/model_info")
    print(f"Model info: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))

def test_prediction():
    """Testa previsão de risco cardíaco"""
    print("\n=== TESTANDO PREVISÃO DE RISCO ===")
    
    # Caso 1: Paciente com baixo risco (jovem, boa saúde)
    test_cases = [
        {
            "name": "Paciente Baixo Risco",
            "data": {
                "user_id": "patient_low_risk",
                "age": 30,
                "gender": 1,
                "height": 165,
                "weight": 60.0,
                "ap_hi": 110,
                "ap_lo": 70,
                "cholesterol": 1,
                "gluc": 1,
                "smoke": 0,
                "alco": 0,
                "active": 1
            }
        },
        {
            "name": "Paciente Alto Risco",
            "data": {
                "user_id": "patient_high_risk",
                "age": 60,
                "gender": 2,
                "height": 175,
                "weight": 95.0,
                "ap_hi": 180,
                "ap_lo": 110,
                "cholesterol": 3,
                "gluc": 3,
                "smoke": 1,
                "alco": 1,
                "active": 0
            }
        },
        {
            "name": "Paciente Moderado",
            "data": {
                "user_id": "patient_moderate_risk",
                "age": 45,
                "gender": 1,
                "height": 165,
                "weight": 70.5,
                "ap_hi": 130,
                "ap_lo": 85,
                "cholesterol": 2,
                "gluc": 1,
                "smoke": 0,
                "alco": 0,
                "active": 1
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n--- {test_case['name']} ---")
        print(f"Dados de entrada:")
        print(json.dumps(test_case['data'], indent=2))
        
        try:
            response = requests.post(f"{API_URL}/predict_risk", json=test_case['data'])
            
            if response.status_code == 200:
                result = response.json()
                print(f"Resposta:")
                print(json.dumps(result, indent=2))
                
                # Análise do resultado
                risk_score = result['chronic_risk_score']
                risk_level = result['risk_level']
                print(f"Resumo: Risco = {risk_score:.4f} ({risk_level})")
                
            else:
                print(f"Erro: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Erro na requisição: {e}")

def test_validation():
    """Testa validação de dados"""
    print("\n=== TESTANDO VALIDAÇÃO DE DADOS ===")
    
    # Caso com dados inválidos
    invalid_cases = [
        {
            "name": "Pressão arterial inválida",
            "data": {
                "user_id": "invalid_bp",
                "age": 45,
                "gender": 1,
                "height": 165,
                "weight": 70.5,
                "ap_hi": 70,  # Menor que diastólica
                "ap_lo": 80,
                "cholesterol": 1,
                "gluc": 1,
                "smoke": 0,
                "alco": 0,
                "active": 1
            }
        }
    ]
    
    for test_case in invalid_cases:
        print(f"\n--- {test_case['name']} ---")
        try:
            response = requests.post(f"{API_URL}/predict_risk", json=test_case['data'])
            print(f"Status: {response.status_code}")
            print(f"Resposta: {response.text}")
        except Exception as e:
            print(f"Erro: {e}")

def main():
    """Função principal de teste"""
    print("INICIANDO TESTES DA API DE PREVISÃO DE RISCO CARDÍACO")
    print("=" * 60)
    
    # Aguardar a API estar pronta
    time.sleep(1)
    
    # Executar testes
    test_api_basic()
    test_prediction()
    test_validation()
    
    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS")

if __name__ == "__main__":
    main()
