from datetime import date, datetime

from .utilities import settings, util
from .utilities.errors import MissingArgumentsError
from .utilities.request import Request


class BulkCharges(Request):

    """
    The Bulk Charges API allows you create and manage multiple recurring payments from your customers
    """

    path = '/bulkcharge'

    def initiate(self, *charges):
        for x in charges:
            if ('authorization', 'amount') not in x:
                raise MissingArgumentsError(
                    'provide authorization and amount')

            x['authorization'] = util.check_code(
                settings.AUTHORIZATION, x['authorization'])

        return self.post(self.path, charges)

    def list_batches(self, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None):
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch_batches(self, batch_id: int = None, batch_code: str = None):
        path = f"{self.path}/{util.id_or_code(_id=batch_id, code=batch_code, data=settings.BULK_CHARGE_BATCH)}"

        return self.get(path)

    def fetch_charges_in_batch(self, batch_id: int = None, batch_code: str = None, status: str = None, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None):
        path = f"{self.path}/{util.id_or_code(_id=batch_id, code=batch_code, data=settings.BULK_CHARGE_BATCH)}/charges"

        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if status:
            params['status'] = util.check_membership(
                settings.BULK_CHARGE_STATUSES, status, status)

        if params:
            return self.get(util.handle_query_params(path, params))
        return self.get(path)

    def pause_batch(self, batch_code: str):
        path = f"{self.path}/pause/{util.check_code(settings.BULK_CHARGE_BATCH, batch_code)}"

        return self.get(path)

    def resume_batch(self, batch_code: str):
        path = f"{self.path}/resume/{util.check_code(settings.BULK_CHARGE_BATCH, batch_code)}"

        return self.get(path)
