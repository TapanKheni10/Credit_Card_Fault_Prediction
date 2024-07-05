from CreditCardFraudDetection.entity.config_entity import DataValidationConfig
from CreditCardFraudDetection import logger
import pandas as pd
from typing import List

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
        assert isinstance(self.config.local_data_path, List[str]), "local_data_path should be a list of strings"
        assert isinstance(self.config.all_schema, List[dict]), "all_schema should be a list of dictionaries"
        assert len(self.config.local_data_path) == len(self.config.all_schema), "Mismatch between the number of data files and schema provided"

    def validate_all_columns(self) -> bool:

        logger.info("Validation process of all columns in the data started...")
        
        try:
            validation_status = None

            i = 0
            for data_path in self.config.local_data_path:
                data = pd.read_csv(data_path)
                schema = self.config.all_schema[i].keys()

                data_columns = list(data.columns)

                for col in data_columns:
                    if col not in schema:
                        validation_status = False
                        with open(self.config.STATUS_FILE, "w") as file:
                            file.write(f"Validation status: {validation_status}")

                        logger.error(f"Column {col} not in schema for data stored at {data_path}")
                        break
                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, "w") as file:
                        file.write(f"Validation status: {validation_status}")
                
                i += 1
                
            logger.info("Validation process of all columns in the data completed.")
            return validation_status
            
        except Exception as e:
            logger.error(f"Error in validating all columns: {e}")
            raise e