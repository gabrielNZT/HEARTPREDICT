Com certeza. Este arquivo `instructions.md` servirá como um guia técnico detalhado para orientar o desenvolvimento do projeto. Ele consolida toda a arquitetura e os fluxos de trabalho que discutimos.

---

# **Instruções de Projeto: Sistema Multiagentes para Alerta de Risco Cardíaco**

## 1. Visão Geral do Projeto

Este documento detalha a arquitetura e o plano de implementação para um sistema de alerta de risco cardíaco. O objetivo é criar uma plataforma robusta que combina análise de dados em tempo real com um sistema multiagentes (SMA) inteligente para tomada de decisão, notificação e explicabilidade (XAI).

A filosofia central é uma arquitetura híbrida:
* **Motor de Tempo Real:** Componentes de alta performance para ingestão e análise de dados de sensores.
* **Cérebro Operacional:** Uma plataforma de agentes (JADE) que orquestra a lógica de negócio, personaliza alertas e fornece explicações, agindo de forma autônoma e desacoplada.

## 2. Pilha de Tecnologia (Stack)

| Camada | Componente | Tecnologia | Linguagem/Framework |
| :--- | :--- | :--- | :--- |
| **Front-End** | Aplicação Web/Mobile | React ou Vue.js | JavaScript/TypeScript |
| **Back-End** | API Gateway | FastAPI | Python |
| **Agentes** | Plataforma SMA | JADE | Java |
| **Ciência de Dados**| Serviços de IA | FastAPI, Scikit-learn, TensorFlow | Python |
| **Banco de Dados** | Persistência | PostgreSQL + TimescaleDB | SQL |
| **Mensageria** | Tempo Real / Filas | MQTT Broker (ex: Mosquitto), RabbitMQ (Opcional) | N/A |
| **Comunicação** | Protocolos | REST API, MQTT, ACL | N/A |
| **Deployment** | Contêineres | Docker, Docker Compose | N/A |

## 3. Arquitetura Detalhada

### 3.1. Microsserviços de Ciência de Dados (Python)

Estes serviços devem ser desenvolvidos primeiro, pois são dependências críticas. Eles serão expostos como APIs REST e consumidos pelo Back-End e pelos Agentes JADE.

* **Serviço 1: Risco Crônico (`chronic-risk-service`)**
    * **Endpoint:** `POST /predict`
    * **Input (JSON):** `{ "age": 20000, "gender": 1, "ap_hi": 120, ... }`
    * **Output (JSON):** `{ "user_id": "...", "chronic_risk_score": 0.75 }`
    * **Modelo:** `XGBoost` ou `RandomForestClassifier` treinado com o dataset estático.

* **Serviço 2: Anomalia em Tempo Real (`realtime-anomaly-service`)**
    * **Endpoint:** `POST /predict`
    * **Input (JSON):** `{ "ecg_window": [0.1, 0.12, 0.15, ...] }` (array de floats)
    * **Output (JSON):** `{ "anomaly_score": 0.96, "classification": "arrhythmia" }`
    * **Modelo:** `LSTM` ou `CNN` treinado com um dataset de séries temporais (ex: MIT-BIH).

* **Serviço 3: Explicabilidade (`xai-service`)**
    * **Endpoint 1:** `POST /explain/chronic`
        * **Input:** `{ "user_features": {...} }`
        * **Output:** `{ "shap_values": {"ap_hi": 0.3, ...} }`
        * **Tecnologia:** Biblioteca `SHAP`.
    * **Endpoint 2:** `POST /explain/realtime`
        * **Input:** `{ "ecg_window": [...] }`
        * **Output:** `{ "original_signal": [...], "heatmap": [...] }`
        * **Tecnologia:** `Grad-CAM` ou similar.

### 3.2. Back-End: API Gateway (Python/FastAPI)

Atua como a fachada do sistema para o mundo exterior (Front-End).

* **Endpoints Principais:**
    * `POST /register`: Recebe dados do usuário, chama o `chronic-risk-service`, e envia uma mensagem para o `Agente Gateway` do JADE para iniciar o processo de criação de agentes.
    * `POST /login`: Autentica o usuário (JWT).
    * `GET /dashboard/{user_id}`: Retorna dados do perfil e histórico de alertas do PostgreSQL.
    * `POST /explain/{alert_id}`: Recebe a solicitação de explicação e a encaminha para o `Agente Gateway` do JADE.

### 3.3. Plataforma de Agentes (JADE/Java)

O coração do sistema. Cada agente é uma classe Java que herda de `jade.core.Agent`.

* **`AgenteGateway`**
    * **Comportamento:** `CyclicBehaviour` que escuta por requisições HTTP (usando uma lib como `SparkJava` embarcada) ou mensagens de uma fila (RabbitMQ).
    * **Lógica:** Traduz as requisições externas em mensagens `ACLMessage` e as envia para os agentes internos apropriados.

* **`AgenteGerenciadorPacientes`**
    * **Comportamento:** `CyclicBehaviour` que espera por mensagens de `REQUEST` para criar novos pacientes.
    * **Lógica:** Ao receber um pedido do `AgenteGateway`, usa o `ContainerController` para criar dinamicamente uma nova instância do `AgentePaciente` e `AgenteMonitor`.

