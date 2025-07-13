"""
Pipeline Avançado de Treinamento para Modelo de Risco Cardíaco
Versão 2.0 - Implementação de metodologia científica rigorosa

Autor: Cientista de Dados Sênior
Data: 2025-07-13
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from typing import Dict, List, Tuple, Any
import joblib
import os
from datetime import datetime

# Machine Learning
from sklearn.model_selection import (
    StratifiedKFold, cross_validate, RandomizedSearchCV,
    train_test_split
)
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, precision_recall_curve
)
import xgboost as xgb
import lightgbm as lgb

# Interpretabilidade
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    print("⚠️  SHAP não disponível. Instale com: pip install shap")

# Configurações
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8')
np.random.seed(42)

class CardiacRiskModelPipeline:
    """
    Pipeline completo para desenvolvimento de modelo de risco cardíaco
    """
    
    def __init__(self, data_path: str = "data/cardio_train.csv"):
        self.data_path = data_path
        self.df_raw = None
        self.df_clean = None
        self.X_processed = None
        self.y = None
        self.preprocessing_pipeline = None
        self.best_model = None
        self.best_model_name = None
        self.cv_results = {}
        self.final_metrics = {}

        self.threshold = 0.4
        
        # Configurações de validação
        self.cv_folds = 5
        self.test_size = 0.2
        self.random_state = 42
        
        print("🔬 Pipeline de Desenvolvimento de Modelo de Risco Cardíaco")
        print("=" * 60)
    
    def load_and_explore_data(self) -> pd.DataFrame:
        """
        Fase 1: Carregamento e Análise Exploratória dos Dados
        """
        print("\n📊 FASE 1: ANÁLISE EXPLORATÓRIA DOS DADOS")
        print("-" * 50)
        
        # Carregar dados
        print("Carregando dataset...")
        self.df_raw = pd.read_csv(self.data_path, sep=';')
        
        print(f"✓ Dataset carregado: {self.df_raw.shape}")
        print(f"  Colunas: {list(self.df_raw.columns)}")
        print(f"  Memória utilizada: {self.df_raw.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Análise básica
        print("\n📈 Estatísticas Descritivas:")
        print(self.df_raw.describe())
        
        # Verificar valores faltantes
        missing_values = self.df_raw.isnull().sum()
        if missing_values.sum() > 0:
            print(f"\n⚠️  Valores faltantes encontrados:")
            print(missing_values[missing_values > 0])
        else:
            print("\n✓ Nenhum valor faltante encontrado")
        
        # Análise da variável target
        print(f"\n🎯 Distribuição da Variável Target (cardio):")
        target_dist = self.df_raw['cardio'].value_counts(normalize=True)
        print(f"  Classe 0 (Sem doença): {target_dist[0]:.3f}")
        print(f"  Classe 1 (Com doença): {target_dist[1]:.3f}")
        
        return self.df_raw
    
    def clean_and_validate_data(self) -> pd.DataFrame:
        """
        Fase 1.5: Limpeza Profunda e Validação dos Dados
        """
        print("\n🧹 LIMPEZA E VALIDAÇÃO DOS DADOS")
        print("-" * 40)
        
        df = self.df_raw.copy()
        initial_rows = len(df)
        
        # 1. Remover coluna ID
        df = df.drop('id', axis=1)
        print("✓ Coluna 'id' removida")
        
        # 2. Converter idade de dias para anos
        df['age'] = (df['age'] / 365.25).astype(int)
        print("✓ Idade convertida para anos")
        
        # 3. Calcular BMI
        df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
        print("✓ BMI calculado")
        
        # 4. Limpeza específica - Pressão arterial inválida
        invalid_bp = df['ap_hi'] <= df['ap_lo']
        print(f"📋 Registros com pressão arterial inválida: {invalid_bp.sum()}")
        df = df[~invalid_bp]
        
        # 5. Limpeza - Valores de pressão implausíveis
        # Pressão sistólica: 70-250 mmHg, diastólica: 40-150 mmHg
        valid_pressure = (
            (df['ap_hi'] >= 70) & (df['ap_hi'] <= 250) &
            (df['ap_lo'] >= 40) & (df['ap_lo'] <= 150)
        )
        invalid_pressure = ~valid_pressure
        print(f"📋 Registros com pressão implausível: {invalid_pressure.sum()}")
        df = df[valid_pressure]
        
        # 6. Tratamento de outliers usando IQR
        numeric_columns = ['height', 'weight', 'bmi']
        outliers_removed = 0
        
        for col in numeric_columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
            outliers_count = outliers.sum()
            outliers_removed += outliers_count
            
            print(f"📊 {col}: {outliers_count} outliers detectados (IQR: {lower_bound:.1f} - {upper_bound:.1f})")
            
            # Aplicar clipping em vez de remoção para preservar dados
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        
        final_rows = len(df)
        removed_rows = initial_rows - final_rows
        
        print(f"\n📊 Resumo da Limpeza:")
        print(f"  Registros iniciais: {initial_rows:,}")
        print(f"  Registros removidos: {removed_rows:,} ({removed_rows/initial_rows*100:.2f}%)")
        print(f"  Registros finais: {final_rows:,}")
        print(f"  Outliers tratados: {outliers_removed} (clipping aplicado)")
        
        self.df_clean = df
        return df
    
    def engineer_features(self) -> pd.DataFrame:
        """
        Fase 2: Engenharia de Features Avançada
        """
        print("\n🔧 FASE 2: ENGENHARIA DE FEATURES")
        print("-" * 40)
        
        df = self.df_clean.copy()
        
        # 1. Categorias de BMI baseadas em padrões médicos
        def categorize_bmi(bmi):
            if bmi < 18.5:
                return 'Underweight'
            elif bmi < 25:
                return 'Normal'
            elif bmi < 30:
                return 'Overweight'
            else:
                return 'Obese'
        
        df['bmi_category'] = df['bmi'].apply(categorize_bmi)
        print("✓ Categorias de BMI criadas")
        
        # 2. Categorias de Pressão Arterial (American Heart Association)
        def categorize_blood_pressure(systolic, diastolic):
            if systolic < 120 and diastolic < 80:
                return 'Normal'
            elif systolic < 130 and diastolic < 80:
                return 'Elevated'
            elif (systolic >= 130 and systolic < 140) or (diastolic >= 80 and diastolic < 90):
                return 'Stage1_Hypertension'
            elif systolic >= 140 or diastolic >= 90:
                return 'Stage2_Hypertension'
            else:
                return 'Hypertensive_Crisis'
        
        df['bp_category'] = df.apply(lambda x: categorize_blood_pressure(x['ap_hi'], x['ap_lo']), axis=1)
        print("✓ Categorias de pressão arterial criadas")
        
        # 3. Features de interação clinicamente relevantes
        df['age_cholesterol_interaction'] = df['age'] * df['cholesterol']
        df['bmi_age_interaction'] = df['bmi'] * df['age']
        df['pressure_pulse'] = df['ap_hi'] - df['ap_lo']  # Pressão de pulso
        print("✓ Features de interação criadas")
        
        # 4. Lifestyle score (combinação de fatores de estilo de vida)
        df['lifestyle_score'] = df['smoke'] + df['alco'] - df['active']
        print("✓ Score de estilo de vida criado")
        
        # 5. Categorização de idade
        def categorize_age(age):
            if age < 40:
                return 'Young'
            elif age < 55:
                return 'Middle_aged'
            else:
                return 'Senior'
        
        df['age_category'] = df['age'].apply(categorize_age)
        print("✓ Categorias de idade criadas")
        
        print(f"\n📊 Features finais: {df.shape[1]} colunas")
        print(f"  Features categóricas criadas: bmi_category, bp_category, age_category")
        print(f"  Features de interação: age_cholesterol_interaction, bmi_age_interaction, pressure_pulse")
        print(f"  Features derivadas: lifestyle_score")
        
        return df
    
    def create_preprocessing_pipeline(self, df: pd.DataFrame) -> Pipeline:
        """
        Fase 3: Criação do Pipeline de Pré-processamento
        """
        print("\n⚙️ FASE 3: PIPELINE DE PRÉ-PROCESSAMENTO")
        print("-" * 40)
        
        # Separar features numéricas e categóricas
        numeric_features = [
            'age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo',
            'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'bmi',
            'age_cholesterol_interaction', 'bmi_age_interaction', 
            'pressure_pulse', 'lifestyle_score'
        ]
        
        categorical_features = ['bmi_category', 'bp_category', 'age_category']
        
        print(f"✓ Features numéricas ({len(numeric_features)}): {numeric_features}")
        print(f"✓ Features categóricas ({len(categorical_features)}): {categorical_features}")
        
        # Criar transformadores
        numeric_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(drop='first', sparse_output=False)
        
        # Criar pipeline de pré-processamento
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)
            ]
        )
        
        self.preprocessing_pipeline = preprocessor
        print("✓ Pipeline de pré-processamento criado")
        
        return preprocessor
    
    def prepare_data_for_modeling(self, df: pd.DataFrame) -> Tuple[Any, np.ndarray]:
        """
        Preparação final dos dados para modelagem
        """
        # Separar features e target
        X = df.drop('cardio', axis=1)
        y = df['cardio'].values
        
        print(f"✓ Dados preparados: X={X.shape}, y={y.shape}")
        print(f"  Distribuição target: {np.bincount(y) / len(y)}")
        
        self.y = y
        return X, y
    
    def train_and_compare_models(self, X: pd.DataFrame, y: np.ndarray) -> Dict:
        """
        Fase 4: Treinamento e Comparação de Modelos com Validação Cruzada
        """
        print("\n🤖 FASE 4: TREINAMENTO E COMPARAÇÃO DE MODELOS")
        print("-" * 50)
        
        # Definir modelos para comparação
        models = {
            'Logistic_Regression': Pipeline([
                ('preprocessor', self.preprocessing_pipeline),
                ('classifier', LogisticRegression(random_state=self.random_state, max_iter=1000))
            ]),
            'Random_Forest': Pipeline([
                ('preprocessor', self.preprocessing_pipeline),
                ('classifier', RandomForestClassifier(random_state=self.random_state, n_estimators=100))
            ]),
            'XGBoost': Pipeline([
                ('preprocessor', self.preprocessing_pipeline),
                ('classifier', xgb.XGBClassifier(random_state=self.random_state, eval_metric='logloss'))
            ]),
            'LightGBM': Pipeline([
                ('preprocessor', self.preprocessing_pipeline),
                ('classifier', lgb.LGBMClassifier(random_state=self.random_state, verbose=-1))
            ])
        }
        
        # Configurar validação cruzada estratificada
        cv = StratifiedKFold(n_splits=self.cv_folds, shuffle=True, random_state=self.random_state)
        
        # Métricas a serem avaliadas
        scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
        
        results = {}
        
        print(f"🔄 Executando validação cruzada ({self.cv_folds}-fold) para {len(models)} modelos...")
        
        for name, model in models.items():
            print(f"\n📈 Treinando {name}...")
            
            cv_results = cross_validate(
                model, X, y, cv=cv, scoring=scoring,
                return_train_score=True, n_jobs=-1
            )
            
            # Calcular estatísticas
            results[name] = {
                'accuracy_mean': cv_results['test_accuracy'].mean(),
                'accuracy_std': cv_results['test_accuracy'].std(),
                'precision_mean': cv_results['test_precision'].mean(),
                'precision_std': cv_results['test_precision'].std(),
                'recall_mean': cv_results['test_recall'].mean(),
                'recall_std': cv_results['test_recall'].std(),
                'f1_mean': cv_results['test_f1'].mean(),
                'f1_std': cv_results['test_f1'].std(),
                'roc_auc_mean': cv_results['test_roc_auc'].mean(),
                'roc_auc_std': cv_results['test_roc_auc'].std(),
                'cv_results': cv_results
            }
            
            print(f"  Acurácia: {results[name]['accuracy_mean']:.4f} ± {results[name]['accuracy_std']:.4f}")
            print(f"  F1-Score: {results[name]['f1_mean']:.4f} ± {results[name]['f1_std']:.4f}")
            print(f"  ROC-AUC: {results[name]['roc_auc_mean']:.4f} ± {results[name]['roc_auc_std']:.4f}")
        
        # Encontrar melhor modelo baseado em ROC-AUC
        best_model_name = max(results.keys(), key=lambda x: results[x]['roc_auc_mean'])
        best_model = models[best_model_name]
        
        print(f"\n🏆 Melhor modelo: {best_model_name}")
        print(f"  ROC-AUC: {results[best_model_name]['roc_auc_mean']:.4f} ± {results[best_model_name]['roc_auc_std']:.4f}")
        
        self.cv_results = results
        self.best_model = best_model
        self.best_model_name = best_model_name
        
        return results
    
    def optimize_hyperparameters(self, X: pd.DataFrame, y: np.ndarray) -> Pipeline:
        """
        Fase 5: Otimização de Hiperparâmetros
        """
        print("\n🎯 FASE 5: OTIMIZAÇÃO DE HIPERPARÂMETROS")
        print("-" * 45)
        
        print(f"Otimizando hiperparâmetros para: {self.best_model_name}")
        
        # Definir espaço de busca baseado no melhor modelo
        if self.best_model_name == 'XGBoost':
            param_distributions = {
                'classifier__n_estimators': [100, 200, 300],
                'classifier__max_depth': [3, 4, 5, 6, 7],
                'classifier__learning_rate': [0.01, 0.1, 0.2],
                'classifier__subsample': [0.8, 0.9, 1.0],
                'classifier__colsample_bytree': [0.8, 0.9, 1.0]
            }
        elif self.best_model_name == 'LightGBM':
            param_distributions = {
                'classifier__n_estimators': [100, 200, 300],
                'classifier__max_depth': [3, 4, 5, 6, 7],
                'classifier__learning_rate': [0.01, 0.1, 0.2],
                'classifier__subsample': [0.8, 0.9, 1.0],
                'classifier__colsample_bytree': [0.8, 0.9, 1.0]
            }
        elif self.best_model_name == 'Random_Forest':
            param_distributions = {
                'classifier__n_estimators': [100, 200, 300],
                'classifier__max_depth': [10, 20, None],
                'classifier__min_samples_split': [2, 5, 10],
                'classifier__min_samples_leaf': [1, 2, 4]
            }
        else:  # Logistic Regression
            param_distributions = {
                'classifier__C': [0.1, 1.0, 10.0, 100.0],
                'classifier__penalty': ['l1', 'l2'],
                'classifier__solver': ['liblinear', 'saga']
            }
        
        # Configurar busca randomizada
        cv = StratifiedKFold(n_splits=self.cv_folds, shuffle=True, random_state=self.random_state)
        
        random_search = RandomizedSearchCV(
            self.best_model,
            param_distributions=param_distributions,
            n_iter=50,  # Número de combinações a testar
            cv=cv,
            scoring='roc_auc',
            n_jobs=-1,
            random_state=self.random_state,
            verbose=1
        )
        
        print("🔍 Executando busca randomizada...")
        random_search.fit(X, y)
        
        optimized_model = random_search.best_estimator_
        
        print(f"✓ Otimização concluída!")
        print(f"  Melhor ROC-AUC: {random_search.best_score_:.4f}")
        print(f"  Melhores parâmetros: {random_search.best_params_}")
        
        self.best_model = optimized_model
        return optimized_model
    
    def final_evaluation(self, X: pd.DataFrame, y: np.ndarray) -> Dict:
        """
        Fase 6: Avaliação Final Detalhada
        """
        print("\n📊 FASE 6: AVALIAÇÃO FINAL DO MODELO")
        print("-" * 40)
        
        # Dividir dados para avaliação final
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )
        
        # Treinar modelo final
        print("🔄 Treinando modelo final...")
        self.best_model.fit(X_train, y_train)
        
        # Fazer previsões
        y_pred = self.best_model.predict(X_test)
        y_pred_proba = self.best_model.predict_proba(X_test)[:, 1]

        y_pred = (y_pred_proba >= self.threshold).astype(int)
        
        # Calcular métricas
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }
        
        print(f"\n🏆 MÉTRICAS FINAIS ({self.best_model_name}):")
        for metric, value in metrics.items():
            print(f"  {metric.upper()}: {value:.4f}")
        
        # Matriz de confusão
        cm = confusion_matrix(y_test, y_pred)
        print(f"\n📊 MATRIZ DE CONFUSÃO:")
        print(f"              Predito")
        print(f"              0     1")
        print(f"Real    0   {cm[0,0]:4d}  {cm[0,1]:4d}")
        print(f"        1   {cm[1,0]:4d}  {cm[1,1]:4d}")
        
        # Relatório de classificação
        print(f"\n📋 RELATÓRIO DE CLASSIFICAÇÃO:")
        print(classification_report(y_test, y_pred, target_names=['Sem Doença', 'Com Doença']))
        
        self.final_metrics = metrics
        self.X_processed = X
        
        return metrics, y_test, y_pred, y_pred_proba
    
    def generate_shap_analysis(self, X_sample: pd.DataFrame = None, sample_size: int = 1000):
        """
        Análise de Interpretabilidade com SHAP
        """
        if not SHAP_AVAILABLE:
            print("⚠️  SHAP não disponível. Pulando análise de interpretabilidade.")
            return
        
        print("\n🔍 ANÁLISE DE INTERPRETABILIDADE COM SHAP")
        print("-" * 45)
        
        # O X_sample aqui deve ser os dados ANTES do pré-processamento, mas DEPOIS da engenharia de features.
        # Usamos self.X_processed, que foi definido na avaliação final e contém o conjunto de dados X completo.
        if self.X_processed is None:
            print("⚠️  Dados com features de engenharia não encontrados (self.X_processed). Pulando análise SHAP.")
            return

        X_data_for_sampling = self.X_processed
        
        if len(X_data_for_sampling) > sample_size:
            X_sample = X_data_for_sampling.sample(sample_size, random_state=self.random_state)
        else:
            X_sample = X_data_for_sampling
            
        print(f"Analisando {len(X_sample)} amostras...")
        
        try:
            # A biblioteca SHAP é capaz de lidar com pipelines do scikit-learn diretamente.
            # Ao passar o pipeline completo, o SHAP gerencia internamente o pré-processamento.
            # Isso evita discrepâncias de ponto flutuante que podem ocorrer ao transformar
            # os dados manualmente, resolvendo o erro "Additivity check failed".

            # 1. Criar o explainer sobre o pipeline completo, usando a amostra original (não transformada)
            # como dados de fundo (background data).
            explainer = shap.Explainer(self.best_model, X_sample)

            # 2. Calcular os valores SHAP para a mesma amostra não transformada.
            shap_values = explainer(X_sample)

            # Salvar gráfico de resumo
            plt.figure(figsize=(10, 8))
            # Usar o DataFrame transformado para que o plot tenha os valores corretos
            shap.plots.beeswarm(shap_values, max_display=15, show=False) 
            plt.title(f'SHAP Summary Plot - {self.best_model_name}')
            plt.tight_layout()
            plt.savefig('models/shap_summary_plot.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            print("✓ Análise SHAP concluída")
            print("  Gráfico salvo em: models/shap_summary_plot.png")
            
        except Exception as e:
            print(f"⚠️  Erro na análise SHAP: {e}")
    
    def save_model_and_pipeline(self) -> str:
        """
        Salva o modelo final e pipeline
        """
        print("\n💾 SALVANDO MODELO E PIPELINE")
        print("-" * 35)
        
        # Criar diretório se não existir
        os.makedirs('models', exist_ok=True)
        
        # Salvar modelo
        model_path = 'models/cardiac_risck_model_v2.joblib'
        joblib.dump(self.best_model, model_path)
        print(f"✓ Modelo salvo em: {model_path}")
        
        # Salvar pipeline de pré-processamento separadamente
        pipeline_path = 'models/preprocessing_pipeline.joblib'
        joblib.dump(self.preprocessing_pipeline, pipeline_path)
        print(f"✓ Pipeline salvo em: {pipeline_path}")
        
        # Salvar metadados
        metadata = {
            'model_name': self.best_model_name,
            'final_metrics': self.final_metrics,
            'cv_results': self.cv_results,
            'training_date': datetime.now().isoformat(),
            'data_shape': self.df_clean.shape,
            'features_count': self.X_processed.shape[1] if self.X_processed is not None else 0
        }
        
        metadata_path = 'models/model_metadata.joblib'
        joblib.dump(metadata, metadata_path)
        print(f"✓ Metadados salvos em: {metadata_path}")
        
        return model_path
    
    def run_complete_pipeline(self) -> Dict:
        """
        Executa o pipeline completo
        """
        print("🚀 INICIANDO PIPELINE COMPLETO DE DESENVOLVIMENTO")
        print("=" * 65)
        
        start_time = datetime.now()
        
        try:
            # Fase 1: EDA e limpeza
            self.load_and_explore_data()
            df_clean = self.clean_and_validate_data()
            
            # Fase 2: Engenharia de features
            df_engineered = self.engineer_features()
            
            # Fase 3: Pipeline de pré-processamento
            self.create_preprocessing_pipeline(df_engineered)
            
            # Preparar dados
            X, y = self.prepare_data_for_modeling(df_engineered)
            
            # Fase 4: Comparação de modelos
            self.train_and_compare_models(X, y)
            
            # Fase 5: Otimização
            self.optimize_hyperparameters(X, y)
            
            # Fase 6: Avaliação final
            final_metrics, y_test, y_pred, y_pred_proba = self.final_evaluation(X, y)
            
            # Interpretabilidade
            self.generate_shap_analysis()
            
            # Salvar modelo
            model_path = self.save_model_and_pipeline()
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            print(f"\n🎉 PIPELINE CONCLUÍDO COM SUCESSO!")
            print(f"⏱️  Tempo total: {duration}")
            print(f"🏆 Melhor modelo: {self.best_model_name}")
            print(f"📈 ROC-AUC final: {final_metrics['roc_auc']:.4f}")
            print(f"💾 Modelo salvo em: {model_path}")
            
            return {
                'success': True,
                'model_name': self.best_model_name,
                'final_metrics': final_metrics,
                'model_path': model_path,
                'duration': str(duration)
            }
            
        except Exception as e:
            print(f"\n❌ ERRO NO PIPELINE: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}

def main():
    """
    Função principal
    """
    # Criar e executar pipeline
    pipeline = CardiacRiskModelPipeline()
    results = pipeline.run_complete_pipeline()
    
    if results['success']:
        print("\n" + "=" * 65)
        print("✅ DESENVOLVIMENTO DE MODELO CONCLUÍDO COM SUCESSO!")
        print("=" * 65)
    else:
        print("\n" + "=" * 65)
        print("❌ FALHA NO DESENVOLVIMENTO DO MODELO")
        print("=" * 65)

if __name__ == "__main__":
    main()
