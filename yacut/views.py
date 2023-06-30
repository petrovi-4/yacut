from flask import flash, redirect, render_template, request, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .generator import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        if custom_id and URLMap.query.filter_by(
            short=custom_id).first() is not None:
            flash(f'Имя {custom_id} уже занято!')
            return redirect(url_for('index_view'))

        if not original_link:
            flash('Введите оригинальную ссылку')
            return redirect(url_for('index_view'))

        if not custom_id:
            custom_id = get_unique_short_id()

        new_link = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(new_link)
        db.session.commit()
        short_url = f'{request.host_url}{custom_id}'
        return render_template('index.html', form=form, short_url=short_url)
    return render_template('index.html', form=form)


@app.route('/<short>')
def redirect_link(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
