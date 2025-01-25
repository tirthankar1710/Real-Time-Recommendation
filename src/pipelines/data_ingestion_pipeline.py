import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src import logger
from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion



STAGE_NAME="Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        """
        Constructor for the DataIngestionTrainingPipeline class.
        Initializes any required attributes.
        """
        pass

    def initiate_data_ingestion(self, job_id):
        """
        Method to initiate the data ingestion process.
        This method creates a ConfigurationManager instance, retrieves the data ingestion configuration,
        creates a DataIngestion instance with the configuration, and starts the data ingestion flow.
        """
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.data_ingestion_flow(job_id=job_id)

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    Extracts the job ID from the event and initiates the data ingestion process.
    """
    try:
        job_id = event.get("job_id")
        if not job_id:
            raise ValueError("Job ID is required!")
        
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        #TODO: Add the job_id as a parameter
        obj.initiate_data_ingestion(job_id)
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
        return {
                'statusCode': 200,
                'body': {
                    'message': f"Data ingestion completed for job ID: {job_id}",
                    'job_id': job_id
                }
            }
    except Exception as e:
        logger.exception(e)
        return {
            'statusCode': 500,
            'body': str(e)
        }

if __name__ == '__main__':
    # For local testing
    event = {'job_id': '123438954260589'}
    context = {}
    lambda_handler(event, context)