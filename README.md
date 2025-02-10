# Real Time Recommendation
MLOPS Project for Real Time Recommendation!

## Source of data
Link: https://amazon-reviews-2023.github.io   
We have worked with the Video Games Dataset.

## Running the Main Script

The `sagemaker_main.py` script allows you to run different stages of the data pipeline. You can specify a particular stage to run or run all stages sequentially.

### Available Stages
- `ingestion_stage`: Runs the data ingestion pipeline.
- `validation_stage`: Runs the data validation pipeline.
- `transformation_stage`: Runs the data transformation pipeline.
- `training_stage`: Runs the model training pipeline.
- `all`: Runs all the stages sequentially.

### Running a Specific Stage

To run a specific stage, use the following command:

python sagemaker_main.py <stage_name>

## Data Transformation Process  

The data transformation process prepares raw data for model training by performing the following steps:

- Data Download: Downloads user and item data from S3.
- Filtering: Filters items based on the number of ratings.
- Weighted Rating Calculation: Computes a weighted rating for each item to balance the average rating with the number of ratings.
- Cleanup: Removes unnecessary columns after transformation

## Model Training Process  

The model training process involves the following steps to build a collaborative filtering recommendation model:

- Data Loading: Loads user feedback data from JSON files and combines it with the input DataFrame.
- Filtering: Filters users with a minimum number of ratings to ensure sufficient data for training.
- Data Preparation: Prepares the data for training by creating a dataset suitable for the Surprise library.
- Model Training: Trains an SVD model using the Surprise library, performs hyperparameter tuning using GridSearchCV, and saves the trained model.