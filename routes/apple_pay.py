from .utilities import util, decorators
from .utilities.request import Request


@decorators.class_type_checker
class ApplePay(Request):

    """
    The Apple Pay API allows you register your application's top-level domain or subdomain
    """

    path = '/apple-pay/domain'

    def register(self, domain: str):

        payload = {
            'domainName': util.check_domain(domain)
        }
        return self.post(self.path, payload=payload)

    def list_domains(self):
        return self.get(self.path)

    def unregister(self, domain: str):
        payload = {
            'domainName': util.check_domain(domain)
        }
        return self.delete(self.path, payload=payload)
