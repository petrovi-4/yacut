from flask import flash, redirect, render_template

from . import app, db
from .error_handlers import InvalidAPIUsage
from .forms import URLMapForm
from .generator import get_unique_short_id
from .models import URLMap
from .validators import validate_link


@app.route('/', methods=['GET', 'POST'])
def add_link_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original = form.original_link.data
        if form.custom_id.data:
            custom_id = form.custom_id.data
        else:
            custom_id = get_unique_short_id()
        error = validate_link(original, custom_id)
        if error:
            flash(error)
            return render_template('index.html', form=form)
        urlmap = URLMap(
            original=original,
            short=custom_id
        )
        try:
            with db.session.no_autoflush:
                db.session.add(urlmap)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise InvalidAPIUsage(f'Ошибка при сохранении данных: {str(e)}')
        return render_template('index.html', form=form, urlmap=urlmap)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def link_view(short):
    urlmap = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(urlmap.original)