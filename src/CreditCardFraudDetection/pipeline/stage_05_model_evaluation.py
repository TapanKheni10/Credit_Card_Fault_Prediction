from CreditCardFraudDetection.components.model_evaluation import ModelEvaluation
from CreditCardFraudDetection.config.configuration import ConfigurationManager
from CreditCardFraudDetection import logger

class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config_manager = ConfigurationManager()
            model_evaluation_config = config_manager.get_model_evaluation_config()
            model_evaluation = ModelEvaluation(config = model_evaluation_config)

            model_evaluation.evaluate_model(model_number = 1)
            model_evaluation.evaluate_model(model_number = 2)

        except Exception as e:
            logger.error(e)
            raise e
        
if __name__ == "__main__":
    pass