## Py4paystack

A paystack API wrapper with type checking written in python

## Contents

- [Installation](#installation)
- [Type Checking](#type-checking)
- [Requirements](#requirements)
- [Changelog](#changelog)
- [Accept payments](#accept-payments)
- [Advanced Usage](#advanced-usage)
- [API Routes](#routes)

<br>
<br>

## Installation

Run `pip install py4paystack` on the commandline to install.

<br>

<br>

## Requirements

- python-dotenv

<br>

<br>

## Changelog

**V1.0.2**
- Bug fixes

<br>

<br>

## Type Checking

The Type checking funtion is on by default, turn of by setting `TYPE_CHECK` to `False` in your .env file.

<br>

## Accept Payments

To accept payments, you can import the Transaction class from the routes module if that'll be all you need, alternatively you can import the Paystack class like if you need more functionality.

```{python}
from py4paystack.routes.transactions import Transaction # or from py4paystack.paystack import Paystack

trans = Transaction('ExampleSecretKey') # or
trans = Paystack('ExampleSecretKey).transaction()

res = trans.initialize('testemail@test.com', 120934)
```

Where 'testemail@test.com' is the users email and 120934 is the amount in the smallest denomination of the currency i.e in Naira the user would be paying N1,209.34k

This returns data in JSON format e.g something that looks like this

    {
      "status": true,
      "message": "Authorization URL created",
      "data": {
        "authorization_url": "https://checkout.paystack.com/0peioxfhpn",
        "access_code": "0peioxfhpn",
        "reference": "7PVGX8MEk85tgeEpVDtD"
      }
    }

Redirect the user to "authorization_url" to accept the payment.

<br>

## Advanced Usage

For more use cases keep reading........... or check out [paystack api documentation](https://paystack.com/docs/api)

<br>

## Routes

- [Paystack](#paystack)
- [Apple Pay](#apple-pay)
- [Bulk Charges](#bulk-charges)
- [Charge](#charge)
- [Control Panel](#control-panel)
- [Customer](#customer)
- [Disputes](#disputes)
- [Dedicated Virtual Accounts](#dedicated-virtual-accounts)
- [Invoice](#invoice)
- [Miscellaneous](#miscellaneous)
- [Payment Pages](#payment-pages)
- [Plan](#plan)
- [Product](#product)
- [Refund](#refund)
- [Settlements](#settlements)
- [Subaccount](#subaccounts)
- [Subscription](#subscription)
- [Transaction Split](#transaction-split)
- [Transaction](#transaction)
- [Transfer Control](#transfer-control)
- [Transfer Recipient](#transfer-recipient)
- [Transfer](#transfer)
- [Verification](#verification)

<br>
<br>
<hr>
<br>
<br>

## **Paystack**

    py4paystack.paystack.Paystack

<br>

`Paystack(secret_key: str)`

General class that hold all the functionalities of the Paystack API (essentially a class to rule them all). Methods returns and instance of the class with the same name i.e `Paystack('Paystack secret_key').charge()` is equivalent to `Charge('Paystack secret_key')`, use the first approach if you are going to need multiple functionalities and don't want to import each class individually and the second when you just need one class or functionality e.g you just need the Transaction class.

**Methods**

- `applepay(self)`

- `bulk_charges(self)`

- `charge(self)`

- `control_panel(self)`

- `customers(self)`

- `dedicated_virtual_accounts(self)`

- `dispute(self)`

- `invoices(self)`

- `miscellaneous(self)`

- `payment_pages(self)`

- `plans(self)`

- `product(self)`

- `refund(self)`

- `settlement(self)`

- `subaccounts(self)`

- `subscriptions(self)`

- `transaction(self)`

- `transactionsplit(self)`

- `transfer(self)`

- `transfer_control(self)`

- `transfer_recipient(self)`

- `verification(self)`

<br>

[Back to the top](#routes)
<br>
<br>

## **Apple Pay**

    py4paystack.routes.apple_pay.ApplePay

<br>

`ApplePay(secret_key: str)`

The Apple Pay API allows you register your application's top-level domain or subdomain

<br>

### **Methods**

- `list_domains(self)`

  Lists all registered domains on your integration.
  Returns an empty array if no domains have been added.

  **Returns**:

        json: Data fetched from paystack API

<br>

- `register(self, domain: str)`

  Register a top-level domain or subdomain for your Apple Pay integration.

  **Args**:

        domain [str]: The domain name to be registered.

  **Returns**:

        json: Data fetched from paystack API

<br>

- `unregister(self, domain: str)`

  Unregister a top-level domain or subdomain previously used for your Apple Pay integration.

  **Args**:

        domain [str]: The domain name to be unregistered

  **Returns**:

        json: Data fetched from paystack API

<br>

[Back to the top](#routes)
<br>
<br>

## **Bulk Charges**

    py4paystack.routes.bulk_charges.BulkCharges

<br>

`BulkCharges(secret_key: str)`

The Bulk Charges API allows you create and manage multiple recurring payments from your customers

<br>

### **Methods**

- `fetch_batches(self, id_or_code: Union[int, str])`

  This endpoint retrieves a specific batch code.
  It also returns useful information on its progress by way of the total_charges and pending_charges attributes.

  **Args**:

        id_or_code (Union[int, str]): An ID or code for the charge whose batches you want to retrieve.

  **Returns**:

        json: Data fetched from paystack API

<br>

- `fetch_charges_in_batch(self, id_or_code: Union[int, str], status: str = None, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None)`

  This endpoint retrieves the charges associated with a specified batch code.
  Pagination parameters are available.
  You can also filter by status. Charge statuses can be pending, success or failed.

  **Args**:

        id_or_code (Union[int, str]): An ID or code for the batch whose charges you want to retrieve.

        status ( str ): Either one of these values: 'pending', 'success' or 'failed'

        per_page (Optional[ int ]): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

        page (Optional[ int ]): Specify exactly what transfer you want to page. If not specify we use a default value of 1.

        from_date (Optional[ Union[date, datetime, str] ]): A timestamp from which to start listing batches e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

        to_date (Optional[ Union[date, datetime, str] ]): A timestamp at which to stop listing batches e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

  **Returns**:

        json: Data fetched from paystack API

<br>

- `initiate(self, charges: Sequence)`

  Send list of tuples with authorization codes and amount (in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR )
  so we can process transactions as a batch.

  **Args**:

        charges ( Sequence[tuple[str, int]] ): List of tuples each containing an authorization code as a string
            and an amount to be charged as an integer eg [( "AUTH_n95vpedf", 2500 ), ( "AUTH_n95vpedf", 2500 ), ( "AUTH_n95vpedf", 2500 )]

  **Returns**:

        json: Data fetched from paystack API

<br>

- `list_batches(self, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None)`

  This lists all bulk charge batches created by the integration. Statuses can be active, paused, or complete.

  **Args**:

        per_page (Optional[ int ]): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

        page (Optional[ int ]): Specify exactly what transfer you want to page. If not specify we use a default value of 1.

        from_date (Optional[ Union[date, datetime, str] ]): A timestamp from which to start listing batches e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

        to_date (Optional[ Union[date, datetime, str] ]): A timestamp at which to stop listing batches e.g. 2016-09-24T00:00:05.000Z, 2016-09-21

  **Returns**:

        json: Data fetched from paystack API

<br>

- `pause_batch(self, batch_code: str)`

  Use this endpoint to pause processing a batch

  **Args**:

        batch_code (str): The batch code for the bulk charge you want to pause

  **Returns**:

        json: Data fetched from paystack API

<br>

- `resume_batch(self, batch_code: str)`

  Use this endpoint to resume processing a batch

  **Args**:

        batch_code (str): The batch code for the bulk charge you want to resume

  **Returns**:

        json: Data fetched from paystack API

<br>

[Back to the top](#routes)
<br>
<br>

## **Charge**

    py4paystack.routes.charge.Charge

<br>

`Charge(secret_key: str)`

The Charge API allows you to configure payment channel of your choice when initiating a payment.

<br>

### **Methods**:

- `check_pending_charge(self, reference: str)`

  When you get "pending" as a charge status or if there was an exception when calling any of the /charge endpoints,
  wait 10 seconds or more, then make a check to see if its status has changed.
  Don't call too early as you may get a lot more pending than you should.

  **Args**:

        reference (str): Reference to check

  **Returns**:

        JSON: Data fetched from API

<br>

- `create(self, email: str, amount: int, bank_code: str = None, account_number: str = None, currency: str = None, authorization_code: str = None, reference: str = None, pin: str = None, ussd: int = None, phone: str = None, provider: str = None, metadata: dict = None, device_id: str = None, generate_reference: bool = False)`

      The Charge API allows you to configure payment channel of your choice when initiating a payment.

      **Args**:

          email (str): Customer's email address

          amount (int): Amount should be in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR

          bank_code (str, optional): Bank code to use. Provide with account_number. Don't send if you sending authorization_code. Defaults to None.

          account_number (str, optional): Account number to charge. Provide with bank_code. Don't send if you sending authorization_code. Defaults to None.

          currency (str, optional): The currency you want to charge in. Defaults to None.

          authorization_code (str, optional): An authorization code to charge (don't send if charging a bank account). Defaults to None.

          reference (str, optional): Unique transaction reference. Only -, .`, = and alphanumeric characters allowed.. Defaults to None.

          pin (str, optional): 4-digit PIN (send with a non-reusable authorization code). Defaults to None.

          ussd (int, optional): USSD type to charge (don't send if charging an authorization code, bank or card). Defaults to None.

          phone (str, optional): 11 digit str phone number to use with mobile money. Provide with provider. Defaults to None.

          provider (str, optional): mobile money provider, your choices are 'tgo' for Airtel/Tigo, 'mtn' for MTN, 'vod' for vodafone. Defaults to None.

          metadata (dict, optional): A JSON object. Defaults to None.

          device_id (str, optional): This is the unique identifier of the device a user uses in making payment. Only -, .`, = and alphanumeric characters allowed.. Defaults to None.

          generate_reference (bool, optional): Whether to generate reference for you. Defaults to False.

      **Raises**:

          MissingArgumentsError: raised when a wanted argument is missing

          UnwantedArgumentsError: raised when an unwanted argument is provided

      **Returns**:

          json: Data fetched from API

  <br>

- `submit_address(self, reference: str, address: str, city: str, state: str, zipcode: str)`

      Submit address to continue charge

      **Args**:

          reference (str): Reference for the ongoing transaction

          address (str): Address submitted by the user

          city (str): City submitted by the user

          state (str): State submitted by the user

          zipcode (str): Zipcode submitted by the user

      **Returns**:

          JSON: Data fetched from paystack API

  <br>

- `submit_birthday(self, birthday: Union[datetime.datetime, datetime.date, str], reference: str)`

      Submit Phone when requested

      **Args**:

          birthday ( Union[date, datetime, str] ): birthday submitted by the user

          reference (str): Reference of the ongoing transaction

      **Returns**:

          JSON: Data fetched from API

  <br>

- `submit_otp(self, otp: str, reference: str)`

      Submit OTP to complete a charge

      **Args**:

          otp (str): OTP submitted by the user

          reference (str): Reference for the ongoing transation

      **Returns**:

          JSON: Data fetched from API

  <br>

- `submit_phone(self, phone: str, reference: str)`

  Submit Phone when requested

  **Args**:

        phone (str): Phone number submitted by the user

        reference (str): Reference of the ongoing transation

  **Returns**:

        JSON: Data fetched from API

<br>

- `submit_pin(self, pin: str, reference: str)`

  Submit PIN to continue a charge

  **Args**:

        pin (str): Pin provided by the user

        reference (str): reference of the transaction that requested the pin

  **Returns**:

        JSON: Data fetched from API

<br>

[Back to the top](#routes)
<br>
<br>

## **Control Panel**
    py4paystack.routes.control_panel.ControlPanel
<br>

`ControlPanel(*args, **kwargs)`

The Control Panel API allows you manage some settings on your integration
<br>

### **Methods**:

- `fetch_payment_session_timeout(self)`

      Fetch the payment session timeout on your integration

      **Returns**:

          JSON: Data fetched from API

  <br>

- `update_payment_session_timeout(self, time_out: int)`

  Update the payment session timeout on your integration

  **Args**:

        time_out (int): Time before stopping session (in seconds). Set to 0 to cancel session timeouts

  **Returns**:

        JSON: Data fetched from API

<br>

[Back to the top](#routes)
<br>
<br>

## **Customer**
    py4paystack.routes.customer.Customer
<br>

`Customer(secret_key: str)`

    The Customers class allows you create and manage customers on your integration.

<br>

### **Methods**:

- `create(self, email: str, first_name: str = None, last_name: str = None, phone: str = None, metadata: dict = None)`

      Create a customer on your integration. The first_name, last_name and phone are optional parameters.
      However, when creating a customer that would be assigned a Dedicated Virtual Account and your business catgeory falls under Betting,
      Financial services, and General Service, then these parameters become compulsory.

      **Args**:

          email (str): Customer's email address.

          first_name (str, optional): Customer's first name. Defaults to None.

          last_name (str, optional): Customer's last name. Defaults to None.

          phone (str, optional): Customer's phone number. Defaults to None.

          metadata (dict, optional): A set of key/value pairs that you can attach to the customer.It can be used to store additional information in a structured format. Defaults to None.

      **Returns**:

          JSON: Data fetched from API.

  <br>

- `deactivate_authorization(self, authorization_code: str)`

      Deactivate an authorization when the card needs to be forgotten

      **Args**:

          authorization_code (str): Authorization code for a card that needs to be forgotten.

      **Returns**:

          JSON: Data fetched from API

  <br>

- `fetch(self, email_or_customer_code: str)`

      Get details of a customer on your integration.

      **Args**:

          email_or_customer_code (str): An email or customer code for the customer you want to fetch

      **Returns**:

          JSON: Data fetched from API

  <br>

- `list_customers(self, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None)`

      List customers available on your integration.

      **Args**:

          per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

          page (int, optional): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.

          from_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp from which to start listing customers e.g 2016-09-24T00:00:05.000Z, 2016. Defaults to None.

          to_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp at which to stop listing customers e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

      **Returns**:

          JSON: Data fetched from API

  <br>

- `update(self, customer_code: str, first_name: str = None, last_name: str = None, phone: str = None, metadata: dict = None)`

      Update a customer's details on your integration

      **Args**:

          customer_code (str): Code for the customer you want to update.

          first_name (str, optional): Customer's first name. Defaults to None.

          last_name (str, optional): Customer's last name. Defaults to None.

          phone (str, optional): Customer's phone number. Defaults to None.

          metadata (dict, optional): A set of key/value pairs that you can attach to the customer. It can be used to store additional information in a structured format. Defaults to None.

      **Returns**:

          JSON: Data fetched from API

  <br>

- `validate(self, customer_code: str, first_name: str, last_name: str, identification_type: str, country: str, bvn: str, bank_code: str = None, account_number: str = None, middle_name: str = None)`

      Validate a customer's identity

      **Args**:

          customer_code (str): Code for the customer you want to validate

          first_name (str): Customer's first name
          last_name (str): Customer's last name

          identification_type (str): Predefined types of identification. Valid values: bvn, bank_account

          country (str): 2 letter country code of identification issuer

          bvn (str): Customer's Bank Verification Number

          bank_code (str, optional): You can get the list of Bank Codes by calling the List Banks endpoint. (required if type is bank_account). Defaults to None.

          account_number (str, optional): Customer's bank account number. (required if type is bank_account). Defaults to None.

          middle_name (str, optional): Customer's middle name. Defaults to None.

      **Returns**:

          JSON: Data fetched from API

  <br>

- `whitelist_blacklist(self, email_or_customer_code: str, risk_action: str)`

  Whitelist or blacklist a customer on your integration

  **Args**:

        email_or_customer_code (str): Customer's code or email address

        risk_action (str): One of the possible risk actions [ default, allow, deny ], allow to whitelist, deny to blacklist. Customers start with a default risk action.

  **Returns**:

        JSON: Data fetched from API

<br>

[Back to the top](#routes)
<br>
<br>

## **Disputes**

    py4paystack.routes.disputes.Disputes

<br>

`Disputes(secret_key: str)`

The Disputes API allows you manage transaction disputes on your integration

<br>
 	
### **Methods**:

- `add_evidence(self, dispute_id: int, customer_email: str, customer_name: str, customer_phone: str, service_details: str, delivery_address: str = None, delivery_date: Union[datetime.datetime, datetime.date, str] = None)`

      Provide evidence for the dispute.

      **Args**:

          dispute_id (int): ID of the dispute to add evidence for.

          customer_email (str): Customer's email address

          customer_name (str): Customer's name

          customer_phone (str):Customer's phone number

          service_details (str): Details of the service involved

          delivery_address (str, optional): Delivery Address. Defaults to None.

          delivery_date (Union[date, datetime, str], optional): ISO 8601 representation of delivery date (YYYY-MM-DD). Defaults to None.

      **Returns**:

          JSON: Data fetched from API

  <br>

- `export(self, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None, transaction_id: int = None, status: str = None)`

      Export disputes available on your integration

      **Args**:

          per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50. Defaults to None.

          page (int, optional): Specify exactly what dispute you want to page. If not specify we use a default value of 1. Defaults to None.

          from_date (Union[date, datetime, str], optional): A timestamp from which to start listing dispute e.g. 2016-09-21. Defaults to None.

          to_date (Union[date, datetime, str], optional): A timestamp at which to stop listing dispute e.g. 2016-09-21. Defaults to None.

          transaction_id (int, optional): Transaction ID. Defaults to None.

          status (str, optional): Dispute Status. Acceptable values: { awaiting-merchant-feedback | awaiting-bank-feedback | pending | resolved }. Defaults to None.

      **Returns**:

          JSON: Data fetched from API

  <br>

- `fetch(self, dispute_id: int)`

  Get more details about a dispute

  **Args**:

        dispute_id (int): The ID of the dispute your want to fetch

  **Returns**:

        JSON: Data fetched from API

<br>

- `get_upload_url(self, dispute_id: int, upload_filename: str = None)`

      Get URL to upload a dispute evidence.

      **Args**:

          dispute_id (int): ID of the dispute

          upload_filename (str, optional): The file name, with its extension, that you want to upload. e.g filename.pdf. Defaults to None.

      **Returns**:

          JSON: Data fetched from API

  <br>

- `list_disputes(self, page: int = None, per_page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None, transaction_id: int = None, status: str = None)`

      List all the dispute filed against you.

      **Args**:

          page (int, optional): Specify exactly what dispute you want to page. If not specify we use a default value of 1. Defaults to None.

          per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.Defaults to None.

          from_date (Union[date, datetime, str], optional): A timestamp from which to start listing dispute e.g. 2016-09-21. Defaults to None.

          to_date (Union[date, datetime, str], optional): A timestamp at which to stop listing dispute e.g. 2016-09-21. Defaults to None.

          transaction_id (int, optional): Transaction Id. Defaults to None.

          status (str, optional): Dispute Status. Acceptable values: { awaiting-merchant-feedback | awaiting-bank-feedback | pending | resolved }. Defaults to None.

      **Returns**:

          JSON: Data fetched from API

  <br>

- `list_transaction_disputes(self, transaction_id: int) Retrieve disputes for a particular transaction`

      **Args**:

          transaction_id (int): ID of the transaction whose dispute you want to fetch

      **Returns**:

          JSON: Data fetched from API

  <br>

- `resolve(self, dispute_id: int, resolution: str, message: str, refund_amount: int, upload_url: str, evidence_id: int = None)`

      Resolve disputes on your integration

      **Args**:

          dispute_id (int): ID of the dispute to be resolved.

          resolution (str): Dispute resolution. Accepted values: { merchant-accepted | declined }.

          message (str): Reason for resolving

          refund_amount (int): The amount to refund, in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR

          upload_url (str): Filename of attachment returned via response

          from upload url(GET /dispute/:id/upload_url)

          evidence_id (int, optional): Evidence Id for fraud claims. Defaults to None.

      **Returns**:

          JSON: Data fetched from API

  <br>

- `update(self, dispute_id: int, refund_amount: int = None, uploaded_filename: str = None)`

      Update details of a dispute on your integration

      **Args**:

          dispute_id (int): The ID of the dispute to be updated

          refund_amount (int, optional): The amount to refund, in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR. Defaults to None

          uploaded_filename (str, optional): filename of attachment returned via response from upload url(GET /dispute/:id/upload_url). Defaults to None.

      **Returns**:

          JSON: Data fetched from API

  <br>

[Back to the top](#routes)
<br>
<br>

## **Dedicated Virtual Accounts**

    py4paystack.routes.virtual_accounts.DedicatedVirtualAccounts

<br>

`DedicatedVirtualAccounts(secret_key: str)`

The Dedicated Virtual Account class enables Nigerian merchants to manage unique payment accounts of their customers.

### **Methods**:

<br>

- `create(self, customer: Union[int, str], preferred_bank: str, subaccount: str = None, split_code: str = None, first_name: str = None, last_name: str = None, phone: str = None)`

  Create a dedicated virtual account and assign to a customer. Paystack currently supports Access Bank and Wema Bank.

  **Args**:

      customer (Union[int, str]): Customer ID or code

      preferred_bank (str): The bank slug for preferred bank. To get a list of available banks, use the List Providers endpoint

      subaccount (str, optional): Subaccount code of the account you want to split the transaction with. Defaults to None.

      split_code (str, optional): Split code consisting of the lists of accounts you want to split the transaction with. Defaults to None.

      first_name (str, optional): Customer's first name. Defaults to None.

      last_name (str, optional): Customer's last name. Defaults to None.

      phone (str, optional): Customer's phone number. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `deactivate(self, dedicated_account_id: int)`

  Deactivate a dedicated virtual account on your integration.

  **Args**:

      dedicated_account_id (int): ID of dedicated virtual account

  **Returns**:

      JSON: Data fetched from API

<br>

- `fetch(self, dedicated_account_id: int)`

  Get details of a dedicated virtual account on your integration.

  **Args**:

      dedicated_account_id (int): ID of dedicated virtual account

  **Returns**:

      JSON: Data fetched from API

<br>

- `fetch_bank_providers(self)`

  Get available bank providers for a dedicated virtual account

  **Returns**:

      JSON: Data fetched from API

<br>

- `list_accounts(self, active: bool = None, currency: str = None, provider_slug: str = None, bank_id: int = None, customer_id: str = None)`

  List dedicated virtual accounts available on your integration.

  **Args**:

      active (bool, optional): Status of the dedicated virtual account. Defaults to None.

      currency (str, optional): The currency of the dedicated virtual account. Only NGN is currently allowed. Defaults to None.

      provider_slug (str, optional): The bank's slug in lowercase, without spaces e.g. wema-bank. Defaults to None.

      bank_id (int, optional): The bank's ID e.g. 035. Defaults to None.

      customer_id (str, optional): The customer's ID. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `remove_split(self, account_number: str)`

  If you've previously set up split payment for transactions on a dedicated virtual account,
  you can remove it with this endpoint

  **Args**:

      account_number (str): Dedicated virtual account number

  **Returns**:

      JSON: Data fetched from API

<br>

- `requery(self, account_number: str, provider_slug: str, date: str = None)`

  Requery Dedicated Virtual Account for new transactions

  **Args**:

      account_number (str): Virtual account number to requery

      provider_slug (str): The bank's slug in lowercase, without spaces e.g. wema-bank

      date (str, optional): The day the transfer was made in YYYY-MM-DD format. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `split_transaction(self, customer: Union[int, str], preferred_bank: str, subaccount: Union[str, list] = None, split_code: Union[str, list] = None)`

  Split a dedicated virtual account transaction with one or more accounts

  **Args**:

      customer (Union[int, str]): Customer ID or code.

      preferred_bank (str): The bank slug for preferred bank. To get a list of available banks, use the List Providers endpoint

      subaccount (Union[str, list], optional): Subaccount code of the account you want to split the transaction with. Defaults to None.

      split_code (Union[str, list], optional): Split code consisting of the lists of accounts you want to split the transaction with. Defaults to None.

  **Raises**:

  MissingArgumentsError: Raised when required arguments are missing.

  **Returns**:

      JSON: Data fetched from API

<br>

[Back to the top](#routes)
<br>
<br>

## **Invoice**

    py4paystack.routes.invoice.Invoice

`Invoice(secret_key: str)`

The Invoices API allows you issue out and manage payment requests

### **Methods**:

- `archive(self, invoice: Union[int, str])`

  Used to archive an invoice. Invoice will no longer be fetched on list or returned on verify:

  **Args**:

        invoice (Union[int, str]): The invoice ID or code

  **Returns**:

  JSON: Data fetched from API

<br>

- `create(self, customer: Union[int, str], description: str, due_date: Union[datetime.datetime, datetime.date, str], amount: int = None, line_items: list[dict[str]] = None, tax: list[dict[str]] = None, currency: str = None, send_notification: bool = None, draft: bool = None, has_invoice: bool = None, invoice_number: int = None, split_code: str = None)`

  Create an invoice for payment on your integration.

  **Args**:

        customer (Union[int, str]): Customer ID or code.
        description (str): A short description of the payment request

        due_date (Union[date, datetime, str]): ISO 8601 representation of request due datec eg. 2016-09-24T00:00:05.000Z, 2016-09-21.

        amount (int, optional): Payment request amount. It should be used when line items and tax values aren't specified.
        Defaults to None.

        line_items (list[dict[str]], optional): Array of line items int the format [{"name":"item 1", "amount":2000, "quantity": 1}]. Defaults to None.

        tax (list[dict[str]], optional): Array of taxes to be charged in the format [{"name":"VAT", "amount":2000}]. Defaults to None.

        currency (str, optional): Specify the currency of the invoice. Allowed values are NGN, GHS, ZAR and USD. Defaults to NGN. Defaults to None.

        send_notification (bool, optional): Indicates whether Paystack sends an email notification to customer. Defaults to true.

        draft (bool, optional): Indicate if request should be saved as draft. Defaults to false and overrides send_notification. Defaults to None.

        has_invoice (bool, optional): Set to true to create a draft invoice (adds an auto incrementing invoice number if none is provided) even if there are no line_items or tax passed. Defaults to None.

        invoice_number (int, optional): Numeric value of invoice. Invoice will start from 1 and auto increment from there. This field is to help override whatever value Paystack decides. Auto increment for subsequent invoices continue from this point. Defaults to None.

        split_code (str, optional): The split code of the transaction split. e.g. SPL_98WF13Eb3w. Defaults to None.

  **Raises**:

        UnwantedArgumentsError: Raised when an argument passed is unwanted.

  **Returns**:

  JSON: Data fetched from API

<br>

- `finalize(self, invoice_code: str)`

  Finalize a Draft Invoice

  **Args**:

        invoice_code (str): The invoice code

  **Returns**:

  JSON: Data fetched from API

<br>

- `list_invoices(self, per_page: int = None, page: int = None, customer: int = None, status: str = None, currency: str = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None, include_archive: str = None)`

  List invoice available on your integration

  **Args**:

  per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

  page (int, optional): Specify exactly what invoice you want to page. If not specify we use a default value of 1.

  customer (int, optional): Filter by customer ID. Defaults to None.

  currency (str, optional): Filter by currency. Allowed values are NGN, GHS, ZAR and USD.

  status (str, optional): Filter by invoice status. Defaults to None.

  from_date (Union[date, datetime, str], optional): A timestamp from which to start listing invoice e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

  to_date (Union[date, datetime, str], optional): A timestamp at which to stop listing invoice e.g. 2016-09-24T00:00:05.000Z, 201. Defaults to None.

  include_archive (str, optional): Show archived invoices. Defaults to None.

  **Returns**:

  JSON: Data fetched from API

<br>

- `send_notification(self, invoice_code: str)`

  Send notification of an invoice to your customers

  **Args**:

        invoice_code (str): The invoice code

  **Returns**:

  JSON: Data fetched from API

- `total(self)`

  Get invoice metrics for dashboard

  **Returns**:

  JSON: Data fetched from API

<br>

- `update(self, invoice: Union[int, str], customer: Union[int, str] = None, amount: int = None, currency: str = None, due_date: Union[datetime.datetime, datetime.date, str] = None, description: str = None, line_items: list[dict[str]] = None, tax: list[dict[str]] = None, send_notification: bool = None, draft: bool = None, invoice_number: int = None, split_code: str = None)`

  Update an invoice details on your integration.

  **Args**:

        invoice_id (int, optional): The invoice id or code.

        customer_code (str, optional): Customer's code or ID. Defaults to None.

        amount (int, optional): Payment request amount. Only useful if line items and tax values are ignored.

        endpoint will throw a friendly warning if neither is available. Defaults to None.

        currency (str, optional): Specify the currency of the invoice. Allowed values are NGN, GHS, ZAR and USD Defaults to NGN

        due_date (Union[date, datetime, str], optional): ISO 8601 representation of request due date. Defaults to None.

        description (str, optional): A short description of the payment request. Defaults to None.

        line_items (list[dict[str]], optional): Array of line items int the format [{"name":"item 1", "amount":2000}]. Defaults to None.

        tax (list[dict[str]], optional): Array of taxes to be charged in the format [{"name":"VAT", "amount":2000}]. Defaults to None.

        send_notification (bool, optional): Indicates whether Paystack sends an email notification to customer. Defaults to true.

        draft (bool, optional): Indicate if request should be saved as draft. Defaults to false and overrides send_notification.

        invoice_number (int, optional): Numeric value of invoice.
        Invoice will start from 1 and auto increment from there. This field is to help override whatever value Paystack decides. Auto increment for subsequent invoices continue from this point. Defaults to None.

        split_code (str, optional): The split code of the transaction split. e.g. SPL_98WF13Eb3w. Defaults to None.

  **Return**:

  JSON: Data fetched from API

<br>

- `verify(self, invoice_code: str)`

  Verify details of an invoice on your integration.

  **Args**:

        invoice_code (str): The invoice code.

  **Returns**:

  JSON: Data fetched from API

<br>

- `view(self, invoice: Union[int, str])`

  Get details of an invoice on your integration.

  **Args**:

        invoice (Union[int, str]): ID or code of the invoice

  **Returns**:

  JSON: Data fetched from API

<br>

[Back to the top](#routes)
<br>
<br>

## **Miscellaneous**

    py4paystack.routes.miscellaneous.Miscellaneous

<br>

`Miscellaneous(secret_key: str)`

The Miscellaneous API are supporting APIs that can be used to provide more details to other APIs

### **Methods**:

- `list_banks(self, country: str = None, use_cursor: bool = False, per_page: int = None, next: str = None, previous: str = None, gateway: str = None, type: str = None, currency: str = None)`

  Get a list of all supported banks and their properties

  **Args**:

        country (str, optional): The country from which to obtain the list of supported banks. e.g country=ghana or country=nigeria. Defaults to None.

        use_cursor (bool, optional): Use_curFlag to enable cursor pagination on the endpointsor. Defaults to False.

        per_page (int, optional): The number of objects to return per page. Defaults to 50, and limited to 100 records per page.

        next (str, optional): A cursor that indicates your place in the list. It can be used to fetch the next page of the list. Defaults to None.

        previous (str, optional): A cursor that indicates your place in the list. It should be used to fetch the previous page of the list after an intial next request. Defaults to None.

        gateway (str, optional): The gateway type of the bank.
        It can be one of these: [emandate, digitalbankmandate]. Defaults to None.

        type (str, optional): Type of financial channel. For Ghanaian channels, please use either mobile_money for mobile money channels OR ghipps for bank channels. Defaults to None.

        currency (str, optional): Any of NGN, USD, GHS or ZAR. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `list_providers(self, pay_with_bank_transfer: bool = None)`

  Get a list of all providers for Dedicated Virtual Account

  **Args**:

        pay_with_bank_transfer (bool, optional): A flag to filter for available providers. Defaults to None.

  **Returns**:

        JSON: Data fetched from API

<br>

- `list_search_countries(self)`

  Gets a list of Countries that Paystack currently supports

  **Returns**:

        JSON: Data fetched from API

<br>

- `list_states(self, country: int = None)`

      Get a list of states for a country for address verification.

      **Args**:

          country (int, optional): The country code of the states to list.It is gotten after the charge request. Defaults to None.

      **Returns**:

          JSON: Data fetched from API

  <br>

[Back to the top](#routes)
<br>
<br>

## **Payment Pages**

    py4paystack.routes.payment_pages.PaymentPages

<br>

`PaymentPages(secret_key: str)`

The Payment Pages API provides a quick and secure way to collect payment for products.

### **Methods**:

- `add_product(self, page_id: int, product_id: list[int])`

  Add products to a payment page

  **Args**:

      page_id (int): ID of the payment page.

      product_id (list[int]): A list of ids of all the product.

  **Returns**:

      JSON: Data fetched from API

<br>

- `check_slug_availability(self, slug: str)`

  Check the availability of a slug for a payment page.

  **Args**:

      slug (str): URL slug to be confirmed.

  **Returns**:

      JSON: Data fetched from API

<br>

- `create(self, name: str, description: str, amount: int, slug: str = None, metadata: dict = None, redirect_url: str = None, custom_fields: list = None)`

  Create a payment page on your integration

  **Args**:

      name (str): Name of page

      description (str): A description for this page

      amount (int): Amount should be in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR

      slug (str, optional): URL slug you would like to be associated with this page. Page will be accessible at https://paystack.com/pay/[slug]. Defaults to None.

      metadata (dict, optional): Extra data to configure the payment page including subaccount, logo image, transaction charge. Defaults to None.

      redirect_url (str, optional): If you would like Paystack to redirect someplace upon successful payment, specify the URL here. Defaults to None.

      custom_fields (list, optional): If you would like to accept custom fields, specify them here. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `fetch(self, id_or_slug: Union[int, str])`

  Get details of a payment page on your integration.

  **Args**:

      id_or_slug (Union[int, str]): The page ID or slug you want to fetch

  **Returns**:

      JSON: Data fetched from API

<br>

- `list_pages(self, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None)`

  List payment pages available on your integration.

  **Args**:

      per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

      page (int, optional): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.

        from_date (Union[date, datetime, str], optional): A timestamp from which to start listing page e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

        to_date (Union[date, datetime, str], optional): A timestamp at which to stop listing page e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `update(self, id_or_slug: Union[int, str], name: str = None, description: str = None, amount: int = None, active: bool = None)`

  Update a payment page details on your integration

  **Args**:

      id_or_slug (Union[int, str]): Page ID or slug.

      name (str, optional): Name of page. Defaults to None.

      description (str, optional): A description for this page. Defaults to None.

      amount (int, optional): Default amount you want to accept using this page. If none is set, customer is free to provide any amount of their choice. The latter scenario is useful for accepting donations. Defaults to None.

        active (bool, optional): Set to false to deactivate page url. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

[Back to the top](#routes)
<br>
<br>

## **Plan**

    py4paystack.routes.plans.Plan

<br>

`Plan(secret_key: str)`

The Plans API allows you create and manage installment payment options on your integration

### **Methods**:

<br>

- `create(self, name: str, amount: int, interval: str, description: str = None, send_invoices: bool = None, send_sms: bool = None, currency: str = None, invoice_limit: int = None)`

  Create a plan on your integration

  **Args**:

      name (str): Name of plan

      amount (int): Amount should be in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR

        interval (str): Interval in words. Valid intervals are: daily, weekly, monthly,biannually, annually.

      description (str, optional): A description for this plan. Defaults to None.

      send_invoices (bool, optional): Set to false if you don't want invoices to be sent to your customers. Defaults to None.

      send_sms (bool, optional): Set to false if you don't want text messages to be sent to your customers. Defaults to None.

      currency (str, optional): Currency in which amount is set.Allowed values are NGN, GHS, ZAR or USD. Defaults to None.

        invoice_limit (int, optional): Number of invoices to raise during subscription to this plan. Can be overridden by specifying an invoice_limit while subscribing. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `fetch(self, plan: Union[int, str])`

  Get details of a plan on your integration.

  **Args**:

      plan (Union[int, str]): The plan ID or code you want to fetch.

  **Returns**:

      JSON: Data fetched from API

<br>

- `list_plans(self, per_page: int = None, page: int = None, status: str = None, interval: str = None, amount: int = None)`

  List plans available on your integration.

  **Args**:

      per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

        page (int, optional): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.

        status (str, optional): Filter list by plans with specified status. Defaults to None.

      interval (str, optional): Filter list by plans with specified interval. Defaults to None.

      amount (int, optional): Filter list by plans with specified amount ( kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR). Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `update(self, plan: Union[int, str], name: str = None, amount: int = None, interval: str = None, description: str = None, currency: str = None, send_invoices: bool = None, send_sms: bool = None, invoice_limit: int = None)`

      Update a plan details on your integration.

      **Args**:

      	plan (Union[int, str]): Code or ID of the plan to update.

      	name (str, optional): Name of plan. Defaults to None.

      	amount (int, optional): Amount should be in kobo if currency is NGN and pesewas for GHS. Defaults to None.

      	interval (str, optional): Interval in words. Valid intervals are hourly, daily, weekly, monthly,biannually, annually. Defaults to None.

      	description (str, optional): A description for this plan. Defaults to None.

      	send_invoices (bool, optional): Set to false if you don't want invoices to be sent to your customers. Defaults to None.

      	send_sms (bool, optional): Set to false if you don't want text messages to be sent to your customers. Defaults to None.

      	currency (str, optional): Currency in which amount is set. Any of NGN, GHS, ZAR or USD. Defaults to None.

      	invoice_limit (int, optional): Number of invoices to raise during subscription to this plan. Can be overridden by specifying an invoice_limit while subscribing. Defaults to None.

      **Returns**:

      	JSON: Data fetched from API

  <br>

[Back to the top](#routes)
<br>
<br>

## **Product**

    py4paystack.routes.product.Product

<br>

`Product(secret_key: str)`

The Products API allows you create and manage inventories on your integration

### **Methods**:

<br>

- `create(self, name: str, description: str, price: int, currency: str, unlimited: bool = None, quantity: int = None)`

  Create a product on your integration

  **Args**:

      name (str): Name of product

      description (str): A description for this product

      price (int): Price should be in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR

        currency (str): Currency in which price is set. Allowed values are: NGN, GHS, ZAR or USD

      unlimited (bool, optional): Set to true if the product has unlimited stock. Leave as false if the product has limited stock. Defaults to None.

        quantity (int, optional): Number of products in stock. Use if unlimited is false. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `fetch(self, product_id: int)`

  Get details of a product on your integration.

  **Args**:

      product_id (int): The product ID you want to fetch

  **Returns**:

      JSON: Data fetched from API

<br>

- `list_products(self, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None)`

  List products available on your integration.

  **Args**:

        per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

        page (int, optional): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.. Defaults to None.

        from_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp from which to start listing product e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

        to_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp at which to stop listing product e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `update(self, product_id: int, name: str = None, description: str = None, price: int = None, currency: str = None, unlimited: bool = None, quantity: int = None)`

  Update a product details on your integration

  **Args**:

      product_id (int): Product ID

      name (str, optional): Name of product. Defaults to None.

      description (str, optional): A description for this product. Defaults to None.

      price (int, optional): Price should be in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR. Defaults to None.

        currency (str, optional): Currency in which price is set.Allowed values are: NGN, GHS, ZAR or USD. Defaults to None.

        unlimited (bool, optional): Set to true if the product has unlimited stock. Leave as false if the product has limited stock.

        quantity (int, optional): Number of products in stock. Use if unlimited is false. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

[Back to the top](#routes)
<br>
<br>

## **Refund**

    py4paystack.routes.refund.Refund

<br>

`Refund(secret_key: str)`

The Refunds API allows you create and manage transaction refunds

### **Methods**:

<br>

- `create(self, transaction: Union[str, int], amount: int = None, currency: str = None, customer_note: str = None, merchant_note: str = None)`

  Initiate a refund on your integration

  **Args**:

      transaction (Union[str, int]): Transaction reference or id

      amount (int, optional): Amount ( in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR ) to be refunded to the customer. Amount is optional(defaults to original transaction amount) and cannot be more than the original transaction amount.. Defaults to None.

      currency (str, optional): Three-letter ISO currency. Allowed values are: NGN, GHS, ZAR or USD. Defaults to None.

      customer_note (str, optional): Customer reason. Defaults to None.

      merchant_note (str, optional): Merchant reason. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `fetch(self, reference: str)`

  Get details of a refund on your integration.

  **Args**:

      reference (str): Identifier for transaction to be refunded

  **Returns**:

      JSON: Data fetched from API

<br>

- `list_refunds(self, reference: str = None, currency: str = None, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None)`

      List refunds available on your integration.

      **Args**:

      	reference (str, optional): Identifier for transaction to be refunded. Defaults to None.

      	currency (str, optional): Three-letter ISO currency. Allowed values are: NGN, GHS, ZAR or USD. Defaults to None.

          per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

          page (int, optional): Specify exactly what refund you want to page. If not specify we use a default value of 1.

      	from_date (Union[date, datetime, str], optional): A timestamp from which to start listing refund e.g. 2016-09-21. Defaults to None.

          to_date (Union[date, datetime, str], optional): A timestamp at which to stop listing refund e.g. 2016-09-21. Defaults to None.

      **Returns**:

      	JSON: Data fetched from API

  <br>

[Back to the top](#routes)
<br>
<br>

## **Settlements**

    py4paystack.routes.settlement.Settlement

<br>

`Settlements(secret_key: str)`

The Settlements API allows you gain insights into payouts made by Paystack to your bank account

### **Methods**:

<br>

- `fetch(self, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None, subaccount: str = None)`

  Fetch settlements made to your settlement accounts.

  **Args**:

      per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

        page (int, optional): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.

        from_date (Union[date, datetime, str], optional): A timestamp from which to start listing settlements e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

        to_date (Union[date, datetime, str], optional): A timestamp at which to stop listing settlements e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

        subaccount (str, optional): Provide a subaccount ID to export only settlements for that subaccount. Set to none to export only transactions for the account. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `fetch_transactions(self, settlement_id: int, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None)`

  Get the transactions that make up a particular settlement

  **Args**:

      settlement_id (int): The settlement ID in which you want to fetch its transactions.

      per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

        page (int, optional): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.. Defaults to None.

        from_date (Union[date, datetime, str], optional): A timestamp from which to start listing settlement transactions e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

        to_date (Union[date, datetime, str], optional): A timestamp at which to stop listing settlement transactions e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

[Back to the top](#routes)
<br>
<br>

## **SubAccounts**

    py4paystack.routes.subaccounts.SubAccounts

<br>

`SubAccounts(secret_key: str)`

The Subaccounts API allows you create and manage subaccounts on your integration.
Subaccounts can be used to split payment between two accounts (your main account and a sub account)

### **Methods**:

<br>

- `create(self, business_name: str, settlement_bank: str, account_number: str, percentage_charge: float, description: str = None, primary_contact_email: str = None, primary_contact_name: str = None, primary_contact_phone: str = None, metadata: str = None)`

  Create a subacount on your integration

  **Args**:

      business_name (str): Name of business for subaccount

      settlement_bank (str): Bank Code for the bank. You can get the list of Bank Codes by calling the List Banks endpoint.

      account_number (str): Bank Account Number

      percentage_charge (float): The default percentage charged when receiving on behalf of this subaccount

      description (str, optional): A description for this subaccount. Defaults to None.

      primary_contact_email (str, optional): A contact email for the subaccount. Defaults to None.

      primary_contact_name (str, optional): A name for the contact person for this subaccount. Defaults to None.

      primary_contact_phone (str, optional): A phone number to call for this subaccount. Defaults to None.

      metadata (str, optional): Stringified JSON object. Add a custom_fields attribute which has an array of objects if you would like the fields to be added to your transaction when displayed on the dashboard. Sample: {"custom_fields":[{"display_name":"Cart ID","variable_name": "cart_id","value": "8393"}]}. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `fetch(self, subaccount: Union[int, str])`

  Get details of a subaccount on your integration.

  **Args**:

      subaccount (Union[int, str]): The subaccount ID or code you want to fetch.

  **Returns**:

      JSON: Data fetched from API

<br>

- `list_subaccounts(self, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None)`

  List subaccounts available on your integration.

  **Args**:

      per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

        page (int, optional): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.

        from_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp from which to start listing subaccounts e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

        to_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp at which to stop listing subaccounts e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `update(self, subaccount: Union[int, str], active: bool = None, business_name: str = None, settlement_bank: str = None, account_number: str = None, settlement_schedule: str = None, percentage_charge: float = None, description: str = None, primary_contact_email: str = None, primary_contact_name: str = None, primary_contact_phone: str = None, metadata: str = None)`

  Update a subaccount details on your integration.

  **Args**:

      subaccount (Union[int, str]): Subaccount's ID or code.

      active (bool, optional): Activate or deactivate a subaccount. Set value to true to activate subaccount or false to deactivate the subaccount.

        business_name (str, optional): Name of business for subaccount. Defaults to None.

      settlement_bank (str, optional): Bank Code for the bank.You can get the list of Bank Codes by calling the List Banks endpoint. Defaults to None.

        account_number (str, optional): Bank Account Number. Defaults to None.

      settlement_schedule (str, optional): Any of auto, weekly, `monthly`, `manual`. Auto means payout is T+1 and manual means payout to the subaccount should only be made when requested. Defaults to auto.

        percentage_charge (float, optional): The default percentage charged when receiving on behalf of this subaccount. Defaults to None.

      description (str, optional): A description for this subaccount. Defaults to None.

      primary_contact_email (str, optional): A contact email for the subaccount. Defaults to None.

      primary_contact_name (str, optional): A name for the contact person for this subaccount. Defaults to None.

      primary_contact_phone (str, optional): A phone number to call for this subaccount. Defaults to None.

      metadata (str, optional): Stringified JSON object. Add a custom_fields attribute which has an array of objects if you would like the fields to be added to your transaction when displayed on the dashboard. Sample: {"custom_fields":[{"display_name":"Cart ID","variable_name": "cart_id","value": "8393"}]}. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

[Back to the top](#routes)
<br>
<br>

## **Subscription**

<br>

`Subscription(secret_key: str)`

    py4paystack.routes.subscription.Subscription

The Subscriptions API allows you create and manage recurring payment on your integration

### **Methods**:

<br>

- `create(self, email_or_customer_code: str, plan_code: str, authorization_code: str = None, start_date: Union[datetime.datetime, datetime.date, str] = None)`

  Create a subscription on your integration

  **Args**:

      email_or_customer_code (str): Customer's email address or customer code

      plan_code (str): Plan code

      authorization_code (str, optional): If customer has multiple authorizations, you can set the desired authorization you wish to use for this subscription here. If this is not supplied, the customer's most recent authorization would be used. Defaults to None.

      start_date (Union[datetime.datetime, datetime.date, str], optional): Set the date for the first debit. (ISO 8601 format) e.g. 2017-05-16T00:30:13+01:00. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `disable(self, subscription_code: str, email_token: str)`

  Disable a subscription on your integration

  **Args**:

      subscription_code (str): Subscription code

      email_token (str): Email token

  **Returns**:

      JSON: Data fetched from API

<br>

- `enable(self, subscription_code: str, email_token: str)`

  Enable a subscription on your integration

  **Args**:

      subscription_code (str): Subscription code

      email_token (str): Email token

  **Returns**:

      JSON: Data fetched from API

<br>

- `fetch(self, subscription: Union[int, str])`

  Get details of a subscription on your integration.

  **Args**:

      subscription (Union[int, str]): The subscription ID or code you want to fetch.

  **Returns**:

      JSON: Data fetched from API

<br>

- `generate_update_link(self, subscription_code: str)`

  Generate a link for updating the card on a subscription

  **Args**:

      subscription_code (str): Subscription code

  **Returns**:

      JSON: Data fetched from API

<br>

- `list_subscriptions(self, per_page: int = None, page: int = None, customer: int = None, plan: int = None)`

  List subscriptions available on your integration.

  **Args**:

      per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.. Defaults to None.

      page (int, optional): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.. Defaults to None.

      customer (int, optional): Filter by Customer ID. Defaults to None.

      plan (int, optional): Filter by Plan ID. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `send_update_link(self, subscription_code: str)`

      Email a customer a link for updating the card on their subscription

      **Args**:

      	subscription_code (str): Subscription code

      **Returns**:

      	JSON: Data fetched from API

  <br>

[Back to the top](#routes)
<br>
<br>

## **Transaction Split**

<br>

    py4paystack.routes.transaction_split.TransactionSplit

`TransactionSplit(secret_key: str)`

Create, list, retrieve, update split transaction configuration with one or more SubAccounts (You should have subaccounts on your integration to use this)

### **Methods**:

<br>

- `add_update_subaccount(self, split_id: int, subaccount: str, share: int)`

  Add a Subaccount to a Transaction Split, or update the share of an existing Subaccount in a Transaction Split

  **Args**:

      split_id (int): Split Id

      subaccount (str): This is the sub account code

      share (int): This is the transaction share for the subaccount

  **Returns**:

      JSON: Data fetched from API

<br>

- `create(self, name: str, split_type: str, currency: str, subaccounts: Iterable[tuple[str, int]], bearer_type: str, bearer_subaccount: str)`

  Create a split payment on your integration

  **Args**:

      name (str): Name of the transaction split

      split_type (str): The type of transaction split you want to create. You can use one of the following: percentage | flat

      currency (str): Any of NGN, GHS, ZAR, or USD

      subaccounts (Iterable[tuple[str, int]]): A list of object containing subaccount code and number of shares: [('ACT_xxxxxxxxxx', xxx)]

      bearer_type (str): Any of subaccount | account | all-proportional | all

      bearer_subaccount (str): Subaccount code

  **Returns**:

      JSON: Data fetched from API

<br>

- `fetch(self, split_id: int)`

  Get details of a split on your integration.

  **Args**:

      split_id (int): The id of the split

  **Returns**:

      JSON: Data fetched from API

<br>

- `list_search(self, name: str = None, active: bool = None, sort_by: str = None, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None)`

  List/search for the transaction splits available on your integration.

  **Args**:

      name (str, optional): The name of the split. Defaults to None.

      active (bool, optional): Any of true or false. Defaults to None.

      sort_by (str, optional): Sort by name, defaults to createdAt date. Defaults to None.

      per_page (int, optional): Number of splits per page. If not specify we use a default value of 50.

      page (int, optional): Page number to view. If not specify we use a default value of 1.

      from_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp from which to start listing splits e.g. 2019-09-24T00:00:05.000Z, 2019-09-21. Defaults to None.

      to_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp at which to stop listing splits e.g 2019-09-24T00:00:05.000Z, 2019-09-21. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `remove_subaccount(self, split_id: int, subaccount: str)`

  Remove a subaccount from a transaction split

  **Args**:

      split_id (int): Split Id

      subaccount (str): This is the sub account code

  **Returns**:

      JSON: Data fetched from API

<br>

- `update(self, split_id: int, name: str = None, active: bool = None, bearer_type: str = None, bearer_subaccount: str = None)`

  Update a transaction split details on your integration

  **Args**:

      split_id (int): Split ID

      name (str, optional): Name of the transaction split. Defaults to None.

      active (bool, optional): True or False. Defaults to None.

      bearer_type (str, optional): Any of the following values: subaccount | account | all-proportional | all. Defaults to None.

      bearer_subaccount (str, optional): Subaccount code of a subaccount in the split group. This should be specified only if the bearer_type is subaccount. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

[Back to the top](#routes)
<br>
<br>

## **Transaction**

    py4paystack.routes.transaction.Transaction

<br>

`Transaction(secret_key: str)`

Accept payment from your customers.
The Transactions API allows you create and manage payments on your integration

### **Methods**:

<br>

- `charge_authorization(self, email: str, amount: int, authorization_code: str, currency: str = None, reference: str = None, channels: Union[list, str] = None, queue: bool = False, split_code: str = None, subaccount: str = None, transaction_charge: int = None, bearer: str = None, metadata: dict = None, generate_reference: bool = False)`

  All authorizations marked as reusable can be charged with this endpoint whenever you need to receive payments.

  **Args**:

      email (str): Customer's email address

      amount (int): Amount should be in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR

      authorization_code (str): Valid authorization code to charge

      currency (str, optional): Currency in which amount should be charged. Allowed values are: NGN, GHS, ZAR or USD. Defaults to None.

      reference (str, optional): Unique transaction reference.Only -, ., = and alphanumeric characters allowed.. Defaults to None.

      channels (Union[list, str], optional): Send us 'card' or 'bank' or 'card','bank' as an array ( or just a string if you plan to use one payment option ) to specify what options to show the user paying. Defaults to None.

      queue (bool, optional): If you are making a scheduled charge call, it is a good idea to queue them so the processing system does not get overloaded causing transaction processing errors. Send queue:true to take advantage of our queued charging. Defaults to False.

      split_code (str, optional): _description_. Defaults to None.

      subaccount (str, optional): The code for the subaccount that owns the payment. e.g. ACCT_8f4s1eq7ml6rlzj. Defaults to None.

      transaction_charge (int, optional): A flat fee to charge the subaccount for this transaction (in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR). This overrides the split percentage set when the subaccount was created. Ideally, you will need to use this if you are splitting in flat rates (since subaccount creation only allows for percentage split).e.g. 7000 for a 70 naira flat fee.. Defaults to None.

      bearer (str, optional): Who bears Paystack charges? account or subaccount (defaults to account)

      metadata (dict, optional): A dictionary with custom_fields attribute which has an array of objects if you would like the fields to be added to your transaction when displayed on the dashboard. Sample: {"custom_fields":[{"display_name":"Cart ID","variable_name": "cart_id","value": "8393"}]}. Defaults to None.

      generate_reference (bool, optional): Whether to generate a reference for you. Defaults to False.

  **Returns**:

      JSON: Data fetched from API

<br>

- `check_authorization(self, email: str, amount: int, authorization_code: str, currency: str = None)`

  This feature is only available to businesses in Nigeria.
  All Mastercard and Visa authorizations can be checked with this endpoint to know
  if they have funds for the payment you seek.

  This endpoint should be used when you do not know the exact amount to charge a card when rendering a service.
  It should be used to check if a card has enough funds based on a maximum range value. It is well suited for:

  Ride hailing services
  Logistics services

  WARNING.
  You shouldn't use this endpoint to check a card for sufficient funds if you are going to charge the user immediately.
  This is because we hold funds when this endpoint is called which can lead to an insufficient funds error.

  **Args**:

      email (str): Customer's email address

      amount (int): Amount should be in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR

      authorization_code (str): Valid authorization code to charge

      currency (str, optional): Currency in which amount should be charged. Allowed values are: NGN, GHS, ZAR or USD. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `export(self, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None, customer: int = None, status: str = None, currency: str = None, amount: int = None, settled: bool = None, settlement: int = None, payment_page: int = None)`

  List transactions carried out on your integration.

  **Args**:

      per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

      page (int, optional): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.

      from_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp from which to start listing transaction e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

      to_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp at which to stop listing transaction e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

      customer (int, optional): Specify an ID for the customer whose transactions you want to retrieve. Defaults to None.

      status (str, optional): Filter transactions by status ('failed', 'success', 'abandoned'). Defaults to None.

      currency (str, optional): Specify the transaction currency to export. Allowed values are: in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR. Defaults to None.

      amount (int, optional): Filter transactions by amount. Specify the amount, in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR. Defaults to None.

      settled (bool, optional): Set to true to export only settled transactions. false for pending transactions. Leave undefined to export all transactions. Defaults to None.

      settlement (int, optional): An ID for the settlement whose transactions we should export. Defaults to None.

      payment_page (int, optional): Specify a payment page's id to export only transactions conducted on said page. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `fetch(self, transaction_id: int)`

  Get details of a transaction carried out on your integration.

  **Args**:

      transaction_id (int): ID of the transaction to fetch.

  **Returns**:

      JSON: Data fetched from API

<br>

- `initialize(self, email: str, amount: int, callback_url: str, reference: str = None, currency: str = None, plan: str = None, invoice_limit: int = None, channels: Union[str, list] = None, split_code: str = None, transaction_charge: int = None, subaccount: str = None, bearer: str = 'account', metadata: dict = None, generate_reference: bool = False)`

  Initialize a transaction from your backend

  **Args**:

      email (str): Customer's email address

      amount (int): Amount should be in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR

      callback_url (str): Fully qualified url, e.g. https://example.com/ . Use this to override the callback url provided on the dashboard for this transaction

      reference (str, optional): Unique transaction reference.Only -, ., = and alphanumeric characters allowed. Defaults to None.

      currency (str, optional): The transaction currency (NGN, GHS, ZAR or USD). Defaults to your integration currency.. Defaults to None.

      plan (str, optional): If transaction is to create a subscription to a predefined plan, provide plan code here. This would invalidate the value provided in amount. Defaults to None.

      invoice_limit (int, optional): Number of times to charge customer during subscription to plan. Defaults to None.

      channels (Union[str, list], optional): An array of payment channels ( or a string of one channel ) to control what channels you want to make available to the user to make a payment with. Available channels include: ['card', 'bank', 'ussd', 'qr', 'mobile_money', 'bank_transfer']. Defaults to None.

      split_code (str, optional): The split code of the transaction split. e.g. SPL_98WF13Eb3w. Defaults to None.

      transaction_charge (int, optional): An amount used to override the split configuration for a single split payment. If set, the amount specified goes to the main account regardless of the split configuration. Defaults to None.

      subaccount (str, optional): The code for the subaccount that owns the payment. e.g. ACCT_8f4s1eq7ml6rlzj. Defaults to None.

      bearer (str, optional): Who bears Paystack charges? account or subaccount (defaults to account).

      metadata (dict, optional): Stringified JSON object of custom data. Kindly check the Metadata page for more information.. Defaults to None.

      generate_reference (bool, optional): Would you want a reference generated for you. It will override the reference if provided. Defaults to False.

  **Returns**:

      JSON: Data fetched from API

<br>

- `list_transactions(self, per_page: int = None, page: int = None, customer: int = None, status: str = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None, amount: int = None)`

  List transactions carried out on your integration.

  **Args**:

      per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.. Defaults to None.

      page (int, optional): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.

      customer (int, optional): Specify an ID for the customer whose transactions you want to retrieve. Defaults to None.

      status (str, optional): Filter transactions by status ('failed', 'success', 'abandoned'). Defaults to None.

      from_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp from which to start listing transaction e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

      to_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp at which to stop listing transaction e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

      amount (int, optional): Filter transactions by amount. Specify the amount (in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR). Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `partial_debit(self, email: str, amount: int, currency: str, authorization_code: str, reference: str = None, at_least: str = None, generate_reference: bool = False)`

  Retrieve part of a payment from a customer

  **Args**:

      email (str): Customer's email address

      amount (int): Amount should be in kobo if currency is NGN, pesewas, if currency is GHS, and cents, if currency is ZAR

      currency (str): Specify the currency you want to debit. Allowed values are NGN, GHS, ZAR or USD.

      authorization_code (str): Authorization Code

      reference (str, optional): Unique transaction reference. Only -, ., = and alphanumeric characters allowed. Defaults to None.

      at_least (str, optional): Minimum amount to charge. Defaults to None.

      generate_reference (bool, optional): Whether to generate reference for you. Defaults to False.

  **Returns**:

      JSON: Data fetched from API

<br>

- `timeline(self, id_or_reference: Union[int, str] = None)`

  View the timeline of a transaction.

  **Args**:

      id_or_reference (Union[int, str], optional): The ID or the reference of the transaction. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `totals(self, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None)`

  Total amount received on your account

  **Args**:

      per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50.

      page (int, optional): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.

      from_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp from which to start listing transaction e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

      to_date (Union[datetime.datetime, datetime.date, str], optional): A timestamp at which to stop listing transaction e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `verify(self, reference: str)`

      Confirm the status of a transaction

      **Args**:

      	reference (str): The transaction reference used to intiate the transaction

      **Returns**:

      	JSON: Data fetched from API

  <br>

[Back to the top](#routes)
<br>
<br>

## **Transfer Recipient**

    py4paystack.routes.transfer_recipient.TransferRecipient

<br>

`TransferRecipient(secret_key: str)`

The Transfer Recipients API allows you create and manage beneficiaries that you send money to

### **Methods**:

<br>

- `bulk_create(self, *recipients: dict[str])`

  A list of transfer recipient object. Each object should contain type, name, and bank_code. Any Create Transfer Recipient param can also be passed.

  **Args**:

      recipients (dict[str]): Recipient objects. Each object should contain type, name, and bank_code. Any Create Transfer Recipient param can also be passed.

  **Returns**:

      JSON: Data fetched from API

<br>

- `create(self, recipient_type: str, name: str, email: str = None, account_number: str = None, bank_code: str = None, description: str = None, currency: str = None, authorization_code: str = None, metadata: dict = None)`

  Creates a new recipient. A duplicate account number will lead to the retrieval of the existing record.

  **Args**:

      recipient_type (str): Recipient Type. It could be one of: nuban, mobile_money, basa, authorization.

      name (str): A name for the recipient

      email (str, optional): Required if recipient_type is authorization. Defaults to None.

      account_number (str, optional): Required if type is nuban or basa. Defaults to None.

      bank_code (str, optional): Required if type is nuban or basa. You can get the list of Bank Codes by calling the List Banks endpoint. Defaults to None.

      description (str, optional): A description for this recipient. Defaults to None.

      currency (str, optional): Currency for the account receiving the transfer. Defaults to None.

      authorization_code (str, optional): An authorization code from a previous transaction. Defaults to None.

      metadata (dict, optional): Store additional information about your recipient in a structured format, JSON. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `delete(self, recipient: Union[int, str])`

  Deletes a transfer recipient (sets the transfer recipient to inactive).

  **Args**:

      recipient (Union[int, str]): An ID or code for the recipient who you want to delete.

  **Returns**:

      JSON: Data fetched from API

<br>

- `fetch(self, recipient: Union[int, str])`

  Fetch the details of a transfer recipient.

  **Args**:

      recipient (Union[int, str]): An ID or code for the recipient whose details you want to receive..

  **Returns**:

      JSON: Data fetched from API

<br>

- `list_recipients(self, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None)`

  List transfer recipients available on your integration

  **Args**:

      per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50. Defaults to None.

      page (int, optional): Specify exactly what page you want to retrieve. If not specify we use a default value of 1.. Defaults to None.

      from_date (Union[date, datetime, str], optional): A timestamp from which to start listing transfer recipients e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

      to_date (Union[date, datetime, str], optional): A timestamp at which to stop listing transfer recipients e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `update(self, recipient: Union[int, str], name: str = None, email: str = None)`

  Update an existing recipient. An duplicate account number will lead to the retrieval of the existing record.

  **Args**:

      recipient (Union[int, str]): Transfer Recipient's ID or code

      name (str, optional): A name for the recipient. Defaults to None.

      email (str, optional): Email address of the recipient. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

[Back to the top](#routes)
<br>
<br>

## **Transfer Control**

    py4paystack.routes.transfer_control.TransferControl

<br>

`TransferControl(secret_key: str)`

The Transfers Control API allows you manage settings of your transfers

### **Methods**:

<br>

- `check_balance(self)`

  Fetch the available balance on your integration

  **Returns**:

      JSON: Data fetched from API

<br>

- `disable_otp(self)`

  This is used in the event that you want to be able to complete transfers programmatically without use of OTPs.
  No arguments required. You will get an OTP to complete the request.
  This feature is only available to businesses in Nigeria and Ghana.

  **Returns**:

      JSON: Data fetched from API

<br>

- `enable_otp(self)`

  In the event that a customer wants to stop being able to complete transfers programmatically,
  this endpoint helps turn OTP requirement back on. No arguments required.
  This feature is only available to businesses in Nigeria and Ghana.

  **Returns**:

      JSON: Data fetched from API

<br>

- `fetch_balance_ledger(self)`

  Fetch all pay-ins and pay-outs that occured on your integration

  **Returns**:

      JSON: Data fetched from API

<br>

- `finalize_disable_otp(self, otp: str)`

  Finalize the request to disable OTP on your transfers.
  This feature is only available to businesses in Nigeria and Ghana.

  **Args**:

      otp (str): OTP sent to business phone to verify disabling OTP requirement

  **Returns**:

      JSON: Data fetched from API

<br>

- `resend_otp(self, transfer_code: str, reason: str)`

  Generates a new OTP and sends to customer in the event they are having trouble receiving one. This feature is only available businesses in Nigeria and Ghana.

  **Args**:

      transfer_code (str): Transfer code

      reason (str): Either resend_otp or transfer

  **Returns**:

      JSON: Data fetched from API

<br>

[Back to the top](#routes)
<br>
<br>

## **Transfer**

    py4paystack.routes.transfer.Transfer

<br>

`Transfer(secret_key: str)`

The Transfers API allows you automate sending money on your integration

### **Methods**:

<br>

- `fetch(self, transfer: Union[int, str])`

  Get details of a transfer on your integration.

  **Args**:

      transfer (Union[int, str]): The transfer ID or code you want to fetch

  **Returns**:

      JSON: Data fetched from API

<br>

- `finalize(self, transfer_code: str, otp: str)`

  Finalize an initiated transfer

  **Args**:

      transfer_code (str): The transfer code you want to finalize

      otp (str): OTP sent to business phone to verify transfer

  **Returns**:

      JSON: Data fetched from API

<br>

- `initiate(self, source: str, amount: int, recipient: str, reason: str = None, currency: str = None, reference: str = None, generate_reference: bool = False)`

  Status of transfer object returned will be pending if OTP is disabled. In the event that an OTP is required, status will read otp.

  **Args**:

      source (str): Where should we transfer from? Only balance for now

      amount (int): Amount to transfer in kobo if currency is NGN and pesewas if currency is GHS.

      recipient (str): Code for transfer recipient

      reason (str, optional): The reason for the transfer. Defaults to None.

      currency (str, optional): Specify the currency of the transfer. Defaults to NGN. Defaults to None.

      reference (str, optional): If specified, the field should be a unique identifier (in lowercase) for the object. Only -,_ and alphanumeric characters allowed. Defaults to None.

      generate_reference (bool, optional): Whether to generate reference for you. Defaults to False.

  **Returns**:

      JSON: Data fetched from API

<br>

- `initiate_bulk(self, source: str, *transfers: dict)`

  You need to disable the Transfers OTP requirement to use this endpoint.

  **Args**:

      source (str): Where should we transfer from? Only balance for now

      transfers (dict): Transfer objects. Each object should contain amount, recipient, and reference

  **Raises**:

  MissingArgumentsError: raised when a required argument is missing.

  **Returns**:

      JSON: Data fetched from API

<br>

- `list_transfers(self, per_page: int = None, page: int = None, from_date: Union[datetime.datetime, datetime.date, str] = None, to_date: Union[datetime.datetime, datetime.date, str] = None, customer_id: int = None)`

  List the transfers made on your integration.

  **Args**:

      per_page (int, optional): Specify how many records you want to retrieve per page. If not specify we use a default value of 50. Defaults to None.

      page (int, optional): Specify exactly what transfer you want to page. If not specify we use a default value of 1. Defaults to None.

      from_date (Union[date, datetime, str], optional): A timestamp from which to start listing transfer e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

      to_date (Union[date, datetime, str], optional): A timestamp at which to stop listing transfer e.g. 2016-09-24T00:00:05.000Z, 2016-09-21. Defaults to None.

      customer_id (int, optional): Filter by customer ID. Defaults to None.

  **Returns**:

      JSON: Data fetched from API

<br>

- `verify(self, reference: str)`

      Verify the status of a transfer on your integration.

      **Args**:

      	reference (str): Transfer reference

      **Returns**:

      	JSON: Data fetched from API

  <br>

[Back to the top](#routes)
<br>
<br>

## **Verification**

    py4paystack.routes.verification.Verification

<br>

`Verification(secret_key: str)`

The Verification class allows you perform KYC ( Know Your Customer ) processes.
This feature is only available to businesses in Nigeria.

### **Methods**:

<br>

- `resolve_acct_number(self, account_number: str, bank_code: str)`

  Confirm an account belongs to the right customer

  **Args**:

      account_number (str): Account Number

      bank_code (str): You can get the list of bank codes by calling the List Bank endpoint

  **Returns**:

      JSON: Data fetched from API

<br>

- `resolve_card_bin(self, card_bin: str)`

  Get more information about a customer's card

  **Args**:

      card_bin (str): First 6 characters of card

  **Raises**:

  ValueError: raised when card_bin is less or greater than 6 or is not made up of digits.

  **Returns**:

      JSON: Data fetched from API

<br>

- `validate_account(self, account_name: str, account_number: str, account_type: str, bank_code: str, country_code: str, document_type: str, document_number: str)`

  Confirm the authenticity of a customer's account number before sending money

  **Args**:

      account_name (str): Customer's first and last name registered with their bank

      account_number (str): Customer's account number

      account_type (str): This can take one of: [ personal, business ]

      bank_code (str): The bank code of the customer's bank. You can fetch the bank codes by using our List Bank endpoint

      country_code (str): The two digit ISO code of the customer's bank e.g GH for Ghana

      document_type (str): Customer's mode of identity. This could be one of: [ identityNumber, passportNumber, businessRegistrationNumber ]

      document_number (str): Customer's mode of identity number.

  **Returns**:

      JSON: Data fetched from API

<br>

[Back to the top](#routes)
<br>
<br>
