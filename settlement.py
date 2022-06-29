from datetime import date, datetime
from .request import Request
from . import util


class Settlements(Request):

    """
    The Settlements API allows you gain insights into payouts made by Paystack to your bank account
    """

    path = '/settlement'

    def fetch(self, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None, subaccount: str = None):
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        params.update({'subaccount': subaccount})
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch_transactions(self, settlement_id: int, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None):
        path = f"{self.path}/{settlement_id}/transactions"
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            return self.get(util.handle_query_params(path, params))
        return self.get(path)

