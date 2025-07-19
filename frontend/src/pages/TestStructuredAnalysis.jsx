import React from 'react';
import StructuredRiskAnalysis from '../components/StructuredRiskAnalysis';

const sampleData = {
  "patientName": "gabriel",
  "riskScore": 0.63,
  "riskLevel": "alto",
  "predictionStatus": "positiva",
  "predictionSummary": "A predição indica alta probabilidade de desenvolver doença cardiovascular no futuro. É crucial tomar medidas para reduzir os riscos.",
  "contributingFactors": [
    {
      "factorName": "IMC",
      "factorValue": "28.3",
      "riskType": "alerta",
      "details": "Seu IMC indica sobrepeso, aumentando o risco de doenças cardíacas. Perda de peso é recomendada."
    },
    {
      "factorName": "Pressão Arterial",
      "factorValue": "Stage1 Hypertension",
      "riskType": "alerta",
      "details": "Sua pressão arterial está elevada (Hipertensão Estágio 1), um fator de risco significativo para doenças cardíacas. Controle regular é essencial."
    },
    {
      "factorName": "Estilo de Vida",
      "factorValue": "Score 0",
      "riskType": "alerta",
      "details": "Seu score de estilo de vida indica necessidade de melhorias significativas em hábitos como dieta, exercício e controle do estresse para reduzir o risco cardiovascular."
    }
  ],
  "recommendations": [
    {
      "title": "Mudanças no Estilo de Vida",
      "details": "Incorpore uma dieta rica em frutas, vegetais e grãos integrais, reduza o consumo de sódio e gorduras saturadas. Inicie um programa regular de exercícios físicos, pelo menos 30 minutos na maioria dos dias da semana. Pratique técnicas de gerenciamento do estresse, como ioga ou meditação."
    },
    {
      "title": "Monitoramento Médico",
      "details": "Agende consultas regulares com seu médico para monitorar sua pressão arterial, colesterol e outros fatores de risco. Considere medicação se necessário, conforme orientação médica."
    }
  ],
  "modelInfo": {
    "accuracy": 80.1,
    "disclaimer": "Este modelo tem uma precisão de 80.1%, o que significa que existe uma margem de erro. Este resultado não substitui uma avaliação médica completa."
  }
};

export default function TestStructuredAnalysis() {
  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #e6f4ff 0%, #f0f9ff 50%, #ecfdf5 100%)',
      padding: '2rem'
    }}>
      <h1 style={{ textAlign: 'center', marginBottom: '2rem' }}>Teste do Componente Estruturado</h1>
      <StructuredRiskAnalysis explanation={sampleData} />
    </div>
  );
}
