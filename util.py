import uuid
import re
import datetime
from . import settings


def check_auth_code(auth_code: str) -> str:
    if not auth_code.startswith('AUTH_'):
        raise ValueError(
            "Invalid auth_code: auth_code must start with 'AUTH_'")
    return auth_code

def check_currency(currency) -> str:
    currencies = settings.CURRENCIES
    if not currency in currencies:
        raise ValueError(
            f"Invalid currency: choices are {', '.join(currencies)}")
    return currency


def _check_one_split_code(split_code: str) -> str:
    if not split_code.startswith('SPL_'):
        raise ValueError(
            "Invalid split code: split code must start with 'SPL_'")
    return split_code


def check_split_code(split_code: str | list) -> str | list:
    if isinstance(split_code, (list, tuple)):
        split_code = list(map(_check_one_split_code, split_code))
    else:
        split_code = _check_one_split_code(split_code)

    return split_code


def check_bvn(bvn: str) -> str:
    if not bvn.isdigit() or len(bvn) != 11:
        raise ValueError("bvn must contain only digits and be 11 digits long")
    return bvn


def _check_one_subaccount(subaccount: str) -> str:
    if not subaccount.startswith('ACCT_'):
        raise ValueError(
            "Invalid subaccount code: sub account must startwith 'ACCT_'")
    return subaccount


def check_subaccount(subaccount: str | list) -> str | list:
    if isinstance(subaccount, (list, tuple)):
        subaccount = map(_check_one_subaccount, subaccount)
    else:
        subaccount = _check_one_subaccount(subaccount)
    return subaccount


def check_bearer(bearer) -> str:
    if not bearer in settings.BEARER_TYPES:
        raise ValueError(
            f"Invalid bearer: choices are {', '.join(settings.BEARER_TYPES)}")
    return bearer


def check_customer(customer) -> str:
    if not customer.startswith('CUS_'):
        raise ValueError(
            "Invalid customer code: customer code must start with 'CUS_'")
    return customer


def create_ref() -> str:
    return str(uuid.uuid4()).replace('-', '')


def check_channels(channel) -> list:
    channels = settings.PAYMENT_CHANNELS
    message = f"Invalid payment channel, choices are: {', '.join(channels)}"
    if isinstance(channel, list):
        if not set(channel).issubset(channels):
            raise ValueError(message)
    else:
        if not channel in channels:
            raise ValueError(message)
    return [channel]


def handle_date(date: datetime.date | datetime.datetime | str) -> str:
    return date.strftime('%Y-%m-%d') if isinstance(date, (datetime.date, datetime.datetime)) else datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')


def check_email(email: str) -> bool:
    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-z|a-z]{2,}\b', email):
        raise ValueError('provide a valid email!')
    return email


def check_identification_type(id_type: str) -> str:
    id_types = settings.IDENTIFICATION_TYPES
    if not id_type in id_types:
        raise ValueError(
            f"Invalid Identification type, your choices are: {', '.join(id_types)}")
    return id_type


def check_country(country_code: str) -> str:
    if len(country_code) != 2:
        raise ValueError(
            "Invalid country_code, value must be a 2 character string")
    return country_code


def check_account_number(account_number: str) -> str:
    if len(account_number) != 10:
        raise ValueError(
            "Invalid account number, value must be a 10 character string")
    return account_number


def check_risk_action(risk_action: str) -> str:
    risk_actions = settings.RISK_ACTIONS
    if not risk_action in risk_actions:
        raise ValueError(
            f"Invalid risk_action, your choices are: {', '.join(risk_actions)}")
    return risk_action


def check_email_or_customer(email_or_customer_code: str) -> str:
    try:
        customer = check_email(email_or_customer_code)
    except ValueError:
        try:
            customer = check_customer(email_or_customer_code)
        except ValueError as error:
            raise ValueError(
                'Invalid value for email_or_customer_code, provide an email or customer_code') from error
    return customer


def check_preferred_bank(preferred_bank: str) -> str:
    preferred_banks = settings.VIRTUAL_ACCOUNT_PROVIDERS
    if not preferred_bank in preferred_banks:
        raise ValueError(
            f"Value for preferred_bank not supported, your choices are: {', '.join(preferred_banks)}")
    return preferred_bank


def check_document_type(document_type: str) -> str:
    document_types = settings.DOCUMENT_TYPES
    if not document_type in document_types:
        raise ValueError(
            f"Invalid value for document_type, your choices are: {', '.join(document_types)}")
    return document_type


def check_account_types(account_type: str) -> str:
    account_types = settings.ACCOUNT_TYPES
    if not account_type in account_types:
        raise ValueError(f"Your choices are: {', '.join(account_types)}")
    return account_type


def check_bank_code(bank_code: str) -> str:
    if not bank_code.isdigit():
        raise ValueError("bank_code should be a string of digits")
    return bank_code


def check_transaction_status(status: str) -> str:
    statuses = settings.TRANSACTION_STATUS
    if not status in statuses:
        raise ValueError(f"Your choices are: {', '.join(statuses)}")
    return status


def check_domain(domain: str) -> str:
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    if not re.match(pattern, domain):
        raise ValueError('Invalid domain')
    return domain

def handle_query_params(per_page: int = None, page: int = None, from_date: datetime.date | datetime.datetime | str = None, to_date: datetime.date | datetime.datetime | str = None) -> dict | None:
    params = {}
    if per_page:
        params['perPage'] = per_page
    
    if page:
        params['page'] = page

    if from_date:
        params['from'] = handle_date(from_date)

    if to_date:
        params['to'] = handle_date(to_date)
    
    return params

def check_settlement_schedule(settlement_schedule: str) -> str:
    schedules = settings.SETTLEMENT_SCHEDULES
    if not settlement_schedule in schedules:
        raise ValueError(f"Your choices are: {', '.join(schedules)}")
    return settlement_schedule