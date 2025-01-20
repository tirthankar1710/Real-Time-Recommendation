from src import logger
from src.pipelines.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.pipelines.data_validation_pipeline import DataValidationTrainingPipeline
from src.pipelines.data_transformation_pipeline import DataTransformationTrainingPipeline
from src.pipelines.model_trainer_pipeline import ModelTrainerTrainingPipeline

# STAGE_NAME = "Data Ingestion Stage"
# try:
#    logger.info(f">>>>>> stage: {STAGE_NAME} started <<<<<<") 
#    data_ingestion = DataIngestionTrainingPipeline()
#    data_ingestion.initiate_data_ingestion()
#    logger.info(f">>>>>> stage: {STAGE_NAME} completed <<<<<<\n\nx==========x")
# except Exception as e:
#         logger.exception(e)
#         raise e

# STAGE_NAME = "Data Validation Stage"
# try:
#    logger.info(f">>>>>> stage: {STAGE_NAME} started <<<<<<") 
#    data_validation = DataValidationTrainingPipeline()
#    data_validation.initiate_data_validation()
#    logger.info(f">>>>>> stage: {STAGE_NAME} completed <<<<<<\n\nx==========x")
# except Exception as e:
#         logger.exception(e)
#         raise e

# STAGE_NAME = "Data Transformation Stage"
# try:
#    logger.info(f">>>>>> stage: {STAGE_NAME} started <<<<<<") 
#    data_transformation = DataTransformationTrainingPipeline()
#    data_transformation.initiate_data_transformation()
#    logger.info(f">>>>>> stage: {STAGE_NAME} completed <<<<<<\n\nx==========x")
# except Exception as e:
#         logger.exception(e)
#         raise e

STAGE_NAME = "Model Training Stage"
try:
   logger.info(f">>>>>> stage: {STAGE_NAME} started <<<<<<") 
   model_trainer = ModelTrainerTrainingPipeline()
   model_trainer.initiate_model_training()
   logger.info(f">>>>>> stage: {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e