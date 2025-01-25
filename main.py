import sys
from src import logger
from src.pipelines.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.pipelines.data_validation_pipeline import DataValidationTrainingPipeline
from src.pipelines.data_transformation_pipeline import DataTransformationTrainingPipeline
# from src.pipelines.model_trainer_pipeline import ModelTrainerTrainingPipeline

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

    # elif stage_name == "training_stage":
    #     try:
    #         logger.info(f">>>>>> stage: {stage_name} started <<<<<<") 
    #         model_trainer = ModelTrainerTrainingPipeline()
    #         model_trainer.initiate_model_training(job_id=job_id)
    #         logger.info(f">>>>>> stage: {stage_name} completed <<<<<<\n\nx==========x")
    #     except Exception as e:
    #         logger.exception(e)
    #         raise e

def lambda_handler(event, context):
    """
    AWS Lambda handler function.
    Extracts the stage and job_id from the event and runs the corresponding stage.
    """
    try:
        stage_name = event.get("stage")
        job_id = event.get("job_id")
        if not stage_name or not job_id:
            raise ValueError("Both stage name and job ID are required in the event")

        run_stage(stage_name, job_id)
        return {
            'statusCode': 200,
            'body': {
                'message': f"Stage {stage_name} completed successfully",
                'stage': stage_name,
                'job_id': job_id
            }
        }
    except Exception as e:
        logger.exception(e)
        return {
            'statusCode': 500,
            'body': {
                'message': str(e),
                'stage': stage_name if 'stage_name' in locals() else None,
                'job_id': job_id if 'job_id' in locals() else None
            }
        }

# if __name__ == "__main__":
#     stage = sys.argv[1]
#     if stage == "all":
#         stages = ["ingestion_stage", "validation_stage", "transformation_stage", "training_stage"]
#         for stage_name in stages:
#             run_stage(stage_name)
#     else:
#         run_stage(stage)

if __name__ == '__main__':
    # For local testing
    event = {'stage': 'validation_stage', 'job_id': 'test-job-id-from-local'}
    context = {}
    print(lambda_handler(event, context))