from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .validators import validate_create_data


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': urlmap.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    data = validate_create_data(data)
    urlmap = URLMap()
    urlmap.from_dict(data)
    try:
        with db.session.no_autoflush:
            db.session.add(urlmap)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise InvalidAPIUsage(f'Ошибка при сохранении данных: {str(e)}')
    short_url = url_for('link_view', short=urlmap.short, _external=True)
    return jsonify({'url': urlmap.original, 'short_link': short_url}), HTTPStatus.CREATED