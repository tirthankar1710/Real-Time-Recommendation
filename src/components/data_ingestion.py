import pandas as pd

from src import logger
from src.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config=config
    
    def data_ingestion_flow(self):
        logger.info(f"path of jsonl file: {self.config.video_games_user}")
        logger.info(f"path of jsonl file: {self.config.video_games_item}")
        
        user_df = self.get_user_information()
        item_df = self.get_item_information()

        user_df.to_csv(self.config.user_df_output_path, index=False)
        item_df.to_csv(self.config.item_df_output_path, index=False)

    def get_user_information(self):
        chunk_size=500
        user_chunks = pd.read_json(self.config.video_games_user, lines=True, chunksize=chunk_size)
        user_chunks_list= list(user_chunks)
        # use the first x dataframes as configured in the user df number.
        user_df = pd.concat(user_chunks_list[:self.config.user_df_number], ignore_index=True)
        user_df.drop(columns=['images', 'timestamp', 'helpful_vote', 'verified_purchase','asin'], inplace=True)
        
        return user_df

    def get_item_information(self):
        chunk_size=500
        item_chunks = pd.read_json(self.config.video_games_item, lines=True, chunksize=chunk_size)
        item_chunks_list= list(item_chunks)
        # use the first x dataframes as configured in the user df number.
        item_df = pd.concat(item_chunks_list, ignore_index=True)
        item_df.drop(columns=['images', 'videos', 'store','bought_together','subtitle', 'author','details','price'], inplace=True)

        return item_df
        