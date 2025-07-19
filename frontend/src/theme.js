// theme.js - Design System HeartPredict
// Tema moderno para healthcare IA
export const theme = {
  token: {
    // Cores principais do design system
    colorPrimary: '#1890ff',
    colorSuccess: '#10b981',
    colorWarning: '#f59e0b',
    colorError: '#ef4444',
    colorInfo: '#3b82f6',
    
    // Tipografia moderna
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    fontSize: 16,
    fontSizeHeading1: 48,
    fontSizeHeading2: 36,
    fontSizeHeading3: 30,
    fontSizeHeading4: 24,
    fontSizeHeading5: 20,
    fontSizeHeading6: 18,
    
    // Border radius moderno
    borderRadius: 12,
    borderRadiusLG: 16,
    borderRadiusSM: 8,
    
    // Spacing consistente
    padding: 16,
    paddingLG: 24,
    paddingSM: 12,
    paddingXS: 8,
    
    // Shadows modernas
    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    boxShadowSecondary: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    
    // Cores neutras modernas
    colorTextBase: '#262626',
    colorTextSecondary: '#737373',
    colorTextTertiary: '#a3a3a3',
    colorTextQuaternary: '#d4d4d4',
    
    // Background moderno
    colorBgBase: '#ffffff',
    colorBgContainer: '#fafafa',
    colorBgElevated: '#ffffff',
    
    // Transições suaves
    motionDurationSlow: '0.5s',
    motionDurationMid: '0.3s',
    motionDurationFast: '0.15s',
    motionEaseInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    motionEaseOut: 'cubic-bezier(0, 0, 0.2, 1)',
    motionEaseIn: 'cubic-bezier(0.4, 0, 1, 1)',
  },
  
  components: {
    // Input moderno
    Input: {
      borderRadius: 12,
      paddingBlock: 12,
      paddingInline: 16,
      fontSize: 18,
      colorBorder: 'rgba(24, 144, 255, 0.2)',
      colorBorderHover: '#1890ff',
      colorBgContainer: 'rgba(255, 255, 255, 0.9)',
      boxShadow: '0 2px 8px rgba(24, 144, 255, 0.1)',
      controlHeight: 48
    },
    
    // Button moderno
    Button: {
      borderRadius: 12,
      paddingBlock: 12,
      paddingInline: 24,
      fontSize: 16,
      fontWeight: 600,
      controlHeight: 48,
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
      primaryShadow: '0 4px 12px rgba(24, 144, 255, 0.3)'
    },
    
    // Select moderno
    Select: {
      borderRadius: 12,
      controlHeight: 48,
      fontSize: 18,
      paddingBlock: 12,
      colorBorder: 'rgba(24, 144, 255, 0.2)',
      colorBorderHover: '#1890ff',
      colorBgContainer: 'rgba(255, 255, 255, 0.9)',
      boxShadow: '0 2px 8px rgba(24, 144, 255, 0.1)',
      optionPadding: '12px 16px'
    },
    
    // Card moderno
    Card: {
      borderRadius: 16,
      paddingLG: 24,
      boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      colorBorderSecondary: 'rgba(255, 255, 255, 0.2)'
    },
    
    // Spin moderno
    Spin: {
      colorPrimary: '#1890ff',
      fontSize: 18
    },
    
    // Form moderno
    Form: {
      itemMarginBottom: 16,
      labelFontSize: 16,
      labelColor: '#404040'
    }
  }
};
