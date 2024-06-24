from accounts.factories import AccountFactory, AccountProfileFactory, DeliveryAddressFactory, RoleFactory, PermissionFactory
import random
from organizations.factories import OrganizationFactory, OrganizationMembershipFactory, OrganizationProfileFactory, WorkshopFactory, WorkshopMembershipFactory, InventoryFactory, InventoryItemFactory
from designs.factories import DesignerProfileFactory, DesignFactory, StoreFactory, StoreProfileFactory, CollectionFactory

from django.db import transaction
from accounts.models import Account, AccountProfile, DeliveryAddress
from designs.models import DesignerProfile, Design, Store, StoreProfile, Collection
from organizations.models import OrganizationMembership, OrganizationProfile, Organization, OrganizationProfile, Workshop, WorkshopMembership, Inventory, InventoryItem
from django.core.management import call_command

@transaction.atomic
def empty_local_db():
    # Empty the database for relevant models
    DeliveryAddress.objects.all().delete()
    AccountProfile.objects.all().delete()
    Account.objects.all().delete()
    # Add deletion for other models as necessary, following dependencies
    OrganizationMembership.objects.all().delete()
    OrganizationProfile.objects.all().delete()
    Organization.objects.all().delete()
    
    WorkshopMembership.objects.all().delete()
    Workshop.objects.all().delete()
    
    InventoryItem.objects.all().delete()
    Inventory.objects.all().delete()
    
    DesignerProfile.objects.all().delete()
    Design.objects.all().delete()
    
    StoreProfile.objects.all().delete()
    Store.objects.all().delete()
    Collection.objects.all().delete()

def empty_database():
    call_command('flush', '--noinput')


def init_personili_db(data_scale: int=20):

    # Empty the database
    empty_database()

    # Create dynamic data
    for _ in range(data_scale):

        # Create the account
        account = AccountFactory()
        # Create its profile
        account_profile = AccountProfileFactory(account=account)
        # Create its delivery address
        # determine how many delivery addresses it should has (between 1 and 3 )
        delivery_addresses_nb = random.randint(1, 3)
        for _ in range(delivery_addresses_nb):
            delivery_address = DeliveryAddressFactory(account_profile=account_profile)
        
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
            continue

        elif is_designer:
            # Create the designer profile
            designer_profile = DesignerProfileFactory(account_profile=account_profile)
            # Create the store
            store = StoreFactory(designer_profile=designer_profile)
            # Create the store profile
            store_profile = StoreProfileFactory(store=store)
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
                # Create the workshop membership
                workshop_membership = WorkshopMembershipFactory(account=account, workshop=workshop)
                # Create the inventory
                inventory = InventoryFactory(workshop=workshop)
                # Create the inventory item
                inventory_item = InventoryItemFactory(inventory=inventory)
       

        # Log which objects have been created in this round
        print(f"Created account: {account.email}")
        print(f"Created account profile: {account_profile.username}")
        if is_designer:
            print(f"Created designer profile: {designer_profile.designer_name}")
            print(f"Created store: {store.name}")
            print(f"Created store profile: {store_profile.store_name}")
        else:
            print(f"Created organization: {organization.name}")
            print(f"Created organization profile: {organization_profile.organization_name}")
            print(f"Created {workshops_nb} workshops")
            print(f"Created inventory: {inventory.name}")
            print(f"Created inventory item: {inventory_item.name}")
        
        print("\n\n")
        
if __name__ == '__main__':
    init_personili_db()
