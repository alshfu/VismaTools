import re

from flask import render_template, request, redirect, url_for

from db.database_setup import Settings, session


def view_settings():
    settings_list = session.query(Settings).all()
    # # TODO utföra kontroll av duplicering i konto_n   så att de kopplas ihop
    return render_template('settings.html', settings=settings_list)


def create_new_filter():
    # TODO utföra kontroll av duplicering i konto_n   så att de kopplas ihop
    if request.method == 'POST':
        new_filter = Settings(konto=request.form['konto_n'], filter=request.form['filter_list'])
        session.add(new_filter)
        session.commit()
        return redirect(url_for('show_settings'))
    else:
        return render_template('settings.html')


def update_filter(setting_id):
    filters = request.form['filter_list']
    filters = re.sub(r"[\n\t\s]*", "", filters)

    print(setting_id)
    if request.method == 'POST':
        if request.form['konto_n']:
            setting = session.query(Settings).get(setting_id)
            setting.filter = filters
            session.commit()
            return redirect(url_for('show_settings'))
    else:
        return render_template('settings.html')


def remove_filter(setting_id):
    setting_to_delete = session.query(Settings).filter_by(quote_id=setting_id).one()
    if request.method == 'GET':
        session.delete(setting_to_delete)
        session.commit()
        return redirect(url_for('show_settings'))
    else:
        return redirect(url_for('show_settings'))
