from ..utilities import decorators, settings, util
from ..utilities.request import Request


@decorators.class_type_checker
class TransferControl(Request):

    """
    The Transfers Control API allows you manage settings of your transfers
    """

    balance = '/balance'
    transfer = '/transfer'

    def check_balance(self):
        """Fetch the available balance on your integration

        Returns:
            JSON: Data fetched from API
        """

        return self.get(self.balance)

    def fetch_balance_ledger(self):
        """Fetch all pay-ins and pay-outs that occured on your integration

        Returns:
            JSON: Data fetched from API
        """
        path = f'{self.balance}/ledger'

        return self.get(path)

    def resend_otp(self, transfer_code: str, reason: str):
        """Generates a new OTP and sends to customer in the event they are having trouble receiving one.
            This feature is only available to businesses in Nigeria and Ghana.

        Args:
            transfer_code (str): Transfer code
            reason (str): Either resend_otp or transfer

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.transfer}/resend_otp'
        payload = {
            'transfer_code': util.check_code(settings.TRANSFER, transfer_code),
            'reason': util.check_membership(settings.TRANSFER_CONTROL_REASONS, reason, 'reason')
        }

        return self.post(path, payload)

    def disable_otp(self):
        """This is used in the event that you want to be able to complete transfers programmatically without use of OTPs.
            No arguments required. You will get an OTP to complete the request.
            This feature is only available to businesses in Nigeria and Ghana.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.transfer}/disable_otp'

        return self.post(path, {})

    def finalize_disable_otp(self, otp: str):
        """Finalize the request to disable OTP on your transfers.
            This feature is only available to businesses in Nigeria and Ghana.

        Args:
            otp (str): OTP sent to business phone to verify disabling OTP requirement

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.transfer}/disable_otp_finalize'

        return self.post(path, {'otp': otp})

    def enable_otp(self):
        """In the event that a customer wants to stop being able to complete transfers programmatically,
        this endpoint helps turn OTP requirement back on. No arguments required.
        This feature is only available to businesses in Nigeria and Ghana.

        Returns:
           JSON: Data fetched from API
        """
        
        path = f'{self.transfer}/enable_otp'

        return self.post(path)
