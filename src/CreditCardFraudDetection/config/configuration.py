from CreditCardFraudDetection.constants import (
    PARAMS_YAML_FILE_PATH, CONFIG_YAML_FILE_PATH, SCHEMA_YAML_FILE_PATH,
    MONGO_DB_URL, MONGO_DB_DATABASE_NAME, MONGO_DB_COLLECTION_NAME)
from CreditCardFraudDetection.utils.common import read_yaml, create_directories
from CreditCardFraudDetection.entity import config_entity
from pathlib import Path

class ConfigurationManager:
    def __init__(self,
                 params_yaml_file_path = PARAMS_YAML_FILE_PATH,
                 config_yaml_file_path = CONFIG_YAML_FILE_PATH,
                 schema_yaml_file_path = SCHEMA_YAML_FILE_PATH):
        
        self.params = read_yaml(params_yaml_file_path)
        self.config = read_yaml(config_yaml_file_path)
        self.schema = read_yaml(schema_yaml_file_path)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> config_entity.DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        return config_entity.DataIngestionConfig(
            root_dir=Path(config.root_dir),
            local_data_path=config.local_data_path
        )
    
    def get_data_validation_config(self) -> config_entity.DataValidationConfig:
        config = self.config.data_validation
        schema = [self.schema.COLUMNS_DATA1, self.schema.COLUMNS_DATA2]

        create_directories([config.root_dir])

        return config_entity.DataValidationConfig(
            root_dir = Path(config.root_dir),
            local_data_path = config.local_data_path,
            STATUS_FILE = config.STATUS_FILE,
            all_schema = schema
        )