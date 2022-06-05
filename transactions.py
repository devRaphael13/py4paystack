import json
import datetime
from .request import Request
from . import util


class Transaction(Request):

    """
    Accept payment from your customers
    """

    path = '/transaction'

    def __init__(self, secret_key: str) -> None:
        self.secret_key = secret_key

    def initialize(self, email: str, amount: int, currency: str, redirect_url: str, reference: str = None, plan: str = None, channels: str | list = None, split_code: str = None, transaction_charge: int = None, subaccount: str = None, bearer: str = 'account', metadata: dict = None):
        path = f'{self.path}/initialize'

        assert isinstance(
            redirect_url, str), "Provide a valid url on your server that the user will redirect to after payment eg. https://your_domain.com/wherever"
        assert isinstance(
            reference, str), "Provide a unique reference string that will be used for identification"

        payload = {
            'amount': amount,
            'email': util.check_email(email),
            'currency': util.check_currency(currency),
            'reference': reference if reference else util.create_ref(),
            'callback_url': redirect_url
        }

        if plan:
            assert plan.startswith(
                'PLN_'), "Invalid plan code: plan code must start with 'PLN_'"
            payload.pop('amount')
            payload['plan'] = plan

        if channels:
            payload['channels'] = util.check_channels(channels)

        if split_code:
            payload['split_code'] = util.check_split_code(split_code)

        if transaction_charge:
            payload['transaction_charge'] = transaction_charge

        if subaccount:
            payload['subaccount'] = util.check_subaccount(subaccount)
            if bearer:
                payload['bearer'] = util.check_bearer(bearer)
        if metadata:
            payload['metadata'] = json.dumps(metadata)

        return self.post(path, self.secret_key, payload)

    def verify(self, reference: str):
        path = f'{self.path}/verify/{reference}'
        assert isinstance(reference, str), 'reference must be of type str'
        return self.get(path, self.secret_key)

    def list_transactions(self, per_page: int = None, page: int = None, customer: int = None, status: str = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None, amount: int = None):
        path = self.path
        params = util.handle_query_params(per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        params.update({ key: value for key, value in locals().items() if value and key not in params })

        if status:
            params['status'] = util.check_transaction_status(status)
            
        if any(params.values()):
            path += '?'
            for key, value in params.items():
                path += f"{key}={value}&"
        return self.get(path.rstrip('&'), self.secret_key)

    def fetch(self, transaction_id: int):
        path = f'{self.path}/{transaction_id}'
        return self.get(path, self.secret_key)

    def check_authorization(self, email: str, amount: int, authorization_code: str, currency: str):
        path = f'{self.path}/check_authorization'

        payload = {
            'email': util.check_email(email),
            'amount': amount,
            'authorization_code': util.check_auth_code(authorization_code),
            'currency': util.check_currency(currency)
        }
        return self.post(path, self.secret_key, payload)

    def charge_authorization(self, email: str, amount: int, authorization_code: str, currency: str, reference: str = None, channels: list | str = None, queue: bool = False, split_code: str = None, subaccount: str = None, transaction_charge: int = None, bearer: str = 'account'):
        path = f'{self.path}/charge_authorization'

        payload = {
            'email': util.check_email(email),
            'amount': amount,
            'authorization_code': util.check_auth_code(authorization_code),
            'reference': reference if reference else util.create_ref(),
            'currency': util.check_currency(currency)
        }

        if channels:
            payload.update(util.check_channels(channels))

        if queue:
            payload['queue'] = True

        if split_code:
            payload['split_code'] = util.check_split_code(split_code)

        if subaccount:
            payload['subaccount'] = util.check_subaccount(subaccount)
            if bearer:
                payload['bearer'] = util.check_bearer(bearer)

        if transaction_charge:
            payload['transaction_charge'] = transaction_charge

        return self.post(path, self.secret_key, payload)

    def part_payment(self, email: str, amount: int, currency: str, authorization_code: str, reference: str = None, at_least: str = None):
        path = f'{self.path}/part_debit'
        payload = {
            'email': util.check_email(email),
            'amount': amount,
            'currency': currency,
            'authorization_code': util.check_auth_code(authorization_code),
            'reference': reference if reference else util.create_ref()
        }

        if at_least:
            assert isinstance(at_least, str), "'at_least' must be of type str"
            assert at_least.isdigit(), "Invalid at_least value eg. '12000'"
            payload['at_least'] = at_least

        return self.post(path, self.secret_key, payload)

    def totals(self, per_page: int = None, page: int = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None):
        path = f'{self.path}/totals'
        params = util.handle_query_params(per_page=per_page, page=page, from_date=from_date, to_date=to_date).values()
        if any(params):
            for value in params:
                path += f'/{value}'
        return self.get(path, self.secret_key)

    def timeline(self, id_or_reference: int | str = None):
        path = f"{self.path}/timeline/{id_or_reference}" if id_or_reference else '/timeline'
        return self.get(path, self.secret_key)

    def export(self, per_page: int = None, page: int = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None, status: str = None, currency: str = None, amount: int = None, settled: bool = None, settlement: int = None, payment_page: int = None):
        path = f'{self.path}/export'
        params = util.handle_query_params(per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        params.update({ key: value for key, value in locals().items() if value and key not in params })
        
        if currency:
            params['currency'] = util.check_currency(currency)
        
        if status:
            params['status'] = util.check_transaction_status(status)

        if any(params.values()):
            path += '?'
            for key, value in params.items():
                path += f"{key}={value}&"
        return self.get(path.rstrip('&'), self.secret_key)
