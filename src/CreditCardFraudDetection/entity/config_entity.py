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