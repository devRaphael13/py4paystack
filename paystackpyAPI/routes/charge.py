from datetime import date, datetime

from ..utilities import settings, util, decorators
from ..utilities.errors import MissingArgumentsError, UnwantedArgumentsError
from ..utilities.request import Request


@decorators.class_type_checker
class Charge(Request):

    """
    The Charge API allows you to configure payment channel of your choice when initiating a payment.
    """

    path = '/charge'

    def create(self, email: str, amount: int, bank_code: str = None, account_number: str = None, currency: str = None, authorization_code: str = None, reference: str = None, pin: str = None, ussd: int = None, phone: str = None, provider: str = None, metadata: dict = None, device_id: str = None, generate_reference: bool = False):
        """The Charge API allows you to configure payment channel of your choice when initiating a payment.

        Args:
            email (str): Customer's email address
            amount (int): Amount should be in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR
            bank_code (str, optional): Bank code to use. Provide with account_number. Don't send if you sending authorization_code. Defaults to None.
            account_number (str, optional): Account number to charge. Provide with bank_code. Don't send if you sending authorization_code. Defaults to None.
            currency (str, optional): The currency you want to charge in. Defaults to None.
            authorization_code (str, optional): An authorization code to charge (don't send if charging a bank account). Defaults to None.
            reference (str, optional): Unique transaction reference. Only -, .`, = and alphanumeric characters allowed.. Defaults to None.
            pin (str, optional): 4-digit PIN (send with a non-reusable authorization code). Defaults to None.
            ussd (int, optional): USSD type to charge (don't send if charging an authorization code, bank or card). Defaults to None.
            phone (str, optional): 11 digit str phone number to use with mobile money. Provide with provider. Defaults to None.
            provider (str, optional): mobile money provider, your choices are 'tgo' for Airtel/Tigo, 'mtn' for MTN, 'vod' for vodafone. Defaults to None.
            metadata (dict, optional): A JSON object. Defaults to None.
            device_id (str, optional): This is the unique identifier of the device a user uses in making payment. Only -, .`, = and alphanumeric characters allowed.. Defaults to None.
            generate_reference (bool, optional): Whether to generate reference for you. Defaults to False.

        Raises:
            MissingArgumentsError: raised when a wanted argument is missing

            UnwantedArgumentsError: raised when an unwanted argument is provided

        Returns:
            json: Data fetched from API
        """

        payload = {
            'email': util.check_email(email),
            'amount': amount
        }

        methods = {bank_code, account_number,
                   authorization_code, pin, ussd, phone, provider}

        if metadata:
            payload['metadata'] = metadata

        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if reference:
            payload['reference'] = reference

        if not reference and generate_reference:
            payload['reference'] = util.create_ref()

        if device_id:
            payload['device_id'] = device_id

        if bank_code or account_number:
            if not (bank_code and account_number):
                raise MissingArgumentsError(
                    'provide both the bank_code and account_number')

            unwanted = methods.difference({bank_code, account_number})
            if any(unwanted):
                raise UnwantedArgumentsError(
                    f"don't provide these: {', '.join(unwanted)} - if you're going use bank_code and account_number")

            payload.update({'bank': {'code': util.check_bank_code(
                bank_code), 'account_number': util.check_account_number(account_number)}})
            return self.post(self.path, payload)

        if ussd:
            unwanted = methods.difference({ussd})
            if any(unwanted):
                raise UnwantedArgumentsError(
                    f"don't provide these: {', '.join(unwanted)}- if you're going to use ussd")

            payload.update({'ussd': util.check_membership(
                settings.USSD_CODES, ussd, 'ussd code')})
            return self.post(self.path, payload)

        if pin:
            if not (pin and authorization_code):
                raise MissingArgumentsError(
                    'provide pin with a non-reuseable authorization code')

            unwanted = methods.difference({pin, authorization_code})
            if any(unwanted):
                raise UnwantedArgumentsError(
                    f"don't provide these: {', '.join(unwanted)} - if you're going to use pin and authorization_code")
            payload.update(
                {'pin': pin, 'authorization_code': authorization_code})
            return self.post(self.path, payload)

        if authorization_code:
            unwanted = methods.difference({authorization_code})
            if any(unwanted):
                raise UnwantedArgumentsError(
                    f"don't provide these: {', '.join(unwanted)} - if you're going to use authorization_code")
            payload.update({'authorization_code': authorization_code})
            return self.post(self.path, payload)

        if phone or provider:
            if not (phone and provider):
                raise MissingArgumentsError('provide phone and provider')

            unwanted = methods.difference({phone, provider})
            if any(unwanted):
                raise UnwantedArgumentsError(
                    f"don't provide these: {', '.join(unwanted)} - if you're going to use phone and provider for mobile money option")
            payload.update({'mobile_money': {'phone': phone, 'provider': util.check_membership(
                settings.MOBILE_PAYMENT_PROVIDERS, provider, 'provider')}})
            return self.post(self.path, payload)

    def submit_pin(self, pin: str, reference: str):
        """Submit PIN to continue a charge

        Args:
            pin (str): Pin provided by the user
            reference (str): reference of the transaction that requested the pin

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/submit_pin'
        payload = util.generate_payload(locals())
        return self.post(path, payload)

    def submit_otp(self, otp: str, reference: str):
        """Submit OTP to complete a charge

        Args:
            otp (str): OTP submitted by the user
            reference (str): Reference for the ongoing transation

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/submit_otp"
        payload = util.generate_payload(locals)
        return self.post(path, payload)

    def submit_phone(self, phone: str, reference: str):
        """Submit Phone when requested

        Args:
            phone (str): Phone number submitted by the user
            reference (str): Reference of the ongoing transation

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/submit_phone"
        payload = util.generate_payload(locals())
        return self.post(path, payload)

    def submit_birthday(self, birthday: date | datetime | str, reference: str):
        """Submit Phone when requested

        Args:
            birthday ( date | datetime | str ): birthday submitted by the user
            reference (str): Reference of the ongoing transaction

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/submit_birthday"
        payload = util.generate_payload(locals())
        return self.post(path, payload)

    def submit_address(self, reference: str, address: str, city: str, state: str, zipcode: str):
        """Submit address to continue charge

        Args:
            reference (str): Reference for the ongoing transaction
            address (str): Address submitted by the user
            city (str): City submitted by the user
            state (str): State submitted by the user
            zipcode (str): Zipcode submitted by the user

        Returns:
            JSON: Data fetched from paystack API
        """
        path = f"{self.path}/submit_address"
        payload = util.generate_payload(locals())
        return self.post(path, payload)

    def check_pending_charge(self, reference: str):
        """When you get "pending" as a charge status or if there was an exception when calling any of the /charge endpoints,
        wait 10 seconds or more, then make a check to see if its status has changed.
        Don't call too early as you may get a lot more pending than you should.

        Args:
            reference (str): Reference to check

        Returns:
            JSON: Data fetched from API
        """
        path = f"{self.path}/{reference}"
        return self.get(path)
