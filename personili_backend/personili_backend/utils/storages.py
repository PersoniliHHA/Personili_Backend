# Standard library imports
from typing import List, Union, Dict

# Third party imports
import boto3

# Django imports
from django.urls import path, include

###################################
####         S3 File storage  #####
###################################
def store_images_in_bucket(files_and_paths: List[dict[str, Union[str, File]]]) -> List[str]:
    """
    Store a list of images in aws s3 bucket
    """

    # Create the s3 client
    s3_client = boto3.client("s3", region_name=settings.AWS_REGION_NAME)

    # Iterate over the list of files and paths
    for file_and_path in files_and_paths:
        # Get the file and the path
        file = file_and_path.get("file")
        file_path = file_and_path.get("file_path")

        # Store the file in s3
        s3_client.upload_fileobj(
            file,
            settings.AWS_S3_BUCKET_NAME,
            file_path,
        )


def store_image_in_s3(file, file_path) -> str:
    
    if not file or not file_path:
        return None
    
    image_url = None

    # Instantiate a storage
    media_storage = MediaStorage()
    # check that the file doesn already exist
    if not media_storage.exists(file_path):
        
        media_storage.save(file_path, file)
        image_url = media_storage.url(file_path)

    return image_url


def get_presigned_url_for_image(file_path: str):

    if not file_path:
        return None
    
    media_storage = MediaStorage()
    object_key = media_storage._normalize_name(file_path)
    image_url = media_storage.url(object_key)

    return image_url

    
