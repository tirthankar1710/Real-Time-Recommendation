import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

from src import logger
from src.entity.config_entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
    
    def model_trainer_flow(self):
        merged_df_weight = pd.read_csv(self.config.input_data)
        self.get_cosine_similarity(df=merged_df_weight)

    
    def get_cosine_similarity(self, df):
        selected_columns = ['user_id','parent_asin','main_category','title_y','features','description']
        content_df = df[selected_columns]
        # content_df['item_description'] = content_df['main_category'] + " " + content_df['title_y'] + " " + content_df['features'] + " " + content_df['description']
        content_df['item_description'] = (
            content_df['main_category'].fillna('') + " " +
            content_df['title_y'].fillna('') + " " +
            content_df['features'].fillna('') + " " +
            content_df['description'].fillna('')
        )
        content_df = content_df.drop_duplicates(subset=['parent_asin'], keep='first') 
        tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0.5, stop_words='english')
        logger.info(f"shape of content df: {content_df.shape}")

        # tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 1),min_df=0.5, stop_words='english')
        tfidf_matrix = tf.fit_transform(content_df['item_description'])
        
        logger.info("Starting calculation of cosine similarity")
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        logger.info("Cosine similarity calculated.")

        content_df = content_df.reset_index()
        titles = content_df['parent_asin']
        indices = pd.Series(content_df.index, index=content_df['parent_asin'])

        indices.to_pickle(f'{self.config.root_dir}/{self.config.indices_name}')
        np.save(f'{self.config.root_dir}/{self.config.cosine_sim}', cosine_sim)
        content_df.to_csv(self.config.content_df_path, index=False)

        logger.info("Files saved successfully after training.")
