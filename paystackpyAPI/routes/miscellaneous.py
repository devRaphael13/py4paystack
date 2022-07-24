from ..utilities import settings, util, decorators
from ..utilities.request import Request


@decorators.class_type_checker
class Miscellaneous(Request):

    """The Miscellaneous API are supporting APIs that can be used to provide more details to other APIs
    """

    def list_banks(self, country: str = None, use_cursor: bool = False, per_page: int = None, next: str = None, previous: str = None, gateway: str = None, type: str = None, currency: str = None):
        """Get a list of all supported banks and their properties

        Args:
            country (str, optional): The country from which to obtain the list of supported banks.
                e.g country=ghana or country=nigeria. Defaults to None.
            use_cursor (bool, optional): Use_curFlag to enable cursor pagination on the endpointsor. Defaults to False.
            per_page (int, optional): The number of objects to return per page.
                Defaults to 50, and limited to 100 records per page.
            next (str, optional): A cursor that indicates your place in the list.
                It can be used to fetch the next page of the list. Defaults to None.
            previous (str, optional): A cursor that indicates your place in the list.
                It should be used to fetch the previous page of the list after an intial next request. Defaults to None.
            gateway (str, optional): The gateway type of the bank.
                It can be one of these: [emandate, digitalbankmandate]. Defaults to None.
            type (str, optional): Type of financial channel. For Ghanaian channels,
                please use either mobile_money for mobile money channels OR ghipps for bank channels. Defaults to None.
            currency (str, optional): Any of NGN, USD, GHS or ZAR. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = '/bank'
        params = util.generate_payload(locals(), 'per_page', 'currency').update(
            util.check_query_params(per_page=per_page))

        if currency:
            params['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if params:
            path = util.handle_query_params(path, params)
        return self.get(path)

    def list_providers(self, pay_with_bank_transfer: bool = None):
        """Get a list of all providers for Dedicated Virtual Account

        Args:
            pay_with_bank_transfer (bool, optional): A flag to filter for available providers. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = '/bank'
        params = util.generate_payload(locals())

        if params:
            path = util.handle_query_params(path, params)

        return self.get(path)

    def list_search_countries(self):
        """Gets a list of Countries that Paystack currently supports

        Returns:
            JSON: Data fetched from API
        """

        path = '/country'

        return self.get(path)

    def list_states(self, country: int = None):
        """Get a list of states for a country for address verification.

        Args:
            country (int, optional): The country code of the states to list.
                It is gotten after the charge request. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """
        path = f'/address_verification/states?country={country}' if country else '/address_verification/states'

        return self.get(path)
