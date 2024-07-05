from CreditCardFraudDetection.config.configuration import ConfigurationManager
from CreditCardFraudDetection.components.data_validation import DataValidation
from CreditCardFraudDetection import logger

class DataValidationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config_manager = ConfigurationManager()
            data_validation_config = config_manager.get_data_validation_config()
            data_validation = DataValidation(config = data_validation_config)
            data_validation.validate_all_columns()

        except Exception as e:
            logger.error(f"Error in validating all columns: {e}")
            raise e
        
if __name__ == "__main__":
    pass