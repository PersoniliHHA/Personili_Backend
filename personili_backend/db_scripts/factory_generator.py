from accounts.factories import AccountFactory, AccountProfileFactory, DeliveryAddressFactory, RoleFactory, PermissionFactory
import random
from organizations.factories import OrganizationFactory, OrganizationMembershipFactory, OrganizationProfileFactory, WorkshopFactory, WorkshopMembershipFactory, InventoryFactory, InventoryItemFactory
from designs.factories import ThemeFactory, DesignerProfileFactory, DesignFactory, StoreFactory, StoreProfileFactory, CollectionFactory
from django.core.management import call_command

# factory boy imports
import factory
from factory import Faker


def empty_database():
    call_command('flush', '--noinput')

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

    for theme in list_of_themes:
        ThemeFactory(name=theme["name"], 
                     description=theme["description"], 
                     icon_1_path=theme["icon_1_path"], 
                     icon_2_path=theme["icon_2_path"], 
                     icon_3_path=theme["icon_3_path"])

def init_personili_db(data_scale: int=2):
     # Track the number of created entries
    account_count = 0
    account_profile_count = 0
    delivery_address_count = 0
    design_count = 0
    designer_profile_count = 0
    store_count = 0
    store_profile_count = 0
    organization_count = 0
    organization_profile_count = 0
    workshop_count = 0
    inventory_count = 0
    inventory_item_count = 0

    # Empty the database
    #empty_database()

    # Create static data
    # Create the themes
    create_design_themes()

    # Create the roles
    create_roles_and_permissions()
    if False:
        # Create dynamic data
        for i in range(2):

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
                delivery_address_count += 1
            # Determine if this account is a regular user or a designer or a business owner
            is_regular_user = False
            is_designer = False
            is_business_owner = False
            # 50% chance it's a regular user
            # 30% chance it's a designer
            # 20% chance it's a business owner
            which = random.randint(1, 100)
            if which <= 50:
                is_regular_user = True
            elif which > 50 and which <= 80:
                is_designer = True
            else:
                is_business_owner = True
            
            if is_regular_user:
                # Generate some user uploaded designs for the regular user
                # Determine how many designs this regular user should have (between 1 and 10)
                designs_nb = random.randint(1, 10)
                for _ in range(designs_nb):
                    # Create the design
                    design = DesignFactory(regular_user=account_profile, collection=None)

            elif is_designer:
                # Create the designer profile
                designer_profile = DesignerProfileFactory(account_profile=account_profile)
                # Create the store
                store = StoreFactory(designer_profile=designer_profile)
                # Create the store profile
                store_profile = StoreProfileFactory(store=store)

                # Determine how many designs this designer should have (between 1 and 30)
                designs_nb = random.randint(1, 30)
                for _ in range(designs_nb):
                    # Create the design
                    design = DesignFactory(store=store, collection=None)

            else:
                # Create the organization
                organization = OrganizationFactory(account_profile=account_profile)
                # Create the organization profile
                organization_profile = OrganizationProfileFactory(organization=organization)

                # Determine how many workshops this organization should have (between 1 and 5)
                workshops_nb = random.randint(1, 5)
                for _ in range(workshops_nb):
                    # Create the workshop
                    workshop = WorkshopFactory(organization=organization)
                    # For each workshop creates designs
                    designs_nb = random.randint(1, 30)
                    for _ in range(designs_nb):
                        # Create the design
                        design = DesignFactory(workshop=workshop, collection=None)

                    # Create the inventory
                    inventory = InventoryFactory(workshop=workshop)
                    # Create the inventory item
                    inventory_item = InventoryItemFactory(inventory=inventory)
        

            # Log which objects have been created in this round
            print("created data block number ", i)
            # Final counts
            print(f"current count of Accounts: {account_count}")
            print(f"current count of Account Profiles: {account_profile_count}")
            print(f"current count of Delivery Addresses: {delivery_address_count}")
            print(f"current count of Designs: {design_count}")
            print(f"current count of Designer Profiles: {designer_profile_count}")
            print(f"current count of Stores: {store_count}")
            print(f"current count of Store Profiles: {store_profile_count}")
            print(f"current count of Organizations: {organization_count}")
            print(f"current count of Organization Profiles: {organization_profile_count}")
            print(f"current count of Workshops: {workshop_count}")
            print(f"current count of Inventories: {inventory_count}")
            print(f"current count of Inventory Items: {inventory_item_count}")
        

    print(f"total count of Accounts: {account_count}")
    print(f"total count of Account Profiles: {account_profile_count}")
    print(f"total count of Delivery Addresses: {delivery_address_count}")
    print(f"total count of Designs: {design_count}")
    print(f"total count of Designer Profiles: {designer_profile_count}")
    print(f"total count of Stores: {store_count}")
    print(f"total count of Store Profiles: {store_profile_count}")
    print(f"total count of Organizations: {organization_count}")
    print(f"total count of Organization Profiles: {organization_profile_count}")
    print(f"total count of Workshops: {workshop_count}")
    print(f"total count of Inventories: {inventory_count}")
    print(f"total count of Inventory Items: {inventory_item_count}")
