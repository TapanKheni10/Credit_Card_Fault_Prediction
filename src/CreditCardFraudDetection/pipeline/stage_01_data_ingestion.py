from CreditCardFraudDetection.components.data_ingestion import DataIngestion
from CreditCardFraudDetection.config.configuration import ConfigurationManager
from CreditCardFraudDetection import logger

class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config_manager = ConfigurationManager()
            data_ingestion_config = config_manager.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.initiate_data_ingestion()
        except Exception as e:
            logger.error(f"Error in data ingestion: {str(e)}")

if __name__ == "__main__":
    pass