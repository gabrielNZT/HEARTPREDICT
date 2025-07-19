
import React from 'react';
import { HeartPredictWordmark } from './Logo';

export default function WelcomeScreen({ onStart }) {
  return (
    <div className="animate-fade-in" style={{
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      justifyContent: 'center', 
      minHeight: '100vh',
      padding: 'var(--space-12)',
      background: 'linear-gradient(135deg, #e6f4ff 0%, #f0f9ff 50%, #ecfdf5 100%)',
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Elementos decorativos de fundo */}
      <div style={{
        position: 'absolute',
        top: '10%',
        left: '10%',
        width: '100px',
        height: '100px',
        background: 'linear-gradient(135deg, rgba(24, 144, 255, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%)',
        borderRadius: '50%',
        filter: 'blur(40px)',
        animation: 'float 6s ease-in-out infinite'
      }} />
      <div style={{
        position: 'absolute',
        top: '60%',
        right: '15%',
        width: '150px',
        height: '150px',
        background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%)',
        borderRadius: '50%',
        filter: 'blur(50px)',
        animation: 'float 8s ease-in-out infinite reverse'
      }} />
      
      {/* Card principal */}
      <div className="modern-card" style={{
        maxWidth: '520px',
        width: '100%',
        padding: 'var(--space-12)',
        textAlign: 'center',
        position: 'relative',
        zIndex: 1
      }}>
        {/* Logo com animação */}
        <div style={{ marginBottom: 'var(--space-8)' }} className="animate-bounce-in">
          <HeartPredictWordmark size="xl" animated={true} />
        </div>

        {/* Título principal */}
        <h1 className="animate-slide-in-left" style={{
          fontSize: '3rem',
          fontWeight: 800,
          background: 'var(--gradient-primary)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          marginBottom: 'var(--space-4)',
          letterSpacing: '-0.02em',
          lineHeight: 1.1
        }}>
          Tecnologia IA de Ponta
        </h1>

        {/* Subtítulo */}
        <h2 className="animate-slide-in-right" style={{
          fontSize: '1.5rem',
          fontWeight: 500,
          color: 'var(--neutral-600)',
          marginBottom: 'var(--space-6)',
          letterSpacing: '0.01em'
        }}>
          para sua Saúde Cardiovascular
        </h2>

        {/* Descrição */}
        <p className="animate-fade-in" style={{
          fontSize: '1.125rem',
          color: 'var(--neutral-700)',
          lineHeight: 1.6,
          marginBottom: 'var(--space-8)',
          maxWidth: '420px',
          margin: '0 auto var(--space-8) auto'
        }}>
          Descubra seu risco cardíaco em minutos usando{' '}
          <span style={{ 
            fontWeight: 600, 
            background: 'var(--gradient-primary)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            machine learning avançado
          </span>
          . Responda perguntas simples e receba uma análise personalizada, segura e instantânea.
        </p>

        {/* Features */}
        <div className="animate-slide-in-left" style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
          gap: 'var(--space-4)',
          marginBottom: 'var(--space-8)'
        }}>
          <div style={{ textAlign: 'center', padding: 'var(--space-3)' }}>
            <div style={{ fontSize: '2rem', marginBottom: 'var(--space-2)' }}>🧠</div>
            <div style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--neutral-700)' }}>
              IA Avançada
            </div>
          </div>
          <div style={{ textAlign: 'center', padding: 'var(--space-3)' }}>
            <div style={{ fontSize: '2rem', marginBottom: 'var(--space-2)' }}>⚡</div>
            <div style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--neutral-700)' }}>
              Resultado Instantâneo
            </div>
          </div>
          <div style={{ textAlign: 'center', padding: 'var(--space-3)' }}>
            <div style={{ fontSize: '2rem', marginBottom: 'var(--space-2)' }}>🔒</div>
            <div style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--neutral-700)' }}>
              100% Seguro
            </div>
          </div>
        </div>

        {/* Botão principal */}
        <button
          onClick={onStart}
          className="modern-button animate-glow"
          style={{
            fontSize: '1.25rem',
            padding: 'var(--space-4) var(--space-10)',
            marginBottom: 'var(--space-6)',
            position: 'relative',
            overflow: 'hidden'
          }}
        >
          <span style={{ position: 'relative', zIndex: 1 }}>
            Iniciar Avaliação IA 🚀
          </span>
        </button>

        {/* Disclaimer de privacidade */}
        <div className="animate-fade-in" style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 'var(--space-2)',
          color: 'var(--neutral-500)',
          fontSize: '0.875rem',
          fontWeight: 500
        }}>
          <span style={{ fontSize: '1.125rem' }}>�️</span>
          Seus dados são criptografados e usados apenas para esta avaliação
        </div>
      </div>
    </div>
  );
}
