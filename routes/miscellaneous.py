from .utilities import settings, util, decorators
from .utilities.request import Request


@decorators.class_type_checker
class Miscellaneous(Request):

    """The Miscellaneous API are supporting APIs that can be used to provide more details to other APIs
    """

    def list_banks(self, country: str = None, use_cursor: bool = False, per_page: int = None, next: str = None, previous: str = None, gateway: str = None, type: str = None, currency: str = None):
        path = '/bank'
        params = util.generate_payload(locals(), 'per_page').update(
            util.check_query_params(per_page=per_page))

        if currency:
            params['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if params:
            path = util.handle_query_params(path, params)
        return self.get(path)

    def list_providers(self, pay_with_bank_transfer: bool = None):
        path = '/bank'
        params = util.generate_payload(locals())

        if params:
            path = util.handle_query_params(path, params)

        return self.get(path)

    def list_search_countries(self):
        path = '/country'

        return self.get(path)

    def list_states(self, country: int = None):
        path = f'/address_verification/states?country={country}' if country else '/address_verification/states'

        return self.get(path)
