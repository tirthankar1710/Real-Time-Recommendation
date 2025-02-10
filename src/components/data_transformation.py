import pandas as pd
import ast

from src import logger
from src.entity.config_entity import DataTransformationConfig
from src.utils.common import download_file_from_s3, upload_file_to_s3

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
       """
        Initializes the DataTransformation with the given configuration.

        Args:
            config (DataTransformationConfig): Configuration object containing paths and parameters.
        """
       self.config = config
    
    def data_transformation_flow(self, job_id):
        """
        Orchestrates the data transformation workflow.

        Downloads user and item data from S3, merges the data, removes outliers,
        calculates weighted ratings, and uploads the transformed data back to S3.

        Args:
            job_id (str): Job ID for tracking purposes.

        Returns:
            pd.DataFrame: The transformed DataFrame.
        """

        download_file_from_s3(
            bucket_name="ml-recommendation-capstone",
            job_id=job_id,
            folder_name='data_ingestion',
            file_name='user_df.csv',
            download_path=self.config.video_games_user
        )
        download_file_from_s3(
            bucket_name="ml-recommendation-capstone",
            job_id=job_id,
            folder_name='data_ingestion',
            file_name='item_df.csv',
            download_path=self.config.video_games_item
        )

        user_df = pd.read_csv(self.config.video_games_user)
        item_df = pd.read_csv(self.config.video_games_item)
        merged_df_weight = self.prepare_merged_df(user_df=user_df, item_df=item_df)
        logger.info(f"shape of merged_df_weight: {merged_df_weight.shape}")

        merged_df_weight.to_csv(self.config.output_path_df, index=False)

        upload_file_to_s3(
            file_path=self.config.output_path_df,
            bucket_name="ml-recommendation-capstone",
            job_id=job_id,
            folder_name='data_transformation'
        )
        
        return merged_df_weight

   
    def prepare_merged_df(self, user_df, item_df):
        """
        Merges user and item data, processes text fields, removes outliers, and calculates weighted ratings.

        Args:
            user_df (pd.DataFrame): DataFrame containing user data.
            item_df (pd.DataFrame): DataFrame containing item data.

        Returns:
            pd.DataFrame: The merged and processed DataFrame.
        """
        # Merging the two columns on the product id
        merged_df = pd.merge(user_df, item_df, on='parent_asin', how='inner')
        categories_to_keep = ['Video Games', 'Computers', 'All Electronics']
        merged_df = merged_df[merged_df['main_category'].isin(categories_to_keep)]

        def safe_join(x):
            if isinstance(x, str):  
                try:
                    x = ast.literal_eval(x)  # Convert string representation of list back to list
                except (ValueError, SyntaxError):
                    pass  # If it's not a list string, keep it as is
            return " ".join(x) if isinstance(x, list) else x

        # Converting them from list of strings to one string.
        merged_df['features'] = merged_df['features'].apply(safe_join)
        merged_df['description'] = merged_df['description'].apply(safe_join)
        merged_df['categories'] = merged_df['categories'].apply(safe_join)

        # converting the column to appropriate data type from object
        merged_df['title_x'] = merged_df['title_x'].astype(str)
        merged_df['text'] = merged_df['text'].astype(str)
        merged_df['main_category'] = merged_df['main_category'].astype(str)
        merged_df['title_y'] = merged_df['title_y'].astype(str)
        
        # Removing outliers
        merged_df = self.remove_outliers(df=merged_df)

        # Creating weighted ratings
        merged_df_weight = self.create_weighted_ratings(df=merged_df)

        return merged_df_weight

    def remove_outliers(self, df):
        """
        Removes outliers from the DataFrame based on the IQR method.

        Args:
            df (pd.DataFrame): DataFrame from which to remove outliers.

        Returns:
            pd.DataFrame: DataFrame with outliers removed.
        """
        q1 = df['rating_number'].quantile(0.25)
        q3 = df['rating_number'].quantile(0.75)
        IQR = q3 - q1
        lower_bound = q1 - 1.5 * IQR
        upper_bound = q3 +1.5 * IQR
        # Removing the outliers
        merged_df = df[(df['rating_number']>=lower_bound) & (df['rating_number']<=upper_bound)]
        
        return merged_df
    
    def create_weighted_ratings(self, df):
        """
        Calculates weighted ratings for items based on the number of ratings and average rating.

        Args:
            df (pd.DataFrame): DataFrame containing item ratings.

        Returns:
            pd.DataFrame: DataFrame with weighted ratings.
        """
        averages = df['average_rating']
        C = averages.mean() # mean of average rating
        rating_number=df['rating_number']
        m = rating_number.quantile(0.4)
        merged_df_weight = df[df['rating_number']>=m]
        
        def weighted_rating(x):
            v = x['rating_number']
            R = x['average_rating']
            return (v/(v+m) * R) + (m/(m+v) * C)
        
        merged_df_weight['weighted_rating'] = merged_df_weight.apply(weighted_rating, axis=1)
        merged_df_weight.drop(columns=['average_rating', 'rating_number'], inplace=True)

        return merged_df_weight
        