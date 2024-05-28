import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings

class BrevoService:
    def __init__(self):
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key['api-key'] = settings.BREVO_API_KEY
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))
   
    def send_email(self, to_email="heytem.boumaza@gmail.com", subject=None, html_content=None, from_email='contact@personili.com', from_name='Personili support team'):
        
        subject = 'Email Confirmation'
        html_content = '<p>Please confirm your email address by clicking the link below:</p>'
        
        
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