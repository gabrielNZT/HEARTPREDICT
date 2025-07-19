
import { useState } from 'react';
import { Spin, Skeleton } from 'antd';
import { ChatWindow } from './components/ChatWindow';
import { ConversationalForm } from './components/ConversationalForm';
import { useRiskAssessment } from './hooks/useRiskAssessment';
import { Header } from './components/Header';
import { questions } from './components/ConversationalForm';
import WelcomeScreen from './components/WelcomeScreen';
import './styles/animations.css';

export default function App() {
  const [chatMessages, setChatMessages] = useState([
    { text: questions[0].label, sender: 'system' },
  ]);
  const [formFinished, setFormFinished] = useState(false);
  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const { loading, messages, sendPatientData } = useRiskAssessment();
  const [started, setStarted] = useState(false);

  const handleFormStep = (value, errorMsg) => {
    if (errorMsg) {
      setChatMessages((prev) => [
        ...prev,
        { text: errorMsg, sender: 'system', error: true },
      ]);
      return;
    }
    setChatMessages((prev) => [
      ...prev,
      { text: value, sender: 'user' },
    ]);
    const updatedAnswers = { ...answers, [questions[step].key]: value };
    setAnswers(updatedAnswers);
    if (step < questions.length - 1) {
      setStep(step + 1);
      setTimeout(() => {
        setChatMessages((prev) => [
          ...prev,
          { text: questions[step + 1].label, sender: 'system' },
        ]);
      }, 400);
    } else {
      setFormFinished(true);
      setChatMessages((prev) => [
        ...prev,
        { text: 'Dados enviados. Aguarde a análise...', sender: 'system' },
      ]);
      sendPatientData(updatedAnswers);
    }
  };

  // Atualiza chat com mensagens do backend
  if (messages.length > 0 && formFinished && !chatMessages.some(m => m.sender === 'llm')) {
    setChatMessages((prev) => [...prev, ...messages.map(msg => ({ ...msg, sender: 'llm' }))]);
  }

  if (!started) {
    return <WelcomeScreen onStart={() => setStarted(true)} />;
  }

  return (
    <div
      className="animate-fade-in"
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #e6f4ff 0%, #f0f9ff 50%, #ecfdf5 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Elementos decorativos de fundo */}
      <div style={{
        position: 'absolute',
        top: '20%',
        left: '5%',
        width: '200px',
        height: '200px',
        background: 'radial-gradient(circle, rgba(24, 144, 255, 0.1) 0%, transparent 70%)',
        borderRadius: '50%',
        filter: 'blur(60px)',
        animation: 'float 8s ease-in-out infinite'
      }} />
      <div style={{
        position: 'absolute',
        bottom: '20%',
        right: '5%',
        width: '250px',
        height: '250px',
        background: 'radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 70%)',
        borderRadius: '50%',
        filter: 'blur(80px)',
        animation: 'float 10s ease-in-out infinite reverse'
      }} />

      <div
        className="modern-card animate-scale-in"
        style={{
          width: '100%',
          height: '100vh',
          background: 'var(--gradient-card)',
          boxShadow: 'var(--shadow-xl), var(--shadow-glass)',
          padding: 'var(--space-12)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
          backdropFilter: 'blur(20px)',
          position: 'relative',
          zIndex: 1,
          borderRadius: 0,
        }}
      >
        <Header />
        <ChatWindow messages={chatMessages}>
          {!formFinished && (
            <ConversationalForm
              step={step}
              onStep={handleFormStep}
            />
          )}
        </ChatWindow>
        {loading && (
          <div className="animate-pulse" style={{ 
            marginTop: 'var(--space-8)', 
            textAlign: 'center',
            padding: 'var(--space-6)',
            background: 'rgba(24, 144, 255, 0.05)',
            borderRadius: 'var(--radius-lg)',
            border: '1px solid rgba(24, 144, 255, 0.1)'
          }}>
            <div className="modern-spinner" style={{ margin: '0 auto var(--space-4) auto' }} />
            <div style={{ 
              fontSize: '1.125rem',
              fontWeight: 600,
              color: 'var(--primary-600)',
              marginBottom: 'var(--space-2)'
            }}>
              Analisando com IA...
            </div>
            <Skeleton 
              active 
              paragraph={{ rows: 2 }} 
              style={{ marginTop: 'var(--space-4)' }} 
            />
          </div>
        )}
      </div>

      {/* Media queries para responsividade */}
      <style jsx>{`
        @media (max-width: 768px) {
          div[style*='maxWidth: 700'] {
            max-width: 100vw !important;
            min-width: 320px !important;
            border-radius: var(--radius-xl) !important;
            padding: var(--space-6) !important;
            margin: var(--space-4) !important;
          }
        }
      `}</style>
    </div>
  );
}
