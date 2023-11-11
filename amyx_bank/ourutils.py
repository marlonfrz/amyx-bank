import random
import string
from prettyconf import config
import requests

URL = 'https://raw.githubusercontent.com/sdelquin/dsw/main/ut3/te1/files/banks.json'
RESPONSE = requests.get(URL)
BANKS = RESPONSE.json()
# print(BANKS)


def generate_random_code(code_length):
    valid_chars = string.ascii_uppercase + string.digits
    random_code = "".join(random.choice(valid_chars) for _ in range(code_length))
    return random_code


def get_bank_address(bank_account_or_card):
    bank_id = int(bank_account_or_card[1])
    for bank in BANKS:
        if bank["id"] != bank_id:
            continue
        else:
            return bank['url']


def calc_commission_percentage(transferred_amount, transference_type):
    SMALL_UPPER_LIMIT = 50
    MEDIUM_UPPER_LIMIT = 500
    COMMISSION_TABLES= {
        "OUTGOING" : {"SMALL": 0.02 , "MEDIUM": 0.04, "LARGE": 0.06}, 
        "INCOMING" : {"SMALL": 0.01 , "MEDIUM": 0.02, "LARGE": 0.03},
        "PAYMENTS" : {"SMALL": 0.03 , "MEDIUM": 0.05, "LARGE": 0.07}
    }
    if transferred_amount < SMALL_UPPER_LIMIT:
        transference_size = "SMALL"
    elif MEDIUM_UPPER_LIMIT > transferred_amount > SMALL_UPPER_LIMIT:
        transference_size = "MEDIUM"
    elif transferred_amount > MEDIUM_UPPER_LIMIT:
        transference_size = "LARGE"
    return transferred_amount * (1 + COMMISSION_TABLES[transference_type][transference_size])