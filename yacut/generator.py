import random
import string


def get_unique_short_id():
    letters_and_digits = string.ascii_letters + string.digits
    unique_short_id = ''.join(random.sample(letters_and_digits, 6))
    return unique_short_id