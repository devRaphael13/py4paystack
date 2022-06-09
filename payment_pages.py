from datetime import date, datetime
from .request import Request
from . import util


class PaymentPages(Request):

    """
    The Payment Pages API provides a quick and secure way to collect payment for products.
    """

    path = "/page"

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create(self, name: str, description: str, amount: int, slug: str = None, metadata: dict = None, redirect_url: str = None, custom_fields: list = None):
        payload = {key: value for key, value in locals().items()
                   if value is not None}
        return self.post(self.path, self.secret_key, payload)

    def list_pages(self, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None):
        path = self.path
        params = util.handle_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            path += '?'
            for key, value in params.items():
                path += f"{key}={value}&"
        return self.get(path, self.secret_key)

    def fetch(self, id_or_slug: int | str):
        path = f"{self.path}/{id_or_slug}"
        return self.get(path, self.secret_key)

    def update(self, id_or_slug: int | str, name: str = None, description: str = None, amount: int = None, active: bool = None):
        path = f"{self.path}/{id_or_slug}"
        payload = {key: value for key, value in locals().items()
                   if value is not None}
        if amount == 0:
            payload['amount'] = None
        return self.put(path, self.secret_key, payload)

    def check_slug_availability(self, slug: str):
        path = f"{self.path}/check_slug_availability/{slug}"
        return self.get(path, self.secret_key)

    def add_product(self, page_id: int, product_id: list[int]):
        path = f"{self.path}/{page_id}/product"
        payload = {'product': product_id}
        return self.post(path, self.secret_key, payload)
