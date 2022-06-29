from . import util
from .request import Request
from . import settings
from .errors import MissingArgumentsError, UnwantedArgumentsError


class Plan(Request):

    """
    The Plans API allows you create and manage installment payment options on your integration
    """

    path = '/plan'


    def create(self, name: str, amount: int, interval: str, description: str = None, send_invoices: bool = None, send_sms: bool = None, currency: str = None, invoice_limit: int = None):
        payload = util.generate_payload(locals())
        payload['interval'] = util.check_membership(settings.PLAN_INTERVALS, interval, 'interval')
        if currency:
            payload['currency'] = util.check_membership(settings.CURRENCIES, currency, 'currency')

        return self.post(self.path, payload=payload)

    def list_plans(self, per_page: int = None, page: int = None, status: str = None, interval: str = None, amount: int = None):
        params = util.check_query_params(per_page=per_page, page=page)

        if interval:
            params['interval'] = util.check_membership(settings.PLAN_INTERVALS, interval, 'interval')

        if status:
            params['status'] = util.check_membership(settings.PLAN_STATUSES, status, 'status')

        if params:
            return self.get(util.handle_query_params(self.path, paramsh)
        return self.get(self.path)

    def fetch(self, plan_id: int = None, plan_code: str = None):
        path = self.path
        if not (plan_id or plan_code):
            raise MissingArgumentsError("Provide plan id or code")

        if plan_id:
            path += f'/{plan_id}'

        if plan_code and not plan_id:
            path += f"/{util.check_code(settings.CODE_NAMES['plan'], plan_code)}"

        return self.get(path)

    def update(self, plan_id: int = None, plan_code: str = None, name: str = None, interval: str = None, description: str = None, send_invoices: bool = None, send_sms: bool = None, invoice_limit: int = None):
        path = self.path
        if not (plan_id or plan_code):
            raise MissingArgumentsError("Provide plan id or code")

        if plan_id:
            path += f"/{plan_id}"

        if plan_code and not plan_id:
            path += f"/{util.check_code(settings.CODE_NAMES['plan'], plan_code)}"

        payload = util.generate_payload(locals(), 'plan_id', 'plan_code', 'path')

        if interval:
            payload['interval'] = util.check_membership(settings.PLAN_INTERVALS, interval, 'interval')

        return self.put(path, payload=payload)
