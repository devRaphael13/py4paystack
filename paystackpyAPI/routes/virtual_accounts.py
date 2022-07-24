from ..utilities import decorators, settings, util
from ..utilities.errors import MissingArgumentsError
from ..utilities.request import Request


@decorators.class_type_checker
class DedicatedVirtualAccounts(Request):

    """
    The Dedicated Virtual Account class enables Nigerian merchants to manage unique payment accounts of their customers.
    """

    path = '/dedicated_account'

    def create(self, customer: int | str, preferred_bank: str, subaccount: str = None, split_code: str = None, first_name: str = None, last_name: str = None, phone: str = None):
        """Create a dedicated virtual account and assign to a customer
            Paystack currently supports Access Bank and Wema Bank.

        Args:
            customer (int | str): Customer ID or code
            preferred_bank (str): The bank slug for preferred bank. To get a list of available banks, use the List Providers endpoint
            subaccount (str, optional): Subaccount code of the account you want to split the transaction with. Defaults to None.
            split_code (str, optional): Split code consisting of the lists of accounts you want to split the transaction with. Defaults to None.
            first_name (str, optional): Customer's first name. Defaults to None.
            last_name (str, optional): Customer's last name. Defaults to None.
            phone (str, optional): Customer's phone number. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        payload = util.generate_payload(
            locals(), 'customer', 'preferred_bank', 'subaccount', 'split_code')
        payload['customer'] = util.id_or_code(customer, data=settings.CUSTOMER)
        payload['preferred_bank'] = util.check_membership(
            settings.VIRTUAL_ACCOUNT_PROVIDERS, preferred_bank, 'preferred_bank')

        if subaccount:
            payload['subaccount'] = util.check_code(
                settings.SUBACCOUNT, subaccount)

        if split_code:
            payload['split_code'] = util.check_code(settings.SPLIT, split_code)

        return self.post(self.path, payload=payload)

    def list_accounts(self, active: bool = None, currency: str = None, provider_slug: str = None, bank_id: int = None, customer_id: str = None):
        """List dedicated virtual accounts available on your integration.

        Args:
            active (bool, optional): Status of the dedicated virtual account. Defaults to None.
            currency (str, optional): The currency of the dedicated virtual account. Only NGN is currently allowed. Defaults to None.
            provider_slug (str, optional): The bank's slug in lowercase, without spaces e.g. wema-bank. Defaults to None.
            bank_id (int, optional): The bank's ID e.g. 035. Defaults to None.
            customer_id (str, optional): The customer's ID. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        params = util.generate_payload(locals(), 'currency', 'provider_slug')
        if currency:
            params['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if provider_slug:
            params['provider_slug'] = util.check_membership(
                settings.VIRTUAL_ACCOUNT_PROVIDERS, provider_slug, 'provider_slug')

        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, dedicated_account_id: int):
        """Get details of a dedicated virtual account on your integration.

        Args:
            dedicated_account_id (int): ID of dedicated virtual account

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{dedicated_account_id}'
        return self.get(path)

    def requery(self, account_number: str, provider_slug: str, date: str = None):
        """Requery Dedicated Virtual Account for new transactions

        Args:
            account_number (str): Virtual account number to requery
            provider_slug (str): The bank's slug in lowercase, without spaces e.g. wema-bank
            date (str, optional): The day the transfer was made in YYYY-MM-DD format. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/requery?account_number={util.check_account_number(account_number)}&provider_slug={util.check_membership(settings.VIRTUAL_ACCOUNT_PROVIDERS, provider_slug, 'provider_slug')}"
        if date:
            path += f'&date={util.handle_date(date)}'
        return self.get(path)

    def deactivate(self, dedicated_account_id: int):
        """Deactivate a dedicated virtual account on your integration.

        Args:
            dedicated_account_id (int): ID of dedicated virtual account

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{dedicated_account_id}'
        return self.delete(path)

    def split_transaction(self, customer: int | str, preferred_bank: str,  subaccount: str | list = None, split_code: str | list = None):
        """Split a dedicated virtual account transaction with one or more accounts

        Args:
            customer (int | str): Customer ID or code.
            preferred_bank (str): The bank slug for preferred bank. To get a list of available banks, use the List Providers endpoint
            subaccount (str | list, optional): Subaccount code of the account you want to split the transaction with. Defaults to None.
            split_code (str | list, optional): Split code consisting of the lists of accounts you want to split the transaction with. Defaults to None.

        Raises:
            MissingArgumentsError: Raised when required arguments are missing.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/split'

        payload = {
            'preferred_bank': util.check_membership(settings.VIRTUAL_ACCOUNT_PROVIDERS, preferred_bank, 'preferred_bank')
        }

        payload['customer'] = util.id_or_code(customer, data=settings.CUSTOMER)

        if not (subaccount or split_code):
            raise MissingArgumentsError(
                'Provide subaccount, split_code, a list of subaccounts or a list of split_codes')

        if subaccount:
            payload['subaccount'] = util.check_code(
                settings.SUBACCOUNT, subaccount)

        if split_code:
            payload['split_code'] = util.check_code(settings.SPLIT, split_code)

        return self.post(path, payload=payload)

    def remove_split(self, account_number: str):
        """If you've previously set up split payment for transactions on a dedicated virtual account,
            you can remove it with this endpoint

        Args:
            account_number (str): Dedicated virtual account number

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/split'
        payload = {
            'account_number': util.check_account_number(account_number)
        }
        return self.delete(path, payload=payload)

    def fetch_bank_providers(self):
        """Get available bank providers for a dedicated virtual account

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/available_providers'
        return self.get(path)
