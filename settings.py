DOCUMENT_TYPES = ('identityNumber', 'passportNumber',
                  'businessRegistrationNumber')

CODE_PREFIXES = {
    'ACCT': 'subaccount',
    'PLN': 'plan',
    'SUB': 'subscription',
    'CUS': 'customer',
    'AUTH': 'authorization',
    'SPL': 'split',
    'PROD': 'product',
    'PRQ': 'invoice'
}

CODE_NAMES = { value: key for key, value in CODE_PREFIXES.items() }

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
