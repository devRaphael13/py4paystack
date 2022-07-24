from datetime import date, datetime

from ..utilities import settings, util, decorators
from ..utilities.errors import UnwantedArgumentsError
from ..utilities.request import Request


@decorators.class_type_checker
class Invoice(Request):

    """
    The Invoices API allows you issue out and manage payment requests
    """

    path = '/paymentrequest'

    def create(self, customer: int | str, description: str, due_date: date | datetime | str, amount: int = None, line_items: list[dict[str]] = None, tax: list[dict[str]] = None, currency: str = None, send_notification: bool = None, draft: bool = None, has_invoice: bool = None, invoice_number: int = None, split_code: str = None):
        """Create an invoice for payment on your integration.

        Args:
            customer (int | str): Customer ID or code.
            description (str): A short description of the payment request
            due_date (date | datetime | str): ISO 8601 representation of request due date
                eg. 2016-09-24T00:00:05.000Z, 2016-09-21. 
            amount (int, optional): Payment request amount. It should be used when line items and tax values aren't specified.
                Defaults to None.
            line_items (list[dict[str]], optional): Array of line items int the format [{"name":"item 1", "amount":2000, "quantity": 1}]. Defaults to None.
            tax (list[dict[str]], optional): Array of taxes to be charged in the format [{"name":"VAT", "amount":2000}]. Defaults to None.
            currency (str, optional): Specify the currency of the invoice. Allowed values are NGN, GHS, ZAR and USD. Defaults to NGN. Defaults to None.
            send_notification (bool, optional): Indicates whether Paystack sends an email notification to customer. Defaults to true. Defaults to None.
            draft (bool, optional): Indicate if request should be saved as draft. Defaults to false and overrides send_notification. Defaults to None.
            has_invoice (bool, optional): Set to true to create a draft invoice (adds an auto incrementing invoice number if none is provided) even if there are no line_items or tax passed. Defaults to None.
            invoice_number (int, optional): Numeric value of invoice. Invoice will start from 1 and auto increment from there. This field is to help override whatever value Paystack decides. Auto increment for subsequent invoices continue from this point.. Defaults to None.
            split_code (str, optional): The split code of the transaction split. e.g. SPL_98WF13Eb3w. Defaults to None.

        Raises:
            UnwantedArgumentsError: Raised when an argument passed is unwanted.

        Returns:
            JSON: Data fetched from API
        """

        if (amount and (line_items or tax)) or not (amount or line_items):
            raise UnwantedArgumentsError(
                'provide either amount or line_items not both!')

        payload = util.generate_payload(
            locals(), 'customer_id', 'customer_code', 'due_date', 'currency', 'split_code')
        payload['customer'] = util.id_or_code(customer, data=settings.CUSTOMER)
        payload['due_date'] = util.handle_date(due_date)

        if currency:
            payload['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if split_code:
            payload['split_code'] = util.check_code(
                settings.SPLIT, split_code)

        return self.post(self.path, payload)

    def list_invoices(self, per_page: int = None, page: int = None, customer: int = None, status: str = None, currency: str = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None, include_archive: str = None):
        """List invoice available on your integration

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50.
            page (int, optional): Specify exactly what invoice you want to page.
                If not specify we use a default value of 1.
            customer (int, optional): Filter by customer ID. Defaults to None.
            currency (str, optional): Filter by currency. Allowed values are NGN, GHS, ZAR and USD.
            status (str, optional): Filter by invoice status. Defaults to None.
            from_date (date | datetime | str, optional): A timestamp from which to start listing invoice
                e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.
            to_date (date | datetime | str, optional): A timestamp at which to stop listing invoice
                e.g. 2016-09-24T00:00:05.000Z, 201. Defaults to None.
            include_archive (str, optional): Show archived invoices. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        params = util.generate_payload(
            locals(), 'per_page', 'page', 'from_date', 'to_date', 'currency')
        params.update(
            util.check_query_params(per_page=per_page, page=page, from_date=from_date, to_date=to_date))

        if currency:
            params['currency'] = util.check_membership(
                settings.CURRENCIES, currency, 'currency')

        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def view(self, invoice: int | str):
        """Get details of an invoice on your integration.

        Args:
            invoice (int | str): ID or code of the invoice

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{util.id_or_code(invoice, data=settings.INVOICE)}'

        return self.get(path)

    def verify(self, invoice_code: str):
        """Verify details of an invoice on your integration.

        Args:
            invoice_code (str): The invoice code.

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/verify/{util.check_code(settings.INVOICE, invoice_code)}"
        return self.get(path)

    def send_notification(self, invoice_code: str):
        """Send notification of an invoice to your customers

        Args:
            invoice_code (str): The invoice code

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/notify/{util.check_code(settings.INVOICE, invoice_code)}"
        return self.get(path)

    def total(self):
        """Get invoice metrics for dashboard

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/totals"
        return self.get(path)

    def finalize(self, invoice_code: str):
        """Finalize a Draft Invoice

        Args:
            invoice_code (str): The invoice code

        Returns:
            JSON: Data fetched from API
        """

        path = f"{self.path}/finalize/{util.check_code(settings.INVOICE, invoice_code)}"
        return self.get(path)

    def update(self, invoice: int | str, customer: int | str = None, amount: int = None, currency: str = None, due_date: date | datetime | str = None, description: str = None, line_items: list[dict[str]] = None, tax: list[dict[str]] = None, send_notification: bool = None, draft: bool = None, invoice_number: int = None, split_code: str = None):
        """Update an invoice details on your integration.

        Args:
            invoice_id (int, optional): The invoice id or code.
            customer_code (str, optional): Customer's code or ID. Defaults to None.
            amount (int, optional): Payment request amount. Only useful if line items and tax values are ignored.
                endpoint will throw a friendly warning if neither is available.. Defaults to None.
            currency (str, optional): Specify the currency of the invoice. Allowed values are NGN, GHS, ZAR and USD Defaults to NGN
            due_date (date | datetime | str, optional): ISO 8601 representation of request due date. Defaults to None.
            description (str, optional): A short description of the payment request. Defaults to None.
            line_items (list[dict[str]], optional): Array of line items int the format [{"name":"item 1", "amount":2000}]. Defaults to None.
            tax (list[dict[str]], optional): Array of taxes to be charged in the format [{"name":"VAT", "amount":2000}]. Defaults to None.
            send_notification (bool, optional): Indicates whether Paystack sends an email notification to customer. Defaults to true.
            draft (bool, optional): Indicate if request should be saved as draft. Defaults to false and overrides send_notification.
            invoice_number (int, optional): Numeric value of invoice.
                Invoice will start from 1 and auto increment from there. This field is to help override whatever value Paystack decides. Auto increment for subsequent invoices continue from this point.. Defaults to None.
            split_code (str, optional): The split code of the transaction split. e.g. SPL_98WF13Eb3w. Defaults to None.

        Return:
            JSON: Data fetched from API
        """
        
        path = f'{self.path}/{util.id_or_code(invoice, data=settings.INVOICE)}'

        payload = util.generate_payload(
            locals(), 'customer_code', 'customer_id', 'invoice_code', 'invoice_id')

        payload['customer'] = util.id_or_code(customer, data=settings.CUSTOMER)

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

        return self.put(path, payload)

    def archive(self, invoice: int | str):
        """Used to archive an invoice. Invoice will no longer be fetched on list or returned on verify:

        Args:
            invoice (int | str): The invoice ID or code

        Returns:
            JSON: Data fetched from API
        """
        path = f"{self.path}/archive/{util.id_or_code(invoice, data=settings.INVOICE)}"

        return self.get(path)
