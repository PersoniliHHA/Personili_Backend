# Standard imports
import itertools
from typing import Tuple, List

from accounts.factories import AccountFactory, AccountProfileFactory, DeliveryAddressFactory, RoleFactory, PermissionFactory
import random
from random import randint
from organizations.factories import BusinessOwnerProfileFactory, OrganizationFactory, OrganizationMembershipFactory, OrganizationProfileFactory, WorkshopFactory, WorkshopMembershipFactory, InventoryFactory, InventoryItemFactory
from designs.factories import DesignPreviewFactory,ThemeFactory, DesignerProfileFactory, DesignFactory, StoreFactory, StoreProfileFactory, CollectionFactory
from personalizables.factories import CategoryFactory, DepartmentFactory, PersonalizableFactory, PersonalizableVariantFactory, PersonalizableVariantValueFactory, OptionFactory, OptionValueFactory, DesignedPersonalizableVariantFactory, DesignedPersonalizableZoneFactory, PersonalizableOptionFactory, PersonalizableZoneFactory, PersonalizationMethodFactory, PersonalizationTypeFactory
from personalizables.factories import DesignedZoneRelatedDesignFactory

# Import data
from personalizables.factories import CATEGORIES_LIST, DEPARTMENTS_LIST, OPTIONS_AND_VALUES, generate_random_shape

# factory boy imports
import factory
from factory import Faker
from django.db import transaction

def create_roles_and_permissions():
    """
    Create the roles
    """
    roles = [
        {
         "name": "Regular User",
         "description": "This is the default role for every user",
         "permissions":
            [
                {
                    "name": "CRUD main account",
                    "description": "Can view account"
                },
                {
                    "name": "CRUD account profile",
                    "description": "Can view account profile"
                },
                {
                    "name": "CRUD delivery address",
                    "description": "Can view delivery address"
                },

            ]
        },
        {
        "name": "Designer",
        "description": "This role is for designers",
        "permissions" :
            [
                {
                    "name": "CRUD designer profile",
                    "description": "Can view designer profile"
                },
                {
                    "name": "CRUD store",
                    "description": "Can view store"
                },
                {
                    "name": "CRUD store profile",
                    "description": "Can view store profile"
                },
                {
                    "name": "CRUD collection",
                    "description": "Can view collection"
                },
                {
                    "name": "CRUD design",
                    "description": "Can view design"
                },
            ]
        },
        {
        "name": "Business Owner",
        "description": "This role is for business owners",
        },
        {
        "name": "Admin",
        "description": "This role is for admins",
        },
        {
        "name": "Superuser",
        "description": "This role is for superusers",
        },
        {
        "name": "Staff",
        "description": "This role is for staff",
        },
        {
        "name": "Customer Service",
        "description": "This role is for customer service",
        },
        {
        "name": "Workshop manager",
        "description": "This role is for workshop managers",
        },
        {
        "name": "Workshop employer",
        "description": "This role is for workshop employers",
        },
        {
        "name": "Organization manager",
        "description": "This role is for organization managers",

        }
    ]

    for role in roles:
        if role.get("name") == "Regular User" or role.get("name") == "Designer":
            
            permission_list = []
            for permission in role.get("permissions"):
                permission_list.append(PermissionFactory(name=permission["name"], description=permission["description"]))
            
            RoleFactory(name=role["name"], description=role["description"]).permissions.set(permission_list)
                
def create_design_themes():
    """
    Create the themes
    """
    list_of_themes = [
        {
            "name": "Modern",
            "description": "This theme is modern",
            "icon_1_path": Faker("image_url"),
            "icon_2_path": Faker("image_url"),
            "icon_3_path": Faker("image_url"),
        },
        {
            "name": "Classic",
            "description": "This theme is classic",
            "icon_1_path": Faker("image_url"),
            "icon_2_path": Faker("image_url"),
            "icon_3_path": Faker("image_url"),
        },
        {
            "name": "Vintage",
            "description": "This theme is vintage",
            "icon_1_path": Faker("image_url"),
            "icon_2_path": Faker("image_url"),
            "icon_3_path": Faker("image_url"),
        },
        {
            "name": "Retro",
            "description": "This theme is retro",
            "icon_1_path": Faker("image_url"),
            "icon_2_path": Faker("image_url"),
            "icon_3_path": Faker("image_url"),
        },
        {
            "name": "Contemporary",
            "description": "This theme is contemporary",
            "icon_1_path": Faker("image_url"),
            "icon_2_path": Faker("image_url"),
            "icon_3_path": Faker("image_url"),
        },
        {
            "name": "Minimalist",
            "description": "This theme is minimalist",
            "icon_1_path": Faker("image_url"),
            "icon_2_path": Faker("image_url"),
            "icon_3_path": Faker("image_url"),
        },
        {
            "name": "Futuristic",
            "description": "This theme is futuristic",
            "icon_1_path": Faker("image_url"),
            "icon_2_path": Faker("image_url"),
            "icon_3_path": Faker("image_url"),
        },
        {
            "name": "Industrial",
            "description": "This theme is industrial",
            "icon_1_path": Faker("image_url"),
            "icon_2_path": Faker("image_url"),
            "icon_3_path": Faker("image_url"),
        },
        {
            "name": "Anime",
            "description": "This theme is Anime",
            "icon_1_path": Faker("image_url"),
            "icon_2_path": Faker("image_url"),
            "icon_3_path": Faker("image_url"),
        },

    ]
    theme_instances = []
    for theme in list_of_themes:
        theme_instances.append(
        ThemeFactory(name=theme["name"], 
                     description=theme["description"], 
                     icon_1_path=theme["icon_1_path"], 
                     icon_2_path=theme["icon_2_path"], 
                     icon_3_path=theme["icon_3_path"]))
    
    return theme_instances

