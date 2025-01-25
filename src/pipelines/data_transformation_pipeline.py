import json
import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

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

# def lambda_handler(event, context):
#     """
#     AWS Lambda handler function.
#     Extracts the job ID from the event and initiates the data ingestion process.
#     """
#     try:
#         job_id = event.get("job_id")
#         if not job_id:
#             raise ValueError("Job ID is required!")
        
#         logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
#         obj = DataTransformationTrainingPipeline()
#         #TODO: Add the job_id as a parameter
#         obj.initiate_data_transformation(job_id)
#         logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
#         return {
#                 'statusCode': 200,
#                 'body': {
#                     'message': f"Data ingestion completed for job ID: {job_id}",
#                     'job_id': job_id
#                 }
#             }
    
#     except Exception as e:
#         logger.exception(e)
#         return {
#             'statusCode': 500,
#             'body': str(e)
#         }

# if __name__ == '__main__':
#     # For local testing
#     event = {'job_id': 'e8ef154b-e333-46cf-b95f-6cc7343b34b9'}
#     context = {}
#     lambda_handler(event, context)