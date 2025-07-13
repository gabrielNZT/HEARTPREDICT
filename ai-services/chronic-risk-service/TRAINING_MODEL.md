# Relatório Técnico: Pipeline Avançado de Modelo de Risco Cardíaco

**Versão:** 2.0  
**Data:** 13 de Julho de 2025  
**Autor:** Cientista de Dados Sênior  

---

## 📋 Resumo do Projeto

Este projeto representa uma reestruturação completa do pipeline de desenvolvimento de modelo de risco cardíaco, evoluindo de uma abordagem básica para uma metodologia científica rigorosa e estado-da-arte. O objetivo principal foi maximizar a performance preditiva, garantir robustez estatística e fornecer interpretabilidade clínica através de técnicas avançadas de machine learning.

### Resultados Principais
- **Melhoria substancial na robustez**: Implementação de validação cruzada estratificada (5-fold) substituindo divisão única treino-teste
- **Limpeza científica dos dados**: Remoção de 2-5% de registros inválidos usando critérios médicos rigorosos
- **Engenharia de features clínica**: Criação de 8 novas features baseadas em conhecimento médico
- **Comparação sistemática**: Benchmarking entre 4 algoritmos diferentes (Logistic Regression, Random Forest, XGBoost, LightGBM)
- **Otimização automática**: Busca randomizada de hiperparâmetros com 50 iterações
- **Interpretabilidade avançada**: Implementação de análise SHAP para explicações locais e globais

---

## 🔧 Pipeline de Machine Learning

### Arquitetura Geral
```
Dados Brutos → Limpeza Rigorosa → Engenharia de Features → 
Pipeline de Pré-processamento → Comparação de Modelos → 
Otimização de Hiperparâmetros → Avaliação Final → 
Interpretabilidade SHAP → Salvamento do Modelo
```

### Fases Implementadas

1. **Análise Exploratória e Limpeza Profunda (EDA & Deep Cleaning)**
2. **Engenharia de Features Avançada**
3. **Pipeline de Pré-processamento Robusto**
4. **Treinamento e Validação Cruzada**
5. **Otimização de Hiperparâmetros**
6. **Avaliação Final e Interpretabilidade**

---

## 🧪 Técnicas Utilizadas e Justificativas

### 1. Limpeza de Dados Científica

#### Problema Original
O script anterior não realizava nenhuma validação ou limpeza dos dados, potencialmente incluindo registros clinicamente impossíveis ou implausíveis no treinamento.

#### Solução Implementada
**Filtros de Validação Médica:**
- Remoção de registros onde pressão diastólica > sistólica (impossível fisiologicamente)
- Filtro de pressão arterial dentro de limites plausíveis (70-250 mmHg sistólica, 40-150 mmHg diastólica)

**Tratamento de Outliers com IQR:**
```python
Q1 = df[col].quantile(0.25)
Q3 = df[col].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
```

#### Justificativa
- **IQR vs Percentis Fixos**: O método IQR é mais resistente a valores extremos na distribuição, adaptando-se automaticamente à variabilidade específica de cada feature
- **Clipping vs Remoção**: Optamos por *clipping* (ajuste aos limites) em vez de remoção para preservar o tamanho da amostra, especialmente importante em dados médicos
- **Critérios Médicos**: Os limites de pressão arterial foram baseados em diretrizes clínicas reconhecidas, não em estatísticas arbitrárias

### 2. Engenharia de Features Clínica

#### Problema Original
O modelo anterior utilizava apenas IMC e conversão de idade, perdendo oportunidades de capturar padrões clínicos relevantes.

#### Features Criadas

**Categorizações Médicas:**
- `bmi_category`: Underweight, Normal, Overweight, Obese (baseado em padrões WHO)
- `bp_category`: Normal, Elevated, Stage1_Hypertension, Stage2_Hypertension (American Heart Association)
- `age_category`: Young (<40), Middle_aged (40-55), Senior (>55)

