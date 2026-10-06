#!/bin/bash

# Script para executar todos os agentes JADE incluindo o AgenteExplicador
# Usa o arquivo JAR compilado

echo "Iniciando plataforma JADE com todos os agentes..."

# Caminho para o JAR compilado
JAR_PATH="target/cardiac-alert-jade.jar"

mvn clean package
# Verifica se a chave da API está configurada
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  AVISO: Variável GEMINI_API_KEY não configurada"
    echo "   O AgenteExplicador não funcionará sem a chave da API do Gemini"
    echo "   Configure com: export GEMINI_API_KEY='sua_chave_aqui'"
    echo ""
fi

if [ -z "$GEMINI_MODEL" ]; then
    echo "⚠️  AVISO: Variável GEMINI_MODEL não configurada"
    echo "   Defina um modelo vigente, ex.: export GEMINI_MODEL='<id-do-modelo>'"
    echo "   Lista oficial: https://ai.google.dev/gemini-api/docs/deprecations"
    echo ""
fi

# Executa a plataforma JADE com todos os agentes incluindo o novo AgenteClassificador
echo "Iniciando agentes: Gerenciador, Classificador, Julgador e Explicador..."
java --add-exports java.xml/com.sun.org.apache.xerces.internal.jaxp=ALL-UNNAMED \
    -jar "$JAR_PATH" \
    -gui \
    "gerenciador:br.com.yourproject.agents.AgenteGerenciadorPacientes;classificador:br.com.yourproject.agents.AgenteClassificador;julgador:br.com.yourproject.agents.AgenteJulgador;explicador:br.com.yourproject.agents.AgenteExplicador"

echo "Plataforma JADE iniciada com sucesso!"
