import datetime

from .utilities import settings, util
from .utilities.errors import MissingArgumentsError
from .utilities.request import Request


class SubAccounts(Request):

    """
    The Subaccounts API allows you create and manage subaccounts on your integration.
    Subaccounts can be used to split payment between two accounts (your main account and a sub account)
    """

    path = '/subaccount'

    def create(self, business_name: str, settlement_bank: str, account_number: str, percentage_charge: float, description: str = None, primary_contact_email: str = None, primary_contact_name: str = None, primary_contact_phone: str = None, metadata: str = None):
        payload = util.generate_payload(locals())
        payload['settlement_bank'] = util.check_bank_code(settlement_bank)
        payload['account_number'] = util.check_account_number(account_number)

        if primary_contact_email:
            payload['primary_contact_email'] = util.check_email(
                primary_contact_email)
        return self.post(self.path, payload=payload)

    def list_subaccounts(self, per_page: int = None, page: int = None, from_date: datetime.date | datetime.datetime | str = None, to_date: datetime.date | datetime.datetime | str = None):
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, subaccount_id: int = None, subaccount_code: str = None):
        path = self.path
        if not (subaccount_id or subaccount_code):
            raise MissingArgumentsError("Provide a subaccount id or code")

        if subaccount_id:
            path += f"/{subaccount_id}"

        if subaccount_code and not subaccount_id:
            path += f"/{util.check_code(settings.CODE_NAMES['subaccount'], subaccount_code)}"

        return self.get(path)

    def update(self, subaccount_id: int = None, subaccount_code: str = None, active: bool = None, business_name: str = None, settlement_bank: str = None, account_number: str = None, settlement_schedule: str = None, percentage_charge: float = None, description: str = None, primary_contact_email: str = None, primary_contact_name: str = None, primary_contact_phone: str = None, metadata: str = None):
        path = self.path

        if not (subaccount_id or subaccount_code):
            raise MissingArgumentsError("Provide a subaccount id or code")

        if subaccount_id:
            path += f"/{subaccount_id}"

        if subaccount_code and not subaccount_id:
            path += f"/{util.check_code(settings.CODE_NAMES['subaccount'], subaccount_code)}"

        payload = util.generate_payload(locals(), 'subaccount_id', 'subaccount_code', 'path')
        
        if settlement_bank:
            payload['settlement_bank'] = util.check_bank_code(settlement_bank)

        if settlement_schedule:
            payload['settlement_schedule'] = util.check_membership(settings.SETTLEMENT_SCHEDULES, settlement_schedule, 'settlement_schedule')

        if account_number:
            payload['account_number'] = util.check_account_number(
                account_number)

        if primary_contact_email:
            payload['primary_contact_email'] = util.check_email(
                primary_contact_email)

        return self.put(path, payload=payload)
