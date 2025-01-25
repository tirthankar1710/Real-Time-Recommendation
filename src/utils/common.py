from ensure import ensure_annotations
import os
from pathlib import Path
from box import ConfigBox
from box.exceptions import BoxValueError
import yaml
import boto3
from dotenv import load_dotenv

from src import logger

# Load environment variables from .env file
load_dotenv()

# Initialize a session using credentials from environment variables
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    # aws_session_token=os.getenv('AWS_SESSION_TOKEN')
)

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")

def download_file_from_s3(bucket_name:str, file_name:str, download_path:str, job_id:str=None, folder_name:str=None,):
    """
    Downloads a file from an S3 bucket inside a folder named after the job ID,
    which contains another folder named after the folder name.

    Args:
        bucket_name (str): The name of the S3 bucket.
        job_id (str): The job ID used as the parent folder name.
        folder_name (str): The folder name inside the job ID folder.
        file_name (str): The name of the file to be downloaded.
        download_path (str): The local path where the file will be saved.

    Returns:
        str: The local path to the downloaded file.
    """
    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # Construct the S3 object key
    if job_id:
        object_key = f"{job_id}/{folder_name}/{file_name}"
    else:
        object_key = f"{file_name}"

    try:
        # object_key = 
        # Download the file from S3
        logger.info(f"starting to download: {object_key}")
        s3_client.download_file(bucket_name, object_key, f"{download_path}")
        logger.info(f"File {file_name} downloaded from s3://{bucket_name}/{object_key} to {download_path}")

        # Return the local path to the downloaded file
        return download_path
    except Exception as e:
        print(f"Error downloading file: {e}")
        raise

def upload_file_to_s3(file_path, bucket_name, job_id, folder_name):
    """
    Uploads a file to an S3 bucket inside a folder named after the job ID,
    which contains another folder named after the folder name.

    Args:
        file_path (str): The path to the file to be uploaded.
        bucket_name (str): The name of the S3 bucket.
        job_id (str): The job ID to be used as the parent folder name.
        folder_name (str): The folder name inside the job ID folder.

    Returns:
        str: The S3 object URL.
    """
    # Initialize the S3 client
    s3_client = boto3.client('s3')

    # Construct the S3 object key
    object_key = f"{job_id}/{folder_name}/{os.path.basename(file_path)}"

    try:
        logger.info(f"starting to upload: {object_key}")
        # Upload the file to S3
        s3_client.upload_file(file_path, bucket_name, object_key)
        logger.info(f"File {file_path} uploaded to s3://{bucket_name}/{object_key}")

        # Return the S3 object URL
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
        return s3_url
    except Exception as e:
        print(f"Error uploading file: {e}")
        raise