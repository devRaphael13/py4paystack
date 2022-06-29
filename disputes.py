from datetime import date, datetime

from . import settings, util
from .request import Request


class Disputes(Request):

    """The Disputes API allows you manage transaction disputes on your integration
    """

    path = '/dispute'


    def list_disputes(self, page: int = None, per_page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None, transaction_id: int = None, status: str = None):
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)

        if transaction_id:
            params['transaction'] = transaction_id

        if status:
            params['status'] = util.check_membership(
                settings.DISPUTE_STATUSES, status, 'status')

        if params:
            path = util.handle_query_params(self.path, params)
            return self.get(path)
        return self.get(self.path)

    def fetch(self, dispute_id: int):
        path = f'{self.path}/{dispute_id}'
        return self.get(path)

    def list_transaction_disputes(self, transaction_id: int):
        path = f'{self.path}/transaction/{transaction_id}'
        return self.get(path)

    def update(self, dispute_id: int, refund_amount: int, uploaded_filename: str = None):
        path = f'{self.path}/{dispute_id}'
        payload = util.generate_payload(locals(), 'dispute_id')
        return self.put(path, payload)

    def add_evidence(self, dispute_id: int, customer_email: str, customer_name: str, customer_phone: str, service_details: str, delivery_address: str = None, delivery_date: date | datetime | str = None):
        path = f'{self.path}/{dispute_id}/evidence'
        payload = util.generate_payload(locals(), 'dispute_id')
        payload['customer_email'] = util.check_email(customer_email)

        if delivery_date:
            payload['delivery_date'] = util.handle_date(delivery_date)
        return self.post(path, payload)

    def get_upload_url(self, dispute_id: int, upload_filename: str = None):
        path = f'{self.path}/{dispute_id}/upload_url'
        if upload_filename:
            path = util.handle_query_params(
                path, {'upload_filename': upload_filename})
        return self.get(path)

    def resolve(self, dispute_id: int, resolution: str, message: str, refund_amount: int, upload_url: str, evidence_id: int = None):
        path = f'{self.path}/{dispute_id}/resolve'
        payload = util.generate_payload(locals(), 'dispute_id')
        payload['resolution'] = util.check_membership(
            settings.DISPUTE_RESOLUTION, resolution, 'resolution')

        if evidence_id:
            payload['evidence'] = payload.pop('evidence_id')
        return self.put(path, payload)

    def export(self, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date:  date | datetime | str = None, transaction_id: int = None, status: str = None):
        path = f'{self.path}/export'
        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)

        if transaction_id:
            params['transaction'] = transaction_id

        if status:
            params['status'] = util.check_membership(
                settings.DISPUTE_STATUSES, status, 'status')

        if params:
            path = util.handle_query_params(path, params)
        return self.get(path)
