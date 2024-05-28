import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
import os

class BrevoService:
    def __init__(self):
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key['api-key'] = settings.BREVO_API_KEY
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))
   
    def send_email(self, to_email: str=None, subject: str =None, template_name=None, from_email='contact@personili.com', from_name='Personili support team'):
        
        # The templates folder
        template_folder = os.path.join(os.getcwd(), "templates")
        # The template file
        template_file = os.path.join(template_folder, f"{template_name}.html")

        # Check if the template file exists
        if not os.path.isfile(template_file):
            print(f"Template file {template_file} not found")
            return None

        # Read the content of template
        with open(template_file, "r") as f:
            html_content = f.read()

        # Send the actual email
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to_email}],
            sender={"email": from_email, "name": from_name},
            subject=subject,
            html_content=html_content
        )
        try:
            api_response = self.api_instance.send_transac_email(send_smtp_email)
            return api_response
        except ApiException as e:
            print(f"Exception when calling SMTPApi->send_transac_email: {e}\n")
            return None
        

brevo_engine = BrevoService()