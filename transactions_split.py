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
    
    def create(self, name: str, split_type: str, currency: str, subaccounts: Iterable[tuple[str, int]], bearer_type: str, bearer_subaccount: str):
        payload = {
            'name': name,
            'type': util.check_membership(settings.SPLIT_TYPES, split_type, 'split_type'),
            'currency': util.check_membership(settings.CURRENCIES, currency, 'currency'),
            'bearer_type': util.check_membership(settings.BEARER_TYPES, bearer_type, 'bearer_type'),
            'subaccounts': [{ 'subaccount': util.check_code(settings.CODE_NAMES['subaccount'], subaccount), 'share': share } for subaccount, share in subaccounts],
        }

        if bearer_type == 'subaccount':
            payload['bearer_subaccount'] = util.check_code(settings.CODE_NAMES['subaccount'], bearer_subaccount)

        return self.post(self.path, payload=payload)

    def list_search(self, name: str = None, active: bool = None, sort_by: str = None, per_page: int = None, page: int = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None):
        params = util.generate_payload(locals())
        params.update(util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date))      
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, split_id: int):
        path = f'{self.path}/{split_id}'
        return self.get(path)

    def update(self, split_id: int, name: str = None, active: bool = None, bearer_type: str = None, bearer_subaccount: str = None):
        path = f'{self.path}/{split_id}'
        payload = {key: value for key, value in locals(
        ).items() if key not in ('split_id', 'path') and value is not None}

        if bearer_type:
            payload['bearer_type'] = util.check_membership(settings.BEARER_TYPES, bearer_type, 'bearer_type')

        if 'bearer_type' in payload and payload['bearer_type'] != 'subaccount':
            payload.pop('bearer_subaccount')

        return self.put(path, payload=payload)

    def add_update_subaccount(self, split_id: int, subaccount: str, share: int):
        path = f'{self.path}/{split_id}/subaccount/add'
        payload = {
            'subaccount': util.check_code(settings.CODE_NAMES['subaccount'], subaccount),
            'share': share
        }
        return self.post(path, payload=payload)

    def remove_subaccount(self, split_id: int, subaccount: str):
        path = f'{self.path}/{split_id}/subaccount/remove'
        payload = {
            'subaccount': util.check_code(settings.CODE_NAMES['subaccount'], subaccount)
        }
        return self.post(path, payload=payload)
