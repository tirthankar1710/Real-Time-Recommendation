import sys
import os

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