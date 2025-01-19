from src import logger
from src.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config=config

    def read_jsonl_file(self):
        logger.info(f"path of jsonl file: {self.config.video_games_user}")
        logger.info(f"path of jsonl file: {self.config.video_games_item}")
        