import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from CreditCardFraudDetection import logger

class FraudulentPredictionPipeline:
    def __init__(self):
        self.model = joblib.load('artifacts/model_trainer/default.joblib')
        self.preprocessor = joblib.load('artifacts/data_transformation/default_on_payment/preprocessor.joblib')

    def predict(self, data: pd.DataFrame) -> str:
        logger.info("Predicting default status of credit card users")
        transformed_data = self.preprocessor.transform(data)
        prediction = int(self.model.predict(transformed_data))

        if prediction == 1:
            prediction = "The credit card user will default on their payments"
        else:
            prediction = "The credit card user will not default on their payments"

        logger.info(f"Prediction: {prediction}")
        return prediction