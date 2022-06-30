from .utilities.request import Request


class ControlPanel(Request):

    """
    The Control Panel API allows you manage some settings on your integration
    """

    path = 'integration/payment_session_timeout'

    def fetch_payment_session_timeout(self):
        return self.get(self.path)

    def update_payment_session_timeout(self, time_out: int):
        return self.put(self.path, {'timeout': time_out})
