import datetime
from .request import Request
from . import util


class SubAccounts(Request):

    """
    The Subaccounts API allows you create and manage subaccounts on your integration.
    Subaccounts can be used to split payment between two accounts (your main account and a sub account)
    """

    path = '/subaccount'

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create(self, business_name: str, settlement_bank: str, account_number: str, percentage_charge: float, description: str = None, primary_contact_email: str = None, primary_contact_name: str = None, primary_contact_phone: int = None, metadata: str = None):
        payload = {key: value for key, value in locals().items() if value}
        payload['settlement_bank'] = util.check_bank_code(settlement_bank)
        payload['account_number'] = util.check_account_number(account_number)

        if primary_contact_email:
            payload['primary_contact_email'] = util.check_email(
                primary_contact_email)
        return self.post(self.path, self.secret_key, payload)

    def list_subaccounts(self, per_page: int = None, page: int = None, from_date: datetime.date | datetime.datetime | str = None, to_date: datetime.date | datetime.datetime | str = None):
        path = self.path
        params = util.handle_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            path += '?'
            for key, value in params:
                path += f'{key}={value}'
        return self.get(path, self.secret_key)

    def fetch(self, subaccount_id: int = None, subaccount_code: str = None):
        path = f'{self.path}/'
        if not (subaccount_id or subaccount_code):
            raise ValueError("Provide a subaccount id or code")

        if subaccount_id:
            path += str(subaccount_id)

        if subaccount_code and not subaccount_id:
            path += util.check_subaccount(subaccount_code)

        return self.get(path, self.secret_key)

    def update(self, subaccount_id: int = None, subaccount_code: str = None, active: bool = None, business_name: str = None, settlement_bank: str = None, account_number: str = None, settlement_schedule: str = None, percentage_charge: float = None, description: str = None, primary_contact_email: str = None, primary_contact_name: str = None, primary_contact_phone: int = None, metadata: str = None):
        path = f'{self.path}/'

        if not (subaccount_id or subaccount_code):
            raise ValueError("Provide a subaccount id or code")

        if subaccount_id:
            path += str(subaccount_id)

        if subaccount_code and not subaccount_id:
            path += util.check_subaccount(subaccount_code)

        payload = {key: value for key, value in locals().items() if key not in (
            'subaccount_id', 'subaccount_code') and value is not None}

        if settlement_bank:
            payload['settlement_bank'] = util.check_bank_code(settlement_bank)

        if settlement_schedule:
            payload['settlement_schedule'] = util.check_settlement_schedule(
                settlement_schedule)

        if account_number:
            payload['account_number'] = util.check_account_number(
                account_number)

        if primary_contact_email:
            payload['primary_contact_email'] = util.check_email(
                primary_contact_email)
            
        return self.put(path, self.secret_key, payload)

    
    
