import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config.configuration import ConfigurationManager
from src.components.model_trainer import ModelTrainer
from src import logger

STAGE_NAME = "model_trainer"

class ModelTrainerTrainingPipeline:
    def __init__(self):
        """
        Constructor for the ModelTrainerTrainingPipeline class.
        Initializes any required attributes.
        """
        pass

    def initiate_model_training(self, job_id):
        """
        Method to initiate the model training process.
        This method creates a ConfigurationManager instance, retrieves the model trainer configuration,
        creates a ModelTrainer instance with the configuration, and starts the model training flow.
        """
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.model_trainer_flow(job_id)


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
#         obj = ModelTrainerTrainingPipeline()
#         obj.initiate_model_training(job_id)
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