from datetime import date, datetime
from .request import Request
from . import settings
from . import util


class Invoice(Request):

    """
    The Invoices API allows you issue out and manage payment requests
    """

    path = '/paymentrequest'

    def __init__(self, secret_key: str) -> None:
        self.secret_key = secret_key

    def create(self, description: str, due_date: date | datetime | str, customer_id: int = None, customer_code: str = None, amount: int = None, line_items: list[dict[str]] = None, tax: list[dict[str]] = None, currency: str = None, send_notification: bool = None, draft: bool = None, has_invoice: bool = None, invoice_number: int = None, split_code: str = None):
        if (amount and (line_items or tax)) or not (amount or line_items):
            raise ValueError('provide either amount or line_items not both!')

        if not (customer_id or customer_code):
            raise ValueError('provide either customer code or id')

        payload = {key: value for key, value in locals().items()
                   if value is not None}
        payload['due_date'] = util.handle_date(due_date)

        if customer_id:
            payload['customer'] = customer_id

        if customer_code and not customer_id:
            payload['customer'] = util.check_code(
                settings.CODE_NAMES['customer'], customer_code)

        if currency:
            payload['currency'] = util.check_currency(currency)

        if split_code:
            payload['split_code'] = util.check_code(
                settings.CODE_NAMES['split'], split_code)

        return self.post(self.path, self.secret_key, payload)

    def list_invoices(self, per_page: int = None, page: int = None, customer: int = None, status: str = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None, include_archive: str = None):
        path = self.path
        params = {key: value for key, value in locals().items() if value is not None}.update(
            util.check_query_params(per_page=per_page, page=page, from_date=from_date, to_date=to_date))
        if params:
            path = util.handle_query_params(path, params)
        return self.get(path, self.secret_key)

    def view(self, invoice_id: int = None, invoice_code: str = None):
        path = self.path

        if not (invoice_id or invoice_code):
            raise ValueError('provide either request id or code')

        if invoice_id:
            path += f"{invoice_id}/"

        if invoice_code and not invoice_id:
            path += f"{util.check_code(settings.CODE_NAMES['invoice'], invoice_code)}/"

        return self.get(path, self.secret_key)

    def verify(self, invoice_code: str):
        path = f"{self.path}/verify/{util.check_code(settings.CODE_NAMES['invoice'], invoice_code)}"
        return self.get(path, self.secret_key)

    def send_notification(self, invoice_code: str):
        path = f"{self.path}/notify/{util.check_code(settings.CODE_NAMES['invoice'], invoice_code)}"
        return self.get(path, self.secret_key)

    def total(self):
        path = f"{self.path}/totals"
        return self.get(path, self.secret_key)

    def finalize(self, invoice_code: str):
        path = f"{self.path}/finalize/{util.check_code(settings.CODE_NAMES['invoice'], invoice_code)}"
        return self.get(path, self.secret_key)

    def update(self, invoice_id: int = None, invoice_code: str = None, customer_code: str = None, customer_id: int = None, amount: int = None, currency: str = None, due_date: date | datetime | str = None, description: str = None, line_items: list[dict[str]] = None, tax: list[dict[str]] = None, send_notification: bool = None, draft: bool = None, invoice_number: int = None, split_code: str = None):
        path = self.path

        if not (invoice_id or invoice_code):
            raise ValueError('provide either request id or code')

        if invoice_id:
            path += f"{invoice_id}/"

        if invoice_code and not invoice_id:
            path += f"{util.check_code(settings.CODE_NAMES['invoice'], invoice_code)}/"

        if not (customer_code or customer_id):
            raise ValueError("provide either customer_code or customer_id")

        if amount:
            assert not (
                tax or line_items), "you can either provide amount or line_items and/or tax"

        if (tax or line_items):
            assert not amount, "you can either provide amount or line_items and/or tax"

        payload = {key: value for key, value in locals().items() if key not in (
            'customer_code', 'customer_id', 'invoice_code', 'invoice_id') and value is not None}

        if customer_id:
            payload['customer'] = customer_id

        if customer_code and not customer_id:
            payload['customer'] = util.check_code(
                settings.CODE_NAMES['customer'], customer_code)

        if currency:
            payload['currency'] = util.check_currency(currency)

        if due_date:
            payload['due_date'] = util.handle_date(due_date)

        if split_code:
            payload['split_code'] = util.check_code(
                settings.CODE_NAMES['split'], split_code)

        self.put(path, self.secret_key, payload)

    def archive(self, invoice_id: int = None, invoice_code: str = None):
        path = f"{self.path}/archive"

        if not (invoice_id or invoice_code):
            raise ValueError('provide either request id or code')

        if invoice_id:
            path += f"{invoice_id}/"

        if invoice_code and not invoice_id:
            path += f"{util.check_code(settings.CODE_NAMES['invoice'], invoice_code)}/"

        return self.get(path, self.secret_key)
