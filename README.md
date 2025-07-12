# 🫀 Sistema de Alerta Cardíaco

Um sistema multiagentes inteligente para detecção e alerta de riscos cardíacos, combinando análise de dados crônicos e monitoramento em tempo real através de uma arquitetura híbrida de microsserviços e agentes autônomos.

## 🚀 Sobre o Projeto

O **Sistema de Alerta Cardíaco** é uma plataforma inovadora que utiliza Inteligência Artificial e Sistemas Multiagentes para:

- **🔍 Análise de Risco Crônico**: Avaliação de fatores de risco cardiovascular a longo prazo
- **⚡ Detecção de Anomalias em Tempo Real**: Monitoramento contínuo de sinais vitais (ECG, frequência cardíaca)
- **🤖 Agentes Autônomos**: Coordenação inteligente entre diferentes componentes do sistema
- **📊 Explicabilidade (XAI)**: Transparência nas decisões de IA para profissionais de saúde
- **🚨 Alertas Inteligentes**: Notificações contextualizadas e priorizadas

### 🎯 Características Principais

- **Arquitetura Híbrida**: Microsserviços Python + Plataforma JADE (Java)
- **Comunicação Assíncrona**: MQTT para mensagens em tempo real
- **Banco de Dados Temporal**: PostgreSQL + TimescaleDB para séries temporais
- **IA Explicável**: Implementação de técnicas XAI (SHAP, LIME)
- **Containerização**: Docker para facilitar deployment e escalabilidade

## 🛠️ Tecnologias Utilizadas

### Backend & APIs
- **FastAPI** - Framework web moderno e rápido para Python
- **JADE** - Plataforma de agentes autônomos em Java
- **PostgreSQL + TimescaleDB** - Banco de dados relacional com extensão para séries temporais
- **Eclipse Mosquitto** - Broker MQTT para comunicação assíncrona

### Inteligência Artificial
- **TensorFlow/Keras** - Deep Learning para análise de ECG
- **Scikit-learn** - Machine Learning clássico para análise de risco
- **XGBoost** - Gradient Boosting para predições robustas
- **SHAP & LIME** - Explicabilidade de modelos de IA

### DevOps & Infraestrutura
- **Docker & Docker Compose** - Containerização e orquestração
- **GitHub Actions** - CI/CD (planejado)
- **Prometheus** - Monitoramento (planejado)

### Frontend (Planejado)
- **React.js** - Interface web moderna e responsiva
- **Chart.js/D3.js** - Visualizações interativas
- **Material-UI** - Componentes de interface

## 📦 Como Rodar (Setup)

### Pré-requisitos

- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- **Git**
- **Java** >= 17 (para desenvolvimento JADE)
- **Python** >= 3.11 (para desenvolvimento dos microsserviços)
- **Node.js** >= 18 (para o frontend)

### 🚀 Início Rápido

1. **Clone o repositório**
   ```bash
   git clone <repository-url>
   cd HEARTPREDICT
   ```

2. **Crie a estrutura de pastas** (se necessário)
   ```bash
   bash create_structure.sh
   ```

3. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

4. **Inicie os serviços de infraestrutura**
   ```bash
   docker-compose up -d postgres-db mqtt-broker
   ```

5. **Aguarde os serviços estarem prontos e inicie o sistema completo**
   ```bash
   docker-compose up -d
   ```

6. **Verifique se todos os serviços estão rodando**
   ```bash
   docker-compose ps
   ```

### 🔗 Endpoints Principais

| Serviço | URL Local | Descrição |
|---------|-----------|-----------|
| **Gateway Principal** | http://localhost:8000 | API principal do sistema |
| **Risco Crônico** | http://localhost:8001 | Serviço de análise de risco |
| **Anomalia Tempo Real** | http://localhost:8002 | Serviço de detecção de anomalias |
| **XAI Service** | http://localhost:8003 | Serviço de explicabilidade |
| **Frontend** | http://localhost:3000 | Interface web |
| **MQTT Broker** | localhost:1883 | Broker de mensagens |
| **PostgreSQL** | localhost:5432 | Banco de dados |

