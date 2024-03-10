# Standard library imports
from typing import List, Union, Dict

# Third party imports
import boto3

# Django imports
from django.urls import path, include




###################################
####         S3 File storage  #####
###################################
def store_images_in_bucket(files_and_paths: List[dict[str, Union[str, str]]]) -> List[str]:
    """
    Store a list of images in aws s3 bucket
    """

    # Create the s3 client
    s3_client = boto3.client("s3", region_name="AWS_REGION_NAME")

    # Iterate over the list of files and paths
    for file_and_path in files_and_paths:
        # Get the file and the path
        file = file_and_path.get("file")
        file_path = file_and_path.get("file_path")

        # Store the file in s3
        s3_client.upload_fileobj(
            file,
            "AWS_S3_BUCKET_NAME",
            file_path,
        )

    
