import { useState } from 'react';
import axios from 'axios';

export function useRiskAssessment() {
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);

  const sendPatientData = async (patientData) => {
    setLoading(true);
    setMessages((prev) => [
      ...prev,
      { text: 'Processando análise de risco...', sender: 'system' },
    ]);
    try {
      await axios.post('/api/risk-assessment', patientData);
      const eventSource = new window.EventSource('/api/risk-assessment/stream');
      eventSource.onmessage = (event) => {
        setMessages((prev) => [
          ...prev,
          { text: event.data, sender: 'system' },
        ]);
        setLoading(false);
        eventSource.close();
      };
      eventSource.onerror = () => {
        setMessages((prev) => [
          ...prev,
          { text: 'Erro ao receber resposta do backend.', sender: 'system' },
        ]);
        setLoading(false);
        eventSource.close();
      };
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { text: 'Erro ao enviar dados.', sender: 'system' },
      ]);
      setLoading(false);
    }
  };

  return { loading, messages, sendPatientData };
}
