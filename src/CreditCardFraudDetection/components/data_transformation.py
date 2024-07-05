from CreditCardFraudDetection import logger
from CreditCardFraudDetection.entity import config_entity
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PowerTransformer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from imblearn.over_sampling import SMOTE
import joblib
from typing import List
import os

class DataTransformation:
    def __init__(self, config: config_entity.DataTransformationConfig):
        self.config = config

    def split_data(self, data: pd.DataFrame, stratify_column: str):
        train_data, test_data = train_test_split(data, stratify=data[stratify_column], test_size = 0.3, random_state = 42)
        logger.info("Data split into train and test sets successfully!")

        train_data, validation_data = train_test_split(train_data, stratify=train_data[stratify_column], test_size = 0.3, random_state = 42)
        logger.info("Train data split into train and validation sets successfully!")

        X_train, y_train, X_test, y_test = train_data.drop(stratify_column, axis=1), train_data[stratify_column], test_data.drop(stratify_column, axis=1), test_data[stratify_column]
        X_val, y_val = validation_data.drop(stratify_column, axis=1), validation_data[stratify_column]
        logger.info("Features and target variable retrieved successfully!")

        return X_train, X_test, X_val, y_train, y_test, y_val
    
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
    
    def get_preprocessor_for_fraudulent_transection(self, data: pd.DataFrame) -> Pipeline:
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
    
    def get_preprocessor_for_default_payment(self, data: pd.DataFrame) -> Pipeline:
        cols_to_preprocess = list(data.columns)
        
        standardization = StandardScaler()

        scaler_pipeline = Pipeline(
            steps=[
                ("standardization", standardization)
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("scaler_pipeline", scaler_pipeline, cols_to_preprocess),
            ],
            remainder='passthrough'
        )

        preprocessor
        logger.info("Preprocessor created successfully!")

        return preprocessor
    
    def get_numerical_features(self, df) -> List[str]:
        numerical_features = []

        for col in df.columns:
            if df[col].nunique() > 13:
                numerical_features.append(col)
            
        return numerical_features 
    
    def remove_outliers(self, df: pd.DataFrame, numerical_features: List[str]) -> pd.DataFrame:
        for col in numerical_features:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            
            IQR = q3 - q1
            lower_bound = q1 - 1.5 * IQR
            upper_bound = q3 + 1.5 * IQR
            
            df[col] = df[col].clip(lower_bound, upper_bound)
            
        return df
    
    def handle_undocumented_categories(self, df: pd.DataFrame) -> pd.DataFrame:
        df["EDUCATION"] = df["EDUCATION"].map(lambda x : 4 if x in (5, 6, 0) else x)

        df["MARRIAGE"] = df["MARRIAGE"].map(lambda x : 3 if x == 0 else x)

        return df
    
    def handle_imbalance(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Handling imbalance in the data...")
        X = df.drop(columns=["default_status_next_month"], axis=1)
        y = df["default_status_next_month"]

        logger.info(f"Distribution of the target feature before resampling: {y.value_counts()}")

        smote = SMOTE(random_state=42)
        X, y = smote.fit_resample(X, y)

        logger.info(f"Distribution of the target feature after resampling: {y.value_counts()}")

        df = X.copy()
        df["default_status_next_month"] = y

        logger.info(f"Shape of the data: {df.shape}\n")

        return df

    def perform_data_transformation_for_fraudulent_transection(self):
        logger.info("Starting data transformation...")

        data_path = self.config.data_path[0]

        data = pd.read_csv(data_path)
        logger.info(f"Data loaded successfully from {data_path}")
        
        X_train, X_test, X_val, y_train, y_test, y_val = self.split_data(data, 'Class') 
        logger.info("Data split into train and test sets retrieved successfully!")

        preprocessor = self.get_preprocessor_for_fraudulent_transection(X_train)
        logger.info("Preprocessor retrieved successfully!")

        logger.info(f"Before transformation: \n{X_train.head()}")

        X_train = preprocessor.fit_transform(X_train)
        X_test = preprocessor.transform(X_test)
        X_val = preprocessor.transform(X_val)

        logger.info(f"After transformation: \n{X_train[:5]}")

        y_train = y_train.to_numpy()
        y_test = y_test.to_numpy()
        y_val = y_val.to_numpy()

        preprocessed_data_path = self.config.preprocessed_data_path[0]
        if not os.path.exists(preprocessed_data_path):
            os.makedirs(preprocessed_data_path, exist_ok=True)

        np.save(os.path.join(preprocessed_data_path, "X_train.npy"), X_train)
        np.save(os.path.join(preprocessed_data_path, "X_test.npy"), X_test)
        np.save(os.path.join(preprocessed_data_path, "X_val.npy"), X_val)
        np.save(os.path.join(preprocessed_data_path, "y_train.npy"), y_train)
        np.save(os.path.join(preprocessed_data_path, "y_test.npy"), y_test)
        np.save(os.path.join(preprocessed_data_path, "y_val.npy"), y_val)

        logger.info("Data saved successfully!")

        joblib.dump(preprocessor, os.path.join(preprocessed_data_path, self.config.preprocessor_name))
        logger.info("Preprocessor saved successfully!")

        logger.info("Data transformation completed successfully!")

    def perform_data_transformation_for_default_payment(self):
        logger.info("Starting data transformation...")

        data_path = self.config.data_path[1]

        data = pd.read_csv(data_path)
        logger.info(f"Data loaded successfully from {data_path}")

        data.rename(columns = {'PAY_0' : 'PAY_1',
                               'default.payment.next.month' : 'default_status_next_month'}, inplace = True)
        logger.info("Columns renamed successfully")
        logger.info(f"Data columns: {data.columns}")

        numerical_features = self.get_numerical_features(data)
        logger.info(f"Numerical features: {numerical_features}")

        data = self.remove_outliers(data, numerical_features)
        logger.info("Outliers removed successfully")

        data = data[data["BILL_AMT1"] >= 0]
        logger.info("Data with BILL_AMT1 >= 0, shape: {data.shape}")

        data = self.handle_undocumented_categories(data)
        logger.info(f"EDUCATION: \n{data['EDUCATION'].value_counts()}")
        logger.info(f"MARRIAGE: \n{data['MARRIAGE'].value_counts()}")
        logger.info("Undocumented categories handled successfully")

        data.drop(columns=["BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6"], axis=1, inplace=True)
        logger.info("Columns BILL_AMT2, BILL_AMT3, BILL_AMT4, BILL_AMT5, BILL_AMT6 dropped successfully")
        logger.info(f"Data columns: {data.columns}")

        data = self.handle_imbalance(data)
        logger.info("Imbalance handled successfully")

        X_train, X_test, X_val, y_train, y_test, y_val = self.split_data(data, "default_status_next_month")
        logger.info("Data split into train and test sets successfully")

        preprocessor = self.get_preprocessor_for_default_payment(X_train)
        logger.info("Preprocessor retrieved successfully")

        logger.info(f"Before transformation: \n{X_train.head()}")

        X_train = preprocessor.fit_transform(X_train)
        X_test = preprocessor.transform(X_test)
        X_val = preprocessor.transform(X_val)

        logger.info(f"After transformation: \n{X_train[:5]}")

        y_train = y_train.to_numpy()
        y_test = y_test.to_numpy()
        y_val = y_val.to_numpy()

        preprocessed_data_path = self.config.preprocessed_data_path[1]
        if not os.path.exists(preprocessed_data_path):
            os.makedirs(preprocessed_data_path, exist_ok=True)

        np.save(os.path.join(preprocessed_data_path, "X_train.npy"), X_train)
        np.save(os.path.join(preprocessed_data_path, "X_test.npy"), X_test)
        np.save(os.path.join(preprocessed_data_path, "X_val.npy"), X_val)
        np.save(os.path.join(preprocessed_data_path, "y_train.npy"), y_train)
        np.save(os.path.join(preprocessed_data_path, "y_test.npy"), y_test)
        np.save(os.path.join(preprocessed_data_path, "y_val.npy"), y_val)

        logger.info("Data saved successfully!")

        joblib.dump(preprocessor, os.path.join(preprocessed_data_path, self.config.preprocessor_name))
        logger.info("Preprocessor saved successfully!")

        logger.info("Data transformation completed successfully!")