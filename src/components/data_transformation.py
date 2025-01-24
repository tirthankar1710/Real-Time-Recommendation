import pandas as pd

from src import logger
from src.entity.config_entity import DataTransformationConfig
from src.utils.common import download_file_from_s3, upload_file_to_s3

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
    
    def data_transformation_flow(self):

        download_file_from_s3(
            bucket_name="ml-recommendation-capstone",
            file_name=""
        )


        user_df = pd.read_csv(self.config.video_games_user)
        item_df = pd.read_csv(self.config.video_games_item)
        merged_df_weight = self.prepare_merged_df(user_df=user_df, item_df=item_df)
        logger.info(f"shape of merged_df_weight: {merged_df_weight.shape}")

        merged_df_weight.to_csv(self.config.output_path_df, index=False)
        
        return merged_df_weight

   
    def prepare_merged_df(self, user_df, item_df):
        # Merging the two columns on the product id
        merged_df = pd.merge(user_df, item_df, on='parent_asin', how='inner')
        categories_to_keep = ['Video Games', 'Computers', 'All Electronics']
        merged_df = merged_df[merged_df['main_category'].isin(categories_to_keep)]

        # Converting them from list of strings to one string.
        merged_df['features'] = merged_df['features'].apply(lambda x: " ".join(x))
        merged_df['description'] = merged_df['description'].apply(lambda x: " ".join(x))
        merged_df['categories'] = merged_df['categories'].apply(lambda x: " ".join(x))

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
        q1 = df['rating_number'].quantile(0.25)
        q3 = df['rating_number'].quantile(0.75)
        IQR = q3 - q1
        lower_bound = q1 - 1.5 * IQR
        upper_bound = q3 +1.5 * IQR
        # Removing the outliers
        merged_df = df[(df['rating_number']>=lower_bound) & (df['rating_number']<=upper_bound)]
        
        return merged_df
    
    def create_weighted_ratings(self, df):
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
        