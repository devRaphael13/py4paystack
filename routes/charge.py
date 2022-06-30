from datetime import date, datetime

from .utilities import settings, util
from .utilities.errors import MissingArgumentsError, UnwantedArgumentsError
from .utilities.request import Request


class Charge(Request):

    """
    The Charge API allows you to configure payment channel of your choice when initiating a payment.
    """

    path = '/charge'

    def create(self, email: str, amount: int, bank_code: str = None, account_number: str = None, currency: str = None, authorization_code: str = None, reference: str = None, pin: str = None, ussd: int = None, phone: str = None, provider: str = None, metadata: dict = None, device_id: str = None, generate_reference: bool = False):
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
            payload.update({'phone': phone, 'provider': util.check_membership(
                settings.MOBILE_PAYMENT_PROVIDERS, provider, 'provider')})
            return self.post(self.path, payload)

    def submit_pin(self, pin: str, reference: str):
        path = f'{self.path}/submit_pin'
        payload = util.generate_payload(locals(), 'path')
        return self.post(path, payload)

    def submit_otp(self, otp: str, reference: str):
        path = f"{self.path}/submit_otp"
        payload = util.generate_payload(locals, 'path')
        return self.post(path, payload)

    def submit_phone(self, phone: str, reference: str):
        path = f"{self.path}/submit_phone"
        payload = util.generate_payload(locals(), 'path')
        return self.post(path, payload)

    def submit_birthday(self, birthday: date | datetime | str, reference: str):
        path = f"{self.path}/submit_birthday"
        payload = util.generate_payload(locals(), 'path')
        return self.post(path, payload)

    def submit_address(self, reference: str, address: str, city: str, state: str, zipcode: str):
        path = f"{self.path}/submit_address"
        payload = util.generate_payload(locals(), 'path')
        return self.post(path, payload)

    def check_pending_charge(self, reference: str):
        path = f"{self.path}/{reference}"
        return self.get(path)
