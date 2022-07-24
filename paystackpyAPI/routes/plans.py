from ..utilities import settings, util, decorators
from ..utilities.request import Request


@decorators.class_type_checker
class Plan(Request):

    """
    The Plans API allows you create and manage installment payment options on your integration
    """

    path = '/plan'

    def create(self, name: str, amount: int, interval: str, description: str = None, send_invoices: bool = None, send_sms: bool = None, currency: str = None, invoice_limit: int = None):
        """Create a plan on your integration

        Args:
            name (str): Name of plan
            amount (int): Amount should be in kobo if currency is NGN, pesewas,
                if currency is GHS, and cents, if currency is ZAR
            interval (str): Interval in words. Valid intervals are: daily, weekly, monthly,biannually, annually.
            description (str, optional): A description for this plan. Defaults to None.
            send_invoices (bool, optional): Set to false if you don't want invoices to be sent to your customers. Defaults to None.
            send_sms (bool, optional): Set to false if you don't want text messages to be sent to your customers. Defaults to None.
            currency (str, optional): Currency in which amount is set.
                Allowed values are NGN, GHS, ZAR or USD. Defaults to None.
            invoice_limit (int, optional): Number of invoices to raise during subscription to this plan.
                Can be overridden by specifying an invoice_limit while subscribing.. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        payload = util.generate_payload(locals(), 'interval', 'currency')
        payload['interval'] = util.check_membership(
            settings.PLAN_INTERVALS, interval, 'interval')
        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        return self.post(self.path, payload=payload)

    def list_plans(self, per_page: int = None, page: int = None, status: str = None, interval: str = None, amount: int = None):
        """List plans available on your integration.

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50.
            page (int, optional): Specify exactly what page you want to retrieve.
                If not specify we use a default value of 1.
            status (str, optional): Filter list by plans with specified status. Defaults to None.
            interval (str, optional): Filter list by plans with specified interval. Defaults to None.
            amount (int, optional): Filter list by plans with specified amount
                ( kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR). Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        params = util.check_query_params(per_page=per_page, page=page)

        if interval:
            params['interval'] = util.check_membership(
                settings.PLAN_INTERVALS, interval, 'interval')

        if status:
            params['status'] = util.check_membership(
                settings.PLAN_STATUSES, status, 'status')

        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, plan: int | str):
        """Get details of a plan on your integration.

        Args:
            plan (int | str): The plan ID or code you want to fetch.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{util.id_or_code(plan, data=settings.PLAN)}'

        return self.get(path)

    def update(self, plan: int | str, name: str = None, amount: int = None, interval: str = None, description: str = None, currency: str = None, send_invoices: bool = None, send_sms: bool = None, invoice_limit: int = None):
        """Update a plan details on your integration.

        Args:
            plan (int | str): Code or ID of the plan to update.
            name (str, optional): Name of plan. Defaults to None.
            amount (int, optional): Amount should be in kobo if currency is NGN and pesewas for GHS. Defaults to None.
            interval (str, optional): Interval in words. Valid intervals are hourly, daily, weekly, monthly,biannually, annually. Defaults to None.
            description (str, optional): A description for this plan. Defaults to None.
            send_invoices (bool, optional): Set to false if you don't want invoices to be sent to your customers. Defaults to None.
            send_sms (bool, optional): Set to false if you don't want text messages to be sent to your customers. Defaults to None.
            currency (str, optional): Currency in which amount is set. Any of NGN, GHS, ZAR or USD. Defaults to None.
            invoice_limit (int, optional): Number of invoices to raise during subscription to this plan.
                Can be overridden by specifying an invoice_limit while subscribing.. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{util.id_or_code(plan, data=settings.PLAN)}'
        payload = util.generate_payload(
            locals(), 'plan_id', 'plan_code', 'interval', 'currency')

        if interval:
            payload['interval'] = util.check_membership(
                settings.PLAN_INTERVALS, interval, 'interval')

        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        return self.put(path, payload=payload)
