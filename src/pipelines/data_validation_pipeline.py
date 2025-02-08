import sys
import os

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