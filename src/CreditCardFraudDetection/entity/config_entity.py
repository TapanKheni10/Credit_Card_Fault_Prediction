from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class DataIngestionConfig:
    root_dir: Path
    local_data_path: List[str]