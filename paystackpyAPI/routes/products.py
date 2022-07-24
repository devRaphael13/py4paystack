import datetime

from ..utilities import settings, util, decorators
from ..utilities.request import Request


@decorators.class_type_checker
class Product(Request):

    """
    The Products API allows you create and manage inventories on your integration
    """
    path = '/product'

    def create(self, name: str, description: str, price: int, currency: str, unlimited: bool = None, quantity: int = None):
        """Create a product on your integration

        Args:
            name (str): Name of product
            description (str): A description for this product
            price (int): Price should be in kobo if currency is NGN, pesewas,
                if currency is GHS, and cents, if currency is ZAR
            currency (str): Currency in which price is set. Allowed values are: NGN, GHS, ZAR or USD
            unlimited (bool, optional): Set to true if the product has unlimited stock.
                Leave as false if the product has limited stock. Defaults to None.
            quantity (int, optional): Number of products in stock. Use if unlimited is false. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        payload = util.generate_payload(locals(), 'currency')
        payload['currency'] = util.check_membership(
            settings.CURRENCIES, currency, 'currency')

        if quantity and quantity != 0:
            assert unlimited is None or unlimited is False, "set unlimited to False then set quantity, set unlimited to True otherwise."
            payload['quantity'] = quantity

        if unlimited is True:
            assert quantity is None, "you can't set quantity with unlimited set to True"
            payload['unlimited'] = True

        return self.post(self.path, payload)

    def list_products(self, per_page: int = None, page: int = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None):
        """List products available on your integration.

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50.. Defaults to None.
            page (int, optional): Specify exactly what page you want to retrieve.
                If not specify we use a default value of 1.. Defaults to None.
            from_date (datetime.datetime | datetime.date | str, optional): A timestamp from which to start listing product
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            to_date (datetime.datetime | datetime.date | str, optional): A timestamp at which to stop listing product
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, product_id: int):
        """Get details of a product on your integration.

        Args:
            product_id (int): The product ID you want to fetch

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/{product_id}"
        return self.get(path)

    def update(self, product_id: int, name: str = None, description: str = None, price: int = None, currency: str = None, unlimited: bool = None, quantity: int = None):
        """Update a product details on your integration

        Args:
            product_id (int): Product ID
            name (str, optional): Name of product. Defaults to None.
            description (str, optional): A description for this product. Defaults to None.
            price (int, optional): Price should be in kobo if currency is NGN, pesewas,
                if currency is GHS, and cents, if currency is ZAR. Defaults to None.
            currency (str, optional): Currency in which price is set.
                Allowed values are: NGN, GHS, ZAR or USD. Defaults to None.
            unlimited (bool, optional): Set to true if the product has unlimited stock.
                Leave as false if the product has limited stock.
            quantity (int, optional): Number of products in stock.
                Use if unlimited is false. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/{product_id}"
        payload = {key: value for key, value in locals(
        ).items() if key not in ('product_id', 'path') and value is not None}

        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if quantity and quantity != 0:
            assert unlimited is None or unlimited is False, "set unlimited to False then set quantity, set unlimited to True otherwise."
            payload['quantity'] = quantity

        if unlimited is True:
            assert quantity is None, "you can't set quantity with unlimited set to True"
            payload['unlimited'] = True

        return self.put(path, payload)
