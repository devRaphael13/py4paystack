from .request import Request
from . import util
from . import settings


class DedicatedVirtualAccounts(Request):

    """
    The Dedicated Virtual Account class enables Nigerian merchants to manage unique payment accounts of their customers.
    """

    path = '/dedicated_account'

    def __init__(self, secret_key: str) -> None:
        self.secret_key = secret_key

    def create(self, customer_code: str, preferred_bank: str, subaccount: str = None, split_code: str = None, first_name: str = None, last_name: str = None, phone: int = None):
        payload = {
            'customer': util.check_code(settings.CODE_NAMES['customer'], customer_code),
            'preferred_bank': util.check_membership(settings.VIRTUAL_ACCOUNT_PROVIDERS, preferred_bank, 'preferred_bank')
        }

        if subaccount:
            payload['subaccount'] = util.check_code(settings.CODE_NAMES['subaccount'], subaccount)

        if split_code:
            payload['split_code'] = util.check_code(settings.CODE_NAMES['split'], split_code)

        if first_name:
            payload['first_name'] = first_name

        if last_name:
            payload['last_name'] = last_name

        if phone:
            payload['phone'] = f'+{phone}'

        return self.post(self.path, self.secret_key, payload=payload)

    def list_accounts(self, active: bool = None, currency: str = None, provider_slug: str = None, bank_id: int = None, customer_id: str = None):
        path = self.path
        params = { key: value for key, value in locals().items() if value is not None }
        if currency:
            params['currency'] = util.check_membership(settings.CURRENCIES, currency, 'currency')

        if provider_slug:
            params['provider_slug'] = util.check_membership(settings.VIRTUAL_ACCOUNT_PROVIDERS, provider_slug, 'provider_slug')
        
        if params:
            path = util.handle_query_params(path, params)
        return self.get(path, self.secret_key)

    def fetch(self, dedicated_account_id: int):
        path = f'{self.path}/{dedicated_account_id}'
        return self.get(path, self.secret_key)

    def requery(self, account_number: str, provider_slug: str, date: str = None):
        path = f"{self.path}/requery?account_number={util.check_account_number(account_number)}&provider_slug={util.check_membership(settings.VIRTUAL_ACCOUNT_PROVIDERS, provider_slug, 'provider_slug')}"
        if date:
            path += f'&date={util.handle_date(date)}'
        return self.get(path, self.secret_key)

    def deactivate(self, dedicated_account_id: int):
        path = f'{self.path}/{dedicated_account_id}'
        return self.delete(path, self.secret_key)

    def split_transaction(self, preferred_bank: str, customer_id: int = None, customer_code: str = None,  subaccount: str | list = None, split_code: str | list = None):
        path = f'{self.path}/split'

        payload = {
            'preferred_bank': util.check_membership(settings.VIRTUAL_ACCOUNT_PROVIDERS, preferred_bank, 'preferred_bank')
        }
        if not ( customer_code or customer_id ):
            raise ValueError('Provide the customer_code or the customer_id')

        if customer_id:
            payload['customer'] = customer_id

        if customer_code and not customer_id:
            payload['customer'] = util.check_code(settings.CODE_NAMES['customer'], customer_code)
        
        if not ( subaccount or split_code ):
            raise ValueError('Provide subaccount or split_code or a list of subaccounts or split_codes')
        
        if subaccount:
            payload['subaccount'] = util.check_code(settings.CODE_NAMES['subaccount'], subaccount)
        
        if split_code:
            payload['split_code'] = util.check_code(settings.CODE_NAMES['split'] ,split_code)
        
        return self.post(path, self.secret_key, payload=payload)

    def remove_split(self, account_number: str):
        path = f'{self.path}/split'
        payload = {
            'account_number': util.check_account_number(account_number)
        }
        return self.delete(path, self.secret_key, payload=payload)

    def fetch_bank_providers(self):
        path = f'{self.path}/available_providers'
        return self.get(path, self.secret_key)
