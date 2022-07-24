import datetime
from typing import Iterable

from ..utilities import settings, util, decorators
from ..utilities.request import Request


@decorators.class_type_checker
class TransactionSplit(Request):
    """
    Create, list, retrieve, update split transaction configuration with one or more SubAccounts (You should have subaccounts on your integration to use this)  
    """

    path = '/split'

    def create(self, name: str, split_type: str, currency: str, subaccounts: Iterable[tuple[str, int]], bearer_type: str, bearer_subaccount: str):
        """Create a split payment on your integration

        Args:
            name (str): Name of the transaction split
            split_type (str): The type of transaction split you want to create. 
                You can use one of the following: percentage | flat
            currency (str): Any of NGN, GHS, ZAR, or USD
            subaccounts (Iterable[tuple[str, int]]): A list of object containing subaccount code and
                number of shares: [('ACT_xxxxxxxxxx', xxx)]
            bearer_type (str): Any of subaccount | account | all-proportional | all
            bearer_subaccount (str): Subaccount code

        Returns:
            JSON: Data fetched from API
        """

        payload = {
            'name': name,
            'type': util.check_membership(settings.SPLIT_TYPES, split_type, 'split_type'),
            'currency': util.check_membership(settings.CURRENCIES, currency, 'currency'),
            'bearer_type': util.check_membership(settings.BEARER_TYPES, bearer_type, 'bearer_type'),
            'subaccounts': [{'subaccount': util.check_code(settings.SUBACCOUNT, subaccount), 'share': share} for subaccount, share in subaccounts],
        }

        if bearer_type == 'subaccount':
            payload['bearer_subaccount'] = util.check_code(
                settings.SUBACCOUNT, bearer_subaccount)

        return self.post(self.path, payload=payload)

    def list_search(self, name: str = None, active: bool = None, sort_by: str = None, per_page: int = None, page: int = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None):
        """List/search for the transaction splits available on your integration.

        Args:
            name (str, optional): The name of the split. Defaults to None.
            active (bool, optional): Any of true or false. Defaults to None.
            sort_by (str, optional): Sort by name, defaults to createdAt date. Defaults to None.
            per_page (int, optional): Number of splits per page. If not specify we use a default value of 50.
            page (int, optional): Page number to view. If not specify we use a default value of 1.
            from_date (datetime.datetime | datetime.date | str, optional): A timestamp from which to start listing splits
                e.g. 2019-09-24T00:00:05.000Z, 2019-09-21. Defaults to None.
            to_date (datetime.datetime | datetime.date | str, optional): A timestamp at which to stop listing splits
                e.g. 2019-09-24T00:00:05.000Z, 2019-09-21. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        params = util.generate_payload(
            locals(), 'per_page', 'page', 'from_date', 'to_date')
        params.update(util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date))
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, split_id: int):
        """Get details of a split on your integration.

        Args:
            split_id (int): The id of the split

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{split_id}'
        return self.get(path)

    def update(self, split_id: int, name: str = None, active: bool = None, bearer_type: str = None, bearer_subaccount: str = None):
        """Update a transaction split details on your integration

        Args:
            split_id (int): Split ID
            name (str, optional): Name of the transaction split. Defaults to None.
            active (bool, optional): True or False. Defaults to None.
            bearer_type (str, optional): Any of the following values:
                subaccount | account | all-proportional | all. Defaults to None.
            bearer_subaccount (str, optional): Subaccount code of a subaccount in the split group.
                This should be specified only if the bearer_type is subaccount. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{split_id}'
        payload = {key: value for key, value in locals(
        ).items() if key not in ('split_id', 'path') and value is not None}

        if bearer_type:
            payload['bearer_type'] = util.check_membership(
                settings.BEARER_TYPES, bearer_type, 'bearer_type')

        if 'bearer_type' in payload and payload['bearer_type'] != 'subaccount':
            payload.pop('bearer_subaccount')

        return self.put(path, payload=payload)

    def add_update_subaccount(self, split_id: int, subaccount: str, share: int):
        """Add a Subaccount to a Transaction Split, or update the share of an existing Subaccount in a Transaction Split

        Args:
            split_id (int): Split Id
            subaccount (str): This is the sub account code
            share (int): This is the transaction share for the subaccount

        Returns:
            JSON: Data fetched from API   
        """

        path = f'{self.path}/{split_id}/subaccount/add'
        payload = {
            'subaccount': util.check_code(settings.SUBACCOUNT, subaccount),
            'share': share
        }
        return self.post(path, payload=payload)

    def remove_subaccount(self, split_id: int, subaccount: str):
        """Remove a subaccount from a transaction split

        Args:
            split_id (int): Split Id
            subaccount (str): This is the sub account code

        Returns:
            JSON: Data fetched from API        
        """

        path = f'{self.path}/{split_id}/subaccount/remove'
        payload = {
            'subaccount': util.check_code(settings.SUBACCOUNT, subaccount)
        }
        return self.post(path, payload=payload)
