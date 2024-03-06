"""
design images
design previews
product previews

"""
# Constants for image path prefixes and suffixes in the S3 bucket
WORKSHOP_IMAGES_PATH_PREFIX = {
    'designs_images': 'admin/designs/',
    'stores_images': 'admin/stores/',
    'events_images': 'admin/events/',
    'promotions_images': 'admin/promotions/',
}
# Designer uploaded images for designs and stores
DESIGNER_UPLOADED_IMAGES_PATH_TEMPLATES = {
    'uploaded_designs': 'designer_uploaded_images/designs/{designer_id}-{designer_email}/{collection_id}-{collection_title}/{design_id}-{design_title}',
    'store': 'designer_uploaded_images/stores/{designer_id-designer_email}/store/',
}

# User uploaded images
USER_UPLOADED_PROFILE_IMAGES_PATH_PREFIX = {
    'profile_pictures': 'images/user/profile_pictures/{user_profile}-{user_email}',
}

# Personalizable zones
PERSONALIZABLES_IMAGES_PATH_PREFIX = {
    'personalizables': 'images/personalizables/{personalizable_id}-{personalizable_name}/{personalizable_zone_id}-{personalizable_zone_name}',
}

# Personalization methods
PERSONALIZATION_METHODS_IMAGES_PATH_PREFIX = {
'personalization_methods': 'images/personalization_methods/{personalization_method_id}-{personalization_method_name}',
}


# Categories
CATEGORIES_IMAGES_PATH_PREFIX = {
'icons': 'images/categories/icons/{category_id}-{category_name}',
'images': 'images/categories/images/{category_id}-{category_name}',
}


ADMIN_UPLOADED_IMAGES_PATH_PREFIX = {
    'designs_images': 'images/admin/designs/',
    'stores_images': 'images/admin/stores/',
    'events_images': 'images/admin/events/',
    'promotions_images': 'images/admin/promotions/',
}





