from CreditCardFraudDetection import logger
from CreditCardFraudDetection.entity import config_entity
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib
from typing import List
import os

class DataTransformation:
    def __init__(self, config: config_entity.DataTransformationConfig):
        self.config = config

    def split_data(self, data: pd.DataFrame, stratify_column: str):
        train_data, test_data = train_test_split(data, stratify=data[stratify_column], test_size = 0.3, random_state = 42)
        logger.info("Data split into train and test sets successfully!")

        X_train, y_train, X_test, y_test = train_data.drop(stratify_column, axis=1), train_data[stratify_column], test_data.drop(stratify_column, axis=1), test_data[stratify_column]
        logger.info("Features and target variable retrieved successfully!")

        return X_train, X_test, y_train, y_test
    
    def get_skewed_features(self, data: pd.DataFrame) -> List[str]:
        skewed_features = []

        for col in data.select_dtypes(include=[np.number]).columns:
            mean = data[col].mean()
            median = data[col].median()
            mode = data[col].mode().iloc[0]

            if mean > median > mode:
                skewed_features.append(col)
            elif mean < median < mode:
                skewed_features.append(col)
            else:
                continue

        logger.info(f"Skewed features: {skewed_features}")

        return skewed_features
    
    def get_preprocessor(self, data: pd.DataFrame) -> Pipeline:
        non_skewed_features = list(data.columns)
        skewed_features = self.get_skewed_features(data)
        non_skewed_features = [col for col in non_skewed_features if col not in skewed_features]
        logger.info(f"Non-skewed features: {non_skewed_features}")

        power_transformation = PowerTransformer(method="yeo-johnson", copy=False, standardize=True)
        standard_scaler = StandardScaler()

        power_pipeline = Pipeline(
            steps=[
                ("power_transformation", power_transformation)
            ]
        )

        numeric_pipeline = Pipeline(
            steps=[
                ("scaler", standard_scaler)
            ]
        )

        preprocessor = ColumnTransformer(
        transformers=[
                ("power_pipeline", power_pipeline, skewed_features),
                ("numeric_pipeline", numeric_pipeline, non_skewed_features),
            ],
            remainder='passthrough'
        )
        logger.info("Preprocessor created successfully!")

        return preprocessor

    def perform_data_transformation(self):
        logger.info("Starting data transformation...")

        data_path = self.config.data_path[0]

        data = pd.read_csv(data_path)
        logger.info(f"Data loaded successfully from {data_path}")
        
        X_train, X_test, y_train, y_test = self.split_data(data, 'Class') 
        logger.info("Data split into train and test sets retrieved successfully!")

        preprocessor = self.get_preprocessor(X_train)
        logger.info("Preprocessor retrieved successfully!")

        logger.info(f"Before transformation: \n{X_train.head()}")

        X_train = preprocessor.fit_transform(X_train)
        X_test = preprocessor.transform(X_test)

        logger.info(f"After transformation: \n{X_train[:5]}")

        y_train = y_train.to_numpy()
        y_test = y_test.to_numpy()

        preprocessed_data_path = self.config.preprocessed_data_path[0]
        if not os.path.exists(preprocessed_data_path):
            os.makedirs(preprocessed_data_path, exist_ok=True)

        np.save(os.path.join(preprocessed_data_path, "X_train.npy"), X_train)
        np.save(os.path.join(preprocessed_data_path, "X_test.npy"), X_test)
        np.save(os.path.join(preprocessed_data_path, "y_train.npy"), y_train)
        np.save(os.path.join(preprocessed_data_path, "y_test.npy"), y_test)

        logger.info("Data saved successfully!")

        joblib.dump(preprocessor, os.path.join(preprocessed_data_path, self.config.preprocessor_name))
        logger.info("Preprocessor saved successfully!")

        logger.info("Data transformation completed successfully!")