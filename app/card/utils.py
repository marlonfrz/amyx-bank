import random
import string


def generate_random_code(code_length):
    valid_chars = string.ascii_uppercase + string.digits
    random_code = "".join(random.choice(valid_chars) for _ in range(code_length))
    return random_code
