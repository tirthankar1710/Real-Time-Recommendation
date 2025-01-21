import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src import logger
from src.config.configuration import ConfigurationManager
from src.components.data_validation import DataValidation

STAGE_NAME = "Data Validation stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        """
        Constructor for the DataValidationTrainingPipeline class.
        Initializes any required attributes.
        """
        pass

    def initiate_data_validation(self):
        """
        Method to initiate the data validation process.
        This method creates a ConfigurationManager instance, retrieves the data validation configuration,
        creates a DataValidation instance with the configuration, and runs the validation rules.
        It returns the validation status.
        """
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        validation_status = data_validation.validation_rules()

        return validation_status

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataValidationTrainingPipeline()
        obj.initiate_data_validation()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e