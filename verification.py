from .request import Request
from . import util

class Verification(Request):

    """
    The Verification class allows you perform KYC ( Know Your Customer ) processes
    """

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def resolve_acct_number(self, account_number: str, bank_code: str):
        path = f'/bank/resolve?account_number={util.check_account_number(account_number)}&bank_code={util.check_bank_code(bank_code)}'
        return self.get(path, self.secret_key)

    def validate_account(self, account_name: str, account_number: str, account_type: str, bank_code: str, country_code: str, document_type: str, document_number: str):
        path = '/bank/validate'
        payload = {
            'account_name': account_name,
            'account_number': util.check_account_number(account_number),
            'account_type': util.check_account_types(account_type),
            'bank_code': util.check_bank_code(bank_code),
            'country_code': util.check_country(country_code),
            'document_type': util.check_document_type(document_type),
            'document_number': document_number
        }
        return self.post(path, self.secret_key, payload)

    def resolve_card_bin(self, card_bin: int):
        path = '/decision/bin/{}'
        assert len(str(card_bin)) == 6, "value for card_bin must be 6 digits"
        return self.get(path.format(card_bin), self.secret_key)
    