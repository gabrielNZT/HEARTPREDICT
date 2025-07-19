export function MessageBubble({ message, sender, isError = false, animationDelay = 0 }) {
  const isUser = sender === 'user';
  const isSystem = sender === 'system';
  const isLLM = sender === 'llm';
  
  return (
    <div 
      style={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        marginBottom: 'var(--space-4)'
      }}
    >
      <div
        style={{
          maxWidth: '80%',
          minWidth: '120px',
          padding: 'var(--space-3) var(--space-4)',
          borderRadius: isUser ? 
            'var(--radius-lg) var(--radius-sm) var(--radius-lg) var(--radius-lg)' : 
            'var(--radius-sm) var(--radius-lg) var(--radius-lg) var(--radius-lg)',
          background: isUser ? 
            'var(--gradient-primary)' : 
            isError ? 
              'linear-gradient(135deg, #fee2e2 0%, #fecaca 100%)' :
              isLLM ?
                'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)' :
                'rgba(255, 255, 255, 0.9)',
          color: isUser ? 'white' : 
                 isError ? '#b91c1c' : 
                 isLLM ? '#065f46' : 
                 'var(--neutral-700)',
          fontSize: '1rem',
          fontWeight: isUser ? 500 : 400,
          lineHeight: 1.5,
          boxShadow: isUser ? 
            'var(--shadow-md), 0 0 20px rgba(24, 144, 255, 0.2)' : 
            'var(--shadow-sm)',
          border: isUser ? 
            'none' : 
            isError ? 
              '1px solid #fca5a5' :
              isLLM ?
                '1px solid #a7f3d0' :
                '1px solid rgba(24, 144, 255, 0.1)',
          backdropFilter: 'blur(10px)',
          position: 'relative',
          transition: 'all var(--duration-normal) var(--easing-default)'
        }}
      >
        {/* Indicador de tipo de mensagem */}
        {isSystem && !isError && (
          <div style={{
            position: 'absolute',
            top: '-6px',
            left: '16px',
            background: 'var(--gradient-primary)',
            color: 'white',
            fontSize: '0.75rem',
            fontWeight: 600,
            padding: '2px 8px',
            borderRadius: 'var(--radius-md)',
            textTransform: 'uppercase',
            letterSpacing: '0.05em'
          }}>
            BOT
          </div>
        )}
        
        {isLLM && (
          <div style={{
            position: 'absolute',
            top: '-6px',
            left: '16px',
            background: 'var(--accent-500)',
            color: 'white',
            fontSize: '0.75rem',
            fontWeight: 600,
            padding: '2px 8px',
            borderRadius: 'var(--radius-md)',
            textTransform: 'uppercase',
            letterSpacing: '0.05em'
          }}>
            Análise
          </div>
        )}
        
        {isError && (
          <div style={{
            position: 'absolute',
            top: '-6px',
            left: '16px',
            background: '#ef4444',
            color: 'white',
            fontSize: '0.75rem',
            fontWeight: 600,
            padding: '2px 8px',
            borderRadius: 'var(--radius-md)',
            textTransform: 'uppercase',
            letterSpacing: '0.05em'
          }}>
            ⚠️ Erro
          </div>
        )}

        {/* Conteúdo da mensagem */}
        <div style={{ marginTop: isSystem || isLLM || isError ? 'var(--space-2)' : 0 }}>
          {message}
        </div>

        {/* Efeito de brilho para mensagens do usuário */}
        {isUser && (
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%)',
            borderRadius: 'inherit',
            pointerEvents: 'none',
            animation: 'shimmer 2s ease-in-out infinite'
          }} />
        )}
      </div>
    </div>
  );
}
