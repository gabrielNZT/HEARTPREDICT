"""
Script para treinar o modelo XGBoost para previsão de risco cardíaco
"""

import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np

def load_and_preprocess_data(file_path):
    """
    Carrega e preprocessa os dados do dataset cardiovascular
    """
    print("Carregando dados...")
    df = pd.read_csv(file_path, sep=';')
    
    print(f"Dataset carregado: {df.shape}")
    print(f"Colunas: {df.colíumns.tolist()}")
    
    # Remover coluna ID (não é útil para predição)
    df = df.drop('id', axis=1)
    
    # Converter idade de dias para anos
    df['age'] = (df['age'] / 365.25).astype(int)
    
    # Criar feature BMI (Body Mass Index)
    # BMI = peso (kg) / (altura (m))^2
    df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
    
    print("Pré-processamento concluído:")
    print(f"- Idade convertida para anos")
    print(f"- BMI calculado")
    print(f"- Coluna 'id' removida")
    print(f"Estatísticas básicas da idade:")
    print(f"  Min: {df['age'].min()}, Max: {df['age'].max()}, Média: {df['age'].mean():.1f}")
    
    return df

def train_model(df):
    """
    Treina o modelo XGBoost
    """
    print("\nPreparando dados para treinamento...")
    
    # Separar features (X) e target (y)
    X = df.drop('cardio', axis=1)
    y = df['cardio']
    
    print(f"Features utilizadas: {X.columns.tolist()}")
    print(f"Distribuição da classe target:")
    print(y.value_counts(normalize=True))
    
    # Dividir dados em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nConjunto de treino: {X_train.shape}")
    print(f"Conjunto de teste: {X_test.shape}")
    
    # Configurar e treinar o modelo XGBoost
    print("\nTreinando modelo XGBoost...")
    
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='logloss'
    )
    
    # Treinar o modelo
    model.fit(X_train, y_train)
    
    print("Treinamento concluído!")
    
    return model, X_train, X_test, y_train, y_test

def evaluate_model(model, X_test, y_test):
    """
    Avalia o modelo treinado
    """
    print("\n" + "="*50)
    print("AVALIAÇÃO DO MODELO")
    print("="*50)
    
    # Fazer previsões
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calcular acurácia
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia: {accuracy:.4f}")
    
    # Relatório de classificação
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred, target_names=['Sem Doença', 'Com Doença']))
    
    # Matriz de confusão
    cm = confusion_matrix(y_test, y_pred)
    print("\nMatriz de Confusão:")
    print(f"                 Predito")
    print(f"                 0     1")
    print(f"Real    0     {cm[0,0]:6d} {cm[0,1]:6d}")
    print(f"        1     {cm[1,0]:6d} {cm[1,1]:6d}")
    
    # Estatísticas adicionais
    print(f"\nEstatísticas Adicionais:")
    print(f"- Verdadeiros Negativos: {cm[0,0]}")
    print(f"- Falsos Positivos: {cm[0,1]}")
    print(f"- Falsos Negativos: {cm[1,0]}")
    print(f"- Verdadeiros Positivos: {cm[1,1]}")
    
    # Importância das features
    feature_importance = model.feature_importances_
    feature_names = X_test.columns
    
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': feature_importance
    }).sort_values('importance', ascending=False)
    
    print(f"\nImportância das Features (Top 10):")
    print(importance_df.head(10).to_string(index=False))
    
    return accuracy, y_pred_proba

def save_model(model, file_path):
    """
    Salva o modelo treinado
    """
    print(f"\nSalvando modelo em: {file_path}")
    joblib.dump(model, file_path)
    print("Modelo salvo com sucesso!")

def main():
    """
    Função principal que executa todo o pipeline de treinamento
    """
    print("INICIANDO TREINAMENTO DO MODELO DE RISCO CARDÍACO")
    print("="*60)
    
    # Caminhos dos arquivos
    data_path = "data/cardio_train.csv"
    model_path = "models/cardiac_risk_model.joblib"
    
    try:
        # 1. Carregar e preprocessar dados
        df = load_and_preprocess_data(data_path)
        
        # 2. Treinar modelo
        model, X_train, X_test, y_train, y_test = train_model(df)
        
        # 3. Avaliar modelo
        accuracy, y_pred_proba = evaluate_model(model, X_test, y_test)
        
        # 4. Salvar modelo
        save_model(model, model_path)
        
        print("\n" + "="*60)
        print("TREINAMENTO CONCLUÍDO COM SUCESSO!")
        print(f"Acurácia final: {accuracy:.4f}")
        print(f"Modelo salvo em: {model_path}")
        print("="*60)
        
    except Exception as e:
        print(f"Erro durante o treinamento: {e}")
        raise

if __name__ == "__main__":
    main()
