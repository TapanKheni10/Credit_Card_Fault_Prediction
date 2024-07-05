from CreditCardFraudDetection.config.configuration import ConfigurationManager
from CreditCardFraudDetection.components.fraudulent_transection.data_transformation import DataTransformation
from CreditCardFraudDetection import logger

class DataTransformationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config_manager = ConfigurationManager()
            data_transformation_config = config_manager.get_data_transformation_config()
            data_transformer = DataTransformation(config = data_transformation_config)
            data_transformer.perform_data_transformation()

        except Exception as e:
            logger.error(f"Failed to perform data transformation! Error: {e}")
            raise e
        
if __name__ == "__main__":
    pass