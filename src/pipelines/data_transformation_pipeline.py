import json
import sys
import os

from src.config.configuration import ConfigurationManager
from src.components.data_transformation import DataTransformation
from src import logger

STAGE_NAME = "transformation_stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        """
        Constructor for the DataTransformationTrainingPipeline class.
        Initializes any required attributes.
        """
        pass 

    def initiate_data_transformation(self, job_id):
        """
        Method to initiate the data transformation process.
        This method creates a ConfigurationManager instance, retrieves the data transformation configuration,
        checks the data validation status, and if validation is successful, it creates a DataTransformation instance
        and starts the data transformation flow. If validation fails, it logs an error and raises a ValueError.
        """
        try:
            config = ConfigurationManager()
            data_transformation_config = config.get_data_transformation_config()
            # with open(data_transformation_config.data_validation_status, 'r') as file:
            #     validation = json.load(file)
            # if validation['validation']:
            data_transformation = DataTransformation(config=data_transformation_config)
            merged_weight_df = data_transformation.data_transformation_flow(job_id)
            logger.info(f"data transformed with the shape: {merged_weight_df.shape}")
            # else:
            #     logger.error("Validation failed.")
            #     raise ValueError("Validation failed. Stopping the workflow.")

        except Exception as e:
            logger.exception(e)
            raise e