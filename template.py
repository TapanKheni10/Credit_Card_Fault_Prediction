import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]:[%(message)s]')

project_name = 'CreditCardFraudDetection'

## There are some list of the files that we need
list_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "upload_data_to_DB.py",
    "main.py",
    "app.py",
    "research/trails.py",
    "research/01_data_ingestion.ipynb",
    "research/02_data_validation.ipynb",
    "research/03_data_preprocessing.ipynb",
    "research/04_model_trainer.ipynb",
    "research/05_model_evaluation.ipynb",
]

for filepath in list_of_files:
    filepath = Path(filepath)

    ## Getting the directory path and filename
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating an empty file: {filepath}")

    else:
        logging.info(f"{filename} file is already exist. No need to create it.")