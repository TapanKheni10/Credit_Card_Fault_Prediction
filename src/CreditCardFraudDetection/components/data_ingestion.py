import pandas as pd
import numpy as np
from pymongo import MongoClient
from CreditCardFraudDetection import logger
from CreditCardFraudDetection.utils.common import get_size
from CreditCardFraudDetection.constants import MONGO_DB_URL, MONGO_DB_DATABASE_NAME, MONGO_DB_COLLECTION_NAME
from CreditCardFraudDetection.entity.config_entity import DataIngestionConfig
from pathlib import Path  
import os

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def export_collection_as_dataframe(self, collection_name: str) -> pd.DataFrame:
        logger.info("Exporting MongoDB collection to DataFrame")
        client = MongoClient(MONGO_DB_URL)
        collection = client[MONGO_DB_DATABASE_NAME][collection_name]

        try:
            client.server_info()
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return pd.DataFrame()
        
        number_of_documents = collection.count_documents({})
        logger.info(f"Number of documents in collection {collection_name}: {number_of_documents}")

        try:
            data = list(collection.find())
            logger.info(f"Data retrieved from collection {data[:2]}")
        except Exception as e:
            logger.error(f"Failed to retrieve data from collection: {e}")
            return pd.DataFrame()
        
        df = pd.DataFrame(data)

        logger.info(f"DataFrame columns: {df.columns.to_list()}")

        if "_id" in df.columns.to_list():
            df.drop(columns=["_id"], axis=1, inplace=True)
        
        logger.info(f"DataFrame columns: {df.columns.to_list()}")

        logger.info(f"DataFrame shape: {df.shape}")
        logger.info("Data retrieved successfully")

        client.close()

        return df
    
    def export_data_to_file_path(self):
        logger.info("Exporting data from mongoDB to store it into the desired artifacts.")

        i = 0
        for collection_name in MONGO_DB_COLLECTION_NAME:
            logger.info(f"Exporting data from collection {collection_name}")
            
            df = self.export_collection_as_dataframe(collection_name)

            logger.info(f"Exporting data to {self.config.root_dir}")

            file_path = Path(self.config.local_data_path[i])
            if not os.path.exists(file_path):
                df.to_csv(file_path, index=False)

                logger.info(f"exported data from mongoDB to {file_path}")
            else:
                logger.info(f"file already exists at {file_path} of size {get_size(file_path)}")
            
            i += 1

    def initiate_data_ingestion(self):
        logger.info("data ingestion process initiated.")

        self.export_data_to_file_path()

        logger.info("data ingestion process completed.")