import datetime

from ..utilities import settings, util, decorators
from ..utilities.request import Request


@decorators.class_type_checker
class Customer(Request):

    """
    The Customers class allows you create and manage customers on your integration.
    """

    path = '/customer'

    def create(self, email: str, first_name: str = None, last_name: str = None, phone: str = None, metadata: dict = None):
        """Create a customer on your integration. The first_name, last_name and phone are optional parameters.
            However, when creating a customer that would be assigned a Dedicated Virtual Account and your business catgeory falls under Betting,
            Financial services, and General Service, then these parameters become compulsory.

        Args:
            email (str): Customer's email address.
            first_name (str, optional): Customer's first name. Defaults to None.
            last_name (str, optional): Customer's last name. Defaults to None.
            phone (str, optional): Customer's phone number. Defaults to None.
            metadata (dict, optional): A set of key/value pairs that you can attach to the customer.
                It can be used to store additional information in a structured format. Defaults to None.

        Returns:
            JSON: Data fetched from API.
        """

        payload = util.generate_payload(locals(), 'email')
        payload['email'] = util.check_email(email)
        return self.post(self.path, payload)

    def list_customers(self, per_page: int = None, page: int = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None):
        """List customers available on your integration.

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50. Defaults to None.
            page (int, optional): Specify exactly what page you want to retrieve.
                If not specify we use a default value of 1. Defaults to None.
            from_date (datetime.datetime | datetime.date | str, optional): A timestamp from which to start listing customers
                e.g. 2016-09-24T00:00:05.000Z, 2016. Defaults to None.
            to_date (datetime.datetime | datetime.date | str, optional): A timestamp at which to stop listing customers
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, email_or_customer_code: str):
        """Get details of a customer on your integration.

        Args:
            email_or_customer_code (str): An email or customer code for the customer you want to fetch

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{util.check_email_or_customer(email_or_customer_code)}'
        return self.get(path)

    def update(self, customer_code: str, first_name: str = None, last_name: str = None, phone: str = None, metadata: dict = None):
        """Update a customer's details on your integration

        Args:
            customer_code (str): Code for the customer you want to update.
            first_name (str, optional): Customer's first name. Defaults to None.
            last_name (str, optional): Customer's last name. Defaults to None.
            phone (str, optional): Customer's phone number. Defaults to None.
            metadata (dict, optional): A set of key/value pairs that you can attach to the customer.
                It can be used to store additional information in a structured format. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{util.check_code(settings.CUSTOMER, customer_code)}'
        payload = util.generate_payload(locals(), 'customer_code')
        return self.put(path, payload=payload)

    def validate(self, customer_code: str, first_name: str, last_name: str, identification_type: str, country: str, bvn: str, bank_code: str = None, account_number: str = None, middle_name: str = None):
        """Validate a customer's identity

        Args:
            customer_code (str): Code for the customer you want to validate
            first_name (str): Customer's first name
            last_name (str): Customer's last name
            identification_type (str): Predefined types of identification. Valid values: bvn, bank_account
            country (str): 2 letter country code of identification issuer
            bvn (str): Customer's Bank Verification Number
            bank_code (str, optional): You can get the list of Bank Codes by calling the List Banks endpoint. (required if type is bank_account). Defaults to None.
            account_number (str, optional): Customer's bank account number. (required if type is bank_account). Defaults to None.
            middle_name (str, optional): Customer's middle name. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{util.check_code(settings.CUSTOMER, customer_code)}/identification'
        payload = {
            'first_name': first_name,
            'last_name': last_name,
            'type': util.check_membership(settings.IDENTIFICATION_TYPES, identification_type, 'identification_type'),
            'country': util.check_country(country),
            'bvn': util.check_bvn(bvn)
        }

        if payload['type'] == 'bank_account':
            assert bank_code and account_number, "You'll need the customers bank_code and account_number for this type of verification"
            payload.update(
                {'bank_code': bank_code, 'account_number': account_number})

        if middle_name is not None:
            payload['middle_name'] = middle_name

        return self.post(path, payload=payload)

    def whitelist_blacklist(self, email_or_customer_code: str, risk_action: str):
        """Whitelist or blacklist a customer on your integration

        Args:
            email_or_customer_code (str): Customer's code or email address
            risk_action (str): One of the possible risk actions [ default, allow, deny ].
                allow to whitelist. deny to blacklist. Customers start with a default risk action.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/set_risk_action'

        payload = {
            'risk_action': util.check_membership(settings.RISK_ACTIONS, risk_action, 'risk_action'),
            'customer': util.check_email_or_customer(email_or_customer_code)
        }

        return self.post(path, payload=payload)

    def deactivate_authorization(self, authorization_code: str):
        """Deactivate an authorization when the card needs to be forgotten

        Args:
            authorization_code (str): Authorization code for a card that needs to be forgotten.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/deactivate_authorization'

        payload = {'authorization_code': util.check_code(
            settings.AUTHORIZATION, authorization_code)}

        return self.post(path, payload=payload)