**Features de Interação:**
- `age_cholesterol_interaction`: Captura sinergia entre idade e colesterol
- `bmi_age_interaction`: Relação não-linear entre IMC e idade
- `pressure_pulse`: Pressão de pulso (sistólica - diastólica), indicador cardiovascular

**Features Derivadas:**
- `lifestyle_score`: Score composto de fatores de risco (fumo + álcool - atividade física)

#### Justificativa
- **Base Clínica**: Todas as categorizações seguem diretrizes médicas estabelecidas
- **Captura de Não-linearidades**: As interações permitem ao modelo capturar efeitos sinérgicos entre variáveis
- **Interpretabilidade**: Features categóricas facilitam a interpretação clínica dos resultados

### 3. Pipeline de Pré-processamento Robusto

#### Problema Original
Transformações aplicadas diretamente nos dados sem pipeline, criando risco de *data leakage* e inconsistências.

#### Solução: ColumnTransformer + Pipeline
```python
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(drop='first'), categorical_features)
    ]
)
```

#### Justificativa
- **Prevenção de Data Leakage**: Pipeline garante que transformações sejam aplicadas apenas em dados de treino
- **Reprodutibilidade**: Mesmas transformações aplicadas consistentemente em novos dados
- **Modularidade**: Facilita manutenção e modificações futuras

### 4. Validação Cruzada Estratificada

#### Problema Original
Uso de divisão única `train_test_split`, fornecendo estimativa instável da performance e dependente da "sorte" na amostragem.

#### Solução: Stratified K-Fold Cross-Validation
```python
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_results = cross_validate(model, X, y, cv=cv, scoring=scoring)
```

#### Justificativa
- **Robustez Estatística**: 5 estimativas independentes da performance reduzem variância
- **Estratificação**: Mantém proporção das classes em cada fold, crucial para dados médicos balanceados
- **Confiabilidade**: Média e desvio padrão fornecem intervalos de confiança para as métricas

### 5. Benchmarking Sistemático de Modelos

#### Problema Original
Uso exclusivo do XGBoost sem comparação com outras abordagens.

#### Modelos Comparados
1. **Logistic Regression**: Baseline interpretável
2. **Random Forest**: Ensemble robusto
3. **XGBoost**: Gradient boosting avançado
4. **LightGBM**: Alternativa eficiente ao XGBoost

#### Justificativa
- **Eliminação de Viés**: Evita assumir que XGBoost é sempre a melhor escolha
- **Baseline Sólido**: Logistic Regression fornece referência interpretável
- **Diversidade de Abordagens**: Diferentes algoritmos capturam padrões distintos nos dados

### 6. Otimização de Hiperparâmetros

#### Problema Original
Hiperparâmetros fixos e não otimizados.

#### Solução: RandomizedSearchCV
```python
random_search = RandomizedSearchCV(
    best_model, param_distributions, n_iter=50,
    cv=cv, scoring='roc_auc', n_jobs=-1
)
```

#### Justificativa
- **Eficiência**: RandomizedSearchCV é mais eficiente que GridSearchCV para espaços grandes
- **ROC-AUC como Métrica**: Mais informativa que acurácia para problemas de classificação médica
- **Integração com CV**: Otimização baseada na mesma validação cruzada usada na comparação

### 7. Interpretabilidade com SHAP

#### Problema Original
Uso de `feature_importance_` padrão do XGBoost, que pode ser enganosa e fornece apenas importância global.

#### Solução: SHAP (SHapley Additive exPlanations)
```python
explainer = shap.Explainer(best_model, X_sample)
shap_values = explainer(X_sample)
shap.plots.beeswarm(shap_values)
```

#### Justificativa
- **Fundamentação Teórica**: SHAP baseia-se na teoria dos jogos (valores de Shapley)
- **Explicações Locais**: Explica previsões individuais, não apenas importância global
- **Consistência**: Satisfaz propriedades desejáveis de métodos de explicação
- **Aplicação Médica**: Essencial para confiança e auditabilidade em sistemas de saúde

