from datetime import date, datetime
from .request import Request
from . import util


class Settlements(Request):

    """
    The Settlements API allows you gain insights into payouts made by Paystack to your bank account
    """

    path = '/settlement'

    def __init__(self, secret_key: str) -> str:
        self.secret_key = secret_key

    def fetch(self, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None, subaccount: str = None):
        path = self.path
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date).update({'subaccount': subaccount})
        if params:
            path = util.handle_query_params(path, params)
        return self.get(path, self.secret_key)

    def fetch_transactions(self, settlement_id: int, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None):
        path = f"{self.path}/{settlement_id}/transactions"
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            path = util.handle_query_params(path, params)
        return self.get(path, self.secret_key)
