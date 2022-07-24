import datetime
import re
import uuid
from typing import Sequence

from . import settings
from .errors import MissingArgumentsError


def check_bvn(bvn: str) -> str:
    if not bvn.isdigit() or len(bvn) != 11:
        raise ValueError("bvn must contain only digits and be 11 digits long")
    return bvn


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


def check_email_or_customer(email_or_customer_code: str) -> str:
    try:
        customer = check_email(email_or_customer_code)
    except ValueError:
        try:
            customer = check_code(email_or_customer_code, 'CUS')
        except ValueError as error:
            raise ValueError(
                'Invalid value for email_or_customer_code, provide an email or customer_code') from error
    return customer


def check_bank_code(bank_code: str) -> str:
    if not bank_code.isdigit():
        raise ValueError("bank_code should be a string of digits")
    return bank_code


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


def check_query_params(per_page: int = None, page: int = None, from_date: datetime.date | datetime.datetime | str = None, to_date: datetime.date | datetime.datetime | str = None) -> dict:
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


def handle_query_params(path: str, params: dict) -> str:
    path += '?'
    for key, value in params.items():
        path += f"{key}={value}&"
    return path.rstrip('&')


def check_code(data: tuple[str, str], code: Sequence[str] | str) -> str | list:
    if isinstance(code, (str)):
        code = tuple(code)

    for x in code:
        pre = x.split('_')[0]
        if pre != data.prefix:
            raise ValueError("Invalid {0}: {0} must start with {1} not {2}".format(
                data.name, data.prefix, pre))
    if len(code) == 1:
        return code[0]
    return code


def check_membership(group: Sequence, member: str, name: str) -> str:
    if member not in group:
        raise ValueError(
            f"Invalid value for {name}, your choices are: {', '.join(group)}")
    return member


def generate_payload(payload: dict, *unwanted) -> dict:
    rem = ['self', 'path']
    rem.extend(unwanted)
    return {key: value for key, value in payload.items() if value is not None and key not in rem}


def id_or_code(value: str | int, data: tuple = None):
    if isinstance(value, int):
        return value
    return check_code(data, value)
