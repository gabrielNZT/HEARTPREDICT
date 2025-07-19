import React from 'react';
import styles from '../styles/RiskAnalysisResult.module.css';

function parseAnalysis(text) {
  // Regex para separar blocos e recomendações
  const blocks = text.split(/\n\n|\n- |\n\*/).filter(Boolean);
  const recommendations = [];
  let main = [];
  let foundRec = false;

  blocks.forEach(block => {
    if (block.match(/Recomendo|recomendo|\d+\./)) {
      foundRec = true;
      recommendations.push(block.replace(/\d+\.\s*/, ''));
    } else if (!foundRec) {
      main.push(block);
    }
  });

  return { main, recommendations };
}

const RiskAnalysisResult = ({ explanation }) => {
  if (!explanation) return null;
  const { main, recommendations } = parseAnalysis(explanation);

  return (
    <div className={styles.analysisCard}>
      <h2 className={styles.title}>Resumo da Análise Cardiovascular</h2>
      <div className={styles.mainText}>
        {main.map((block, i) => (
          <p key={i}>{block.trim()}</p>
        ))}
      </div>
      {recommendations.length > 0 && (
        <div className={styles.recommendationsSection}>
          <h3>Recomendações Práticas</h3>
          <ul>
            {recommendations.map((rec, i) => (
              <li key={i}>{rec.trim()}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default RiskAnalysisResult;