* **`AgentePaciente`**
    * **Estado Interno:** Mantém o ID do usuário, o escore de risco crônico e outros estados relevantes.
    * **Comportamento:** `CyclicBehaviour` para receber mensagens de seu `AgenteMonitor`.
    * **Lógica:** Ao receber um `INFORM` sobre uma anomalia, combina essa informação com seu escore de risco crônico para determinar a severidade. Envia `REQUEST` para o `AgenteNotificador` e/ou `AgenteExplicador`.

* **`AgenteMonitor`**
    * **Comportamento:** `OneShotBehaviour` na inicialização para se inscrever no tópico MQTT correto (ex: `/pacientes/{id}`). `CyclicBehaviour` para receber as mensagens MQTT (usando uma lib como `Paho MQTT Client`).
    * **Lógica:** Para cada mensagem recebida, chama o `realtime-anomaly-service`. Se o score for alto, envia um `INFORM` para seu `AgentePaciente` pai.

* **`AgenteNotificador`**
    * **Comportamento:** `CyclicBehaviour` esperando por `REQUEST` de notificação.
    * **Lógica:** Usa bibliotecas Java (ex: Twilio SDK) para enviar notificações via SMS, email, etc., com base no conteúdo da mensagem.

* **`AgenteExplicador (AXAI)`**
    * **Comportamento:** `CyclicBehaviour` esperando por `REQUEST` de explicação.
    * **Lógica:** Recebe o pedido, chama o `xai-service` correspondente, recebe a explicação técnica (JSON), e a formata em linguagem natural (usando templates de string) antes de responder.

### 3.4. Persistência de Dados (PostgreSQL + TimescaleDB)

* **Tabela `pacientes` (PostgreSQL):**
    * `id` (UUID, PK), `nome` (TEXT), `email` (TEXT), `dados_perfil` (JSONB), `risco_cronico` (FLOAT)
* **Tabela `alertas` (PostgreSQL):**
    * `id` (UUID, PK), `paciente_id` (FK), `timestamp` (TIMESTAMPTZ), `severidade` (TEXT), `dados_gatilho` (JSONB), `texto_explicacao` (TEXT)
* **Hipertabela `leituras_ecg` (TimescaleDB):**
    * `timestamp` (TIMESTAMPTZ), `paciente_id` (UUID), `valor` (FLOAT)

## 4. Fluxos de Trabalho Essenciais para Codificação

### Fluxo 1: Onboarding de Novo Usuário
1.  **Front-End:** Envia `POST /register` com dados do formulário.
2.  **Back-End:** Recebe, chama o `chronic-risk-service` para obter o escore.
3.  **Back-End:** Envia mensagem (HTTP/RabbitMQ) para o `AgenteGateway` com todos os dados.
4.  **`AgenteGateway`:** Envia `ACLMessage` (REQUEST) para `AgenteGerenciadorPacientes`.
5.  **`AgenteGerenciadorPacientes`:** Cria `AgentePaciente` e `AgenteMonitor`.
6.  **`AgentePaciente`:** Salva os dados do paciente e o escore no PostgreSQL.
7.  **`AgenteMonitor`:** Inscreve-se no tópico MQTT do novo paciente.

### Fluxo 2: Detecção e Explicação de Alerta
1.  **Dispositivo:** Publica dados de ECG no tópico MQTT.
2.  **`AgenteMonitor`:** Recebe a mensagem, chama o `realtime-anomaly-service`.
3.  **`AgenteMonitor`:** Se anomalia detectada, envia `INFORM` para seu `AgentePaciente`.
4.  **`AgentePaciente`:** Recebe, avalia a severidade, e envia `REQUEST` para o `AgenteNotificador`.
5.  **`AgenteNotificador`:** Envia o alerta (SMS/Push).
6.  **Front-End:** Usuário clica em "Explicar" no alerta.
7.  **Back-End:** Envia pedido para o `AgenteGateway`.
8.  **`AgenteGateway`:** Encaminha o `REQUEST` de explicação para o `AgenteExplicador (AXAI)`.
9.  **`AXAI`:** Chama o `xai-service`, formata a resposta e a devolve.
10. **Front-End:** Exibe a explicação recebida.

## 5. Ordem de Implementação Sugerida

1.  **Setup do Ambiente:** Crie um arquivo `docker-compose.yml` para subir o PostgreSQL/TimescaleDB e um broker MQTT (Mosquitto).
2.  **Serviços de IA:** Desenvolva e teste os 3 serviços em Python. Eles são o alicerce. Crie endpoints de "mock" que retornem dados fixos para facilitar os testes das outras camadas.
3.  **Plataforma JADE:** Crie o esqueleto de todos os agentes em Java. Implemente a comunicação interna (ACL) entre eles primeiro. Teste a criação dinâmica de agentes.
4.  **Integração JADE <-> IA/MQTT:** Implemente as chamadas do `AgenteMonitor` para o serviço de IA e a inscrição no MQTT. Implemente as chamadas do `AXAI` para o serviço de XAI.
5.  **Back-End Gateway:** Desenvolva a API em FastAPI e a lógica para se comunicar com o `AgenteGateway`.
6.  **Front-End:** Com a API do Back-End estável, desenvolva a interface do usuário.