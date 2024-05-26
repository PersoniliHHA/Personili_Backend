import boto3
import os
from datetime import datetime, timedelta

class IamEngine:
    """
    Class to handle IAM roles and users configuration
    """

    def __init__(self, environment: str = "dev", 
                       session_name: str = "LocalSession", 
                       role_name: str="AWS_DEV_BACK_ROLE_ARN") -> None:
        
        self.session_name = session_name
        self.environment = environment
        self.sts_session_validity_duration = os.environ.get("STS_SESSION_VALIDITY_DURATION")

        self.role_name = role_name
        self.role_arn = os.environ.get(self.role_name)
        

    def get_iam_user_client(self):
        """
        This method returns a boto3 client for IAM using the credentials in the env variables
        """
        return boto3.client(
            "sts",
            aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY"), 
        )

    def assume_iam_role(self) -> dict:
        """
        This method is used to assume an IAM role and return the credentials
        """
        sts_client = self.get_iam_user_client()
        response = sts_client.assume_role(
            RoleArn = self.role_arn,
            RoleSessionName = self.session_name,
            DurationSeconds = self.sts_session_validity_duration
        )
        # Get the credentials
        credentials = response.get("Credentials")
        # Update the temporary credentials env variables
        os.environ["TEMP_AWS_ACCESS_KEY_ID"] = credentials.get("AccessKeyId")
        os.environ["TEMP_AWS_SECRET"] = credentials.get("SecretAccessKey")
        os.environ["TEMP_AWS_SESSION_TOKEN"] = credentials.get("SessionToken")
        os.environ["STS_SESSION_EXPIRATION_TIME"] = datetime.now() + timedelta(seconds=int(self.sts_session_validity_duration))

        return response['Credentials']
    
    def get_sts_session(self) -> boto3.Session:
        """
        This method is used to get an STS session
        """
        # First check if the temporary credentials already exists
        if (not os.environ.get("TEMP_AWS_ACCESS_KEY_ID") or not os.environ.get("TEMP_AWS_SECRET") or not os.environ.get("TEMP_AWS_SESSION_TOKEN")):
            credentials: dict = self.assume_iam_role()
        else:
            # Check if the temporary credentials haven't expired
            expiration_time = os.environ.get("TEMP_AWS_EXPIRATION_TIME")
            if expiration_time < datetime.now():
                credentials: dict = self.assume_iam_role()
            else:
                credentials = {
                    "AccessKeyId": os.environ.get("TEMP_AWS_ACCESS_KEY_ID"),
                    "SecretAccessKey": os.environ.get("TEMP_AWS_SECRET"),
                    "SessionToken": os.environ.get("TEMP_AWS_SESSION_TOKEN")
                }
        
        # Generate the sts session using the temporary credentials
        return boto3.Session(
            aws_access_key_id = credentials.get('AccessKeyId'),
            aws_secret_access_key = credentials.get('SecretAccessKey'),
            aws_session_token = credentials.get('SessionToken')
        )