---

## 📊 Métricas de Avaliação

### Métricas Utilizadas
- **Acurácia**: Proporção geral de classificações corretas
- **Precisão**: Proporção de positivos verdadeiros entre previsões positivas
- **Recall (Sensibilidade)**: Proporção de positivos verdadeiros identificados
- **F1-Score**: Média harmônica entre precisão e recall
- **ROC-AUC**: Área sob a curva ROC, métrica principal para seleção

### Justificativa das Métricas
- **ROC-AUC como Principal**: Invariante ao threshold e menos sensível ao desbalanceamento
- **F1-Score**: Balanceia precisão e recall, importante em aplicações médicas
- **Múltiplas Métricas**: Visão holística da performance do modelo

---

## 🔍 Melhorias Implementadas vs. Versão Original

| Aspecto | Versão Original | Versão Aprimorada |
|---------|----------------|-------------------|
| **Limpeza de Dados** | Nenhuma | Filtros médicos rigorosos + IQR outliers |
| **Features** | 12 básicas | 20+ incluindo interações clínicas |
| **Validação** | Train-test split único | Validação cruzada estratificada 5-fold |
| **Modelos** | Apenas XGBoost | Comparação de 4 algoritmos |
| **Hiperparâmetros** | Fixos | Otimização automática (50 iterações) |
| **Interpretabilidade** | Feature importance básica | Análise SHAP completa |
| **Pipeline** | Transformações manuais | Pipeline robusto e reproduzível |
| **Métricas** | Acurácia simples | 5 métricas com intervalos de confiança |

---

## 🚀 Próximos Passos e Melhorias Futuras

### Melhorias de Curto Prazo
1. **Validação Externa**: Teste em dataset independente para validação externa
2. **Análise de Subgrupos**: Performance por faixas etárias e gêneros
3. **Threshold Optimization**: Otimização do ponto de corte baseado em custos clínicos

### Melhorias de Médio Prazo
1. **Feature Selection**: Implementação de seleção automática de features
2. **Ensemble Methods**: Combinação dos melhores modelos
3. **Monitoramento**: Sistema de detecção de deriva do modelo (model drift)

### Melhorias de Longo Prazo
1. **Deep Learning**: Exploração de redes neurais para padrões complexos
2. **Dados Temporais**: Incorporação de histórico longitudinal dos pacientes
3. **Integração Clínica**: Interface para uso direto por profissionais de saúde

---

## 📈 Impacto Esperado

### Técnico
- **Aumento da Robustez**: Validação cruzada reduz overfitting
- **Melhoria da Performance**: Otimização sistemática maximiza métricas
- **Reprodutibilidade**: Pipeline padronizado facilita manutenção

### Clínico
- **Confiança Médica**: Interpretabilidade SHAP aumenta aceitação clínica
- **Redução de Erros**: Limpeza rigorosa elimina predições baseadas em dados inválidos
- **Personalização**: Explicações individuais permitem decisões personalizadas

### Operacional
- **Escalabilidade**: Pipeline automatizado facilita retreinamento
- **Manutenibilidade**: Código modular reduz custos de manutenção
- **Auditabilidade**: Logs detalhados facilitam auditoria regulatória

---

## 📚 Conclusão

A reestruturação do pipeline de desenvolvimento do modelo de risco cardíaco representa uma evolução significativa em termos de rigor científico, robustez estatística e aplicabilidade clínica. As técnicas implementadas seguem as melhores práticas da indústria e literatura acadêmica, garantindo que o modelo resultante seja não apenas mais preciso, mas também mais confiável e interpretável para uso em ambiente clínico real.

A metodologia desenvolvida pode ser facilmente adaptada para outros problemas de classificação em saúde, servindo como template para futuros projetos de machine learning médico na organização.

---

**Autor:** Cientista de Dados Sênior  
**Contato:** [dados@empresa.com](mailto:dados@empresa.com)  
**Repositório:** `/models/cardiac_risck_model_v2/`
