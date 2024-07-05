from CreditCardFraudDetection.config.configuration import ConfigurationManager
from CreditCardFraudDetection.components.model_trainer import ModelTrainer
from CreditCardFraudDetection import logger 

class ModelTrainerPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        try:
            config_manager = ConfigurationManager()
            model_trainer_config = config_manager.get_model_trainer_config()
            model_trainer = ModelTrainer(config = model_trainer_config)

            model_trainer.train(model_number=1)

            model_trainer.train(model_number=2)

        except Exception as e:
            logger.error(e)
            raise e
        
if __name__ == "__main__":
    pass