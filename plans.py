from . import util
from .request import Request
from . import settings


class Plan(Request):

    """
    The Plans API allows you create and manage installment payment options on your integration
    """

    path = '/plan'

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create(self, name: str, amount: int, interval: str, description: str = None, send_invoices: bool = None, send_sms: bool = None, currency: str = None, invoice_limit: int = None):
        payload = {key: value for key, value in locals().items()
                   if value is not None}
        payload['interval'] = util.check_plan_interval(interval)
        if currency:
            payload['currency'] = util.check_currency(currency)

        return self.post(self.path, self.secret_key, payload=payload)

    def list_plans(self, per_page: int = None, page: int = None, status: str = None, interval: str = None, amount: int = None):
        params = util.check_query_params(per_page=per_page, page=page)

        if interval:
            params['interval'] = util.check_plan_interval(interval)

        if status:
            params['status'] = util.check_plan_status(status)

        if params:
            path = util.handle_query_params(self.path, params)
        return self.get(path, self.secret_key)

    def fetch(self, plan_id: int = None, plan_code: str = None):
        path = self.path
        if not (plan_id or plan_code):
            raise ValueError("Provide plan id or code")

        if plan_id:
            path += f'/{plan_id}'

        if plan_code and not plan_id:
            path += f"/{util.check_code(settings.CODE_NAMES['plan'], plan_code)}"

        return self.get(path, self.secret_key)

    def update(self, plan_id: int = None, plan_code: str = None, name: str = None, interval: str = None, description: str = None, send_invoices: bool = None, send_sms: bool = None, invoice_limit: int = None):
        path = self.path
        if not (plan_id or plan_code):
            raise ValueError("Provide plan id or code")

        if plan_id:
            path += f"/{plan_id}"

        if plan_code and not plan_id:
            path += f"/{util.check_code(settings.CODE_NAMES['plan'], plan_code)}"

        payload = {key: value for key, value in locals().items() if key not in (
            'plan_id', 'plan_code') and value is not None}

        if interval:
            payload['interval'] = util.check_plan_interval(interval)

        return self.put(path, self.secret_key, payload=payload)
