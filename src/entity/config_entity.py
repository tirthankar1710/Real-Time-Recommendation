from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    video_games_item: Path
    video_games_user: Path

@dataclass
class DataValidationConfig:
    root_dir: Path
    video_games_item: Path
    video_games_user: Path
    output:Path
    schema:dict

@dataclass
class DataTransformationConfig:
    root_dir: Path
    video_games_item: Path
    video_games_user: Path
    user_df_number: dict
    data_validation_status: Path
    output_path_df:Path