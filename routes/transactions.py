import datetime
import json

from .utilities import settings, util
from .utilities.request import Request


class Transaction(Request):

    """
    Accept payment from your customers
    """

    path = '/transaction'

    def initialize(self, email: str, amount: int, redirect_url: str, reference: str = None, currency: str = None, plan: str = None, channels: str | list = None, split_code: str = None, transaction_charge: int = None, subaccount: str = None, bearer: str = 'account', metadata: dict = None, generate_reference: bool = False):
 
        path = f'{self.path}/initialize'

        payload = {
            'amount': amount,
            'email': util.check_email(email),
            'callback_url': redirect_url
        }

        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if reference:
            payload['reference'] = reference

        if not reference and generate_reference:
            payload['reference'] = util.create_ref()

        if plan:
            payload.pop('amount')
            payload['plan'] = util.check_code(
                settings.PLAN, plan)

        if channels:
            payload['channels'] = util.check_channels(channels)

        if split_code:
            payload['split_code'] = util.check_code(
                settings.SPLIT, split_code)

        if transaction_charge:
            payload['transaction_charge'] = transaction_charge

        if subaccount:
            payload['subaccount'] = util.check_code(
                settings.SUBACCOUNT, subaccount)
            if bearer:
                payload['bearer'] = util.check_membership(
                    settings.BEARER_TYPES, bearer, 'bearer_type')

        if metadata:
            payload['metadata'] = json.dumps(metadata)

        return self.post(path, payload=payload)

    def verify(self, reference: str):
        path = f'{self.path}/verify/{reference}'
        return self.get(path)

    def list_transactions(self, per_page: int = None, page: int = None, customer: int = None, status: str = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None, amount: int = None):
        params = util.generate_payload(locals())
        params.update(util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date))

        if status:
            params['status'] = util.check_membership(
                settings.TRANSACTION_STATUS, status, 'status')

        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, transaction_id: int):
        path = f'{self.path}/{transaction_id}'
        return self.get(path)

    def check_authorization(self, email: str, amount: int, authorization_code: str, currency: str = None):
        path = f'{self.path}/check_authorization'

        payload = {
            'email': util.check_email(email),
            'amount': amount,
            'authorization_code': util.check_code(settings.AUTHORIZATION, authorization_code)
        }

        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        return self.post(path, payload=payload)

    def charge_authorization(self, email: str, amount: int, authorization_code: str, currency: str = None, reference: str = None, channels: list | str = None, queue: bool = False, split_code: str = None, subaccount: str = None, transaction_charge: int = None, bearer: str = 'account', generate_reference: bool = False):
        path = f'{self.path}/charge_authorization'

        payload = {
            'email': util.check_email(email),
            'amount': amount,
            'authorization_code': util.check_code(settings.AUTHORIZATION, authorization_code),
        }

        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if reference:
            payload['reference'] = reference

        if not reference and generate_reference:
            payload['reference'] = util.create_ref()

        if channels:
            payload.update(util.check_channels(channels))

        if queue:
            payload['queue'] = True

        if split_code:
            payload['split_code'] = util.check_code(
                settings.SPLIT, split_code)

        if subaccount:
            payload['subaccount'] = util.check_code(
                settings.SUBACCOUNT, subaccount)
            if bearer:
                payload['bearer'] = util.check_membership(
                    settings.BEARER_TYPES, bearer, 'bearer_type')

        if transaction_charge:
            payload['transaction_charge'] = transaction_charge

        return self.post(path, payload=payload)

    def partial_debit(self, email: str, amount: int, currency: str, authorization_code: str, reference: str = None, at_least: str = None, generate_reference: bool = False):
        path = f'{self.path}/part_debit'
        payload = {
            'email': util.check_email(email),
            'amount': amount,
            'currency': util.check_membership(settings.CURRENCIES, currency, 'currency'),
            'authorization_code': util.check_code(settings.AUTHORIZATION, authorization_code),
        }

        if reference:
            payload['reference'] = reference

        if not reference and generate_reference:
            payload['reference'] = util.create_ref()

        if at_least:
            assert at_least.isdigit(), "Invalid at_least value eg. '12000'"
            payload['at_least'] = at_least

        return self.post(path, payload=payload)

    def totals(self, per_page: int = None, page: int = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None):
        path = f'{self.path}/totals'
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date).values()
        if params:
            return self.get(util.handle_query_params(path, params))
        return self.get(path)

    def timeline(self, id_or_reference: int | str = None):
        path = f"{self.path}/timeline/{id_or_reference}" if id_or_reference else '/timeline'
        return self.get(path)

    def export(self, per_page: int = None, page: int = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None, status: str = None, currency: str = None, amount: int = None, settled: bool = None, settlement: int = None, payment_page: int = None):
        params = util.generate_payload(locals())
        params.update(util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date))

        if currency:
            params['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if status:
            params['status'] = util.check_membership(
                settings.TRANSACTION_STATUS, status, 'status')

        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)
