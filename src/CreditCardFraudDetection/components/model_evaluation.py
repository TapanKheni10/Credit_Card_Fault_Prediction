import pandas as pd 
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
import os
from CreditCardFraudDetection import logger
from CreditCardFraudDetection.entity.config_entity import ModelEvaluationConfig
from pathlib import Path
from CreditCardFraudDetection.utils.common import save_json

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def calculate_metrics(self, y_true, y_pred, y_prob):
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        roc_auc = roc_auc_score(y_true, y_prob)

        return accuracy, precision, recall, f1, roc_auc
    
    def evaluate_model(self, model_number: int):
        assert model_number in [1, 2], "Invalid model number, It should be 1 or 2"

        X_test = np.load(self.config.x_test_data_path[model_number - 1])
        y_test = np.load(self.config.y_test_data_path[model_number - 1])
        logger.info(f"Loaded test data for model {model_number}")

        model = joblib.load(self.config.model_path[model_number - 1])
        logger.info(f"Loaded model {model_number}")

        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        logger.info(f"Predictions for model {model_number} done")

        accuracy, precision, recall, f1, roc_auc = self.calculate_metrics(y_test, y_pred, y_prob)
        logger.info(f"Metrics calculated for model {model_number}")

        scores = {
            "accuracy_score": accuracy,
            "precision_score": precision,
            "recall_score": recall,
            "f1_score": f1,
            "roc_auc_score": roc_auc
        }

        if not os.path.exists(self.config.evaluation_report[model_number - 1]):
            os.makedirs(self.config.evaluation_report[model_number - 1])
            
        save_json(path = Path(os.path.join(self.config.evaluation_report[model_number - 1], "metrics.json")), data = scores)
        np.save(os.path.join(self.config.evaluation_report[model_number - 1], "y_pred.npy"), y_pred)
        np.save(os.path.join(self.config.evaluation_report[model_number - 1], "y_prob.npy"), y_prob)
        logger.info(f"Metrics saved for model {model_number}")

        