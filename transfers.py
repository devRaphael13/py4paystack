from datetime import date, datetime
from .request import Request
from . import util
from . import settings
from .errors import MissingArgumentsError


class Tranfer(Request):

    """
    The Transfers API allows you automate sending money on your integration 
    """

    path = '/transfer'


    @staticmethod
    def get_payload(transfer: dict, generate_reference: bool = False) -> dict:
        payload = util.generate_payload(transfer, 'source', 'generate_reference')
        payload['recipient'] = util.check_code(
            settings.CODE_NAMES['recipient'], payload['recipient'])

        if 'currency' in payload:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, payload['currency'], 'currency')

        if not 'reference' in payload and generate_reference:
            payload['reference'] = util.create_ref()

        return payload

    def initiate(self, source: str, amount: int, recipient: str, reason: str = None, currency: str = None, reference: str = None, generate_reference: bool = False):
        payload = {
            'source': util.check_membership(settings.TRANSFER_SOURCES, source, 'source')
        }
        payload.update(self.get_payload(locals(), generate_reference=generate_reference))

        return self.post(self.path, payload)

    def finalize(self, transfer_code: str, otp: str):
        path = f'{self.path}/finalize_transfer'
        payload = {
            'transfer_code': util.check_code(settings.CODE_NAMES['transfer'], transfer_code),
            'otp': otp
        }

        return self.post(path, payload)

    def initiate_bulk(self, source: str, *transfers: dict):
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
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if customer_id:
            params.update({'customer': customer_id})

        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)


    def fetch(self, transfer_id: int = None, transfer_code: str = None):
        path = self.path

        if not (transfer_id or transfer_code):
            raise MissingArgumentsError('provide either transfer_code or transfer_id')

        if transfer_id:
            path += f'/{transfer_id}'

        if transfer_code and not transfer_id:
            path += f'/{transfer_code}'

        return self.get(path)

    def verify(self, reference: str):
        path = f'{self.path}/verify/{reference}'

        return self.get(path)
