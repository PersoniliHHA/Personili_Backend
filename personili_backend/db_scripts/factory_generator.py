from accounts.factories import AccountFactory, AccountProfileFactory, DeliveryAddressFactory
import random
from organizations.factories import OrganizationFactory, OrganizationMembershipFactory, OrganizationProfileFactory, WorkshopFactory, WorkshopMembershipFactory, InventoryFactory, InventoryItemFactory
from designs.factories import DesignerProfileFactory, DesignFactory, StoreFactory, StoreProfileFactory, CollectionFactory


def personili_local_db_data(data_scale: int=20):

    # Loopt through the accounts
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
        # Create the organization
        # Determine if this account can have an organization or not (70% chance it won't have an organization)
        # Create some designs with the regular user as foreign key

        elif is_designer:
            # Create the organization
            organization = OrganizationFactory()
            # Create the organization profile
            organization_profile = OrganizationProfileFactory(organization=organization)
            # Create the organization membership
            organization_membership = OrganizationMembershipFactory(account=account, organization=organization)
        else:
            # Create the organization
            organization = OrganizationFactory()
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
       

        


if __name__ == '__main__':
    personili_local_db_data()