import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from CreditCardFraudDetection import logger

class FraudulentPredictionPipeline:
    def __init__(self):
        self.model = joblib.load('artifacts/model_trainer/fraudulent.joblib')
        self.preprocessor = joblib.load('artifacts/data_transformation/fraudulent_transection/preprocessor.joblib')

    def predict(self, data: pd.DataFrame) -> str:
        logger.info("Predicting fraudulent transections")
        transformed_data = self.preprocessor.transform(data)
        prediction = int(self.model.predict(transformed_data))

        if prediction == 1:
            prediction = "Fraudulent Transaction"
        else:
            prediction = "Not Fraudulent Transaction"

        logger.info(f"Prediction: {prediction}")
        return prediction