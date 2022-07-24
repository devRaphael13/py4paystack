import datetime

from ..utilities import settings, util, decorators
from ..utilities.request import Request


@decorators.class_type_checker
class SubAccounts(Request):

    """
    The Subaccounts API allows you create and manage subaccounts on your integration.
    Subaccounts can be used to split payment between two accounts (your main account and a sub account)
    """

    path = '/subaccount'

    def create(self, business_name: str, settlement_bank: str, account_number: str, percentage_charge: float, description: str = None, primary_contact_email: str = None, primary_contact_name: str = None, primary_contact_phone: str = None, metadata: str = None):
        """Create a subacount on your integration

        Args:
            business_name (str): Name of business for subaccount
            settlement_bank (str): Bank Code for the bank.
                You can get the list of Bank Codes by calling the List Banks endpoint.
            account_number (str): Bank Account Number
            percentage_charge (float): The default percentage charged when receiving on behalf of this subaccount
            description (str, optional): A description for this subaccount. Defaults to None.
            primary_contact_email (str, optional): A contact email for the subaccount. Defaults to None.
            primary_contact_name (str, optional): A name for the contact person for this subaccount. Defaults to None.
            primary_contact_phone (str, optional): A phone number to call for this subaccount. Defaults to None.
            metadata (str, optional): Stringified JSON object.
                Add a custom_fields attribute which has an array of objects if you would like the fields to be added to your transaction when displayed on the dashboard.
                Sample: {"custom_fields":[{"display_name":"Cart ID","variable_name": "cart_id","value": "8393"}]}.
                Defaults to None.

        Returns:
            JSON: Data fetched from API

        """

        payload = util.generate_payload(
            locals(), 'settlement_bank', 'account_number', 'primary_contact_email')
        payload['settlement_bank'] = util.check_bank_code(settlement_bank)
        payload['account_number'] = util.check_account_number(account_number)

        if primary_contact_email:
            payload['primary_contact_email'] = util.check_email(
                primary_contact_email)
        return self.post(self.path, payload=payload)

    def list_subaccounts(self, per_page: int = None, page: int = None, from_date: datetime.date | datetime.datetime | str = None, to_date: datetime.date | datetime.datetime | str = None):
        """List subaccounts available on your integration.

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50.
            page (int, optional): Specify exactly what page you want to retrieve.
                If not specify we use a default value of 1.
            from_date (datetime.date | datetime.datetime | str, optional): A timestamp from which to start listing subaccounts
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            to_date (datetime.date | datetime.datetime | str, optional): A timestamp at which to stop listing subaccounts
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, subaccount: int | str):
        """Get details of a subaccount on your integration. 

        Args:
            subaccount (int | str): The subaccount ID or code you want to fetch.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{util.id_or_code(subaccount, data=settings.SUBACCOUNT)}'

        return self.get(path)

    def update(self, subaccount: int | str, active: bool = None, business_name: str = None, settlement_bank: str = None, account_number: str = None, settlement_schedule: str = None, percentage_charge: float = None, description: str = None, primary_contact_email: str = None, primary_contact_name: str = None, primary_contact_phone: str = None, metadata: str = None):
        """Update a subaccount details on your integration.

        Args:
            subaccount (int | str): Subaccount's ID or code.
            active (bool, optional): Activate or deactivate a subaccount.
                Set value to true to activate subaccount or false to deactivate the subaccount.
            business_name (str, optional): Name of business for subaccount. Defaults to None.
            settlement_bank (str, optional): Bank Code for the bank.
                You can get the list of Bank Codes by calling the List Banks endpoint. Defaults to None.
            account_number (str, optional): Bank Account Number. Defaults to None.
            settlement_schedule (str, optional): Any of auto, weekly, `monthly`, `manual`.
                Auto means payout is T+1 and manual means payout to the subaccount should only be made when requested. Defaults to auto.
            percentage_charge (float, optional): The default percentage charged when receiving on behalf of this subaccount. Defaults to None.
            description (str, optional): A description for this subaccount. Defaults to None.
            primary_contact_email (str, optional): A contact email for the subaccount. Defaults to None.
            primary_contact_name (str, optional): A name for the contact person for this subaccount. Defaults to None.
            primary_contact_phone (str, optional): A phone number to call for this subaccount. Defaults to None.
            metadata (str, optional): Stringified JSON object. Add a custom_fields attribute which has an array of objects
                if you would like the fields to be added to your transaction when displayed on the dashboard.
                Sample: {"custom_fields":[{"display_name":"Cart ID","variable_name": "cart_id","value": "8393"}]}.
                Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{util.id_or_code(subaccount, data=settings.SUBACCOUNT)}'

        payload = util.generate_payload(
            locals(), 'subaccount_id', 'subaccount_code')

        if settlement_bank:
            payload['settlement_bank'] = util.check_bank_code(settlement_bank)

        if settlement_schedule:
            payload['settlement_schedule'] = util.check_membership(
                settings.SETTLEMENT_SCHEDULES, settlement_schedule, 'settlement_schedule')

        if account_number:
            payload['account_number'] = util.check_account_number(
                account_number)

        if primary_contact_email:
            payload['primary_contact_email'] = util.check_email(
                primary_contact_email)

        return self.put(path, payload=payload)
