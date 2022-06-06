import datetime
from typing import Iterable
from .request import Request
from . import util
from . import settings


class TransactionSplit(Request):
    """
    Create, list, retrieve, update split transaction configuration with one or more SubAccounts (You should have subaccounts on your integration to use this)  
    """

    path = '/split'

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create(self, name: str, split_type: str, currency: str, subaccounts: Iterable[tuple[str, int]], bearer_type: str, bearer_subaccount: str):
        payload = {
            'name': name,
            'type': util.check_split_type(split_type),
            'currency': util.check_currency(currency),
            'bearer_type': util.check_bearer(bearer_type),
            'subaccounts': [{ 'subaccount': util.check_subaccount(subaccount), 'share': share } for subaccount, share in subaccounts],
        }

        if bearer_type == 'subaccount':
            payload['bearer_subaccount'] = util.check_subaccount(
                bearer_subaccount)

        return self.post(self.path, self.secret_key, payload)

    def list_search(self, name: str = None, active: bool = None, sort_by: str = None, per_page: int = None, page: int = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None):
        path = self.path
        params = util.handle_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        params.update({key: value for key, value in locals().items()
                      if value is not None and key not in params})
        if params:
            path += '?'
            for key, value in params.items():
                path += f"{key}={value}&"
        return self.get(path.rstrip('&'), self.secret_key)

    def fetch(self, split_id: int):
        path = f'{self.path}/{split_id}'
        return self.get(path, self.secret_key)

    def update(self, split_id: int, name: str = None, active: bool = None, bearer_type: str = None, bearer_subaccount: str = None):
        path = f'{self.path}/{split_id}'
        payload = {key: value for key, value in locals(
        ).items() if key != 'split_id' and value is not None}

        if bearer_type:
            payload['bearer_type'] = util.check_bearer(bearer_type)

        if 'bearer_type' in payload and payload['bearer_type'] != 'subaccount':
            payload.pop('bearer_subaccount')

        return self.put(path, self.secret_key, payload)

    def add_update_subaccount(self, split_id: int, subaccount: str, share: int):
        path = f'{self.path}/{split_id}/subaccount/add'
        payload = {
            'subaccount': util.check_subaccount(subaccount),
            'share': share
        }
        return self.post(path, self.secret_key, payload)

    def remove_subaccount(self, split_id: int, subaccount: str):
        path = f'{self.path}/{split_id}/subaccount/remove'
        payload = {
            'subaccount': util.check_subaccount(subaccount)
        }
        return self.post(path, self.secret_key, payload)
