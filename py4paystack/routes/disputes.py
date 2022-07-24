from datetime import date, datetime

from ..utilities import settings, util, decorators
from ..utilities.request import Request


@decorators.class_type_checker
class Disputes(Request):

    """
    The Disputes API allows you manage transaction disputes on your integration
    """

    path = '/dispute'

    def list_disputes(self, page: int = None, per_page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None, transaction_id: int = None, status: str = None):
        """List all the dispute filed against you.

        Args:
            page (int, optional): Specify exactly what dispute you want to page. If not specify we use a default value of 1.
                Defaults to None.
            per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.
                Defaults to None.
            from_date (date | datetime | str, optional): A timestamp from which to start listing dispute e.g. 2016-09-21.
                Defaults to None.
            to_date (date | datetime | str, optional): A timestamp at which to stop listing dispute e.g. 2016-09-21.
                Defaults to None.
            transaction_id (int, optional): Transaction Id. Defaults to None.
            status (str, optional): Dispute Status. Acceptable values: { awaiting-merchant-feedback | awaiting-bank-feedback | pending | resolved }.
                Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

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
        """Get more details about a dispute

        Args:
            dispute_id (int): The ID of the dispute your want to fetch

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{dispute_id}'
        return self.get(path)

    def list_transaction_disputes(self, transaction_id: int):
        """Retrieve disputes for a particular transaction

        Args:
            transaction_id (int): ID of the transaction whose dispute you want to fetch

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/transaction/{transaction_id}'
        return self.get(path)

    def update(self, dispute_id: int, refund_amount: int = None, uploaded_filename: str = None):
        """Update details of a dispute on your integration

        Args:
            dispute_id (int): The ID of the dispute to be updated
            refund_amount (int, optional): The amount to refund, in kobo if currency is NGN, pesewas,
                if currency is GHS, and cents, if currency is ZAR. Defaults to None
            uploaded_filename (str, optional): filename of attachment returned via response from upload url(GET /dispute/:id/upload_url).
                Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{dispute_id}'
        payload = util.generate_payload(locals(), 'dispute_id')
        return self.put(path, payload)

    def add_evidence(self, dispute_id: int, customer_email: str, customer_name: str, customer_phone: str, service_details: str, delivery_address: str = None, delivery_date: date | datetime | str = None):
        """Provide evidence for the dispute.

        Args:
            dispute_id (int): ID of the dispute to add evidence for.
            customer_email (str): Customer's email address
            customer_name (str): Customer's name
            customer_phone (str):Customer's phone number
            service_details (str): Details of the service involved
            delivery_address (str, optional): Delivery Address. Defaults to None.
            delivery_date (date | datetime | str, optional): ISO 8601 representation of delivery date (YYYY-MM-DD). 
                Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{dispute_id}/evidence'
        payload = util.generate_payload(locals(), 'dispute_id')
        payload['customer_email'] = util.check_email(customer_email)

        if delivery_date:
            payload['delivery_date'] = util.handle_date(delivery_date)
        return self.post(path, payload)

    def get_upload_url(self, dispute_id: int, upload_filename: str = None):
        """Get URL to upload a dispute evidence.

        Args:
            dispute_id (int): ID of the dispute
            upload_filename (str, optional): The file name, with its extension, that you want to upload.
                e.g filename.pdf. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{dispute_id}/upload_url'
        if upload_filename:
            path = util.handle_query_params(
                path, {'upload_filename': upload_filename})
        return self.get(path)

    def resolve(self, dispute_id: int, resolution: str, message: str, refund_amount: int, upload_url: str, evidence_id: int = None):
        """Resolve disputes on your integration

        Args:
            dispute_id (int): ID of the dispute to be resolved.
            resolution (str): Dispute resolution. Accepted values: { merchant-accepted | declined }.
            message (str): Reason for resolving
            refund_amount (int): The amount to refund, in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR
            upload_url (str): Filename of attachment returned via response from upload url(GET /dispute/:id/upload_url)
            evidence_id (int, optional): Evidence Id for fraud claims. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

        path = f'{self.path}/{dispute_id}/resolve'
        payload = util.generate_payload(locals(), 'dispute_id')
        payload['resolution'] = util.check_membership(
            settings.DISPUTE_RESOLUTION, resolution, 'resolution')

        if evidence_id:
            payload['evidence'] = payload.pop('evidence_id')
        return self.put(path, payload)

    def export(self, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date:  date | datetime | str = None, transaction_id: int = None, status: str = None):
        """Export disputes available on your integration\

        Args:
            per_page (int, optional): Specify how many records you want to retrieve per page.
                If not specify we use a default value of 50.. Defaults to None.
            page (int, optional): Specify exactly what dispute you want to page.
                If not specify we use a default value of 1.. Defaults to None.
            from_date (date | datetime | str, optional): A timestamp from which to start listing dispute
                e.g. 2016-09-21. Defaults to None.
            to_date (date | datetime | str, optional): A timestamp at which to stop listing dispute
                e.g. 2016-09-21. Defaults to None.
            transaction_id (int, optional): Transaction ID. Defaults to None.
            status (str, optional): Dispute Status. Acceptable values: { awaiting-merchant-feedback | awaiting-bank-feedback | pending | resolved }. Defaults to None.

        Returns:
            JSON: Data fetched from API
        """

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
