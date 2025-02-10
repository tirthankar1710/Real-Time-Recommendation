from ensure import ensure_annotations
import os
import pandas as pd
import numpy as np
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
        logger.exception(f"Error downloading file: {e}")
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
        logger.exception(f"Error uploading file: {e}")

def download_s3_folder(bucket_name, folder_prefix, local_dir):
    """
    Downloads only JSON files from a specific folder in an S3 bucket to a local directory.

    :param bucket_name: Name of the S3 bucket
    :param folder_prefix: Path of the folder (prefix) in S3, e.g., 'my-folder/'
    :param local_dir: Local directory to save downloaded files
    """
    s3_client = boto3.client('s3')

    # Ensure the prefix ends with '/' to list a "folder"
    if not folder_prefix.endswith('/'):
        folder_prefix += '/'

    paginator = s3_client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=folder_prefix)

    # Create local directory if it doesn't exist
    os.makedirs(local_dir, exist_ok=True)

    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                s3_key = obj['Key']  # Full path in S3
                if "json" in s3_key:
                    file_name = s3_key[len(folder_prefix):]  # Extract relative file path
                    local_file_path = os.path.join(local_dir, file_name)

                    # Ensure subdirectories are created
                    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

                    s3_client.download_file(bucket_name, s3_key, local_file_path)

    logger.info("User feedback downloaded!!")

def read_json_files_to_dataframe(folder_path):
    """
    Reads all JSON files in a folder and converts them to a single DataFrame.

    Args:
        folder_path (str): The path to the folder containing JSON files.

    Returns:
        pd.DataFrame: A DataFrame containing the data from all JSON files.
    """
    # List all JSON files in the folder
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]


    # Read each JSON file into a DataFrame and append to the list
    json_list = []
    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)
        json_df = pd.read_json(file_path)
        json_list.append(json_df)
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(json_list, ignore_index=True)
    combined_df = combined_df.astype(np.int64)
    combined_df = combined_df.rename(
        columns={"product_id": "parent_asin",
            "feedback": "rating"}
    )
    return combined_df