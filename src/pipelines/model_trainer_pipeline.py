import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

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

    def initiate_model_training(self):
        """
        Method to initiate the model training process.
        This method creates a ConfigurationManager instance, retrieves the model trainer configuration,
        creates a ModelTrainer instance with the configuration, and starts the model training flow.
        """
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.model_trainer_flow()

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainerTrainingPipeline()
        obj.initiate_data_transformation()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e