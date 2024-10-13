# Standard imports
import requests

#

# settings
from django.conf import settings

class AiDesignEngine:
    def __init__(self) -> None:
        self._stabilit_api_key = settings.STABILITY_API_KEY

    
    @property
    def model_parameters(self ):
        pass


    def _send_generation_request(self, host, params):
        """
        Private method to send a generation request to the AI API
        """
        headers: dict = {
            "Accept": "image/*",
            "Authorization": f"Bearer {self._stabilit_api_key}"
        }

        # Encode parameters
        files = {}
        image = params.pop("image", None)
        mask = params.pop("mask", None)
        if image is not None and image != '':
            files["image"] = open(image, 'rb')
        if mask is not None and mask != '':
            files["mask"] = open(mask, 'rb')
        if len(files)==0:
            files["none"] = ''

        # Send request
        print(f"Sending REST request to {host}...")
        response = requests.post(
            host,
            headers=headers,
            files=files,
            data=params
        )
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

        return response
        
        
    def generate_ai_design(self,
                            prompt: str,
                            negative_prompt: str,
                            seed: int,
                            stability_model: str,
                            aspect_ratio: str,
                            output_format: str,
                            mode: str,
                            sd3_model: str,
                            style_preset:str):
        """"
        Generates an AI design using the parameters and current AI model
        """
        pass


        
        