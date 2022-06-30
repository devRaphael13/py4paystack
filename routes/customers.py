import datetime

from .utilities import settings, util
from .utilities.request import Request


class Customer(Request):

    """
    The Customers class allows you create and manage customers on your integration.
    """

    path = '/customer'

    def create(self, email: str, first_name: str, last_name: str, phone: str = None, metadata: dict = None):
        payload = util.generate_payload(locals())
        payload['email'] = util.check_email(email)
        self.post(self.path, payload)

    def list_customers(self, per_page: int = None, page: int = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None):
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, email_or_customer_code: str):
        path = f'{self.path}/{util.check_email_or_customer(email_or_customer_code)}'
        return self.get(path)

    def update(self, customer_code: str, first_name: str = None, last_name: str = None, phone: str = None, metadata: dict = None):
        path = f'{self.path}/{util.check_code(settings.CUSTOMER, customer_code)}'
        payload = util.generate_payload(locals(), 'path', 'customer_code')
        return self.put(path, payload=payload)

    def validate(self, customer_code: str, first_name: str, last_name: str, identification_type: str, country: str, bvn: str, bank_code: str = None, account_number: str = None, middle_name: str = None):
        path = f'{self.path}/{util.check_code(settings.CUSTOMER, customer_code)}/identification'
        payload = {
            'first_name': first_name,
            'last_name': last_name,
            'type': util.check_membership(settings.IDENTIFICATION_TYPES, identification_type, 'identification_type'),
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

        return self.post(path, payload=payload)

    def whitelist_blacklist(self, email_or_customer_code, risk_action):
        path = f'{self.path}/set_risk_action'

        payload = {
            'risk_action': util.check_membership(settings.RISK_ACTIONS, risk_action, 'risk_action'),
            'customer': util.check_email_or_customer(email_or_customer_code)
        }

        return self.post(path, payload=payload)

    def deactivate_authorization(self, authorization_code: str):
        path = f'{self.path}/deactivate_authorization'

        payload = {'authorization_code': util.check_code(
            settings.AUTHORIZATION, authorization_code)}

        return self.post(path, payload=payload)
