from datetime import date, datetime

from ..utilities import decorators, settings, util
from ..utilities.errors import MissingArgumentsError
from ..utilities.request import Request


@decorators.class_type_checker
class TransferRecipient(Request):

    """
    The Transfer Recipients API allows you create and manage beneficiaries that you send money to
    """

    path = '/transferrecipient'

    @staticmethod
    def get_payload(payload: dict):
        payload = util.generate_payload(payload)
        if not ('recipient_type' or 'type') in payload:
            raise MissingArgumentsError(
                f"provide recipient_type or type based on the type of recipient you want to create, your choices are: {', '.join(settings.RECIPIENT_TYPES)}")

        payload['type'] = util.check_membership(settings.RECIPIENT_TYPES, payload.get(
            'recipient_type') or payload.get('type'), 'type')
        r_type = payload.get('type')

        if r_type == 'authorization':
            if not ('email' and 'authorization_code') in payload:
                raise MissingArgumentsError(
                    "provide email and authorization_code params")

            payload['email'] = util.check_email(payload.pop('email'))
            payload['authorization_code'] = util.check_code(
                settings.AUTHORIZATION, payload.pop('authorization_code'))

            for x in ('bank_code', 'account_number'):
                if x in payload:
                    payload.pop(x)

        elif r_type in ('basa', 'nuban', 'mobile_money'):
            if not ('bank_code' and 'account_number') in payload:
                raise MissingArgumentsError(
                    "provide bank_code and account_number")

            payload['bank_code'] = util.check_bank_code(
                payload.pop('bank_code'))
            payload['account_number'] = util.check_account_number(
                payload.pop('account_number'))

            for x in ('authorization_code', 'email'):
                if x in payload:
                    payload.pop(x)

        currency = payload.get('currency')
        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        return payload

    def create(self, recipient_type: str, name: str, email: str = None, account_number: str = None, bank_code: str = None, description: str = None, currency: str = None, authorization_code: str = None, metadata: dict = None):
        """Creates a new recipient. A duplicate account number will lead to the retrieval of the existing record.

        Args:
            recipient_type (str): Recipient Type. It could be one of: nuban, mobile_money, basa, authorization.
            name (str): A name for the recipient
            email (str, optional): Required if recipient_type is authorization. Defaults to None.
            account_number (str, optional): Required if type is nuban or basa. Defaults to None.
            bank_code (str, optional): Required if type is nuban or basa. You can get the list of Bank Codes by calling the List Banks endpoint. Defaults to None.
            description (str, optional): A description for this recipient. Defaults to None.
            currency (str, optional): Currency for the account receiving the transfer. Defaults to None.
            authorization_code (str, optional): An authorization code from a previous transaction. Defaults to None.
            metadata (dict, optional): Store additional information about your recipient in a structured format, JSON. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        return self.post(self.path, self.get_payload(locals()))

    def bulk_create(self, *recipients: dict[str]):
        """A list of transfer recipient object. Each object should contain type, name, and bank_code.
            Any Create Transfer Recipient param can also be passed.

        Args:
            recipients (dict[str]): Recipient objects. Each object should contain type, name, and bank_code.
                Any Create Transfer Recipient param can also be passed.

        Returns:
            JSON: Data fetched from API
        """
        path = f"{self.path}/bulk"
        payload = {
            'batch': [self.get_payload(recipient) for recipient in recipients]
        }
        return self.post(path, payload)

    def list_recipients(self, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None):
        """List transfer recipients available on your integration

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50. Defaults to None.
            page (int, optional): Specify exactly what page you want to retrieve.
                If not specify we use a default value of 1.. Defaults to None.
            from_date (date | datetime | str, optional): A timestamp from which to start listing transfer recipients
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            to_date (date | datetime | str, optional): A timestamp at which to stop listing transfer recipients
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, recipient: int | str):
        """Fetch the details of a transfer recipient.

        Args:
            recipient (int | str): An ID or code for the recipient whose details you want to receive..

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{util.id_or_code(recipient, data=settings.RECIPIENT)}'

        return self.get(path)

    def update(self, recipient: int | str, name: str = None, email: str = None):
        """Update an existing recipient. An duplicate account number will lead to the retrieval of the existing record.
            
        Args:
            recipient (int | str): Transfer Recipient's ID or code
            name (str, optional): A name for the recipient. Defaults to None.
            email (str, optional): Email address of the recipient. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """
        path = f'{self.path}/{util.id_or_code(recipient, data=settings.RECIPIENT)}'

        payload = {}

        if name:
            payload['name'] = name

        if email:
            payload['email'] = util.check_email(email)

        return self.put(path, payload)

    def delete(self, recipient: int | str):
        """Deletes a transfer recipient (sets the transfer recipient to inactive).
        
        Args:
            recipient (int | str): An ID or code for the recipient who you want to delete.
        
        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{util.id_or_code(recipient, data=settings.RECIPIENT)}'

        return super().delete(path)
