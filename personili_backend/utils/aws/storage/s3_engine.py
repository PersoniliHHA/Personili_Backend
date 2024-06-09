import boto3
from utils.aws.iam.iam_engine import IamEngine
from typing import List, Any, Optional
from django.core.files import File
import os


class S3Engine:
    """
    Class to generate S3 paths for different settings
    """
    base_path = "images"

    # Admin S3 paths
    # events
    # designs
    # stores
    # organizations
    # stores

    # Platfrom S3 paths
    base_platform_path = base_path + '/platform'
    # events
    platform_events_path_template = base_platform_path + '/events/{event_id}-{event_title}'
    # categories
    platform_categories_path_template = base_platform_path + '/categories/{category_id}-{category_name}'
    # departments
    platform_departments_path_template = base_platform_path + '/departments/{department_id}-{department_name}'


    # Regular user S3 paths
    base_regular_users_path = base_path + '/regular_users'
    
    # main account profile
    regular_user_profile_path_template = base_regular_users_path + '/{regular_user_profile_id}-{regular_user_email}/profile'
    
    # designs
    regular_user_designs_path_template = base_regular_users_path + '/{regular_user_profile_id}-{regular_user_email}/designs/{design_id}-{design_title}'


    # Designers S3 paths
    base_designers_path = base_path + '/designers'
    # store profile
    store_profile_path_template = base_designers_path + '/{designer_id}-{designer_email}/stores/{store_id}/store_profile'
    # design
    store_designs_path_template = base_designers_path + '/{designer_id}-{designer_email}/stores/{store_id}/designs/{design_id}-{design_title}'
    # store events
    store_events_path_template =  base_designers_path + '/{designer_id}-{designer_email}/stores/{store_id}/events/{event_id}-{event_title}'


    # Organizatioins S3 paths
    base_organizations_path = base_path + '/organizations'
    # organization profile
    organization_profile_path_template = base_organizations_path + '/{organization_id}-{organization_name}/organization_profile'
    # workshop profile
    workshop_profile_path_template = base_organizations_path + '/{organization_id}-{organization_name}/workshops/{workshop_id}-{workshop_title}/workshop_profile'
    # workshop events
    workshop_events_path_template = base_organizations_path + '/{organization_id}-{organization_name}/workshops/{workshop_id}-{workshop_title}/events/{event_id}-{event_title}'
    # workshop designs
    workshop_designs_path_template = base_organizations_path + '/{organization_id}-{organization_name}/workshops/{workshop_id}-{workshop_title}/designs/{design_id}-{design_title}'
    # workshop personalizables
    workshop_personalizables_path_template = base_organizations_path + '/{organization_id}-{organization_name}/workshops/{workshop_id}-{workshop_title}/personalizables/{personalizable_id}-{personalizable_name}'

    # ALL templates organized
    TEMPLATES: dict = {
        'regular_user_profile': regular_user_profile_path_template,
        'regular_user_designs': regular_user_designs_path_template,
        'store_profile': store_profile_path_template,
        'store_designs': store_designs_path_template,
        'store_events': store_events_path_template,
        'organization_profile': organization_profile_path_template,
        'workshop_profile': workshop_profile_path_template,
        'workshop_events': workshop_events_path_template,
        'workshop_designs': workshop_designs_path_template,
        'workshop_personalizables': workshop_personalizables_path_template
    }

    def __init__(self, environment: str= "dev"):
        self.environment = environment
        self.s3_client_session = IamEngine(environment=self.environment).get_sts_session().client('s3')
        self.bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")

    def refresh_sts_session(self):
        """
        Refresh the STS session
        """
        self.s3_client_session = IamEngine(environment=self.environment).get_sts_session().client('s3', region_name=os.environ.get("AWS_S3_REGION_NAME"))
    
    def upload_file_to_s3(self, file : File, template_name: str, placeholder_values:dict[str, Any]) -> str:
        """
        Upload a list of files to the S3 bucket, for each file return the presigned
        """
        # First construct the path
        s3_path: str = self.build_s3_path(template_name, placeholder_values)

        # add the file name to the path
        s3_path = s3_path + '/' + file.name

        try:
            # Upload the file
            self.s3_client_session.upload_fileobj(file, self.bucket_name, s3_path)
            # Return the presigned URL
            return s3_path
        except Exception as e:
            raise Exception(f"Error uploading file to S3: {e}")
    
    def delete_file_from_s3(self, s3_path: str):
        """
        Delete a file from S3
        """
        try:
            self.s3_client_session.delete_object(Bucket=self.bucket_name, Key=s3_path)
        except Exception as e:
            raise Exception(f"Error deleting file from S3: {e}")
    
    def build_s3_path(self, template_name:str = None,  placeholder_values: dict[str, Any]=None) -> str:
        """
        Build a path based on the template name and placeholder_values
        """
        if not template_name:
            raise ValueError("Template name is required")
        if not placeholder_values:
            raise ValueError("Placeholders are required")
        template = self.TEMPLATES.get(template_name)
        if not template:
            raise ValueError("Template name is invalid")
        return template.format(**placeholder_values)
    
    def generate_presigned_s3_url(self, s3_path: str, expiration: int = 60) -> str:
        """
        Generate a presigned URL for the S3 path
        """
        try:
            return self.s3_client_session.generate_presigned_url('get_object', Params={'Bucket': self.bucket_name, 'Key': s3_path}, ExpiresIn=expiration)
        except Exception as e:
            raise e(f"Error generating presigned URL: {e}")    


# Instantiate the class
s3_engine = S3Engine()