### 📋 Comandos Úteis

```bash
# Ver logs de um serviço específico
docker-compose logs -f chronic-risk-service

# Reiniciar um serviço
docker-compose restart backend-gateway

# Acessar shell de um container
docker-compose exec postgres-db psql -U cardiac_user -d cardiac_alert_db

# Parar todos os serviços
docker-compose down

# Parar e remover volumes (⚠️ CUIDADO: remove dados!)
docker-compose down -v
```

## 📂 Estrutura de Pastas

```
HEARTPREDICT/
│
├── 📋 .gitignore                    # Arquivos ignorados pelo Git
├── 🐳 docker-compose.yml           # Orquestração de serviços
├── 📖 README.md                    # Esta documentação
├── 📝 instructions.md              # Planejamento detalhado do projeto
└── 🔨 create_structure.sh          # Script de criação da estrutura
│
├── 🤖 ai-services/                 # Microsserviços de IA
│   │
│   ├── 📊 chronic-risk-service/    # Análise de risco crônico
│   │   ├── app/                    # Código da aplicação FastAPI
│   │   ├── data/                   # Datasets para treinamento
│   │   ├── models/                 # Modelos treinados (.pkl, .h5)
│   │   ├── notebooks/              # Jupyter notebooks
│   │   ├── 🐳 Dockerfile
│   │   └── 📦 requirements.txt
│   │
│   ├── ⚡ realtime-anomaly-service/ # Detecção de anomalias em tempo real
│   │   ├── app/                    # Código da aplicação FastAPI
│   │   ├── models/                 # Modelos de séries temporais
│   │   ├── notebooks/              # Análise e treinamento
│   │   ├── 🐳 Dockerfile
│   │   └── 📦 requirements.txt
│   │
│   └── 🔍 xai-service/            # Explicabilidade de IA
│       ├── app/                    # Endpoints de explicação
│       ├── 🐳 Dockerfile
│       └── 📦 requirements.txt
│
├── 🌐 backend-gateway/             # Gateway principal
│   ├── app/                        # API principal (FastAPI)
│   │   └── clients/                # Clientes para JADE e outros serviços
│   ├── 🐳 Dockerfile
│   └── 📦 requirements.txt
│
├── 🎨 frontend/                    # Interface web (React)
│   ├── public/                     # Arquivos estáticos
│   ├── src/                        # Código-fonte React
│   │   ├── assets/                 # Imagens, CSS, fontes
│   │   ├── components/             # Componentes reutilizáveis
│   │   ├── pages/                  # Páginas da aplicação
│   │   └── services/               # Clientes HTTP
│   ├── 🐳 Dockerfile
│   └── 📦 package.json
│
├── ☕ jade-agents/                 # Plataforma JADE (Java)
│   ├── src/main/java/br/com/yourproject/agents/  # Agentes autônomos
│   │   ├── AgenteGateway.java      # Agente de coordenação
│   │   ├── AgenteGerenciadorPacientes.java
│   │   ├── AgenteMonitor.java      # Monitoramento em tempo real
│   │   ├── AgenteNotificador.java  # Sistema de alertas
│   │   ├── AgentePaciente.java     # Representação de pacientes
│   │   └── AgenteExplicador.java   # Coordenação de XAI
│   ├── src/main/resources/         # Configurações
│   ├── 🐳 Dockerfile
│   └── 📋 pom.xml                  # Dependências Maven
│
└── 📡 mosquitto/                   # Configuração MQTT
    └── config/
        └── mosquitto.conf          # Configuração do broker
```

## 👥 Contribuição

Este projeto está em desenvolvimento ativo. Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## 📞 Contato

- **Equipe de Desenvolvimento**: [seu-email@domain.com]
- **Documentação Técnica**: Ver `instructions.md`
- **Issues**: [GitHub Issues](link-para-issues)

---

⚡ **Feito com ❤️ para salvar vidas através da tecnologia**
