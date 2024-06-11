from personili_backend.accounts.factories import AccountFactory, AccountProfileFactory




for _ in range(10):
    account = AccountFactory()
    account_profile = AccountProfileFactory(account=account)