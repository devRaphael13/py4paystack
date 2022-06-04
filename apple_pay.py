from .request import Request
from . import util


class ApplePay(Request):

    path = '/apple-pay/domain'

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def register(self, domain: str):
        payload = {
            'domainName': util.check_domain(domain)
        }
        return self.post(self.path, self.secret_key, payload)

    def list_domains(self):
        self.get(self.path, self.secret_key)

    def unregister(self, domain: str):
        payload = {
            'domainName': util.check_domain(domain)
        }
        return self.delete(self.path, self.secret_key, payload=payload)
