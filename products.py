from .request import Request
from . import util
import datetime


class Product(Request):

    """
    The Products API allows you create and manage inventories on your integration
    """
    path = '/product'

    def __init__(self, secret_key: str) -> None:
        self.secret_key = secret_key

    def create(self, name: str, description: str, price: int, currency: str, unlimited: bool = None, quantity: int = None):
        payload = {key: value for key, value in locals().items()
                   if value is not None}
        payload['currency'] = util.check_membership(settings.CURRENCIES, currency, 'currency')

        if quantity and quantity != 0:
            assert unlimited is None or unlimited is False, "set unlimited to False then set quantity, set unlimited to True otherwise."
            payload['quantity'] = quantity

        if unlimited is True:
            assert quantity is None, "you can't set quantity with unlimited set to True"
            payload['unlimited'] = True

        return self.post(self.path, self.secret_key, payload)

    def list_products(self, per_page: int = None, page: int = None, from_date: datetime.datetime | datetime.date | str = None, to_date: datetime.datetime | datetime.date | str = None):
        path = self.path
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            path = util.handle_query_params(path, params)
        return self.get(path, self.secret_key)

    def fetch(self, product_id: int):
        path = f"{self.path}/{product_id}"
        self.get(path, self.secret_key)

    def update(self, product_id: int, name: str = None, description: str = None, price: int = None, currency: str = None, unlimited: bool = None, quantity: int = None):
        path = f"{self.path}/{product_id}"
        payload = {key: value for key, value in locals(
        ).items() if key != 'product_id' and value is not None}

        if currency:
            payload['currency'] = util.check_membership(settings.CURRENCIES, currency, 'currency')

        if quantity and quantity != 0:
            assert unlimited is None or unlimited is False, "set unlimited to False then set quantity, set unlimited to True otherwise."
            payload['quantity'] = quantity

        if unlimited is True:
            assert quantity is None, "you can't set quantity with unlimited set to True"
            payload['unlimited'] = True

        return self.put(path, self.secret_key, payload)
