from .utilities import util
from .utilities.request import Request


class ApplePay(Request):

    """
    The Apple Pay API allows you register your application's top-level domain or subdomain
    """

    path = '/apple-pay/domain'

    def register(self, domain: str):
        """Register a top-level domain or subdomain for your Apple Pay integration.

        Args:
            domain (str): Domain name to be registered

        Returns:
            json
        """

        payload = {
            'domainName': util.check_domain(domain)
        }
        return self.post(self.path, payload=payload)

    def list_domains(self):
        """Lists all registered domains on your integration. Returns an empty array if no domains have been added.

        Returns:
            json
        """
        return self.get(self.path)

    def unregister(self, domain: str):
        """Unregister a top-level domain or subdomain previously used for your Apple Pay integration.

        Args:
            domain (str): Domain name to be unregistered

        Returns:
            json
        """
        payload = {
            'domainName': util.check_domain(domain)
        }
        return self.delete(self.path, payload=payload)
