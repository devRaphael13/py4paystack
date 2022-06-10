from datetime import date, datetime

from . import settings, util
from .request import Request


class TransferRecipient(Request):

    """
    The Transfer Recipients API allows you create and manage beneficiaries that you send money to
    """

    path = '/transferrecipient'

    def __init__(self, secret_key: str) -> None:
        self.secret_key = secret_key

    @staticmethod
    def get_payload(payload: dict):
        payload = {key: value for key, value in payload if value is not None}
        if not ('recipient_type' or 'type') in payload:
            raise ValueError(
                f"missing arguments: provide recipient_type or type based on the type of recipient you want to create, your choices are: {', '.join(settings.RECIPIENT_TYPES)}")

        payload['type'] = util.check_recipient_type(payload.pop(
            'recipient_type')) if 'recipient_type' in payload else util.check_recipient_type(payload['type'])

        r_type = payload.get('type')

        if r_type == 'authorization':
            if not ('email' and 'authorization_code') in payload:
                raise ValueError(
                    "missing arguments: provide email and authorization_code params")

            payload['email'] = util.check_email(payload.pop('email'))
            payload['authorization_code'] = util.check_code(
                settings.CODE_NAMES['authorization'], payload.pop('authorization_code'))

            for x in ('bank_code', 'account_number'):
                if x in payload:
                    payload.pop(x)

        elif r_type in ('basa', 'nuban', 'mobile_money'):
            if not ('bank_code' and 'account_number') in payload:
                raise ValueError(
                    "missing arguments: provide bank_code and account_number")

            payload['bank_code'] = util.check_bank_code(
                payload.pop('bank_code'))
            payload['account_number'] = util.check_account_number(
                payload.pop('account_number'))

            for x in ('authorization_code', 'email'):
                if x in payload:
                    payload.pop(x)

        currency = payload.get('currency')
        if currency:
            payload['currency'] = util.check_currency(currency)

        return payload

    def create(self, recipient_type: str, name: str, email: str = None, account_number: str = None, bank_code: str = None, description: str = None, currency: str = None, authorization_code: str = None, metadata: dict = None):
        return self.post(self.path, self.secret_key, self.get_payload(locals()))

    def bulk_create(self, *recipients: dict[str]):
        path = f"{self.path}/bulk"
        payload = {
            'batch': [self.get_payload(recipient) for recipient in recipients]
        }
        return self.post(path, self.secret_key, payload)

    def list_recipients(self, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None):
        path = self.path
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            path = util.handle_query_params(path, params)
        return self.get(path, self.secret_key)

    def fetch(self, recipient_id: int = None, recipient_code: str = None):
        path = self.path

        if not (recipient_id or recipient_code):
            raise ValueError("provide either recipient_id or recipient_code")

        if recipient_id:
            path += f'/{recipient_id}'

        if recipient_code and not recipient_id:
            path += f"/{util.check_code(settings.CODE_NAMES['recipient'], recipient_code)}"

        return self.get(path, self.secret_key)

    def update(self, recipient_id: int = None, recipient_code: str = None, name: str = None, email: str = None):
        path = self.path

        if not (recipient_id or recipient_code):
            raise ValueError("provide either recipient_id or recipient_code")

        if recipient_id:
            path += f'/{recipient_id}'

        if recipient_code and not recipient_id:
            path += f"/{util.check_code(settings.CODE_NAMES['recipient'], recipient_code)}"

        payload = {}

        if name:
            payload['name'] = name

        if email:
            payload['email'] = util.check_email(email)

        return self.put(path, self.secret_key, payload)

    def delete(self, recipient_id: int = None, recipient_code: str = None):
        path = self.path

        if not (recipient_id or recipient_code):
            raise ValueError("provide either recipient_id or recipient_code")

        if recipient_id:
            path += f'/{recipient_id}'

        if recipient_code and not recipient_id:
            path += f"/{util.check_code(settings.CODE_NAMES['recipient'], recipient_code)}"

        return super().delete(path, self.secret_key)