@transaction.atomic
def create_leaf_categories(data, parent=None):
    """

    """
    category = CategoryFactory(name=data["name"], 
                               description=data["description"], 
                               parent_category=parent)

    leaf_categories = []
    if not data.get("sub_categories"):
        leaf_categories.append(category)
    else:
        for sub_category in data["sub_categories"]:
            leaf_categories.extend(create_leaf_categories(sub_category, category))
    
    return leaf_categories

def create_categories():
    """
    Create the categories
    """
    leaf_categories = []
    for category in CATEGORIES_LIST:
        leaf_categories.extend(create_leaf_categories(category))
    
    return leaf_categories

def create_departments():
    """
    create departments
    """
    # Create the departements
    departement_instances = []
    for department in DEPARTMENTS_LIST:
        departement_instances.append(DepartmentFactory(name=department["name"], description=department["description"]))
    
    return departement_instances

def generate_design_usage_parmaters(is_regular_user: bool, 
                                    is_designer: bool, 
                                    is_business_owner: bool):
    """
    Generate the design usage parameters
    """
    parameters = {}
    if is_regular_user:
        base_price = 0
        sponsored = False
        free_usage = True
        latest_publication_date = None
        to_be_published = False
        parameters["base_price"] = base_price
        parameters["sponsored"] = sponsored
        parameters["free_usage"] = free_usage
        parameters["exclusive_usage"] = False
        parameters["limited_usage_with_designer_uploads"] = False
        parameters["limited_usage_with_user_uploads"] = False
        parameters["limited_usage_with_other_workshops"] = False
        parameters["limited_usage_with_other_organizations"] = False
        parameters["limited_usage_with_same_collection"] = False
        parameters["limited_usage_with_same_workshop"] = False
        parameters["limited_usage_with_same_organization"] = False
        parameters["latest_publication_date"] = latest_publication_date
        parameters["to_be_published"] = to_be_published

    else:
        free_usage = randint(0, 1) < 0.5
        exclusive_usage = randint(0, 1) < 0.5
        sponsored = randint(0, 1) < 0.5
        base_price = round(random.uniform(0, 999999), 2)
        latest_publication_date = Faker('date')
        to_be_published = randint(0, 1) < 0.9
        parameters["free_usage"] = free_usage
        parameters["exclusive_usage"] = exclusive_usage
        parameters["sponsored"] = sponsored
        parameters["base_price"] = base_price
        parameters["latest_publication_date"] = latest_publication_date
        parameters["to_be_published"] = to_be_published

        if exclusive_usage:
            free_usage = False
            limited_usage_with_designer_uploads = False
            limited_usage_with_user_uploads = False
            limited_usage_with_other_workshops = False
            limited_usage_with_other_organizations = False
            limited_usage_with_same_collection = False
            limited_usage_with_same_workshop = False
            limited_usage_with_same_organization = False

        elif free_usage:
            exclusive_usage = False
            limited_usage_with_designer_uploads = False
            limited_usage_with_user_uploads = False
            limited_usage_with_other_workshops = False
            limited_usage_with_other_organizations = False
            limited_usage_with_same_collection = False
            limited_usage_with_same_workshop = False
            limited_usage_with_same_organization = False

        else:
            limited_usage_with_same_collection = randint(0, 1) < 0.9
            limited_usage_with_same_workshop = randint(0, 1) < 0.5
            limited_usage_with_same_organization = randint(0, 1) < 0.9
            limited_usage_with_designer_uploads = randint(0, 1) < 0.9
            limited_usage_with_user_uploads = randint(0, 1) < 0.5
            limited_usage_with_other_workshops = randint(0, 1) < 0.9
            limited_usage_with_other_organizations = randint(0, 1) < 0.5
        
        parameters["limited_usage_with_same_collection"] = limited_usage_with_same_collection
        parameters["limited_usage_with_same_workshop"] = limited_usage_with_same_workshop
        parameters["limited_usage_with_same_organization"] = limited_usage_with_same_organization
        parameters["limited_usage_with_designer_uploads"] = limited_usage_with_designer_uploads
        parameters["limited_usage_with_user_uploads"] = limited_usage_with_user_uploads
        parameters["limited_usage_with_other_workshops"] = limited_usage_with_other_workshops
        parameters["limited_usage_with_other_organizations"] = limited_usage_with_other_organizations

    return parameters

