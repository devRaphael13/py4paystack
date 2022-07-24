from . import routes
from .utilities import decorators


class Paystack:

    """
    General class that hold all the functionalities of the Paystack API.
    """

    @decorators.func_type_checker
    def __init__(self, secret_key: str) -> None:
        self.secret_key = secret_key

    def __repr__(self):
        return 'Paystack(paystack_secret_key)'

    def transaction(self):
        return routes.transactions.Transaction(self.secret_key)

    def transactionsplit(self):
        return routes.transactions_split.TransactionSplit(self.secret_key)

    def customers(self):
        return routes.customers.Customer(self.secret_key)

    def dedicated_virtual_accounts(self):
        return routes.virtual_accounts.DedicatedVirtualAccounts(self.secret_key)

    def applepay(self):
        return routes.apple_pay.ApplePay(self.secret_key)

    def subaccounts(self):
        return routes.subaccount.SubAccounts(self.secret_key)

    def plans(self):
        return routes.plans.Plan(self.secret_key)

    def subscriptions(self):
        return routes.subscription.Subscription(self.secret_key)

    def product(self):
        return routes.products.Product(self.secret_key)

    def payment_pages(self):
        return routes.payment_pages.PaymentPages(self.secret_key)

    def invoices(self):
        return routes.invoices.Invoice(self.secret_key)

    def settlement(self):
        return routes.settlement.Settlements(self.secret_key)

    def transfer_recipient(self):
        return routes.transfer_recipient.TransferRecipient(self.secret_key)

    def transfer(self):
        return routes.transfers.Tranfer(self.secret_key)

    def transfer_control(self):
        return routes.transfers_control.TransferControl(self.secret_key)

    def bulk_charges(self):
        return routes.bulk_charges.BulkCharges(self.secret_key)

    def control_panel(self):
        return routes.control_panel.ControlPanel(self.secret_key)

    def charge(self):
        return routes.charge.Charge(self.secret_key)

    def dispute(self):
        return routes.disputes.Disputes(self.secret_key)

    def refund(self):
        return routes.refund.Refund(self.secret_key)

    def verification(self):
        return routes.verification.Verification(self.secret_key)

    def miscellaneous(self):
        return routes.miscellaneous.Miscellaneous(self.secret_key)
