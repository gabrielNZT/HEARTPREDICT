import { HeartPredictWordmark } from './Logo';

export function Header() {
  return (
    <header style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      textAlign: 'center',
      marginBottom: 'var(--space-8)',
      padding: 'var(--space-6) 0',
      borderBottom: '1px solid rgba(255, 255, 255, 0.2)',
      position: 'relative'
    }}>
      {/* Efeito de brilho sutil */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: '50%',
        transform: 'translateX(-50%)',
        width: '100px',
        height: '2px',
        background: 'var(--gradient-primary)',
        borderRadius: '2px',
        opacity: 0.6
      }} />
      
      <div className="animate-slide-in-left" style={{ marginBottom: 'var(--space-3)' }}>
        <HeartPredictWordmark size="md" animated={true} />
      </div>
      
      <div className="animate-slide-in-right" style={{
        fontSize: '1rem',
        fontWeight: 500,
        color: 'var(--neutral-600)',
        letterSpacing: '0.05em',
        textTransform: 'uppercase'
      }}>
        Avaliação Inteligente de Risco Cardíaco
      </div>
      
      {/* Indicador de progresso sutil */}
      <div style={{
        marginTop: 'var(--space-4)',
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--space-2)',
        fontSize: '0.875rem',
        color: 'var(--neutral-500)'
      }}>
        <span style={{ fontSize: '1rem' }}>🔬</span>
        <span>Powered by Advanced ML</span>
      </div>
    </header>
  );
}
