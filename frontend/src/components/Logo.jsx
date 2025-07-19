import React from 'react';

export const HeartPredictLogo = ({ size = 48, animated = true }) => {
  return (
    <div style={{ display: 'inline-flex', alignItems: 'center', gap: 12 }}>
      <svg 
        width={size} 
        height={size} 
        viewBox="0 0 64 64" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
        style={{ 
          filter: 'drop-shadow(0 4px 8px rgba(24, 144, 255, 0.3))',
          animation: animated ? 'heartBeat 2s ease-in-out infinite' : 'none'
        }}
      >
        <defs>
          <linearGradient id="heartGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#1890ff" />
            <stop offset="50%" stopColor="#3b82f6" />
            <stop offset="100%" stopColor="#10b981" />
          </linearGradient>
          <linearGradient id="aiGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#60a5fa" />
            <stop offset="100%" stopColor="#34d399" />
          </linearGradient>
        </defs>
        
        {/* Coração principal */}
        <path
          d="M32 54C32 54 12 40 12 24C12 18 16.5 14 22 14C26 14 30 16 32 20C34 16 38 14 42 14C47.5 14 52 18 52 24C52 40 32 54 32 54Z"
          fill="url(#heartGradient)"
          style={{
            animation: animated ? 'pulse 2s ease-in-out infinite' : 'none'
          }}
        />
        
        {/* Elementos AI/Tech - circuitos neurais */}
        <g opacity="0.9" style={{ animation: animated ? 'rotate 8s linear infinite' : 'none' }}>
          <circle cx="32" cy="28" r="2" fill="url(#aiGradient)" />
          <circle cx="24" cy="24" r="1.5" fill="url(#aiGradient)" />
          <circle cx="40" cy="24" r="1.5" fill="url(#aiGradient)" />
          <circle cx="28" cy="32" r="1" fill="url(#aiGradient)" />
          <circle cx="36" cy="32" r="1" fill="url(#aiGradient)" />
          
          {/* Conexões neurais */}
          <line x1="32" y1="28" x2="24" y2="24" stroke="url(#aiGradient)" strokeWidth="1" opacity="0.6" />
          <line x1="32" y1="28" x2="40" y2="24" stroke="url(#aiGradient)" strokeWidth="1" opacity="0.6" />
          <line x1="32" y1="28" x2="28" y2="32" stroke="url(#aiGradient)" strokeWidth="1" opacity="0.6" />
          <line x1="32" y1="28" x2="36" y2="32" stroke="url(#aiGradient)" strokeWidth="1" opacity="0.6" />
        </g>
        
        {/* Partículas de dados */}
        <g style={{ animation: animated ? 'float 3s ease-in-out infinite' : 'none' }}>
          <circle cx="18" cy="18" r="1" fill="#60a5fa" opacity="0.7" />
          <circle cx="46" cy="18" r="1" fill="#34d399" opacity="0.7" />
          <circle cx="20" cy="40" r="1" fill="#3b82f6" opacity="0.7" />
          <circle cx="44" cy="40" r="1" fill="#10b981" opacity="0.7" />
        </g>
      </svg>
      
      <style jsx>{`
        @keyframes heartBeat {
          0%, 100% { transform: scale(1); }
          50% { transform: scale(1.05); }
        }
        
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.8; }
        }
        
        @keyframes rotate {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        
        @keyframes float {
          0%, 100% { transform: translateY(0px); opacity: 0.7; }
          50% { transform: translateY(-2px); opacity: 1; }
        }
      `}</style>
    </div>
  );
};

export const HeartPredictWordmark = ({ size = 'lg', animated = true }) => {
  const sizes = {
    sm: { logo: 32, font: 20, weight: 600 },
    md: { logo: 40, font: 24, weight: 700 },
    lg: { logo: 48, font: 28, weight: 700 },
    xl: { logo: 56, font: 32, weight: 800 }
  };
  
  const currentSize = sizes[size];
  
  return (
    <div style={{ 
      display: 'flex', 
      alignItems: 'center', 
      gap: 12,
      fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    }}>
      <HeartPredictLogo size={currentSize.logo} animated={animated} />
      <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <span style={{
          fontSize: currentSize.font,
          fontWeight: currentSize.weight,
          background: 'linear-gradient(135deg, #1890ff 0%, #3b82f6 50%, #10b981 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          letterSpacing: '-0.02em'
        }}>
          HeartPredict
        </span>
        {size === 'lg' || size === 'xl' ? (
          <span style={{
            fontSize: currentSize.font * 0.5,
            fontWeight: 500,
            color: '#64748b',
            letterSpacing: '0.05em',
            textTransform: 'uppercase'
          }}>
            AI Health Technology
          </span>
        ) : null}
      </div>
    </div>
  );
};
