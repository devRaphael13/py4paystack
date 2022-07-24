from datetime import date, datetime
from typing import Sequence

from ..utilities import settings, util, decorators
from ..utilities.request import Request


@decorators.class_type_checker
class BulkCharges(Request):

    """
    The Bulk Charges API allows you create and manage multiple recurring payments from your customers
    """

    path = '/bulkcharge'

    def initiate(self, charges: Sequence):
        """Send list of tuples with authorization codes and amount (in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR ) 
        so we can process transactions as a batch.

        Args:
            charges ( Sequence[tuple[str, int]] ): List of tuples each containing an authorization code as a string
                and an amount to be charged as an integer eg [( "AUTH_n95vpedf", 2500 ), ( "AUTH_n95vpedf", 2500 ), ( "AUTH_n95vpedf", 2500 )]

        Returns:
            json: Data fetched from paystack API
        """

        payload = [{'authorization': util.check_code(
            settings.AUTHORIZATION, x[0]), 'amount': x[1]} for x in charges]

        return self.post(self.path, payload)

    def list_batches(self, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None):
        """This lists all bulk charge batches created by the integration. Statuses can be active, paused, or complete.

        Args:
            per_page (Optional[ int ]): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

            page (Optional[ int ]): Specify exactly what transfer you want to page. If not specify we use a default value of 1.

            from_date (Optional[ date | datetime | str ]): A timestamp from which to start listing batches e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

            to_date (Optional[ date | datetime | str ]): A timestamp at which to stop listing batches e.g. 2016-09-24T00:00:05.000Z, 2016-09-21


        Returns:
            json: Data fetched from paystack API
        """

        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch_batches(self, id_or_code: int | str):
        """This endpoint retrieves a specific batch code.
        It also returns useful information on its progress by way of the total_charges and pending_charges attributes.
    
        Args:
            id_or_code (int | str): An ID or code for the charge whose batches you want to retrieve.


        Returns:
            json: Data fetched from paystack API
        """

        path = f"{self.path}/{util.id_or_code(id_or_code, data=settings.BULK_CHARGE_BATCH)}"

        return self.get(path)

    def fetch_charges_in_batch(self, id_or_code: int | str, status: str = None, per_page: int = None, page: int = None, from_date: date | datetime | str = None, to_date: date | datetime | str = None):
        """This endpoint retrieves the charges associated with a specified batch code.
        Pagination parameters are available.
        You can also filter by status. Charge statuses can be pending, success or failed.

        Args:
            id_or_code (int | str): An ID or code for the batch whose charges you want to retrieve.

            status ( str ): Either one of these values: 'pending', 'success' or 'failed'

            per_page (Optional[ int ]): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

            page (Optional[ int ]): Specify exactly what transfer you want to page. If not specify we use a default value of 1.

            from_date (Optional[ date | datetime | str ]): A timestamp from which to start listing batches e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

            to_date (Optional[ date | datetime | str ]): A timestamp at which to stop listing batches e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

        Returns:
            json: Data fetched from paystack API
        """

        path = f"{self.path}/{util.id_or_code(id_or_code, data=settings.BULK_CHARGE_BATCH)}/charges"

        params = util.check_query_params(
            per_page=per_page, page=page, from_date=from_date, to_date=to_date)
        if status:
            params['status'] = util.check_membership(
                settings.BULK_CHARGE_STATUSES, status, status)

        if params:
            return self.get(util.handle_query_params(path, params))
        return self.get(path)

    def pause_batch(self, batch_code: str):
        """Use this endpoint to pause processing a batch

        Args:
            batch_code (str): The batch code for the bulk charge you want to pause

        Returns:
            json: Data fetched from paystack API
        """

        path = f"{self.path}/pause/{util.check_code(settings.BULK_CHARGE_BATCH, batch_code)}"

        return self.get(path)

    def resume_batch(self, batch_code: str):
        """Use this endpoint to resume processing a batch

        Args:
            batch_code (str): The batch code for the bulk charge you want to resume

        Returns:
            json: Data fetched from paystack API
        """
        path = f"{self.path}/resume/{util.check_code(settings.BULK_CHARGE_BATCH, batch_code)}"

        return self.get(path)
