from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    video_games_item: Path
    video_games_user: Path
    user_df_number: dict
    user_df_output_path: Path
    item_df_output_path: Path

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
    data_validation_status: Path
    output_path_df:Path

@dataclass
class ModelTrainerConfig:
    root_dir: Path
    input_data: Path
    model_path: Path
    cosine_sim: str
    indices_name: str
    content_df_path: Path
    user_feedback_path: Path

@dataclass
class PredictionConfig:
    colab_model_path: Path
    cosine_sim_path: Path
    indices_path: Path
    content_df_path: Path