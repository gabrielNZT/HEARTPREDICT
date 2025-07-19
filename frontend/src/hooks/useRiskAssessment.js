import { useState } from 'react';

const BACKEND_URL = 'http://localhost:8000';

export function useRiskAssessment() {
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState(null);

  const sendPatientData = async (patientData) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('Enviando dados para o backend:', patientData);
      
      const response = await fetch(`${BACKEND_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(patientData),
      });

      if (!response.ok) {
        throw new Error(`Erro HTTP: ${response.status}`);
      }

      const result = await response.json();
      console.log('Resposta do backend:', result);

      if (result.success && result.explanation) {
        // Cria uma mensagem formatada para o chat
        const explanation = result.explanation;
        const formattedText = `🏥 **Análise Cardiovascular Completa**

👤 **Paciente:** ${explanation.patientName}
📊 **Score de Risco:** ${explanation.riskScore} (${explanation.riskLevel})
🔍 **Predição:** ${explanation.predictionStatus}

💡 **Resumo:** ${explanation.predictionSummary}

🎯 **Fatores Analisados:**
${explanation.contributingFactors.map(factor => 
  `• **${factor.factorName}:** ${factor.factorValue} ${factor.riskType === 'alerta' ? '⚠️' : factor.riskType === 'sucesso' ? '✅' : '🚨'}
  ${factor.details}`
).join('\n\n')}

💪 **Recomendações:**
${explanation.recommendations.map((rec, index) => 
  `${index + 1}. **${rec.title}**
  ${rec.details}`
).join('\n\n')}

📈 **Sobre o Modelo:** ${explanation.modelInfo.disclaimer}`;

        const explanationMessage = {
          text: formattedText,
          sender: 'llm',
          isStructured: true
        };
        
        setMessages([explanationMessage]);
      } else {
        throw new Error(result.error || 'Erro desconhecido na análise');
      }

    } catch (err) {
      console.error('Erro ao enviar dados:', err);
      setError(err.message);
      
      const errorMessage = {
        text: `Erro na análise: ${err.message}. Tente novamente.`,
        sender: 'system',
        error: true
      };
      
      setMessages([errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    messages,
    error,
    sendPatientData
  };
}
