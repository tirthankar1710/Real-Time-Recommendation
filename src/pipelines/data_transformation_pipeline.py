import json

from src.config.configuration import ConfigurationManager
from src.components.data_transformation import DataTransformation
from src import logger

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass 

    def initiate_data_transformation(self):
        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            with open(data_transformation_config.data_validation_status, 'r') as file:
                validation = json.load(file)
            if validation['validation']:
                data_transformation = DataTransformation(config=data_transformation_config)
                merged_weight_df = data_transformation.data_transformation_flow()
                logger.info(f"data transformed with the shape: {merged_weight_df.shape}")
            else:
                logger.error("Validation failed.")
                raise ValueError("Validation failed. Stopping the workflow.")

        except Exception as e:
            logger.exception(e)
            raise e
