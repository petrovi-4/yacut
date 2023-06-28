import re

from .error_handlers import InvalidAPIUsage
from .generator import get_unique_short_id
from .models import URLMap


def validate_create_data(data):
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' in data:
        if not data['custom_id']:
            data['custom_id'] = get_unique_short_id()
        elif not re.match(r'^[a-zA-Z0-9]{1,16}$', data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        elif URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
    else:
        data['custom_id'] = get_unique_short_id()
    return data


def validate_link(original, custom_id):
    if URLMap.query.filter_by(short=custom_id).first():
        return f'Имя {custom_id} уже занято!'
    if URLMap.query.filter_by(original=original).first():
        return 'Эта ссылка уже есть в базе данных.'
    return None