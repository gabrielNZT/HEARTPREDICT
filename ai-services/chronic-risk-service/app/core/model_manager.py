import joblib
import threading
import os
import logging
import pandas as pd
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ModelManager:
    """
    Gerenciador thread-safe para o modelo aprimorado
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ModelManager, cls).__new__(cls)
                    cls._instance._model = None
                    cls._instance._metadata = None
                    cls._instance._model_lock = threading.RLock()
        return cls._instance

    def load_model(self, model_path: str = "models/cardiac_risck_model_v2.joblib"):
        """
        Carrega o modelo aprimorado de forma thread-safe
        """
        with self._model_lock:
            if self._model is None:
                if not os.path.exists(model_path):
                    raise FileNotFoundError(f"Modelo aprimorado não encontrado em: {model_path}")
                
                self._model = joblib.load(model_path)

                # Carregar metadados se existir
                metadata_path = model_path.replace(
                    'cardiac_risck_model_v2.joblib',
                    'model_metadata.joblib'
                )
                if os.path.exists(metadata_path):
                    self._metadata = joblib.load(metadata_path)

                logger.info(f"Modelo aprimorado carregado com sucesso de: {model_path}")
                if self._metadata:
                    # Logar nome do modelo e ROC-AUC de forma segura
                    final_metrics = self._metadata.get('final_metrics', {})
                    roc_auc = final_metrics.get('roc_auc')
                    try:
                        roc_auc_str = f"{roc_auc:.4f}"
                    except Exception:
                        roc_auc_str = str(roc_auc)
                    logger.info(
                        f"Modelo: {self._metadata.get('model_name')}, ROC-AUC: {roc_auc_str}"
                    )

    def preprocess_patient_data(self, patient_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Preprocessa dados do paciente usando as mesmas transformações do pipeline de treinamento
        """
        df = pd.DataFrame([patient_data])
        # Calcular BMI
        df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
        # Categorias de BMI
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
        # Categorias de Pressão Arterial
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
        # Features de interação
        df['age_cholesterol_interaction'] = df['age'] * df['cholesterol']
        df['bmi_age_interaction'] = df['bmi'] * df['age']
        df['pressure_pulse'] = df['ap_hi'] - df['ap_lo']
        # Lifestyle score
        df['lifestyle_score'] = df['smoke'] + df['alco'] - df['active']
        # Categorização de idade
        def categorize_age(age):
            if age < 40:
                return 'Young'
            elif age < 55:
                return 'Middle_aged'
            else:
                return 'Senior'
        df['age_category'] = df['age'].apply(categorize_age)
        return df

    def predict(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz predição usando o pipeline completo
        """
        with self._model_lock:
            if self._model is None:
                raise RuntimeError("Modelo não carregado")

            df = self.preprocess_patient_data(patient_data)
            
            # Pipeline salva já inclui preprocessamento
            risk_proba = self._model.predict_proba(df)[0][1]
            risk_prediction = self._model.predict(df)[0]
            
            return {
                'risk_probability': risk_proba,
                'risk_prediction': int(risk_prediction),
                'processed_features': df.iloc[0].to_dict()
            }

    def get_model_info(self) -> Dict[str, Any]:
        """
        Retorna informações do modelo aprimorado
        """
        with self._model_lock:
            if self._model is None:
                raise RuntimeError("Modelo não carregado")

            info = {
                "model_type": "Enhanced Pipeline with LightGBM",
                "version": "2.0",
                "pipeline_stages": [
                    "Data Cleaning",
                    "Feature Engineering",
                    "Preprocessing Pipeline",
                    "Model Comparison",
                    "Hyperparameter Optimization",
                    "Cross-Validation"
                ]
            }
            if self._metadata:
                info.update({
                    "model_name": self._metadata.get('model_name'),
                    "training_date": self._metadata.get('training_date'),
                    "final_metrics": self._metadata.get('final_metrics'),
                    "data_shape": self._metadata.get('data_shape'),
                    "features_count": self._metadata.get('features_count')
                })
            return info

    def is_loaded(self) -> bool:
        """
        Verifica se o modelo está carregado
        """
        with self._model_lock:
            return self._model is not None

# Instância global
model_manager = ModelManager()

def get_model_manager() -> ModelManager:
    """
    Dependency injection para o model manager
    """
    return model_manager
