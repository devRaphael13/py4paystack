from datetime import date, datetime

from ..utilities import util, decorators, settings
from ..utilities.request import Request


@decorators.class_type_checker
class Settlements(Request):

    """
    The Settlements API allows you gain insights into payouts made by Paystack to your bank account
    """

    path = '/settlement'

    def fetch(self, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None, subaccount: str = None):
        """Fetch settlements made to your settlement accounts.

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50.
            page (int, optional): Specify exactly what page you want to retrieve.
                If not specify we use a default value of 1.
            from_date (date | datetime | str, optional): A timestamp from which to start listing settlements
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            to_date (date | datetime | str, optional): A timestamp at which to stop listing settlements
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            subaccount (str, optional): Provide a subaccount ID to export only settlements for that subaccount.
                Set to none to export only transactions for the account. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        params.update({'subaccount': util.check_code(
            settings.SUBACCOUNT, subaccount)})

        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch_transactions(self, settlement_id: int, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None):
        """Get the transactions that make up a particular settlement

        Args:
            settlement_id (int): The settlement ID in which you want to fetch its transactions.
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50.. Defaults to None.
            page (int, optional): Specify exactly what page you want to retrieve.
                If not specify we use a default value of 1.. Defaults to None.
            from_date (date | datetime | str, optional): A timestamp from which to start listing settlement transactions
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            to_date (date | datetime | str, optional): A timestamp at which to stop listing settlement transactions
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/{settlement_id}/transactions"
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            return self.get(util.handle_query_params(path, params))
        return self.get(path)
