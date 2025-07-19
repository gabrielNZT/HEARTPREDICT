import React from 'react';
import '../styles/animations.css';

const LoadingOverlay = ({ isLoading, message = "Processando análise de risco cardíaco..." }) => {
  if (!isLoading) return null;

  return (
    <div className="loading-overlay">
      <div className="loading-content">
        <div className="medical-loader">❤️</div>
        
        <div className="ai-thinking">
          <div className="dot"></div>
          <div className="dot"></div>
          <div className="dot"></div>
        </div>
        
        <div className="loading-text">
          {message}
          <div className="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingOverlay;
