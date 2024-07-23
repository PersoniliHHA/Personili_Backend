from designs.models import Design
from accounts.models import AccountProfile, Account

# Settings
from django.conf import settings
from utils.aws.storage.s3_engine import s3_engine

# Standard Library
import requests
from uuid import uuid4 
#######################  DESIGNS MANAGEMENT  #######################

#######################  STORE MANAGEMENT  #########################

####################### DESIGNER PROFILE MANAGEMENT ################

#######################  COLLECTION MANAGEMENT  ####################


################################################# AI GENERATED DESIGNS ########################################################
################################################################################################################################
STABILITY_MODELS_CREDIT_MAPPING = {
    "Ultra": {
        "credit_per_image": 8,
        "base_url": "https://api.stability.ai/v2beta/stable-image/generate",
        "url_extension": "/ultra",
        "gems_cost": 5,
        "params": ["prompt", "negative_prompt", "seed", "aspect_ratio", "output_format"]
    },
    "Core": {
        "credit_per_image": 3,
        "base_url": "https://api.stability.ai/v2beta/stable-image/generate",
        "url_extension": "/core",
        "gems_cost": 3,
        "params": ["prompt", "negative_prompt", "seed", "aspect_ratio", "output_format", "style_preset"]
    },
    "SD4M": {
        "credit_per_image": 3.5,
        "base_url": "https://api.stability.ai/v2beta/stable-image/generate",
        "url_extension": "/sd3",
        "gems_cost": 3.5
    },
    "SD3L": {
        "credit_per_image": 6.5,
        "base_url": "https://api.stability.ai/v2beta/stable-image/generate",
        "url_extenion": "/sd3",

    },
    "SD3LT": {
        "credit_per_image": 4,
        "base_url": "https://api.stability.ai/v2beta/stable-image/generate",
        "url_extension": "/sd3",
    },
    "SDXL 1.0": {
        "credit_per_image": (0.2, 0.6),
        "base_url": "https://api.stability.ai/v2beta/stable-image/generate",
        "url_extension": "",
    },
    "SD 1.6": {
        "credit_per_image": (0.2, 1),
        "base_url": "https://api.stability.ai/v2beta/stable-image/generate",
        "url_extension": "",
    },
}


def send_generation_request(
    host,
    params,
):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {settings.STABILITY_API_KEY}"
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


def generate_ai_design_with_stability(account_profile_id: str, 
                                      for_store: bool = False, 
                                      for_user: bool = False, 
                                      for_workshop: bool = False,
                                      prompt: str=None,
                                      negative_prompt: str="",
                                      seed: int = 0,
                                      stability_model: str = "SDXL 1.0", 
                                      aspect_ratio: str="1:1",
                                      output_format: str="png",
                                      mode: str="text-to-image",
                                      sd3_model: str="",
                                      style_preset: str="3d-model"):
    """
    This function generates an AI design with the specified stability model
    """
    # First validate the parameters
    if not account_profile_id:
        raise ValueError("Account Profile ID is required")
    
    if stability_model not in STABILITY_MODELS_CREDIT_MAPPING:
        raise ValueError("Invalid stability model")
    
    # With XOR test that only one of the flags is set
    if not (for_store ^ for_user ^ for_workshop):
        raise ValueError("You can only generate a design for a store, user or workshop")
    
    if not prompt:
        raise ValueError("Prompt is required")
    
    if output_format not in ["png", "jpeg", "webp"]:
        raise ValueError("Invalid output format")
    
    if aspect_ratio not in ["16:9" ,"1:1", "21:9", "2:3", "3:2", "4:5", "5:4",  "9:16", "9:21"]:
        raise ValueError("Invalid aspect ratio")
    
    # Random seed should be between 0 and 4294967294 
    if seed and (not 0 <= seed <= 4294967294):
        raise ValueError("Invalid seed")
    
    # Construct arguments dict
    args = {
        "account_profile_id": account_profile_id,
        "for_store": for_store,
        "for_user": for_user,
        "for_workshop": for_workshop,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "seed": seed,
        "stability_model": stability_model,
        "aspect_ratio": aspect_ratio,
        "output_format": output_format,
        "mode": mode,
        "sd3_model": sd3_model,
        "style_preset": style_preset
    }
    
    # Get the account personili_gems balance
    available_gems: int = AccountProfile.objects.get(id=account_profile_id).personili_gems

    # Get the credit cost of the stability model
    credit_cost = STABILITY_MODELS_CREDIT_MAPPING[stability_model]["credit_per_image"]
    # Get the gems cost of the stability model
    gems_cost = STABILITY_MODELS_CREDIT_MAPPING[stability_model]["gems_cost"]

    # Check if the user has enough personili_gems
    if available_gems < gems_cost:
        raise ValueError("Insufficient personili_gems balance")

    # Get the list of parameters for the stability model
    params_list = STABILITY_MODELS_CREDIT_MAPPING[stability_model]["params"]
    # construct a params dict based on the params_list and the function arguments
    params = {}
    for param in params_list:
        if args[param]:
            params[param] = args[param]
    
    # Send the generation request
    response = send_generation_request(
        host=STABILITY_MODELS_CREDIT_MAPPING[stability_model]["base_url"] + STABILITY_MODELS_CREDIT_MAPPING[stability_model]["url_extension"],
        params=params
    )
    # Decode response
    output_image = response.content
    finish_reason = response.headers.get("finish-reason")
    seed = response.headers.get("seed")

    # Check for NSFW classification
    if finish_reason == 'CONTENT_FILTERED':
        raise Warning("Generation failed NSFW classifier")
    
    # Store the generated image in the s3 bucket
    account_email = AccountProfile.objects.get(id=account_profile_id).account.email
    s3_path = s3_engine.upload_file_to_s3(output_image, 
                'regular_user_designs', 
                {'regular_user_profile_id': account_profile_id,
                 'regular_user_email': account_email,
                 'design_id': str(uuid4()),
                 'design_title': prompt})
    
    # Deduct the personili_gems from the account
    account_profile = AccountProfile.objects.get(id=account_profile_id)
    account_profile.personili_gems -= gems_cost
    account_profile.save()

    # TODO: Store the design in the database

    # generate a signed url for the image
    signed_url = s3_engine.generate_presigned_s3_url(s3_path)

    

