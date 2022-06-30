from .utilities import settings, util
from .utilities.request import Request


class TransferControl(Request):

    """
    The Transfers Control API allows you manage settings of your transfers
    """

    balance = '/balance'
    transfer = '/transfer'


    def check_balance(self):
        return self.get(self.balance)

    def fetch_balance_ledger(self):
        path = f'{self.balance}/ledger'

        return self.get(path)

    def resend_otp(self, transfer_code: str, reason: str):
        path = f'{self.transfer}/resend_otp'
        payload = {
            'transfer_code': util.check_code(settings.CODE_NAMES['transfer'], transfer_code),
            'reason': util.check_membership(settings.TRANSFER_CONTROL_REASONS, reason, 'reason')
        }

        return self.post(path, payload)

    def disable_otp(self):
        path = f'{self.transfer}/disable_otp'

        return self.post(path, {})

    def finalize_disable_otp(self, otp: str):
        path = f'{self.transfer}/disable_otp_finalize'

        return self.post(path, {'otp': otp})

    def enable_otp(self):
        path = f'{self.transfer}/enable_otp'

        return self.post(path, {})
