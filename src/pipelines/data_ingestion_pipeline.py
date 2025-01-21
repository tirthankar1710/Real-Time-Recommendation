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

    def initiate_data_ingestion(self):
        """
        Method to initiate the data ingestion process.
        This method creates a ConfigurationManager instance, retrieves the data ingestion configuration,
        creates a DataIngestion instance with the configuration, and starts the data ingestion flow.
        """
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.data_ingestion_flow()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.initiate_data_ingestion()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e