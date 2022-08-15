from .routes import (apple_pay, bulk_charges, charge, control_panel, customers,
                     disputes, invoices, miscellaneous, payment_pages, plans,
                     products, refund, settlement, subaccount, subscription,
                     transactions, transactions_split, transfer_recipient,
                     transfers, transfers_control, verification,
                     virtual_accounts)
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
        return transactions.Transaction(self.secret_key)

    def transactionsplit(self):
        return transactions_split.TransactionSplit(self.secret_key)

    def customers(self):
        return customers.Customer(self.secret_key)

    def dedicated_virtual_accounts(self):
        return virtual_accounts.DedicatedVirtualAccounts(self.secret_key)

    def applepay(self):
        return apple_pay.ApplePay(self.secret_key)

    def subaccounts(self):
        return subaccount.SubAccounts(self.secret_key)

    def plans(self):
        return plans.Plan(self.secret_key)

    def subscriptions(self):
        return subscription.Subscription(self.secret_key)

    def product(self):
        return products.Product(self.secret_key)

    def payment_pages(self):
        return payment_pages.PaymentPages(self.secret_key)

    def invoices(self):
        return invoices.Invoice(self.secret_key)

    def settlement(self):
        return settlement.Settlements(self.secret_key)

    def transfer_recipient(self):
        return transfer_recipient.TransferRecipient(self.secret_key)

    def transfer(self):
        return transfers.Tranfer(self.secret_key)

    def transfer_control(self):
        return transfers_control.TransferControl(self.secret_key)

    def bulk_charges(self):
        return bulk_charges.BulkCharges(self.secret_key)

    def control_panel(self):
        return control_panel.ControlPanel(self.secret_key)

    def charge(self):
        return charge.Charge(self.secret_key)

    def dispute(self):
        return disputes.Disputes(self.secret_key)

    def refund(self):
        return refund.Refund(self.secret_key)

    def verification(self):
        return verification.Verification(self.secret_key)

    def miscellaneous(self):
        return miscellaneous.Miscellaneous(self.secret_key)
