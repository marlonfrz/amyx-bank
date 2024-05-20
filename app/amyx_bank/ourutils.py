import random
import string
from decimal import Decimal

import requests

URL = 'https://raw.githubusercontent.com/sdelquin/dsw/main/ut3/te1/notes/files/banks.json'
RESPONSE = requests.get(URL)
BANKS = RESPONSE.json()


def generate_random_code(code_length: int) -> str:
    valid_chars = string.ascii_uppercase + string.digits
    random_code = "".join(random.choice(valid_chars) for _ in range(code_length))
    return random_code


def get_bank_info(bank_account_or_card: str, related_info: str) -> str:
    bank_id = int(bank_account_or_card[1])
    return BANKS[bank_id].get(related_info)


def calc_commission(transferred_amount: Decimal, transference_type: str) -> Decimal:
    SMALL_UPPER_LIMIT = Decimal(50)
    MEDIUM_UPPER_LIMIT = Decimal(500)
    COMMISSION_TABLES = {
        "OUTGOING": {"SMALL": "0.02", "MEDIUM": "0.04", "LARGE": "0.06"},
        "INCOMING": {"SMALL": "0.01", "MEDIUM": "0.02", "LARGE": "0.03"},
        "PAYMENTS": {"SMALL": "0.03", "MEDIUM": "0.05", "LARGE": "0.07"},
    }
    if transferred_amount < SMALL_UPPER_LIMIT:
        transference_size = "SMALL"
    elif MEDIUM_UPPER_LIMIT > transferred_amount >= SMALL_UPPER_LIMIT:
        transference_size = "MEDIUM"
    elif transferred_amount >= MEDIUM_UPPER_LIMIT:
        transference_size = "LARGE"
    return transferred_amount * Decimal(COMMISSION_TABLES[transference_type][transference_size])
