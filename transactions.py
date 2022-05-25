import uuid
import re
import json
from .request import Request


class Transaction(Request):

    """
    Accept payment from your customers
    """

    path = '/transaction'

    def __init__(self, secret_key: str) -> None:
        self.secret_key = secret_key

    @staticmethod
    def check_email(email):
        if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-z|a-z]{2,}\b', email):
            return True
        return False

    @staticmethod
    def create_ref():
        return str(uuid.uuid4()).replace('-', '')

    @staticmethod
    def channels(channel):
        assert isinstance(
            channel, (list, str)), f"Provide a string (if you are going to use one channel) or list of payment option(s) you're willing to support, your choices are: { ', '.join(channel)}"
        channels = ['card', 'bank', 'ussd', 'qr',
                    'mobile_money', 'bank_transfer']
        message = f"Invalid payment channel, choices are: {', '.join(channels)}"
        if isinstance(channel, list):
            assert set(channel).issubset(
                channels), message
        else:
            assert channel in channels, message
            channel = [channel]
        return {'channels': channel}

    @staticmethod
    def camel_case(string: str):
        string = string.split('_')
        result = string[0]
        if len(string) > 1:
            _, *rest = string
            result += f"{''.join(( x.title() for x in rest ))}"
        return result

    @staticmethod
    def currency(currency):
        currencies = {'GHS', 'NGN', 'USD', 'ZAR'}
        assert currency in currencies, f"Invalid currency: choices are {', '.join(currencies)}"
        return currency

    @staticmethod
    def split_code(split_code):
        assert isinstance(
            split_code, str), "split_code must be of type str"
        assert split_code.startswith(
            'SPL_'), "Invalid split code: split code must start with 'SPL_'"
        return {'split_code': split_code}

    @staticmethod
    def transaction_charge(transaction_charge):
        assert isinstance(
            transaction_charge, int), "transaction_charge must be of type int"
        return {'transaction_charge': transaction_charge}

    @staticmethod
    def subaccount(subaccount, bearer='account'):
        bearers = ['account', 'subaccount']
        assert isinstance(
            subaccount, str), "subaccount must be of type str"
        assert subaccount.startswith(
            'ACCT_'), "Invalid subaccount code: sub account must startwith 'ACCT_'"
        if bearer != 'account':
            assert bearer in bearers, f"Invalid bearer: choices are {', '.join(bearers)}"
        return {'subaccount': subaccount, 'bearer': bearer}

    def initialize(self, email: str, amount: int, currency: str, redirect_url: str, reference: str = None, plan: str = None, channels: str | list = None, split_code: str = None, transaction_charge: int = None, subaccount: str = None, bearer: str = 'account', metadata: dict = None):
        path = '/initialize'

        assert self.check_email(email), "Provide a valid email"
        assert isinstance(amount, int), "amount must be of type int"
        assert isinstance(
            redirect_url, str), "Provide a valid url on your server that the user will redirect to after payment eg. https://your_domain.com/wherever"
        assert isinstance(
            reference, str), "Provide a unique reference string that will be used for identification"

        payload = {
            'amount': amount,
            'email': email,
            'currency': self.currency(currency).upper(),
            'reference': reference if reference else self.create_ref(),
            'callback_url': redirect_url
        }

        if plan:
            assert plan.startswith(
                'PLN_'), "Invalid plan code: plan code must start with 'PLN_'"
            payload.pop('amount')
            payload['plan'] = plan

        if channels:
            payload.update(self.channels(channels))

        if split_code:
            payload.update(self.split_code(split_code))

        if transaction_charge:
            payload.update(self.transaction_charge(transaction_charge))

        if subaccount:
            payload.update(self.subaccount(subaccount, bearer))

        if metadata:
            payload['metadata'] = json.dumps(metadata)

        return self.post(path, self.secret_key, payload)

    def verify(self, reference: str):
        path = f'/verify/{reference}'
        assert isinstance(reference, str), 'reference must be of type str'
        return self.get(path, self.secret_key)

    def list_transactions(self, per_page: int = None, page: int = None, customer: int = None, status: str = None, from_date: str = None, to_date: str = None, amount: int = None ):
        path = '/'
        args = locals()
        if any(args.values()):
            args['from'] = args.pop('from_date')
            args['to'] = args.pop('to_date')
            for key, value in args.items():
                path += f"?{self.camel_case(key)}={value}&"
            return self.get(path.rstrip('&'), self.secret_key)
        return self.get(path, self.secret_key)

    def fetch(self, transaction_id: int):
        path = f'/{transaction_id}'
        return self.get(path, self.secret_key)

    def check_auth(self, email: str, amount: int, auth_code: str, currency: str):
        path = '/check_authorization'

        assert self.check_email(email), "Provide a valid email"
        assert isinstance(auth_code, str) and auth_code.startswith(
            'AUTH_'), "Provide a valid Authorization code"
        assert isinstance(amount, int), "amount must be of type int"

        payload = {
            'email': email,
            'amount': amount,
            'authorization_code': auth_code,
            'currency': self.currency(currency).upper()
        }
        return self.post(path, self.secret_key, payload)

    def charge_auth(self, email: str, amount: int, auth_code: str, currency: str, reference: str = None, channels: list | str = None, queue: bool = False, split_code: str = None, subaccount: str = None, transaction_charge: int = None, bearer: str = 'account'):
        path = '/charge_authorization'

        assert self.check_email(email), "Provide a valid email"
        assert isinstance(auth_code, str) and auth_code.startswith(
            'AUTH_'), "Provide a valid Authorization code"
        assert isinstance(amount, int), "amount must be of type int"

        payload = {
            'email': email,
            'amount': amount,
            'authorization_code': auth_code,
            'reference': reference if reference else self.create_ref(),
            'currency': self.currency(currency).upper()
        }

        if channels:
            payload.update(self.channels(channels))

        if queue:
            payload['queue'] = True

        if split_code:
            payload.update(self.split_code(split_code))

        if subaccount:
            payload.update(self.subaccount(subaccount, bearer))

        if transaction_charge:
            payload.update(self.transaction_charge(transaction_charge))

        return self.post(path, self.secret_key, payload)

    def part_payment(self, email: str, amount: int, currency: str, auth_code: str, reference: str = None, at_least: str = None):
        path = '/part_debit'
        assert self.check_email(email), "Provide a valid email"
        assert isinstance(auth_code, str) and auth_code.startswith(
            'AUTH_'), "Provide a valid Authorization code"
        assert isinstance(amount, int), "amount must be of type int"

        payload = {
            'email': email,
            'amount': amount,
            'currency': currency,
            'auth_code': auth_code,
            'reference': reference if reference else self.create_ref()
        }

        if at_least:
            assert isinstance(at_least, str), "'at_least' must be of type str"
            assert at_least.isdigit(), "Invalid at_least value eg. '12000'"
            payload['at_least'] = at_least

        return self.post(path, self.secret_key, payload)

    def totals(self, per_page: int = None, page: int = None):
        path = '/totals'
        args = locals()
        if any(args.values()):
            # args['from'] = args.pop('from_date')
            # args['to'] = args.pop('to_date')
            for key, value in args.items():
                path += f"?{self.camel_case(key)}={value}&"
            return self.get(path.rstrip('&'), self.secret_key)
        return self.get(path, self.secret_key)

    def timeline(self, id_or_reference: int | str = None,  per_page: int = None, page: int = None):
        path = f"/timeline/{id_or_reference}" if id_or_reference else '/timeline'
        return self.get(path, self.secret_key)

    def export(self, **kwargs):
        path = 'export/'
        args = locals()

        if any(args.values()):
            # args['from'] = args.pop('from_date')
            # args['to'] = args.pop('to_date')
            for key, value in args.items():
                path += f"?{self.camel_case(key)}={value}&"
            return self.get(path.rstrip('&'), self.secret_key)
        return self.get(path, self.secret_key)
