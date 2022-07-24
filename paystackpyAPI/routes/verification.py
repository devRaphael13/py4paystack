from ..utilities import settings, util, decorators
from ..utilities.request import Request


@decorators.class_type_checker
class Verification(Request):

    """
    The Verification class allows you perform KYC ( Know Your Customer ) processes.
    This feature is only available to businesses in Nigeria.
    """

    def resolve_acct_number(self, account_number: str, bank_code: str):
        """Confirm an account belongs to the right customer

        Args:
            account_number (str): Account Number
            bank_code (str): You can get the list of bank codes by calling the List Bank endpoint

        Returns:
            JSON: Data fetched from API
        """

        path = f'/bank/resolve?account_number={util.check_account_number(account_number)}&bank_code={util.check_bank_code(bank_code)}'
        return self.get(path)

    def validate_account(self, account_name: str, account_number: str, account_type: str, bank_code: str, country_code: str, document_type: str, document_number: str):
        """Confirm the authenticity of a customer's account number before sending money

        Args:
            account_name (str): Customer's first and last name registered with their bank
            account_number (str): Customer's account number
            account_type (str): This can take one of: [ personal, business ]
            bank_code (str): The bank code of the customer's bank. You can fetch the bank codes by using our List Bank endpoint
            country_code (str): The two digit ISO code of the customer's bank e.g GH for Ghana
            document_type (str): Customer's mode of identity. This could be one of: [ identityNumber, passportNumber, businessRegistrationNumber ]
            document_number (str): Customer's mode of identity number.

        Returns:
            JSON: Data fetched from API
        """

        path = '/bank/validate'
        payload = {
            'account_name': account_name,
            'account_number': util.check_account_number(account_number),
            'account_type': util.check_membership(settings.ACCOUNT_TYPES, account_type, 'account_type'),
            'bank_code': util.check_bank_code(bank_code),
            'country_code': util.check_country(country_code),
            'document_type': util.check_membership(settings.DOCUMENT_TYPES, document_type, 'document_type'),
            'document_number': document_number
        }
        return self.post(path, payload=payload)

    def resolve_card_bin(self, card_bin: str):
        """Get more information about a customer's card

        Args:
            card_bin (str): First 6 characters of card

        Raises:
            ValueError: raised when card_bin is less or greater than 6
            or is not made up of digits.

        Returns:
            JSON: Data fetched from API
        """

        path = '/decision/bin/{}'
        if len(card_bin) != 6 or not card_bin.isdigit():
            raise ValueError('value for card_bin must be 6 digits')
        return self.get(path.format(card_bin))
