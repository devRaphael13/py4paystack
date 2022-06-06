import datetime
from . import util
from .request import Request
from . import settings

class Customer(Request):

    """
    The Customers class allows you create and manage customers on your integration.
    """

    path = '/customer'

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create(self, email: str, first_name: str, last_name: str, phone: int = None, metadata: dict = None):
        payload = locals()
        payload['email'] = util.check_email(email)
        if phone:
            payload['phone'] = f'+{phone}'
        self.post(self.path, self.secret_key, payload)

    def list_customers(self, per_page: int = None, page: int = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None):
        path = self.path
        params = util.handle_query_params(per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            path += '?'
            for key, value in params.items():
                path += f"{key}={value}&"
        return self.get(path.rstrip('&'), self.secret_key)

    def fetch(self, email_or_customer_code: str):
        path = f'{self.path}/{util.check_email_or_customer(email_or_customer_code)}'
        return self.get(path, self.secret_key)

    def update(self, customer_code: str, first_name: str = None, last_name: str = None, phone: int = None, metadata: dict = None):
        path = f'{self.path}/{util.check_code(settings.CODE_NAMES["customer"], customer_code)}'
        payload = locals()
        payload.pop(customer_code)
        payload['phone'] = f'+{phone}'
        return self.put(path, self.secret_key, payload=payload)

    def validate(self, customer_code: str, first_name: str, last_name: str, identification_type: str, country: str, bvn: str, bank_code: str = None, account_number: str = None, middle_name: str = None):
        path = f'{self.path}/{util.check_code(settings.CODE_NAMES["customer"], customer_code)}/identification'
        payload = {
            'first_name': first_name,
            'last_name': last_name,
            'type': util.check_identification_type(identification_type),
            'country': util.check_country(country),
            'bvn': util.check_bvn(bvn)
        }

        if payload['type'] == 'bank_account':
            assert bank_code is not None, "You'll need the customers bank_code for this type of verification"
            assert account_number is not None, "You'll need the customer's account number for this type of verification"
            payload.update(
                {'bank_code': bank_code, 'account_number': account_number})

        if middle_name is not None:
            payload['middle_name'] = middle_name

        return self.post(path, self.secret_key, payload=payload)

    def whitelist_blacklist(self, email_or_customer_code, risk_action):
        path = f'{self.path}/set_risk_action'

        payload = {
            'risk_action': util.check_risk_action(risk_action),
            'customer': util.check_email_or_customer(email_or_customer_code)
        }

        return self.post(path, self.secret_key, payload=payload)

    def deactivate_authorization(self, authorization_code: str):
        path = f'{self.path}/deactivate_authorization'

        payload = {'authorization_code': util.check_code(settings.CODE_NAMES['authorization'], authorization_code)}

        return self.post(path, self.secret_key, payload=payload)
