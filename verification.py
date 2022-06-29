from . import settings, util
from .request import Request


class Verification(Request):

    """
    The Verification class allows you perform KYC ( Know Your Customer ) processes
    """

    def resolve_acct_number(self, account_number: str, bank_code: str):
        path = f'/bank/resolve?account_number={util.check_account_number(account_number)}&bank_code={util.check_bank_code(bank_code)}'
        return self.get(path)

    def validate_account(self, account_name: str, account_number: str, account_type: str, bank_code: str, country_code: str, document_type: str, document_number: str):
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
        path = '/decision/bin/{}'
        if len(card_bin) != 6 or not card_bin.isdigit():
            raise ValueError('value for card_bin must be 6 digits')
        return self.get(path.format(card_bin))
