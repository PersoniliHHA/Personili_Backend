from accounts.factories import AccountFactory, AccountProfileFactory


def personili_local_db_data(nb_accounts: int=20):

    # First create the accounts
    for _ in range(nb_accounts):
        account = AccountFactory()
        account_profile = AccountProfileFactory(account=account)


if __name__ == '__main__':
    personili_local_db_data()