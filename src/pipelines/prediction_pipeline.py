from surprise import dump
import pandas as pd
import numpy as np
from src.config.configuration import ConfigurationManager


class PredictionPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.config = self.config_manager.get_prediction_config()
        self._, self.model = dump.load(self.config.colab_model_path)
        self.cosine_sim = np.load(self.config.cosine_sim_path)
        self.indices = pd.read_pickle(self.config.indices_path)
        self.content_df = pd.read_csv(self.config.content_df_path)

    def get_hybrid_recommendations(self, user_id, parent_asin):
        """
        Using both 
        """
        # print(self.indices)
        idx = self.indices[parent_asin]
        idx = idx
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:31]
        product_indices = [i[0] for i in sim_scores]
        products = self.content_df.iloc[product_indices][['title_y', 'parent_asin']]
        products['estimate'] = 0
        def estimate_product(row):
            product = row['parent_asin']
            row['estimate'] = self.model.predict(uid=user_id, iid=product).est
            return row

        products = products.apply(estimate_product, axis=1)
        products = products.sort_values('estimate', ascending=False)
        
        return products.head()

    
