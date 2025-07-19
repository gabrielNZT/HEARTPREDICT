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

      if (result.success) {
        const explanationMessage = {
          text: result.explanation || 'Análise concluída com sucesso!',
          sender: 'llm'
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
