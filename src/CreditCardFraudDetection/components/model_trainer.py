import pandas as pd
import numpy as np  
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from CreditCardFraudDetection.entity.config_entity import ModelTrainerConfig
import joblib
import os
import time
from CreditCardFraudDetection import logger
# import mlflow
# import mlflow.sklearn as mlf_sklearn
# from urllib.parse import urlparse

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
        self.models = [
            {
                'SVC': SVC(),
                'RandomForestClassifier': RandomForestClassifier(),
                'GradientBoostingClassifier': GradientBoostingClassifier(),
                'AdaBoostClassifier': AdaBoostClassifier(),
                'DecisionTreeClassifier': DecisionTreeClassifier(),
                'KNeighborsClassifier': KNeighborsClassifier()
            },
            {
                'SVC': SVC(),
                'RandomForestClassifier': RandomForestClassifier(),
                'GradientBoostingClassifier': GradientBoostingClassifier(),
                'AdaBoostClassifier': AdaBoostClassifier(),
                'DecisionTreeClassifier': DecisionTreeClassifier(),
                'KNeighborsClassifier': KNeighborsClassifier(),
                'LGBMClassifier': LGBMClassifier(),
                'XGBClassifier': XGBClassifier(),
                'CatBoostClassifier' : CatBoostClassifier()
            } 
        ]

    def evaluate_model(self, true, predicted):

        accuracy = accuracy_score(true, predicted)
        precision = precision_score(true, predicted)
        recall = recall_score(true, predicted)
        f1 = f1_score(true, predicted)

        return accuracy, precision, recall, f1

    def model_training(self, X_train, y_train, X_test, y_test, x: int):
        
        model_performance = pd.DataFrame(columns=["accuracy", "precision", "recall", "f1_score", "training_time", "prediction_time", "total_time"])

        # mlflow.set_experiment(f"model_{x}_comparison_experiment")

        # tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        models = self.models[x-1]

        for i in range(len(models)):
        
            # with mlflow.start_run(run_name=f"{list(models.keys())[i]} model"):
                     
                # mlflow.log_param("model_name", list(models.keys())[i])
                # mlflow.log_param("model_type", str(models[list(models.keys())[i]]))

            start_time = time.time()
            model = list(models.values())[i]
            model.fit(X_train, y_train)
            end_training = time.time()

            y_pred = model.predict(X_test)
            end_prediction = time.time()

            accuracy, precision, recall, f1 = self.evaluate_model(y_test, y_pred)

                # mlflow.log_metric("accuracy", accuracy)
                # mlflow.log_metric("precision", precision)
                # mlflow.log_metric("recall", recall)
                # mlflow.log_metric("f1_score", f1)

                # if tracking_url_type_store != "file":
                #     mlflow.sklearn.log_model(model, f"{list(models.keys())[i]} model", registered_model_name=f"{list(models.keys())[i]}")
                # else:
                #     mlflow.sklearn.log_model(model, f"{list(models.keys())[i]} model")

            model_performance.loc[list(models.keys())[i]] = [accuracy, precision, recall, f1, end_training-start_time, end_prediction-end_training, end_prediction-start_time]

        if not os.path.exists(self.config.root_dir):
            os.makedirs(self.config.root_dir)

        if x == 1:
            performance_file_name = 'fraudulent_model_performance.json'
            matrix = 'recall'
        else:
            performance_file_name = 'default_model_performance.json'
            matrix = 'f1_score'
            
        model_performance.to_json(os.path.join(self.config.root_dir, performance_file_name))
        best_score = model_performance[matrix].max()
        best_model_name = model_performance[model_performance[matrix] == best_score].index[0]

        # logger.info(f"Experiments {mlflow.get_experiment_by_name(f'model_{x}_comparison_experiment').experiment_id} completed")

        return best_score, best_model_name


    def train(self, model_number: int):
        assert model_number in [1, 2], "model_number should be either 1 or 2"

        logger.info(f"Training model_{model_number} started")

        logger.info("Training the model...")
        X_train_path = self.config.x_train_data_path[model_number-1]
        y_train_path = self.config.y_train_data_path[model_number-1]
        X_val_path = self.config.x_val_data_path[model_number-1]
        y_val_path = self.config.y_val_data_path[model_number-1]

        X_train = np.load(X_train_path)
        y_train = np.load(y_train_path)
        X_val = np.load(X_val_path)
        y_val = np.load(y_val_path)
        logger.info("Data loaded successfully")

        logger.info(f"shape of X_train: {X_train.shape}")
        logger.info(f"shape of y_train: {y_train.shape}")
        logger.info(f"shape of X_val: {X_val.shape}")
        logger.info(f"shape of y_val: {y_val.shape}")

        best_model_score, best_model_name = self.model_training(X_train, y_train, X_val, y_val, model_number)
        logger.info(f"Best model name: {best_model_name}")
        logger.info(f"Best model score: {best_model_score}")

        model = self.models[model_number-1][best_model_name]
        model.fit(X_train, y_train)
        logger.info("Model trained successfully")

        model_path = os.path.join(self.config.root_dir, self.config.model_name[model_number-1])
        joblib.dump(model, model_path)
        logger.info(f"Model saved at: {model_path}")

