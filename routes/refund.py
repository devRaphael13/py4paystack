from datetime import date, datetime

from .utilities import settings, util, decorators
from .utilities.request import Request


@decorators.class_type_checker
class Refund(Request):

    """The Refunds API allows you create and manage transaction refunds
    """

    path = '/refund'

    def create(self, transaction: str | int, amount: int = None, currency: str = None, customer_note: str = None, merchant_note: str = None):
        payload = util.generate_payload(locals())

        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        return self.post(self.path, payload)

    def list_refunds(self, reference: str = None, currency: str = None, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date:  date | datetime | str = None):
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
        path = f'{self.path}/{reference}'
        return self.get(path)
