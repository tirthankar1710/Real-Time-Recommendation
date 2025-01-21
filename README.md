# Real Time Recommendation
MLOPS Project for Real Time Recommendation

# Source of data
Link: https://amazon-reviews-2023.github.io   
We have worked with the Video Games Dataset.

## Running the Main Script

The `main.py` script allows you to run different stages of the data pipeline. You can specify a particular stage to run or run all stages sequentially.

### Available Stages
- `ingestion_stage`: Runs the data ingestion pipeline.
- `validation_stage`: Runs the data validation pipeline.
- `transformation_stage`: Runs the data transformation pipeline.
- `training_stage`: Runs the model training pipeline.
- `all`: Runs all the stages sequentially.

### Running a Specific Stage

To run a specific stage, use the following command:

python main.py <stage_name>