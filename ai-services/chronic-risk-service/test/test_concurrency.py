"""
Script para testar concorrência da API de previsão de risco cardíaco
"""

import asyncio
import aiohttp
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# Configurações
API_URL = "http://127.0.0.1:8001"  # Versão concorrente
MOCK_API_URL = "http://127.0.0.1:8000"  # Versão original
NUM_REQUESTS = 500
CONCURRENT_REQUESTS = 10

# Dados de teste
TEST_PATIENTS = [
    {
        "user_id": f"patient_{i}",
        "age": 30 + (i % 40),
        "gender": 1 + (i % 2),
        "height": 160 + (i % 25),
        "weight": 60.0 + (i % 40),
        "ap_hi": 110 + (i % 50),
        "ap_lo": 70 + (i % 30),
        "cholesterol": 1 + (i % 3),
        "gluc": 1 + (i % 3),
        "smoke": i % 2,
        "alco": i % 2,
        "active": 1 - (i % 2)
    }
    for i in range(NUM_REQUESTS)
]

async def make_async_request(session, url, data):
    """
    Faz uma requisição assíncrona
    """
    start_time = time.time()
    try:
        async with session.post(f"{url}/predict_risk", json=data) as response:
            result = await response.json()
            end_time = time.time()
            
            return {
                "success": True,
                "response_time": (end_time - start_time) * 1000,
                "status_code": response.status,
                "user_id": data["user_id"],
                "risk_score": result.get("chronic_risk_score", 0),
                "processing_time": result.get("processing_time_ms", 0)
            }
    except Exception as e:
        end_time = time.time()
        return {
            "success": False,
            "response_time": (end_time - start_time) * 1000,
            "error": str(e),
            "user_id": data["user_id"]
        }

def make_sync_request(url, data):
    """
    Faz uma requisição síncrona
    """
    start_time = time.time()
    try:
        response = requests.post(f"{url}/predict_risk", json=data)
        result = response.json()
        end_time = time.time()
        
        return {
            "success": True,
            "response_time": (end_time - start_time) * 1000,
            "status_code": response.status_code,
            "user_id": data["user_id"],
            "risk_score": result.get("chronic_risk_score", 0),
            "processing_time": result.get("processing_time_ms", 0)
        }
    except Exception as e:
        end_time = time.time()
        return {
            "success": False,
            "response_time": (end_time - start_time) * 1000,
            "error": str(e),
            "user_id": data["user_id"]
        }

async def test_async_concurrent_requests():
    """
    Testa requisições assíncronas concorrentes
    """
    print(f"=== TESTE ASSÍNCRONO CONCORRENTE ===")
    print(f"URL: {API_URL}")
    print(f"Requisições: {NUM_REQUESTS}")
    print(f"Concorrência: {CONCURRENT_REQUESTS}")
    
    connector = aiohttp.TCPConnector(limit=CONCURRENT_REQUESTS)
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(
        connector=connector, 
        timeout=timeout
    ) as session:
        
        start_time = time.time()
        
        # Limitar concorrência usando semáforo
        semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
        
        async def bounded_request(data):
            async with semaphore:
                return await make_async_request(session, API_URL, data)
        
        # Executar todas as requisições
        tasks = [bounded_request(patient) for patient in TEST_PATIENTS]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        
        # Analisar resultados
        analyze_results(results, end_time - start_time, "ASSÍNCRONO")

def test_sync_concurrent_requests():
    """
    Testa requisições síncronas concorrentes usando ThreadPoolExecutor
    """
    print(f"\n=== TESTE SÍNCRONO CONCORRENTE ===")
    print(f"URL: {API_URL}")
    print(f"Requisições: {NUM_REQUESTS}")
    print(f"Threads: {CONCURRENT_REQUESTS}")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        # Submeter todas as requisições
        future_to_patient = {
            executor.submit(make_sync_request, API_URL, patient): patient
            for patient in TEST_PATIENTS
        }
        
        results = []
        for future in as_completed(future_to_patient):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                patient = future_to_patient[future]
                results.append({
                    "success": False,
                    "error": str(e),
                    "user_id": patient["user_id"]
                })
    
    end_time = time.time()
    
    # Analisar resultados
    analyze_results(results, end_time - start_time, "SÍNCRONO")

def test_sequential_requests():
    """
    Testa requisições sequenciais para comparação
    """
    print(f"\n=== TESTE SEQUENCIAL ===")
    print(f"URL: {API_URL}")
    print(f"Requisições: {NUM_REQUESTS}")
    
    start_time = time.time()
    
    results = []
    for patient in TEST_PATIENTS:
        result = make_sync_request(API_URL, patient)
        results.append(result)
    
    end_time = time.time()
    
    # Analisar resultados
    analyze_results(results, end_time - start_time, "SEQUENCIAL")

def analyze_results(results, total_time, test_type):
    """
    Analisa e exibe os resultados dos testes
    """
    successful_results = [r for r in results if r["success"]]
    failed_results = [r for r in results if not r["success"]]
    
    print(f"\n--- RESULTADOS {test_type} ---")
    print(f"Tempo total: {total_time:.2f}s")
    print(f"Requisições bem-sucedidas: {len(successful_results)}")
    print(f"Requisições falhadas: {len(failed_results)}")
    
    if successful_results:
        response_times = [r["response_time"] for r in successful_results]
        processing_times = [r.get("processing_time", 0) for r in successful_results]
        
        print(f"Throughput: {len(successful_results) / total_time:.2f} req/s")
        print(f"Tempo de resposta médio: {statistics.mean(response_times):.2f}ms")
        print(f"Tempo de resposta mediano: {statistics.median(response_times):.2f}ms")
        print(f"Tempo de resposta mín/máx: {min(response_times):.2f}ms / {max(response_times):.2f}ms")
        
        if processing_times and any(pt > 0 for pt in processing_times):
            print(f"Tempo de processamento médio: {statistics.mean(processing_times):.2f}ms")
    
    if failed_results:
        print(f"Erros:")
        for error in failed_results[:5]:  # Mostrar apenas os primeiros 5 erros
            print(f"  - {error['user_id']}: {error.get('error', 'Unknown error')}")

async def test_api_health():
    """
    Testa se a API está funcionando
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/health") as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"API Health Check: ✓ {result}")
                    return True
                else:
                    print(f"API Health Check: ✗ Status {response.status}")
                    return False
    except Exception as e:
        print(f"API Health Check: ✗ Erro: {e}")
        return False

async def main():
    """
    Função principal dos testes
    """
    print("INICIANDO TESTES DE CONCORRÊNCIA")
    print("=" * 50)
    
    # Verificar se a API está funcionando
    if not await test_api_health():
        print("❌ API não está respondendo. Verifique se está rodando.")
        return
    
    # Aguardar um pouco para a API estar pronta
    await asyncio.sleep(2)
    
    # Executar testes
    print(f"\nTestando com {NUM_REQUESTS} requisições...")
    
    # Teste sequencial (baseline)
    test_sequential_requests()
    
    # Teste concorrente síncrono
    test_sync_concurrent_requests()
    
    # Teste concorrente assíncrono
    await test_async_concurrent_requests()
    
    print("\n" + "=" * 50)
    print("TESTES CONCLUÍDOS")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
