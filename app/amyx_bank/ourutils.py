import random, string, requests
from decimal import Decimal

URL = 'https://raw.githubusercontent.com/sdelquin/dsw/main/ut3/te1/files/banks.json'
RESPONSE = requests.get(URL)
BANKS = RESPONSE.json()


def generate_random_code(code_length: int) -> str:
    valid_chars = string.ascii_uppercase + string.digits
    random_code = "".join(random.choice(valid_chars) for _ in range(code_length))
    return random_code


# C5-0003 or A5-0003

def get_bank_info(bank_account_or_card: str, related_info: str) -> str:
    bank_id = int(bank_account_or_card[1]) - 1
    return BANKS[bank_id].get(related_info)


def calc_commission(transferred_amount: int, transference_type: str) -> int:
    SMALL_UPPER_LIMIT = 50
    MEDIUM_UPPER_LIMIT = 500
    COMMISSION_TABLES= {
        "OUTGOING" : {"SMALL": "0.02" , "MEDIUM": "0.04", "LARGE": "0.06"},    # FUNCIONA BIEN
        "INCOMING" : {"SMALL": "0.01" , "MEDIUM": "0.02", "LARGE": "0.03"},    # FUNCIONA BIEN
        "PAYMENTS" : {"SMALL": "0.03" , "MEDIUM": "0.05", "LARGE": "0.07"},    # FUNCIONA BIEN
    }
    if transferred_amount < SMALL_UPPER_LIMIT:
        transference_size = "SMALL"
    elif MEDIUM_UPPER_LIMIT > transferred_amount > SMALL_UPPER_LIMIT:
        transference_size = "MEDIUM"
    elif transferred_amount > MEDIUM_UPPER_LIMIT:
        transference_size = "LARGE"
    return transferred_amount * Decimal(COMMISSION_TABLES[transference_type][transference_size])

#[
#  { "id": 1, "name": "Bankoo", "url": "http://dsw.pc10.aula109" },
#  { "id": 2, "name": "Bank ODPCS", "url": "http://dsw.pc04.aula109" },
#  { "id": 3, "name": "Bank Arrota", "url": "http://dsw.pc07.aula109" },
#  { "id": 4, "name": "Adabank", "url": "http://dsw.pc17.aula109" },
#  { "id": 5, "name": "AMYX Bank", "url": "http://dsw.pc16.aula109" },
#  { "id": 6, "name": "Polaris Bank", "url": "http://dsw.pc28.aula109" },
#  { "id": 7, "name": "Gameda Bank", "url": "http://dsw.pc23.aula109" }
#]