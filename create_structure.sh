#!/bin/bash

# Script para criar a estrutura completa do HEARTPREDICT
# Execute com: bash create_structure.sh

echo "🚀 Criando estrutura do projeto Sistema de Alerta Cardíaco..."

# Criar diretórios principais
mkdir -p HEARTPREDICT/{ai-services,backend-gateway,frontend,jade-agents,mosquitto/config}

# Criar estrutura ai-services
mkdir -p HEARTPREDICT/ai-services/chronic-risk-service/{app,data,models,notebooks}
mkdir -p HEARTPREDICT/ai-services/realtime-anomaly-service/{app,models,notebooks}
mkdir -p HEARTPREDICT/ai-services/xai-service/app

# Criar estrutura backend-gateway
mkdir -p HEARTPREDICT/backend-gateway/app/clients

# Criar estrutura frontend
mkdir -p HEARTPREDICT/frontend/{public,src/{assets,components,pages,services}}

# Criar estrutura jade-agents
mkdir -p HEARTPREDICT/jade-agents/src/main/{java/br/com/yourproject/agents,resources}

# Adicionar arquivos __init__.py para Python
touch HEARTPREDICT/ai-services/chronic-risk-service/app/__init__.py
touch HEARTPREDICT/ai-services/realtime-anomaly-service/app/__init__.py
touch HEARTPREDICT/ai-services/xai-service/app/__init__.py
touch HEARTPREDICT/backend-gateway/app/__init__.py
touch HEARTPREDICT/backend-gateway/app/clients/__init__.py

# Adicionar .gitkeep para diretórios que podem ficar vazios inicialmente
touch HEARTPREDICT/ai-services/chronic-risk-service/data/.gitkeep
touch HEARTPREDICT/ai-services/chronic-risk-service/models/.gitkeep
touch HEARTPREDICT/ai-services/chronic-risk-service/notebooks/.gitkeep
touch HEARTPREDICT/ai-services/realtime-anomaly-service/models/.gitkeep
touch HEARTPREDICT/ai-services/realtime-anomaly-service/notebooks/.gitkeep
touch HEARTPREDICT/frontend/public/.gitkeep
touch HEARTPREDICT/frontend/src/assets/.gitkeep
touch HEARTPREDICT/frontend/src/components/.gitkeep
touch HEARTPREDICT/frontend/src/pages/.gitkeep
touch HEARTPREDICT/frontend/src/services/.gitkeep
touch HEARTPREDICT/jade-agents/src/main/resources/.gitkeep

# Criar diretório para dados do PostgreSQL
mkdir -p HEARTPREDICT/.pgdata

echo "✅ Estrutura criada com sucesso!"
echo "📁 Diretórios principais:"
echo "   - ai-services/ (Microsserviços de IA)"
echo "   - backend-gateway/ (Gateway principal)"
echo "   - frontend/ (Interface do usuário)"
echo "   - jade-agents/ (Plataforma JADE)"
echo "   - mosquitto/ (Configuração MQTT)"
echo ""
echo "🔧 Próximos passos:"
echo "   1. Revisar arquivos de configuração"
echo "   2. Executar: docker-compose up -d"
echo "   3. Configurar ambientes de desenvolvimento"
