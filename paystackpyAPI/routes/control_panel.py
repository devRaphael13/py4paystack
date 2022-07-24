from ..utilities.request import Request
from ..utilities import decorators


@decorators.class_type_checker
class ControlPanel(Request):

    """
    The Control Panel API allows you manage some settings on your integration
    """

    path = 'integration/payment_session_timeout'

    def fetch_payment_session_timeout(self):
        """Fetch the payment session timeout on your integration

        Returns:
            JSON: Data fetched from API
        """
        return self.get(self.path)

    def update_payment_session_timeout(self, time_out: int):
        """Update the payment session timeout on your integration

        Args:
            time_out (int): Time before stopping session (in seconds).
                Set to 0 to cancel session timeouts

        Returns:
            JSON: Data fetched from API
        """
        return self.put(self.path, {'timeout': time_out})
