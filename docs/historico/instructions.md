> **Documento histórico.** Descreve a arquitetura original do projeto (ECG em tempo real, MQTT, TimescaleDB, serviço XAI), que foi **substituída** em 29/09/2026. A arquitetura vigente e as razões da mudança estão em `tcc/00-projeto/escopo-e-arquitetura.md` e `tcc/00-projeto/decisoes.md` (D019, D020).

# 📋 Instruções de Desenvolvimento - Sistema de Alerta Cardíaco

Este documento contém o planejamento técnico detalhado e as instruções para o desenvolvimento do **Sistema Multiagentes para Alerta de Risco Cardíaco**.

## 📑 Índice

1. [Visão Geral da Arquitetura](#-visão-geral-da-arquitetura)
2. [Componentes do Sistema](#-componentes-do-sistema)
3. [Fluxo de Dados](#-fluxo-de-dados)
4. [Sprints de Desenvolvimento](#-sprints-de-desenvolvimento)
5. [Padrões de Desenvolvimento](#-padrões-de-desenvolvimento)
6. [Configuração de Desenvolvimento](#-configuração-de-desenvolvimento)

## 🏗️ Visão Geral da Arquitetura

O sistema utiliza uma **arquitetura híbrida** que combina:

- **Microsserviços Python** para endpoints de IA e gateway
- **Plataforma JADE (Java)** para lógica de agentes autônomos
- **MQTT** para comunicação assíncrona em tempo real
- **PostgreSQL + TimescaleDB** para persistência de dados temporais

### Princípios Arquiteturais

1. **Separação de Responsabilidades**: Cada serviço tem uma função específica
2. **Comunicação Assíncrona**: MQTT para mensagens em tempo real
3. **Escalabilidade Horizontal**: Containerização com Docker
4. **Observabilidade**: Logs estruturados e métricas
5. **Explicabilidade**: XAI integrada ao sistema

## 🔧 Componentes do Sistema

### 1. AI Services (Microsserviços Python)

#### 1.1 Chronic Risk Service (`ai-services/chronic-risk-service/`)
**Responsabilidade**: Análise de risco cardiovascular crônico

**Endpoints Principais**:
- `POST /predict` - Predição de risco baseada em dados do paciente
- `GET /health` - Health check do serviço
- `GET /model-info` - Informações sobre o modelo ativo

**Tecnologias**:
- FastAPI para API REST
- Scikit-learn/XGBoost para ML
- Pandas para processamento de dados

**Entradas**:
```json
{
  "patient_id": "12345",
  "age": 45,
  "gender": "M",
  "blood_pressure_systolic": 140,
  "blood_pressure_diastolic": 90,
  "cholesterol": 240,
  "glucose": 120,
  "smoking": true,
  "alcohol": false,
  "physical_activity": 2
}
```

**Saídas**:
```json
{
  "patient_id": "12345",
  "risk_score": 0.75,
  "risk_level": "HIGH",
  "prediction_timestamp": "2024-01-15T10:30:00Z",
  "model_version": "v1.2.0"
}
```

#### 1.2 Realtime Anomaly Service (`ai-services/realtime-anomaly-service/`)
**Responsabilidade**: Detecção de anomalias em sinais vitais em tempo real

**Endpoints Principais**:
- `POST /predict` - Análise de série temporal de ECG
- `WebSocket /ws/monitor` - Stream de monitoramento em tempo real

**Tecnologias**:
- TensorFlow/Keras para deep learning
- WebSockets para comunicação em tempo real
- MQTT para receber dados de dispositivos

**Entradas** (via MQTT):
```json
{
  "patient_id": "12345",
  "timestamp": "2024-01-15T10:30:00Z",
  "ecg_signal": [0.1, 0.2, 0.15, ...],
  "heart_rate": 75,
  "device_id": "ECG001"
}
```

#### 1.3 XAI Service (`ai-services/xai-service/`)
**Responsabilidade**: Explicabilidade das predições de IA

**Endpoints Principais**:
- `POST /explain/chronic` - Explicação de predição de risco crônico
- `POST /explain/realtime` - Explicação de detecção de anomalia

**Tecnologias**:
- SHAP para explicações globais e locais
- LIME para explicações interpretáveis
- Plotly para visualizações

### 2. Backend Gateway (`backend-gateway/`)
**Responsabilidade**: API principal e coordenação do sistema

**Endpoints Principais**:
- `POST /auth/login` - Autenticação de usuários
- `POST /patients/register` - Cadastro de paciente
- `GET /patients/{id}/risk` - Consulta de risco do paciente
- `GET /patients/{id}/monitoring` - Status de monitoramento
- `POST /alerts/acknowledge` - Confirmação de alertas

### 3. JADE Platform (`jade-agents/`)
**Responsabilidade**: Coordenação através de agentes autônomos

#### Agentes Implementados:

##### 3.1 AgenteGateway
- Coordena comunicação entre agentes
- Interface com o backend-gateway
- Gerencia sessões de usuário

##### 3.2 AgenteGerenciadorPacientes  
- Mantém estado dos pacientes
- Coordena cadastros e atualizações
- Persiste dados no PostgreSQL

##### 3.3 AgenteMonitor
- Monitora sinais vitais em tempo real
- Detecta situações críticas
- Aciona alertas quando necessário

##### 3.4 AgenteNotificador
- Gerencia sistema de alertas
- Prioriza notificações
- Integra com sistemas externos

##### 3.5 AgentePaciente
- Representa um paciente no sistema
- Mantém histórico médico
- Coordena análises personalizadas

##### 3.6 AgenteExplicador
- Coordena requisições de XAI
- Integra explicações com alertas
- Gerencia contexto para explicações

## 🔄 Fluxo de Dados

### Fluxo de Análise de Risco Crônico
1. **Frontend** → `POST /patients/{id}/risk` → **Backend Gateway**
2. **Backend Gateway** → **AgenteGateway** (via JADE)
3. **AgenteGateway** → **AgenteGerenciadorPacientes**
4. **AgenteGerenciadorPacientes** → **Chronic Risk Service** (HTTP)
5. **Chronic Risk Service** retorna predição
6. **AgenteExplicador** → **XAI Service** (para explicação)
7. Resultado consolidado retorna para o frontend

### Fluxo de Monitoramento em Tempo Real
1. **Dispositivo ECG** → **MQTT Broker** (tópico: `patients/{id}/vitals`)
2. **AgenteMonitor** subscreve tópico MQTT
3. **AgenteMonitor** → **Realtime Anomaly Service**
4. Se anomalia detectada → **AgenteNotificador**
5. **AgenteNotificador** dispara alertas via múltiplos canais

## 📅 Sprints de Desenvolvimento

### Sprint 0: Configuração e Estrutura ✅
- [x] Estrutura de pastas do monorepo
- [x] Configuração Docker Compose
- [x] Configuração MQTT Broker
- [x] Setup inicial do JADE
- [x] Documentação inicial

### Sprint 1: Serviços Base (2 semanas)
**Objetivos**:
- [ ] Implementar Chronic Risk Service básico
- [ ] Configurar PostgreSQL + TimescaleDB
- [ ] Implementar Backend Gateway básico
- [ ] Setup inicial dos agentes JADE

**Entregáveis**:
- Chronic Risk Service com endpoint `/predict`
- Backend Gateway com autenticação básica
- Agentes JADE básicos funcionando
- Testes unitários dos serviços

### Sprint 2: Monitoramento em Tempo Real (2 semanas)
**Objetivos**:
- [ ] Implementar Realtime Anomaly Service
- [ ] Configurar comunicação MQTT
- [ ] Implementar WebSockets para frontend
- [ ] Integrar agentes com MQTT

**Entregáveis**:
- Serviço de detecção de anomalias
- Comunicação MQTT funcionando
- Agente Monitor integrado
- Dashboard básico em tempo real

### Sprint 3: Explicabilidade e XAI (2 semanas)
**Objetivos**:
- [ ] Implementar XAI Service
- [ ] Integrar SHAP e LIME
- [ ] Criar visualizações de explicação
- [ ] Implementar Agente Explicador

**Entregáveis**:
- Serviço de explicabilidade completo
- Visualizações XAI no frontend
- Explicações contextualizadas
- Documentação de IA explicável

### Sprint 4: Interface de Usuário (2 semanas)
**Objetivos**:
- [ ] Desenvolver frontend React
- [ ] Implementar dashboard de monitoramento
- [ ] Criar sistema de alertas visuais
- [ ] Integrar com todos os serviços

**Entregáveis**:
- Interface web completa
- Dashboard responsivo
- Sistema de notificações
- UX/UI polida

### Sprint 5: Otimização e Deploy (1 semana)
**Objetivos**:
- [ ] Otimizar performance dos modelos
- [ ] Configurar monitoramento (Prometheus)
- [ ] Setup de produção
- [ ] Testes de carga

**Entregáveis**:
- Sistema otimizado
- Monitoramento implementado
- Documentação de deploy
- Testes de stress aprovados

## 🎯 Padrões de Desenvolvimento

### Estrutura de APIs Python (FastAPI)
```python
# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import structlog

logger = structlog.get_logger()
app = FastAPI(title="Service Name", version="1.0.0")

class PredictionRequest(BaseModel):
    patient_id: str
    # outros campos...

class PredictionResponse(BaseModel):
    risk_score: float
    risk_level: str
    # outros campos...

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    logger.info("Prediction requested", patient_id=request.patient_id)
    # lógica de predição...
    return PredictionResponse(...)
```

### Estrutura de Agentes JADE
```java
public class AgenteGateway extends Agent {
    
    @Override
    protected void setup() {
        // Configuração inicial do agente
        addBehaviour(new ReceiveMessagesBehaviour());
        addBehaviour(new ProcessRequestsBehaviour());
    }
    
    private class ProcessRequestsBehaviour extends CyclicBehaviour {
        @Override
        public void action() {
            ACLMessage msg = receive();
            if (msg != null) {
                processMessage(msg);
            } else {
                block();
            }
        }
    }
}
```

### Padrão de Logging
```python
import structlog

# Configuração padrão
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

logger = structlog.get_logger()

# Uso nos serviços
logger.info("Processing request", 
           patient_id=patient_id, 
           service="chronic-risk",
           request_id=request_id)
```

### Padrão de Configuração
```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "cardiac_alert_db"
    mqtt_broker: str = "localhost"
    mqtt_port: int = 1883
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## ⚙️ Configuração de Desenvolvimento

### Configuração Python
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar serviço
uvicorn app.main:app --reload --port 8000
```

### Configuração Java/JADE
```bash
# Compilar projeto
mvn clean compile

# Executar JADE
mvn exec:java -Dexec.mainClass="jade.Boot" \
  -Dexec.args="-gui -agents gateway:br.com.yourproject.agents.AgenteGateway"
```

### Testes
```bash
# Python
pytest tests/ -v --cov=app

# Java
mvn test
```

### Variáveis de Ambiente

Criar arquivo `.env` na raiz:
```env
# Banco de Dados
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cardiac_alert_db
DB_USER=cardiac_user
DB_PASSWORD=cardiac_password_2024

# MQTT
MQTT_BROKER=localhost
MQTT_PORT=1883

# Serviços
CHRONIC_RISK_SERVICE_URL=http://localhost:8001
REALTIME_ANOMALY_SERVICE_URL=http://localhost:8002
XAI_SERVICE_URL=http://localhost:8003

# Segurança
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
```

## 🔍 Monitoramento e Debugging

### Health Checks
Todos os serviços devem implementar:
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }
```

### Métricas Prometheus
```python
from prometheus_client import Counter, Histogram, generate_latest

prediction_counter = Counter('predictions_total', 'Total predictions')
prediction_duration = Histogram('prediction_duration_seconds', 'Prediction duration')

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

---

Este documento será atualizado conforme o desenvolvimento progride. Para dúvidas técnicas, consulte a documentação de cada componente ou abra uma issue no repositório.
