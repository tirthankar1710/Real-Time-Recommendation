from src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.utils.common import read_yaml, create_directories
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, PredictionConfig

class ConfigurationManager:
    def __init__(self,
                 config_filepath=CONFIG_FILE_PATH,
                 params_filepath = PARAMS_FILE_PATH,
                 schema_filepath = SCHEMA_FILE_PATH):
        """
        Initializes the ConfigurationManager with paths to the configuration, parameters, and schema files.
        Reads the YAML files and creates the necessary directories for artifacts.

        Args:
            config_filepath (str): Path to the configuration file.
            params_filepath (str): Path to the parameters file.
            schema_filepath (str): Path to the schema file.
        """
        self.config=read_yaml(config_filepath)
        self.params=read_yaml(params_filepath)
        self.schema=read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion_config(self)-> DataIngestionConfig:
        """
        Retrieves the data ingestion configuration from the configuration file and creates necessary directories.

        Returns:
            DataIngestionConfig: Configuration object for data ingestion.
        """
        config=self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config=DataIngestionConfig(
            root_dir=config.root_dir,
            video_games_item=config.video_games_item,
            video_games_user=config.video_games_user,
            user_df_number=config.user_df_number,
            user_df_output_path=config.user_df_output_path,
            item_df_output_path=config.item_df_output_path
        )
        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        """
        Retrieves the data validation configuration from the configuration file and creates necessary directories.

        Returns:
            DataValidationConfig: Configuration object for data validation.
        """
        config = self.config.data_validation
        schema = self.schema.COLUMNS
        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            video_games_item = config.video_games_item,
            video_games_user = config.video_games_user,
            output=config.output,
            schema = schema
        )
        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        """
        Retrieves the data transformation configuration from the configuration file and creates necessary directories.

        Returns:
            DataTransformationConfig: Configuration object for data transformation.
        """
        config = self.config.data_transformation
        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            video_games_item = config.video_games_item,
            video_games_user = config.video_games_user,
            output_path_df=config.output_path_df,
            data_validation_status=config.data_validation_status
        )

        return data_transformation_config
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        """
        Retrieves the model trainer configuration from the configuration file and creates necessary directories.

        Returns:
            ModelTrainerConfig: Configuration object for model training.
        """
        config = self.config.model_trainer
        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir = config.root_dir,
            input_data  = config.input_data,
            model_path = config.model_path,
            cosine_sim = config.cosine_sim,
            indices_name = config.indices_name,
            content_df_path = config.content_df_path,
            user_feedback_path = config.user_feedback_path
        )

        return model_trainer_config
    
    def get_prediction_config(self) -> PredictionConfig:
        """
        Retrieves the prediction configuration from the configuration file.

        Returns:
            PredictionConfig: Configuration object for prediction.
        """
        config = self.config.prediction

        prediction_config = PredictionConfig(
                colab_model_path=  config.colab_model_path,
                cosine_sim_path = config.cosine_sim_path,
                indices_path = config.indices_path,
                content_df_path = config.content_df_path
        )

        return prediction_config