def create_options_and_option_values():
    """
    Create the options and their values
    """
    option_instances_values: list[dict] = []
    for option in OPTIONS_AND_VALUES:
        option_value_dict = {
            "option": None,
            "values": []
        }
        option_instance = OptionFactory(name=option["name"])
        option_value_dict["option"] = option_instance
        
        for value in option["values"]:
            option_value_instance=OptionValueFactory(option=option_instance, value=value)
            option_value_dict["values"].append(option_value_instance)
        option_instances_values.append(option_value_dict)
    
    # Generate a unique combinations of option-values
    option_values_combinations: List[Tuple] = list(itertools.product(*[option["values"] for option in option_instances_values]))

    return option_instances_values, option_values_combinations



def init_personili_db(data_scale: int=5):
     # Track the number of created entries
    account_count = 0
    account_profile_count = 0
    business_owner_profile_count = 0
    designer_profile_count = 0
    store_count = 0
    store_profile_count = 0
    organization_count = 0
    organization_profile_count = 0
    workshop_count = 0

    # Create static data
    # Create the themes
    themes_instances = create_design_themes()

    # Create the roles
    create_roles_and_permissions()

    # Create the departements
    department_instances = create_departments()
    # Create the categories
    leaf_categories = create_categories()
    # Create the options and their values
    option_values, value_combinations = create_options_and_option_values()

    # Create dynamic data
    for i in range(data_scale):

        # Create the account
        account = AccountFactory()
        account_count += 1
        # Create its profile
        account_profile = AccountProfileFactory(account=account)
        account_profile_count += 1
        # Create its delivery address
        # determine how many delivery addresses it should has (between 1 and 3 )
        delivery_addresses_nb = random.randint(1, 3)
        for _ in range(delivery_addresses_nb):
            delivery_address = DeliveryAddressFactory(account_profile=account_profile)

        # Determine if this account is a regular user or a designer or a business owner
        is_regular_user = False
        is_designer = False
        is_business_owner = False
        which = random.randint(1, 100)
        if which <= 40:
            is_regular_user = True
        elif which > 40 and which <= 70:
            is_designer = True
        else:
            is_business_owner = True
        
        if is_regular_user:
            # Generate some user uploaded designs for the regular user
            # Determine how many designs this regular user should have (between 1 and 10)
            designs_nb = random.randint(0, 5)
            for _ in range(designs_nb):
                # Create the design
                # Generate the design usage parameters
                parameters = generate_design_usage_parmaters(is_regular_user, is_designer, is_business_owner)
                design = DesignFactory(regular_user=account_profile, 
                                       workshop=None,
                                       store=None,
                                       collection=None, 
                                       theme=random.choice(themes_instances),
                                       **parameters)

        elif is_designer:
            designer_profile_count += 1
            # Create the designer profile
            designer_profile = DesignerProfileFactory(account_profile=account_profile)
            # Create the store
            store = StoreFactory(designer_profile=designer_profile)
            store_count += 1
            # Create the store profile
            store_profile = StoreProfileFactory(store=store)
            store_profile_count += 1

            # Determine how many designs this designer should have (between 1 and 30)
            designs_nb = random.randint(1, 20)
            for _ in range(designs_nb):
                # Create the design
                # Generate the design usage parameters
                parameters = generate_design_usage_parmaters(is_regular_user, is_designer, is_business_owner)
                design = DesignFactory(store=store, 
                                       workshop=None,
                                       regular_user=None,
                                       collection=None, 
                                       theme=random.choice(themes_instances),
                                       **parameters)

        else:
            business_owner_profile_count += 1
            # Create business owner profile
            business_owner_profile = BusinessOwnerProfileFactory(account_profile=account_profile)

            # Create the organization
            organization = OrganizationFactory(business_owner_profile=business_owner_profile)
            organization_count += 1
            # Create the organization profile
            organization_profile = OrganizationProfileFactory(organization=organization)
            organization_profile_count += 1

            # Determine how many workshops this organization should have (between 1 and 5)
            workshops_nb = random.randint(1, 3)
            for _ in range(workshops_nb):
                # Create the workshop
                workshop = WorkshopFactory(organization=organization)
                workshop_count += 1
                # For each workshop creates designs
                designs_nb = random.randint(1, 20)
                designs_list = []

                for _ in range(designs_nb):
                    # Create the design
                    # Generate the design usage parameters
                    parameters = generate_design_usage_parmaters(is_regular_user, is_designer, is_business_owner)
                    design = DesignFactory(workshop=workshop, 
                                           collection=None, 
                                           theme=random.choice(themes_instances),
                                           store=None,
                                           regular_user=None,
                                           **parameters)
                    designs_list.append(design)
                    # Determine the number of design previews
                    design_previews_nb = random.randint(1, 5)
                    for _ in range(design_previews_nb):
                        # Create the design preview
                        design_preview = DesignPreviewFactory(design=design)
                
                # Create the personalizables and their variants
                # First decide how many personalizables this workshop should have (between 1 and 50)
                personalizables_nb = random.randint(1, 10)

                for _ in range(personalizables_nb):
                    # Create the personalizable
                    # First pick a random department and a random leaf category
                    department = random.choice(department_instances)
                    category = random.choice(leaf_categories)
                    personalizable = PersonalizableFactory(workshop=workshop,
                                                           department=department, 
                                                           category=category)
                    # Create the personalizable zones 
                    # First decide how many zones this personalizable should have (between 1 and 3)
                    personalizable_zones_nb = random.randint(1, 3)
                    personalizable_zones = []
                    for _ in range(personalizable_zones_nb):
                        personalizable_zone = PersonalizableZoneFactory(personalizable=personalizable)
                        personalizable_zones.append(personalizable_zone)

                    # Link the personalizable with the options
                    personalizable_options = []
                    for option in option_values:
                        personalizable_option = PersonalizableOptionFactory(personalizable=personalizable, option=option["option"])
                        personalizable_options.append(personalizable_option)
                    
                    # Create the personalizable variants
                    # Determine how many variants per personalizable (between 1 and 5)
                    personalizable_variants = []
                    # this list will hold the option values that have been used
                    option_values_list = []
                    for value_combination in value_combinations:
                        # Create the personalizable variant
                        personalizable_variant = PersonalizableVariantFactory(personalizable=personalizable)
                        personalizable_variants.append(personalizable_variant)

                        # each value combination is a tuple of option values (color, size, material)
                        for index, value in enumerate(value_combination):
                            # For each value in the combination, use the index to get the personalizable option and the option instance
                            personalizable_option = personalizable_options[index]
                            # Create the variant value
                            variant_value = PersonalizableVariantValueFactory(personalizable_variant=personalizable_variant, 
                                                                              personalizable_option=personalizable_option, 
                                                                              option_value=value)
                    
                    # Create the designed personalizable variants
                    # For each designed personalizable variant, create multiple designed personalizable zones
                    for personalizable_variant in personalizable_variants:
                        designed_personalizable_variant = DesignedPersonalizableVariantFactory(
                            personalizable_variant=personalizable_variant,
                        )
                        # Loop through the personalizable zones and create designed personalizable zones
                        for zone in personalizable_zones:
                            designed_personalizable_zone = DesignedPersonalizableZoneFactory(
                                designed_personalizable_variant=designed_personalizable_variant,
                                personalizable_zone=zone,
                                components = generate_random_shape()
                            )
                            # create the designed personalizable zone design
                            for _ in range(zone.max_nb_designs):
                                print("zone max nb designs", zone.max_nb_designs)
                                # Choose a random design
                                design = random.choice(designs_list)
                                designed_zone_related_design = DesignedZoneRelatedDesignFactory(
                                    designed_personalizable_zone=designed_personalizable_zone,
                                    design=design)
                                                         
        print("created data block number ", i)
        # Final counts
        print(f"current count of Accounts: {account_count}")
        print(f"current count of Account Profiles: {account_profile_count}")
        print(f"current count of Designer Profiles: {designer_profile_count}")
        print(f"current count of Stores: {store_count}")
        print(f"current count of Store Profiles: {store_profile_count}")
        print(f"current count of Organizations: {organization_count}")
        print(f"current count of Organization Profiles: {organization_profile_count}")
        print(f"current count of Workshops: {workshop_count}")


    print(f"total count of Accounts: {account_count}")
    print(f"total count of Account Profiles: {account_profile_count}")
    print(f"total count of Designer Profiles: {designer_profile_count}")
    print(f"total count of Stores: {store_count}")
    print(f"total count of Store Profiles: {store_profile_count}")
    print(f"total count of Organizations: {organization_count}")
    print(f"total count of Organization Profiles: {organization_profile_count}")
    print(f"total count of Workshops: {workshop_count}")

