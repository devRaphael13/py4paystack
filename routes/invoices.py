from datetime import date, datetime

from .utilities import settings, util
from .utilities.errors import MissingArgumentsError, UnwantedArgumentsError
from .utilities.request import Request


class Invoice(Request):

    """
    The Invoices API allows you issue out and manage payment requests
    """

    path = '/paymentrequest'

    def create(self, description: str, due_date: date | datetime | str, customer_id: int = None, customer_code: str = None, amount: int = None, line_items: list[dict[str]] = None, tax: list[dict[str]] = None, currency: str = None, send_notification: bool = None, draft: bool = None, has_invoice: bool = None, invoice_number: int = None, split_code: str = None):
        if (amount and (line_items or tax)) or not (amount or line_items):
            raise UnwantedArgumentsError(
                'provide either amount or line_items not both!')

        payload = util.generate_payload(
            locals(), 'customer_id', 'customer_code')
        payload['customer'] = util.id_or_code(_id=customer_id, code=customer_code, data=settings.CUSTOMER)
        payload['due_date'] = util.handle_date(due_date)

        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if split_code:
            payload['split_code'] = util.check_code(
                settings.SPLIT, split_code)

        return self.post(self.path, payload)

    def list_invoices(self, per_page: int = None, page: int = None, customer: int = None, status: str = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None, include_archive: str = None):
        params = util.generate_payload(locals())
        params.update(
            util.check_query_params(per_page=per_page, page=page, from_date=from_date, to_date=to_date))

        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def view(self, invoice_id: int = None, invoice_code: str = None):
        path = f'{self.path}/{util.id_or_code(_id=invoice_id, code=invoice_code, data=settings.INVOICE)}'

        return self.get(path)

    def verify(self, invoice_code: str):
        path = f"{self.path}/verify/{util.check_code(settings.INVOICE, invoice_code)}"
        return self.get(path)

    def send_notification(self, invoice_code: str):
        path = f"{self.path}/notify/{util.check_code(settings.INVOICE, invoice_code)}"
        return self.get(path)

    def total(self):
        path = f"{self.path}/totals"
        return self.get(path)

    def finalize(self, invoice_code: str):
        path = f"{self.path}/finalize/{util.check_code(settings.INVOICE, invoice_code)}"
        return self.get(path)

    def update(self, invoice_id: int = None, invoice_code: str = None, customer_code: str = None, customer_id: int = None, amount: int = None, currency: str = None, due_date: date | datetime | str = None, description: str = None, line_items: list[dict[str]] = None, tax: list[dict[str]] = None, send_notification: bool = None, draft: bool = None, invoice_number: int = None, split_code: str = None):
        path = f'{self.path}/{util.id_or_code(_id=invoice_id, code=invoice_code, data=settings.INVOICE)}'

        payload = util.generate_payload(
            locals(), 'customer_code', 'customer_id', 'invoice_code', 'invoice_id', 'path')

        payload['customer'] = util.id_or_code(_id=customer_id, code=customer_code, data=settings.CUSTOMER)

        if amount:
            assert not (
                tax or line_items), "you can either provide amount or line_items and/or tax"

        if (tax or line_items):
            assert not amount, "you can either provide amount or line_items and/or tax"

        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if due_date:
            payload['due_date'] = util.handle_date(due_date)

        if split_code:
            payload['split_code'] = util.check_code(
                settings.SPLIT, split_code)

        self.put(path, payload)

    def archive(self, invoice_id: int = None, invoice_code: str = None):
        path = f"{self.path}/archive/{util.id_or_code(_id=invoice_id, code=invoice_code, data=settings.INVOICE)}"

        return self.get(path)
