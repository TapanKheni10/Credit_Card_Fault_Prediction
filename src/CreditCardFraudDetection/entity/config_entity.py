from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    local_data_path: List[str]

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    local_data_path: List[str]
    STATUS_FILE: str
    all_schema: List[dict]

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: List[str]
    preprocessed_data_path: List[str]
    preprocessor_name: str

@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    x_train_data_path: List[str]
    y_train_data_path: List[str]
    x_val_data_path: List[str]
    y_val_data_path: List[str]
    model_name: List[str]

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    model_path: List[str]
    x_test_data_path: List[str]
    y_test_data_path: List[str]
    evaluation_report: List[str]