from .utilities import settings, util, decorators
from .utilities.errors import MissingArgumentsError
from .utilities.request import Request


@decorators.class_type_checker
class DedicatedVirtualAccounts(Request):

    """
    The Dedicated Virtual Account class enables Nigerian merchants to manage unique payment accounts of their customers.
    """

    path = '/dedicated_account'

    def create(self, customer_code: str, preferred_bank: str, subaccount: str = None, split_code: str = None, first_name: str = None, last_name: str = None, phone: str = None):
        payload = util.generate_payload(locals())
        payload['customer'] = util.check_code(settings.CUSTOMER, customer_code)
        payload['preferred_bank'] = util.check_membership(settings.VIRTUAL_ACCOUNT_PROVIDERS, preferred_bank, 'preferred_bank')

        if subaccount:
            payload['subaccount'] = util.check_code(settings.SUBACCOUNT, subaccount)

        if split_code:
            payload['split_code'] = util.check_code(settings.SPLIT, split_code)
            
        return self.post(self.path, payload=payload)

    def list_accounts(self, active: bool = None, currency: str = None, provider_slug: str = None, bank_id: int = None, customer_id: str = None):
        params = util.generate_payload(locals())
        if currency:
            params['currency'] = util.check_membership(settings.CURRENCIES, currency, 'currency')

        if provider_slug:
            params['provider_slug'] = util.check_membership(settings.VIRTUAL_ACCOUNT_PROVIDERS, provider_slug, 'provider_slug')
        
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, dedicated_account_id: int):
        path = f'{self.path}/{dedicated_account_id}'
        return self.get(path)

    def requery(self, account_number: str, provider_slug: str, date: str = None):
        path = f"{self.path}/requery?account_number={util.check_account_number(account_number)}&provider_slug={util.check_membership(settings.VIRTUAL_ACCOUNT_PROVIDERS, provider_slug, 'provider_slug')}"
        if date:
            path += f'&date={util.handle_date(date)}'
        return self.get(path)

    def deactivate(self, dedicated_account_id: int):
        path = f'{self.path}/{dedicated_account_id}'
        return self.delete(path)

    def split_transaction(self, preferred_bank: str, customer_id: int = None, customer_code: str = None,  subaccount: str | list = None, split_code: str | list = None):
        path = f'{self.path}/split'

        payload = {
            'preferred_bank': util.check_membership(settings.VIRTUAL_ACCOUNT_PROVIDERS, preferred_bank, 'preferred_bank')
        }

        payload['customer'] = util.id_or_code(_id=customer_id, code=customer_code, data=settings.CUSTOMER)
        
        if not ( subaccount or split_code ):
            raise MissingArgumentsError('Provide subaccount or split_code or a list of subaccounts or split_codes')
        
        if subaccount:
            payload['subaccount'] = util.check_code(settings.SUBACCOUNT, subaccount)
        
        if split_code:
            payload['split_code'] = util.check_code(settings.SPLIT,split_code)
        
        return self.post(path, payload=payload)

    def remove_split(self, account_number: str):
        path = f'{self.path}/split'
        payload = {
            'account_number': util.check_account_number(account_number)
        }
        return self.delete(path, payload=payload)

    def fetch_bank_providers(self):
        path = f'{self.path}/available_providers'
        return self.get(path)
