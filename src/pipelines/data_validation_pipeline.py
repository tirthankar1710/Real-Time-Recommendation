import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src import logger
from src.config.configuration import ConfigurationManager
from src.components.data_validation import DataValidation

STAGE_NAME = "data_validation"

class DataValidationTrainingPipeline:
    def __init__(self):
        """
        Constructor for the DataValidationTrainingPipeline class.
        Initializes any required attributes.
        """
        pass

    def initiate_data_validation(self,job_id):
        """
        Method to initiate the data validation process.
        This method creates a ConfigurationManager instance, retrieves the data validation configuration,
        creates a DataValidation instance with the configuration, and runs the validation rules.
        It returns the validation status.
        """
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        validation_status = data_validation.validation_rules(job_id)

        if validation_status==False:
            logger.error("Validation Failed!")
            raise ValueError("validation failed")
        
        return validation_status

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
#         obj = DataValidationTrainingPipeline()
#         obj.initiate_data_validation(job_id)
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
#     event = {'job_id': 'test-job-id-1234'}
#     context = {}
#     lambda_handler(event, context)
