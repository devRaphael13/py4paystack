from datetime import date, datetime

from ..utilities import decorators, settings, util
from ..utilities.errors import MissingArgumentsError
from ..utilities.request import Request


@decorators.class_type_checker
class Transfer(Request):

    """
    The Transfers API allows you automate sending money on your integration 
    """

    path = '/transfer'

    @staticmethod
    def get_payload(transfer: dict, generate_reference: bool = False) -> dict:
        payload = util.generate_payload(
            transfer, 'source', 'generate_reference')
        payload['recipient'] = util.check_code(
            settings.RECIPIENT, payload['recipient'])

        if 'currency' in payload:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, payload['currency'], 'currency')

        if not 'reference' in payload and generate_reference:
            payload['reference'] = util.create_ref()

        return payload

    def initiate(self, source: str, amount: int, recipient: str, reason: str = None, currency: str = None, reference: str = None, generate_reference: bool = False):
        """ Status of transfer object returned will be pending if OTP is disabled.
        In the event that an OTP is required, status will read otp.

        Args:
            source (str): Where should we transfer from? Only balance for now
            amount (int): Amount to transfer in kobo if currency is NGN and pesewas if currency is GHS.
            recipient (str): Code for transfer recipient
            reason (str, optional): The reason for the transfer. Defaults to None.
            currency (str, optional): Specify the currency of the transfer. Defaults to NGN. Defaults to None.
            reference (str, optional): If specified, the field should be a unique identifier (in lowercase) for the object.
                Only -,_ and alphanumeric characters allowed. Defaults to None.
            generate_reference (bool, optional): Whether to generate reference for you. Defaults to False.

        Returns:
            JSON: Data fetched from API
        """

        payload = {
            'source': util.check_membership(settings.TRANSFER_SOURCES, source, 'source')
        }
        payload.update(self.get_payload(
            locals(), generate_reference=generate_reference))

        return self.post(self.path, payload)

    def finalize(self, transfer_code: str, otp: str):
        """ Finalize an initiated transfer

        Args:
            transfer_code (str): The transfer code you want to finalize
            otp (str): OTP sent to business phone to verify transfer

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/finalize_transfer'
        payload = {
            'transfer_code': util.check_code(settings.TRANSFER, transfer_code),
            'otp': otp
        }

        return self.post(path, payload)

    def initiate_bulk(self, source: str, *transfers: dict):
        """You need to disable the Transfers OTP requirement to use this endpoint.

        Args:
            source (str): Where should we transfer from? Only balance for now
            transfers (dict): Transfer objects. Each object should contain amount, recipient, and reference

        Raises:
            MissingArgumentsError: raised when a required argument is missing.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/bulk'

        for x in transfers:
            if ('amount', 'recipient') not in x:
                raise MissingArgumentsError(
                    'missing arguments: provide the amount and recipient code')

        payload = {
            'source': util.check_membership(settings.TRANSFER_SOURCES, source, 'source'),
            'transfers': [self.get_payload(transfer, generate_reference=True) for transfer in transfers]
        }

        return self.post(path, payload)

    def list_transfers(self, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None, customer_id: int = None):
        """List the transfers made on your integration.

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50. Defaults to None.
            page (int, optional): Specify exactly what transfer you want to page. If not specify we use a default value of 1. Defaults to None.
            from_date (date | datetime | str, optional): A timestamp from which to start listing transfer e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            to_date (date | datetime | str, optional): A timestamp at which to stop listing transfer e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            customer_id (int, optional): Filter by customer ID. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)

        if customer_id:
            params.update({'customer': customer_id})

        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, transfer: int | str):
        """Get details of a transfer on your integration.

        Args:
            transfer (int | str): The transfer ID or code you want to fetch

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{util.id_or_code(transfer, data=settings.TRANSFER)}'

        return self.get(path)

    def verify(self, reference: str):
        """Verify the status of a transfer on your integration.

        Args:
            reference (str): Transfer reference

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/verify/{reference}'

        return self.get(path)
