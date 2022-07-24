import datetime

from ..utilities import settings, util, decorators
from ..utilities.request import Request


@decorators.class_type_checker
class Subscription(Request):

    """
    The Subscriptions API allows you create and manage recurring payment on your integration
    """

    path = "/subscription"

    def create(self, email_or_customer_code: str, plan_code: str, authorization_code: str = None, start_date: datetime.datetime | datetime.date | str = None):
        """Create a subscription on your integration

        Args:
            email_or_customer_code (str): Customer's email address or customer code
            plan_code (str): Plan code
            authorization_code (str, optional): If customer has multiple authorizations,
                you can set the desired authorization you wish to use for this subscription here.
                If this is not supplied, the customer's most recent authorization would be used. Defaults to None.
            start_date (datetime.datetime | datetime.date | str, optional): Set the date for the first debit. 
                (ISO 8601 format) e.g. 2017-05-16T00:30:13+01:00. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        payload = {
            'customer': util.check_email_or_customer(email_or_customer_code),
            'plan': util.check_code(settings.PLAN, plan_code)
        }

        if authorization_code:
            payload['authorization'] = util.check_code(
                settings.AUTHORIZATION, authorization_code)

        if start_date:
            payload['start_date'] = util.handle_date(start_date)

        return self.post(self.path, payload=payload)

    def list_subscriptions(self, per_page: int = None, page: int = None, customer: int = None, plan: int = None):
        """List subscriptions available on your integration.

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50.. Defaults to None.
            page (int, optional): Specify exactly what page you want to retrieve.
                If not specify we use a default value of 1.. Defaults to None.
            customer (int, optional): Filter by Customer ID. Defaults to None.
            plan (int, optional): Filter by Plan ID. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """
        params = util.generate_payload(locals())
        params.update(util.check_query_params(per_page=per_page, page=page))

        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, subscription: int | str):
        """Get details of a subscription on your integration.

        Args:
            subscription (int | str): The subscription ID or code you want to fetch.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{util.id_or_code(subscription, data=settings.SUBSCRIPTION)}'
        
        return self.get(path)

    def enable(self, subscription_code: str, email_token: str):
        """Enable a subscription on your integration

        Args:
            subscription_code (str): Subscription code
            email_token (str): Email token

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/enable"
        payload = {
            'code': util.check_code(settings.SUBSCRIPTION, subscription_code),
            'token': email_token
        }

        return self.post(path, payload)

    def disable(self, subscription_code: str, email_token: str):
        """Disable a subscription on your integration

        Args:
            subscription_code (str): Subscription code
            email_token (str): Email token


        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/disable"
        payload = {
            'code': util.check_code(settings.SUBSCRIPTION, subscription_code),
            'token': email_token
        }
        return self.post(path, payload)

    def generate_update_link(self, subscription_code: str):
        """Generate a link for updating the card on a subscription

        Args:
            subscription_code (str): Subscription code

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/{util.check_code(settings.SUBSCRIPTION, subscription_code)}/manage/link"

        return self.get(path)

    def send_update_link(self, subscription_code: str):
        """ Email a customer a link for updating the card on their subscription

        Args:
            subscription_code (str): Subscription code

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/{util.check_code(settings.SUBSCRIPTION, subscription_code)}/manage/link"

        return self.get(path)
