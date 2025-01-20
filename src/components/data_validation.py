from src import logger
import json
import pandas as pd
from src.entity.config_entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validation_rules(self):
        try:
            validation_status = None
            item_status = False
            user_status = False
            user_data = self.read_json_file(self.config.video_games_user)
            user_df = pd.DataFrame(user_data)
            user_column_length = len(user_df.columns)

            item_data = self.read_json_file(self.config.video_games_item)
            item_df = pd.DataFrame(item_data)
            item_column_length = len(item_df.columns)

            all_schema = self.config.schema.items()
            for key, value in all_schema:
                if key=='item':
                    if item_column_length==value:
                        item_status = True
                if key=='user':
                    if user_column_length==value:
                        user_status = True
            if user_status == True & item_status==True:
                validation_status = True
            else:
                validation_status = False
            validation = {"validation": validation_status}
            save_file_path = self.config.output
            
            with open(save_file_path, "w") as file:
                json.dump(validation, file, indent=4)
            
            logger.info(f"Length of the user df columns: {user_column_length}")
            logger.info(f"Length of the item df columns: {item_column_length}")

            logger.info(f"Validation Status: {validation_status}")

            
        except Exception as e:
            logger.error(e)
            raise e
    
    def read_json_file(self, file_path):
        data = []
        # Read the file line by line
        with open(file_path, 'r') as file:
            for i, line in enumerate(file):
                if i >= 10:  # Stop after 100 lines
                    break
                data.append(json.loads(line))  # Parse the JSON line and add to the list
        return data
