from datetime import date, datetime

from ..utilities import util, decorators
from ..utilities.request import Request


@decorators.class_type_checker
class PaymentPages(Request):

    """
    The Payment Pages API provides a quick and secure way to collect payment for products.
    """

    path = "/page"

    def create(self, name: str, description: str, amount: int, slug: str = None, metadata: dict = None, redirect_url: str = None, custom_fields: list = None):
        """Create a payment page on your integration

        Args:
            name (str): Name of page
            description (str): A description for this page
            amount (int): Amount should be in kobo if currency is NGN, pesewas,
                if currency is GHS, and cents, if currency is ZAR
            slug (str, optional): URL slug you would like to be associated with this page.
                Page will be accessible at https://paystack.com/pay/[slug]. Defaults to None.
            metadata (dict, optional): Extra data to configure the payment page including subaccount,
                logo image, transaction charge. Defaults to None.
            redirect_url (str, optional): If you would like Paystack to redirect someplace upon successful payment,
                specify the URL here. Defaults to None.
            custom_fields (list, optional): If you would like to accept custom fields,
                specify them here. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        payload = util.generate_payload(locals())
        return self.post(self.path, payload)

    def list_pages(self, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None):
        """List payment pages available on your integration.

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50.
            page (int, optional): Specify exactly what page you want to retrieve.
                If not specify we use a default value of 1.
            from_date (date | datetime | str, optional): A timestamp from which to start listing page
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            to_date (date | datetime | str, optional): A timestamp at which to stop listing page
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, id_or_slug: int | str):
        """Get details of a payment page on your integration.

        Args:
            id_or_slug (int | str): The page ID or slug you want to fetch

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/{id_or_slug}"
        return self.get(path)

    def update(self, id_or_slug: int | str, name: str = None, description: str = None, amount: int = None, active: bool = None):
        """Update a payment page details on your integration

        Args:
            id_or_slug (int | str): Page ID or slug.
            name (str, optional): Name of page. Defaults to None.
            description (str, optional): A description for this page. Defaults to None.
            amount (int, optional): Default amount you want to accept using this page.
                If none is set, customer is free to provide any amount of their choice.
                The latter scenario is useful for accepting donations. Defaults to None.
            active (bool, optional): Set to false to deactivate page url. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/{id_or_slug}"
        payload = util.generate_payload(locals(), 'id_or_slug')
        if amount == 0:
            payload['amount'] = None
        return self.put(path, payload)

    def check_slug_availability(self, slug: str):
        """Check the availability of a slug for a payment page.

        Args:
            slug (str): URL slug to be confirmed.

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/check_slug_availability/{slug}"
        return self.get(path)

    def add_product(self, page_id: int, product_id: list[int]):
        """Add products to a payment page

        Args:
            page_id (int): ID of the payment page.
            product_id (list[int]): A list of ids of all the product.

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/{page_id}/product"
        payload = {'product': product_id}
        return self.post(path, payload)
