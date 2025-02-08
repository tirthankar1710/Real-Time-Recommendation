# import sys
import argparse
from src import logger
from src.pipelines.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.pipelines.data_validation_pipeline import DataValidationTrainingPipeline
from src.pipelines.data_transformation_pipeline import DataTransformationTrainingPipeline
from src.pipelines.model_trainer_pipeline import ModelTrainerTrainingPipeline

def run_stage(stage_name, job_id):
    if stage_name == "ingestion_stage":
        try:
            logger.info(f">>>>>> stage: {stage_name} started <<<<<<") 
            data_ingestion = DataIngestionTrainingPipeline()
            data_ingestion.initiate_data_ingestion(job_id=job_id)
            logger.info(f">>>>>> stage: {stage_name} completed <<<<<<\n\nx==========x")
        except Exception as e:
            logger.exception(e)
            raise e

    elif stage_name == "validation_stage":
        try:
            logger.info(f">>>>>> stage: {stage_name} started <<<<<<") 
            data_validation = DataValidationTrainingPipeline()
            data_validation.initiate_data_validation(job_id=job_id)
            logger.info(f">>>>>> stage: {stage_name} completed <<<<<<\n\nx==========x")
        except Exception as e:
            logger.exception(e)
            raise e

    elif stage_name == "transformation_stage":
        try:
            logger.info(f">>>>>> stage: {stage_name} started <<<<<<") 
            data_transformation = DataTransformationTrainingPipeline()
            data_transformation.initiate_data_transformation(job_id=job_id)
            logger.info(f">>>>>> stage: {stage_name} completed <<<<<<\n\nx==========x")
        except Exception as e:
            logger.exception(e)
            raise e

    elif stage_name == "training_stage":
        try:
            logger.info(f">>>>>> stage: {stage_name} started <<<<<<") 
            model_trainer = ModelTrainerTrainingPipeline()
            model_trainer.initiate_model_training(job_id=job_id)
            logger.info(f">>>>>> stage: {stage_name} completed <<<<<<\n\nx==========x")
        except Exception as e:
            logger.exception(e)
            raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage_name", type=str, required=True, help="Name of the processing stage")
    parser.add_argument("--job_id", type=str, required=True, help="Job ID for tracking purposes")
    args = parser.parse_args()
    stage_name = args.stage_name
    job_id = args.job_id
    if stage_name == "all":
        stages = ["ingestion_stage", "validation_stage", "transformation_stage", "training_stage"]
        for stage_name in stages:
            run_stage(stage_name, job_id=job_id)
    else:
        run_stage(stage_name, job_id=job_id)