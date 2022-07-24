from datetime import date, datetime

from ..utilities import settings, util, decorators
from ..utilities.request import Request


@decorators.class_type_checker
class Refund(Request):

    """The Refunds API allows you create and manage transaction refunds
    """

    path = '/refund'

    def create(self, transaction: str | int, amount: int = None, currency: str = None, customer_note: str = None, merchant_note: str = None):
        """Initiate a refund on your integration

        Args:
            transaction (str | int): Transaction reference or id
            amount (int, optional): Amount ( in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR ) to be refunded to the customer. Amount is optional(defaults to original transaction amount) and cannot be more than the original transaction amount.. Defaults to None.
            currency (str, optional): Three-letter ISO currency. Allowed values are: NGN, GHS, ZAR or USD. Defaults to None.
            customer_note (str, optional): Customer reason. Defaults to None.
            merchant_note (str, optional): Merchant reason. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        payload = util.generate_payload(locals(), 'currency')

        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        return self.post(self.path, payload)

    def list_refunds(self, reference: str = None, currency: str = None, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date:  date | datetime | str = None):
        """List refunds available on your integration.

        Args:
            reference (str, optional): Identifier for transaction to be refunded. Defaults to None.
            currency (str, optional): Three-letter ISO currency.
                Allowed values are: NGN, GHS, ZAR or USD. Defaults to None.
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50.. Defaults to None.
            page (int, optional): Specify exactly what refund you want to page.
                If not specify we use a default value of 1.. Defaults to None.
            from_date (date | datetime | str, optional): A timestamp from which to start listing refund
                e.g. 2016-09-21. Defaults to None.
            to_date (date | datetime | str, optional): A timestamp at which to stop listing refund
                e.g. 2016-09-21. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)

        if reference:
            params['reference'] = reference

        if currency:
            params['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if params:
            path = util.handle_query_params(self.path, params)
            return self.get(path)
        return self.get(self.path)

    def fetch(self, reference: str):
        """Get details of a refund on your integration.

        Args:
            reference (str): Identifier for transaction to be refunded

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{reference}'
        return self.get(path)
