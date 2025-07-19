// HeartPredict Design System - Advanced Healthcare UI

export const designTokens = {
  // Paleta de cores moderna para health tech
  colors: {
    primary: {
      50: '#e6f4ff',
      100: '#bae7ff', 
      200: '#91d5ff',
      300: '#69c0ff',
      400: '#40a9ff',
      500: '#1890ff', // Primary
      600: '#0066cc',
      700: '#0052cc',
      800: '#003eb3',
      900: '#002766'
    },
    secondary: {
      50: '#f0f9ff',
      100: '#dbeafe',
      200: '#bfdbfe',
      300: '#93c5fd',
      400: '#60a5fa',
      500: '#3b82f6',
      600: '#2563eb',
      700: '#1d4ed8',
      800: '#1e40af',
      900: '#1e3a8a'
    },
    accent: {
      50: '#ecfdf5',
      100: '#d1fae5',
      200: '#a7f3d0',
      300: '#6ee7b7',
      400: '#34d399',
      500: '#10b981',
      600: '#059669',
      700: '#047857',
      800: '#065f46',
      900: '#064e3b'
    },
    neutral: {
      50: '#fafafa',
      100: '#f5f5f5',
      200: '#e5e5e5',
      300: '#d4d4d4',
      400: '#a3a3a3',
      500: '#737373',
      600: '#525252',
      700: '#404040',
      800: '#262626',
      900: '#171717'
    },
    semantic: {
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6'
    }
  },

  // Gradientes modernos
  gradients: {
    primary: 'linear-gradient(135deg, #1890ff 0%, #3b82f6 50%, #10b981 100%)',
    secondary: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    accent: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    glass: 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
    card: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
    hero: 'linear-gradient(135deg, #e6f4ff 0%, #f0f9ff 50%, #ecfdf5 100%)'
  },

  // Tipografia moderna
  typography: {
    fontFamily: {
      primary: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      mono: '"JetBrains Mono", "Fira Code", Consolas, monospace'
    },
    fontSize: {
      xs: '12px',
      sm: '14px',
      base: '16px',
      lg: '18px',
      xl: '20px',
      '2xl': '24px',
      '3xl': '30px',
      '4xl': '36px',
      '5xl': '48px',
      '6xl': '60px'
    },
    fontWeight: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800
    },
    lineHeight: {
      tight: 1.25,
      snug: 1.375,
      normal: 1.5,
      relaxed: 1.625,
      loose: 2
    }
  },

  // Spacing sistema 8pt
  spacing: {
    px: '1px',
    0: '0',
    1: '4px',
    2: '8px',
    3: '12px',
    4: '16px',
    5: '20px',
    6: '24px',
    8: '32px',
    10: '40px',
    12: '48px',
    16: '64px',
    20: '80px',
    24: '96px',
    32: '128px'
  },

  // Bordas e raios
  borderRadius: {
    none: '0',
    sm: '4px',
    base: '8px',
    md: '12px',
    lg: '16px',
    xl: '20px',
    '2xl': '24px',
    '3xl': '32px',
    full: '9999px'
  },

  // Shadows modernas
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
    glass: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
    glow: '0 0 20px rgba(24, 144, 255, 0.3)'
  },

  // Animações e transições
  animations: {
    duration: {
      fast: '150ms',
      normal: '300ms',
      slow: '500ms',
      slower: '750ms'
    },
    easing: {
      default: 'cubic-bezier(0.4, 0, 0.2, 1)',
      in: 'cubic-bezier(0.4, 0, 1, 1)',
      out: 'cubic-bezier(0, 0, 0.2, 1)',
      inOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      spring: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
    }
  },

  // Breakpoints responsivos
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px'
  }
};

// Componentes base estilizados
export const components = {
  // Card com glassmorphism
  Card: {
    background: designTokens.gradients.card,
    borderRadius: designTokens.borderRadius.xl,
    border: '1px solid rgba(255, 255, 255, 0.2)',
    backdropFilter: 'blur(20px)',
    boxShadow: designTokens.shadows.xl,
    transition: `all ${designTokens.animations.duration.normal} ${designTokens.animations.easing.default}`
  },

  // Button moderno
  Button: {
    primary: {
      background: designTokens.gradients.primary,
      color: 'white',
      border: 'none',
      borderRadius: designTokens.borderRadius.lg,
      padding: `${designTokens.spacing[3]} ${designTokens.spacing[6]}`,
      fontSize: designTokens.typography.fontSize.lg,
      fontWeight: designTokens.typography.fontWeight.semibold,
      cursor: 'pointer',
      transition: `all ${designTokens.animations.duration.normal} ${designTokens.animations.easing.spring}`,
      boxShadow: designTokens.shadows.md,
      ':hover': {
        transform: 'translateY(-2px)',
        boxShadow: designTokens.shadows.xl
      }
    }
  },

  // Input moderno
  Input: {
    background: 'rgba(255, 255, 255, 0.8)',
    border: `1px solid ${designTokens.colors.neutral[200]}`,
    borderRadius: designTokens.borderRadius.md,
    padding: `${designTokens.spacing[3]} ${designTokens.spacing[4]}`,
    fontSize: designTokens.typography.fontSize.lg,
    backdropFilter: 'blur(10px)',
    transition: `all ${designTokens.animations.duration.normal} ${designTokens.animations.easing.default}`,
    ':focus': {
      outline: 'none',
      borderColor: designTokens.colors.primary[500],
      boxShadow: `0 0 0 3px ${designTokens.colors.primary[500]}20`
    }
  }
};
