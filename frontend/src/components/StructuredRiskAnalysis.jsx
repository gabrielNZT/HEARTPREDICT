import React from 'react';
import { CheckCircleOutlined, ExclamationCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import styles from '../styles/StructuredRiskAnalysis.module.css';

const getRiskIcon = (riskType) => {
  switch (riskType) {
    case 'sucesso':
      return <CheckCircleOutlined className={styles.successIcon} />;
    case 'alerta':
      return <ExclamationCircleOutlined className={styles.warningIcon} />;
    case 'perigo':
      return <CloseCircleOutlined className={styles.dangerIcon} />;
    default:
      return <ExclamationCircleOutlined className={styles.warningIcon} />;
  }
};

const getRiskColor = (riskType) => {
  switch (riskType) {
    case 'sucesso': return '#10b981';
    case 'alerta': return '#f59e0b';
    case 'perigo': return '#ef4444';
    default: return '#6b7280';
  }
};

const StructuredRiskAnalysis = ({ explanation }) => {
  if (!explanation) return null;

  return (
    <div className={styles.analysisContainer}>
      {/* Header com score de risco */}
      <div className={styles.headerCard}>
        <h2 className={styles.patientName}>Análise para {explanation.patientName}</h2>
        <div className={styles.riskScoreSection}>
          <div className={styles.scoreCircle}>
            <span className={styles.scoreNumber}>{explanation.riskScore}</span>
            <span className={styles.scoreLabel}>Score de Risco</span>
          </div>
          <div className={styles.predictionInfo}>
            <div className={styles.riskLevel}>
              Nível: <strong>{explanation.riskLevel}</strong>
            </div>
            <div className={styles.predictionStatus}>
              Predição: <strong>{explanation.predictionStatus}</strong>
            </div>
          </div>
        </div>
        <p className={styles.predictionSummary}>{explanation.predictionSummary}</p>
      </div>

      {/* Fatores contribuintes */}
      <div className={styles.factorsSection}>
        <h3 className={styles.sectionTitle}>Fatores Analisados</h3>
        <div className={styles.factorsGrid}>
          {explanation.contributingFactors.map((factor, index) => (
            <div 
              key={index} 
              className={styles.factorCard}
              style={{ borderColor: getRiskColor(factor.riskType) }}
            >
              <div className={styles.factorHeader}>
                {getRiskIcon(factor.riskType)}
                <h4 className={styles.factorName}>{factor.factorName}</h4>
              </div>
              <div className={styles.factorValue}>{factor.factorValue}</div>
              <p className={styles.factorDetails}>{factor.details}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Recomendações */}
      <div className={styles.recommendationsSection}>
        <h3 className={styles.sectionTitle}>Recomendações Práticas</h3>
        <div className={styles.recommendationsList}>
          {explanation.recommendations.map((rec, index) => (
            <div key={index} className={styles.recommendationCard}>
              <h4 className={styles.recommendationTitle}>
                <span className={styles.recommendationNumber}>{index + 1}</span>
                {rec.title}
              </h4>
              <p className={styles.recommendationDetails}>{rec.details}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Informações do modelo */}
      <div className={styles.modelInfoSection}>
        <div className={styles.modelInfo}>
          <strong>Precisão do modelo: {explanation.modelInfo.accuracy}%</strong>
          <p className={styles.disclaimer}>{explanation.modelInfo.disclaimer}</p>
        </div>
      </div>
    </div>
  );
};

export default StructuredRiskAnalysis;
