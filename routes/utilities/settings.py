from collections import namedtuple

Code = namedtuple('Code', ['prefix', 'name'])
SUBACCOUNT = Code('ACCT', 'subaccount')
PLAN = Code('PLN', 'plan')
SUBSCRIPTION = Code('SUB', 'subscription')
AUTHORIZATION = Code('AUTH', 'authorization')
SPLIT = Code('SPL', 'split')
PRODUCT = Code('PROD', 'product')
INVOICE = Code('PRQ', 'invoice')
RECIPIENT = Code('RCP', 'recipient')
TRANSFER = Code('TRF', 'transfer')
BULK_CHARGE_BATCH = Code('BCH', 'bulk_charge_batch')
CUSTOMER = Code('CUS', 'customer')

DOCUMENT_TYPES = ('identityNumber', 'passportNumber',
                  'businessRegistrationNumber')

ACCOUNT_TYPES = ('personal', 'business')

PAYMENT_CHANNELS = ('card', 'bank', 'ussd', 'qr',
                    'mobile_money', 'bank_transfer')

CURRENCIES = ('GHS', 'NGN', 'USD', 'ZAR')

TRANSACTION_STATUS = ('failed', 'success', 'abandoned')

SPLIT_TYPES = ('percentage', 'flat')

BEARER_TYPES = ('account', 'subaccount', 'all-proportional', 'all')

IDENTIFICATION_TYPES = ('bank_account', 'bvn')

RISK_ACTIONS = ('default', 'allow', 'deny')

VIRTUAL_ACCOUNT_PROVIDERS = ('access-bank', 'wema-bank')

SETTLEMENT_SCHEDULES = ('auto', 'weekly', 'monthly')

PLAN_INTERVALS = ('daily', 'weekly', 'monthly', 'biannually', 'annually')

PLAN_STATUSES = ('active', 'complete', 'non-renewing',
                 'attention', 'cancelled')

RECIPIENT_TYPES = ('nuban', 'mobile_money', 'basa', 'authorization')

TRANSFER_SOURCES = ('balance',)

TRANSFER_CONTROL_REASONS = ('resend_otp', 'transfer')

BULK_CHARGE_STATUSES = ('active', 'paused', 'complete')

USSD_CODES = (737, 919, 822, 966)

MOBILE_PAYMENT_PROVIDERS = ("mtn", "vod", "tgo")

DISPUTE_STATUSES = ('awaiting-merchant-feedback',
                    'awaiting-bank-feedback', 'pending', 'resolved')

DISPUTE_RESOLUTION = ('merchant-accepted', 'declined')

BANK_GATEWAYS = ('emandate', 'digitalbankmandate')
