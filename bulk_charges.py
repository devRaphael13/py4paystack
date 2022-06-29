from datetime import date, datetime

from . import settings, util
from .errors import MissingArgumentsError
from .request import Request


class BulkCharges(Request):

    """
    The Bulk Charges API allows you create and manage multiple recurring payments from your customers
    """

    path = '/bulkcharge'

    @staticmethod
    def id_or_code(batch_id: int = None, batch_code: str = None):
        if not (batch_id or batch_code):
            raise MissingArgumentsError(
                'provide either batch_id or batch_code')

        if batch_id:
            return batch_id
        return util.check_code(settings.CODE_NAMES, batch_code)

    def initiate(self, *charges):
        for x in charges:
            if ('authorization', 'amount') not in x:
                raise MissingArgumentsError(
                    'provide authorization and amount')

            x['authorization'] = util.check_code(
                settings.CODE_NAMES['authorization'], x['authorization'])

        return self.post(self.path, charges)

    def list_batches(self, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None):
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch_batches(self, batch_id: int = None, batch_code: str = None):
        path = f"{self.path}/{self.id_or_code(batch_id=batch_id, batch_code=batch_code)}"

        return self.get(path)

    def fetch_charges_in_batch(self, batch_id: int = None, batch_code: str = None, status: str = None, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None):
        path = f"{self.path}/{self.id_or_code(batch_id=batch_id, batch_code=batch_code)}/charges"

        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if status:
            params['status'] = util.check_membership(
                settings.BULK_CHARGE_STATUSES, status, status)

        if params:
            return self.get(util.handle_query_params(path, params))
        return self.get(path)

    def pause_batch(self, batch_code: str):
        path = f"{self.path}/pause/{util.check_code(settings.CODE_NAMES['bulk_charge_batch'], batch_code)}"

        return self.get(path)

    def resume_batch(self, batch_code: str):
        path = f"{self.path}/resume/{util.check_code(settings.CODE_NAMES['bulk_charge_batch'], batch_code)}"

        return self.get(path)
