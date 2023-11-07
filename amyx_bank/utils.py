import random
import string

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
