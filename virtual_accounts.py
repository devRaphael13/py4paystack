from .request import Request
from . import util


class DedicatedVirtualAccounts(Request):

    """
    The Dedicated Virtual Account class enables Nigerian merchants to manage unique payment accounts of their customers.
    """

    path = '/dedicated_account'

    def __init__(self, secret_key: str) -> None:
        self.secret_key = secret_key

    def create(self, customer_code: str, preferred_bank: str, subaccount: str = None, split_code: str = None, first_name: str = None, last_name: str = None, phone: int = None):
        path = self.path

        payload = {
            'customer': util.check_customer(customer_code),
            'preferred_bank': util.check_preferred_bank(preferred_bank)
        }

        if subaccount:
            payload['subaccount'] = util.check_subaccount(subaccount)

        if split_code:
            payload['split_code'] = util.check_split_code(split_code)

        if first_name:
            payload['first_name'] = first_name

        if last_name:
            payload['last_name'] = last_name

        if phone:
            payload['phone'] = f'+{phone}'

        return self.post(path, self.secret_key, payload)

    def list_accounts(self, active: bool = None, currency: str = None, provider_slug: str = None, bank_id: int = None, customer_id: str = None):
        path = self.path
        args = locals()
        if any(locals().values()):
            path += '?'
            if currency:
                args['currency'] = util.check_currency(currency)

            if provider_slug:
                args['provider_slug'] = util.check_preferred_bank(
                    provider_slug)

            for key, value in args.items():
                if value is not None:
                    path += f'{key}={value}&'
        return self.get(path.rstrip('&'), self.secret_key)

    def fetch(self, dedicated_account_id: int):
        path = f'{self.path}/{dedicated_account_id}'
        return self.get(path, self.secret_key)

    def requery(self, account_number: str, provider_slug: str, date: str = None):
        path = f'{self.path}/requery?account_number={util.check_account_number(account_number)}&provider_slug={util.check_preferred_bank(provider_slug)}'
        if date:
            path += f'&date={util.handle_date(date)}'
        return self.get(path, self.secret_key)

    def deactivate(self, dedicated_account_id: int):
        path = f'{self.path}/{dedicated_account_id}'
        return self.delete(path, self.secret_key)

    def split_transaction(self, preferred_bank: str, customer_id: int = None, customer_code: str = None,  subaccount: str | list = None, split_code: str | list = None):
        path = f'{self.path}/split'

        payload = {
            'preferred_bank': util.check_preferred_bank(preferred_bank)
        }
        if not ( customer_code or customer_id ):
            raise ValueError('Provide the customer_code or the customer_id')

        if customer_id:
            payload['customer'] = customer_id

        if customer_code and not customer_id:
            payload['customer'] = util.check_customer(customer_code)
        
        if not ( subaccount or split_code ):
            raise ValueError('Provide subaccount or split_code or a list of subaccounts or split_codes')
        
        if subaccount:
            payload['subaccount'] = util.check_subaccount(subaccount)
        
        if split_code:
            payload['split_code'] = util.check_split_code(split_code)
        
        return self.post(path, self.secret_key, payload)

    def remove_split(self, account_number: str):
        path = f'{self.path}/split'
        payload = {
            'account_number': util.check_account_number(account_number)
        }
        return self.delete(path, self.secret_key, payload=payload)

    def fetch_bank_providers(self):
        path = f'{self.path}/available_providers'
        return self.get(path, self.secret_key)
