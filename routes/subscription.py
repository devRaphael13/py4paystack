import datetime

from .utilities import settings, util
from .utilities.errors import MissingArgumentsError, UnwantedArgumentsError
from .utilities.request import Request


class Subscription(Request):

    """
    The Subscriptions API allows you create and manage recurring payment on your integration
    """

    path = "/subscription"


    def create(self, email_or_customer_code: str, plan_code: str, authorization_code: str = None, start_date: datetime.datetime | datetime.date | str = None):
        payload = {
            'customer': util.check_email_or_customer(email_or_customer_code),
            'plan': util.check_code(settings.CODE_NAMES['plan'], plan_code)
        }

        if authorization_code:
            payload['authorization'] = util.check_code(
                settings.CODE_NAMES['authorization'], authorization_code)

        if start_date:
            payload['start_date'] = util.handle_date(start_date)

        return self.post(self.path, payload=payload)

    def list_subscriptions(self, per_page: int = None, page: int = None, customer: int = None, plan: int = None):
        params = util.generate_payload(locals())
        params.update(util.check_query_params(per_page=per_page, page=page))

        if params:
            return self.get(util.handle_query_params(self.path, params))
        return self.get(self.path)

    def fetch(self, subscription_id: int = None, subscription_code: str = None):
        path = self.path
        if not (subscription_id or subscription_code):
            raise MissingArgumentsError("Provide subscription id or code")

        if subscription_id:
            path += f"/{subscription_id}"

        if subscription_code and not subscription_id:
            path += f"/{util.check_code(settings.CODE_NAMES['subscription'], subscription_code)}"

        return self.get(path)

    def enable(self, subscription_code: str, email_token: str):
        path = f"{self.path}/enable"
        payload = {
            'code': util.check_code(settings.CODE_NAMES['subscription'], subscription_code),
            'token': email_token
        }

        return self.post(path, payload)

    def disable(self, subscription_code: str, email_token: str):
        path = f"{self.path}/disable"
        payload = {
            'code': util.check_code(settings.CODE_NAMES['subscription'], subscription_code),
            'token': email_token
        }
        return self.post(path, payload)

    def generate_update_link(self, subscription_code: str):
        path = f"{self.path}/{util.check_code(settings.CODE_NAMES['subscription'], subscription_code)}/manage/link"

        return self.get(path)

    def send_update_link(self, subscription_code: str):
        path = f"{self.path}/{util.check_code(settings.CODE_NAMES['subscription'], subscription_code)}/manage/link"

        return self.get(path)
