import random
import string

from .models import URLMap


def get_unique_short_id(size=6):
    while True:
        short_id = ''.join(random.choices(
            string.ascii_letters + string.digits, k=size))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id
