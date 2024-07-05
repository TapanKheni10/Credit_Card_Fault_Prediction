from pathlib import Path

PARAMS_YAML_FILE_PATH = Path("params.yaml")
SCHEMA_YAML_FILE_PATH = Path("schema.yaml")
CONFIG_YAML_FILE_PATH = Path("config/config.yaml")

MONGO_DB_URL = f"mongodb+srv://tapankheni:tapankheni@cluster0.blfohxj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB_DATABASE_NAME = "credit_card_fault_detection"
MONGO_DB_COLLECTION_NAME = ['fraudulent_transactions_data', 'default_credit_card_data']