import datetime
import json

from ..utilities import settings, util, decorators
from ..utilities.request import Request


@decorators.class_type_checker
class Transaction(Request):

    """
    Accept payment from your customers.
    The Transactions API allows you create and manage payments on your integration
    """

    path = '/transaction'

    def initialize(self, email: str, amount: int, callback_url: str, reference: str = None, currency: str = None, plan: str = None, invoice_limit: int = None, channels: str | list = None, split_code: str = None, transaction_charge: int = None, subaccount: str = None, bearer: str = 'account', metadata: dict = None, generate_reference: bool = False):
        """Initialize a transaction from your backend

        Args:
            email (str): Customer's email address
            amount (int): Amount should be in kobo if currency is NGN, pesewas,
                if currency is GHS, and cents, if currency is ZAR
            callback_url (str): Fully qualified url, e.g. https://example.com/ .
                Use this to override the callback url provided on the dashboard for this transaction
            reference (str, optional): Unique transaction reference.
                Only -, ., = and alphanumeric characters allowed. Defaults to None.
            currency (str, optional): The transaction currency (NGN, GHS, ZAR or USD).
                Defaults to your integration currency.. Defaults to None.
            plan (str, optional): If transaction is to create a subscription to a predefined plan, provide plan code here.
                This would invalidate the value provided in amount. Defaults to None.
            invoice_limit (int, optional): Number of times to charge customer during subscription to plan. Defaults to None.
            channels (str | list, optional): An array of payment channels ( or a string of one channel ) to control what channels you want to make available to the user to make a payment with.
                Available channels include: ['card', 'bank', 'ussd', 'qr', 'mobile_money', 'bank_transfer']. Defaults to None.
            split_code (str, optional): The split code of the transaction split. e.g. SPL_98WF13Eb3w. Defaults to None.
            transaction_charge (int, optional): An amount used to override the split configuration for a single split payment.
                If set, the amount specified goes to the main account regardless of the split configuration. Defaults to None.
            subaccount (str, optional): The code for the subaccount that owns the payment.
                e.g. ACCT_8f4s1eq7ml6rlzj. Defaults to None.
            bearer (str, optional): Who bears Paystack charges? account or subaccount (defaults to account).
            metadata (dict, optional): Stringified JSON object of custom data.
                Kindly check the Metadata page for more information.. Defaults to None.
            generate_reference (bool, optional): Would you want a reference generated for you.
                It will override the reference if provided. Defaults to False.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/initialize'

        payload = {
            'amount': amount,
            'email': util.check_email(email),
            'callback_url': callback_url
        }

        if invoice_limit:
            payload['invoice_limit'] = invoice_limit

        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if reference:
            payload['reference'] = reference

        if generate_reference:
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
        """Confirm the status of a transaction

        Args:
            reference (str): The transaction reference used to intiate the transaction

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/verify/{reference}'
        return self.get(path)

    def list_transactions(self, per_page: int = None, page: int = None, customer: int = None, status: str = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None, amount: int = None):
        """List transactions carried out on your integration.

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50.. Defaults to None.
            page (int, optional): Specify exactly what page you want to retrieve.
                If not specify we use a default value of 1.
            customer (int, optional): Specify an ID for the customer whose transactions you want to retrieve. Defaults to None.
            status (str, optional): Filter transactions by status ('failed', 'success', 'abandoned'). Defaults to None.
            from_date (datetime.datetime | datetime.date | str, optional): A timestamp from which to start listing transaction
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            to_date (datetime.datetime | datetime.date | str, optional): A timestamp at which to stop listing transaction
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            amount (int, optional): Filter transactions by amount. Specify the amount 
                (in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR). Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        params = util.generate_payload(
            locals(), 'per_page', 'page', 'status', 'from_date', 'to_date')
        params.update(util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date))

        if status:
            params['status'] = util.check_membership(
                settings.TRANSACTION_STATUS, status, 'status')

        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, transaction_id: int):
        """Get details of a transaction carried out on your integration.


        Args:
            transaction_id (int): ID of the transaction to fetch.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{transaction_id}'
        return self.get(path)

    def check_authorization(self, email: str, amount: int, authorization_code: str, currency: str = None):
        """This feature is only available to businesses in Nigeria.
            All Mastercard and Visa authorizations can be checked with this endpoint to know
            if they have funds for the payment you seek.

            This endpoint should be used when you do not know the exact amount to charge a card when rendering a service.
            It should be used to check if a card has enough funds based on a maximum range value. It is well suited for:

            Ride hailing services
            Logistics services

            WARNING.
            You shouldn't use this endpoint to check a card for sufficient funds if you are going to charge the user immediately.
            This is because we hold funds when this endpoint is called which can lead to an insufficient funds error.

        Args:
            email (str): Customer's email address
            amount (int): Amount should be in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR
            authorization_code (str): Valid authorization code to charge
            currency (str, optional): Currency in which amount should be charged. Allowed values are: NGN, GHS, ZAR or USD. Defaults to None.

        Returns:
            JSON: Data fetched from API            
        """

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

    def charge_authorization(self, email: str, amount: int, authorization_code: str, currency: str = None, reference: str = None, channels: list | str = None, queue: bool = False, split_code: str = None, subaccount: str = None, transaction_charge: int = None, bearer: str = None, metadata: dict = None, generate_reference: bool = False):
        """All authorizations marked as reusable can be charged with this endpoint whenever you need to receive payments.

        Args:
            email (str): Customer's email address
            amount (int): Amount should be in kobo if currency is NGN, pesewas,
                if currency is GHS, and cents, if currency is ZAR
            authorization_code (str): Valid authorization code to charge
            currency (str, optional): Currency in which amount should be charged.
                Allowed values are: NGN, GHS, ZAR or USD. Defaults to None.
            reference (str, optional): Unique transaction reference.
                Only -, ., = and alphanumeric characters allowed.. Defaults to None.
            channels (list | str, optional): Send us 'card' or 'bank' or 'card','bank' as an array
                ( or just a string if you plan to use one payment option )
                to specify what options to show the user paying. Defaults to None.
            queue (bool, optional): If you are making a scheduled charge call,
                it is a good idea to queue them so the processing system does not get overloaded causing transaction processing errors.
                Send queue:true to take advantage of our queued charging. Defaults to False.
            split_code (str, optional): _description_. Defaults to None.
            subaccount (str, optional): The code for the subaccount that owns the payment.
                e.g. ACCT_8f4s1eq7ml6rlzj. Defaults to None.
            transaction_charge (int, optional): A flat fee to charge the subaccount for this transaction
                (in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR).
                This overrides the split percentage set when the subaccount was created.
                Ideally, you will need to use this if you are splitting in flat rates
                (since subaccount creation only allows for percentage split).
                e.g. 7000 for a 70 naira flat fee.. Defaults to None.
            bearer (str, optional): Who bears Paystack charges? account or subaccount (defaults to account)
            metadata (dict, optional): A dictionary with custom_fields attribute which has an array of objects
                if you would like the fields to be added to your transaction when displayed on the dashboard.
                Sample: {"custom_fields":[{"display_name":"Cart ID","variable_name": "cart_id","value": "8393"}]}. Defaults to None.
            generate_reference (bool, optional): Whether to generate a reference for you. Defaults to False.

        Returns:
            JSON: Data fetched from API
        """

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
        """Retrieve part of a payment from a customer

        Args:
            email (str): Customer's email address
            amount (int): Amount should be in kobo if currency is NGN, pesewas, 
                if currency is GHS, and cents, if currency is ZAR
            currency (str): Specify the currency you want to debit. Allowed values are NGN, GHS, ZAR or USD.
            authorization_code (str): Authorization Code
            reference (str, optional): Unique transaction reference. Only -, ., = and alphanumeric characters allowed. Defaults to None.
            at_least (str, optional): Minimum amount to charge. Defaults to None.
            generate_reference (bool, optional): Whether to generate reference for you. Defaults to False.

        Returns:
            JSON: Data fetched from API
        """

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
        """Total amount received on your account

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50.
            page (int, optional): Specify exactly what page you want to retrieve.
                If not specify we use a default value of 1.
            from_date (datetime.datetime | datetime.date | str, optional): A timestamp from which to start listing transaction
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            to_date (datetime.datetime | datetime.date | str, optional): A timestamp at which to stop listing transaction
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/totals'
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date).values()
        if params:
            return self.get(util.handle_query_params(path, params))
        return self.get(path)

    def timeline(self, id_or_reference: int | str = None):
        """View the timeline of a transaction.

        Args:
            id_or_reference (int | str, optional): The ID or the reference of the transaction. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/timeline/{id_or_reference}" if id_or_reference else '/timeline'
        return self.get(path)

    def export(self, per_page: int = None, page: int = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None, customer: int = None, status: str = None, currency: str = None, amount: int = None, settled: bool = None, settlement: int = None, payment_page: int = None):
        """List transactions carried out on your integration.

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50.
            page (int, optional): Specify exactly what page you want to retrieve.
                If not specify we use a default value of 1.
            from_date (datetime.datetime | datetime.date | str, optional): A timestamp from which to start listing transaction
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            to_date (datetime.datetime | datetime.date | str, optional): A timestamp at which to stop listing transaction e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            customer (int, optional): Specify an ID for the customer whose transactions you want to retrieve. Defaults to None.
            status (str, optional): Filter transactions by status ('failed', 'success', 'abandoned'). Defaults to None.
            currency (str, optional): Specify the transaction currency to export.
                Allowed values are: in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR. Defaults to None.
            amount (int, optional): Filter transactions by amount. Specify the amount, in kobo
                if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR. Defaults to None.
            settled (bool, optional): Set to true to export only settled transactions. false for pending transactions.
                Leave undefined to export all transactions. Defaults to None.
            settlement (int, optional): An ID for the settlement whose transactions we should export. Defaults to None.
            payment_page (int, optional): Specify a payment page's id to export only transactions conducted on said page. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        params = util.generate_payload(
            locals(), 'per_page', 'page', 'from_date', 'to_date')
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
