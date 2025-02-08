import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# import os
# from surprise.builtin_datasets import get_dataset_dir
# from os.path import join

# # Monkey-patch the get_dataset_dir function
# def custom_get_dataset_dir():
#     return join('/tmp', '.surprise_data')  # Use /tmp for datasets in AWS Lambda

# # Override the original function
# get_dataset_dir.__code__ = custom_get_dataset_dir.__code__

from surprise import Reader, Dataset, SVD, accuracy
from surprise.model_selection import cross_validate, train_test_split, GridSearchCV
from surprise import dump

from src import logger
from src.entity.config_entity import ModelTrainerConfig
from src.utils.common import download_file_from_s3, upload_file_to_s3, download_s3_folder, read_json_files_to_dataframe

from sklearn.preprocessing import LabelEncoder


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
    
    def model_trainer_flow(self, job_id):
        
        download_file_from_s3(
            bucket_name="ml-recommendation-capstone",
            job_id=job_id,
            folder_name="data_transformation",
            file_name="merged_data_weight.csv",
            download_path=self.config.input_data
        )

        download_s3_folder(
            bucket_name="ml-recommendation-capstone",
            folder_prefix="user-feedback",
            local_dir=self.config.user_feedback_path
        )
        
        merged_df_weight = pd.read_csv(self.config.input_data)
        
        # Initialize LabelEncoder
        le_id = LabelEncoder()
        le_prod = LabelEncoder()
        merged_df_weight['parent_asin']= le_id.fit_transform(merged_df_weight['parent_asin'])
        merged_df_weight['user_id'] = le_prod.fit_transform(merged_df_weight['user_id'])

        self.get_cosine_similarity(df=merged_df_weight)
        self.get_svd_model(df=merged_df_weight)

        upload_file_to_s3(
            file_path=self.config.content_df_path,
            bucket_name="ml-recommendation-capstone",
            job_id=job_id,
            folder_name="model_trainer"
        )
        upload_file_to_s3(
            file_path=f'{self.config.root_dir}/{self.config.indices_name}',
            bucket_name="ml-recommendation-capstone",
            job_id=job_id,
            folder_name="model_trainer"
        )
        upload_file_to_s3(
            file_path=f'{self.config.root_dir}/{self.config.cosine_sim}',
            bucket_name="ml-recommendation-capstone",
            job_id=job_id,
            folder_name="model_trainer"
        )
        upload_file_to_s3(
            file_path=self.config.model_path,
            bucket_name="ml-recommendation-capstone",
            job_id=job_id,
            folder_name="model_trainer"
        )


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

        # return indices, cosine_sim, content_df

        logger.info("Content Filterting Files saved successfully after training.")
    
    def get_svd_model(self, df):
        logger.info("Collaborative filtering starting.")
        
        # Loading the user feedback 
        user_feedback_df = read_json_files_to_dataframe(self.config.user_feedback_path)
        df = pd.concat([df,user_feedback_df], ignore_index=True)

        # Filtering the dataframe based with the requirement
        min_rating = 5
        user_counts = df['user_id'].value_counts()
        colab_filter_df = df[df['user_id'].isin(user_counts[user_counts >= min_rating].index)]
        colab_filter_df = colab_filter_df.drop_duplicates(keep='first')

        reader = Reader(rating_scale=(1, 5))
        colab_data = Dataset.load_from_df(colab_filter_df[['user_id', 'parent_asin', 'rating']], reader)
        # Split dataset into train and test sets
        trainset, testset = train_test_split(colab_data, test_size=0.2, random_state=42)

        # TODO: Fetch the parameters from params.yaml
        param_grid = {
            "n_factors": [25, 40, 55],  # default 100
            "n_epochs": [10, 20],  # default 20
            "lr_all": [0.005, 0.025, 0.125],  # learning rate for all parameters. Default 0.005
            "reg_all": [0.08, 0.16, 0.32],  # regularization term for all parameters. Default 0.02
            "random_state": [0],
        }
        grid_search = GridSearchCV(
            SVD,
            param_grid,
            measures=["rmse", "mae"],
            cv=3,  # 5,
            refit=True,
            n_jobs=-1,
            joblib_verbose=2
        )
        logger.info("Training Start....")
        grid_search.fit(colab_data)
        logger.info("Training Completed")

        result_df = pd.DataFrame.from_dict(grid_search.cv_results)[[
            "mean_test_rmse", "mean_test_mae", "param_n_factors",
            "param_n_epochs", "param_lr_all", "param_reg_all"
        ]].sort_values("mean_test_rmse")

        best_model = grid_search.best_estimator["rmse"]

        dump.dump(self.config.model_path,algo=best_model)

        logger.info(f"Model saved with path: {self.config.model_path}")

