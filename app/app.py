import os
from flask import Flask, render_template, send_from_directory
import csv
import verifikations
import make_SE_file
import bank_statements
import clean_db
import settings
from db.database_setup import Base, engine

app = Flask(__name__)
Base.metadata.create_all(engine)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# Home Page
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/csv_reader', methods=['POST', 'GET'])
def csv_reader():
    return csv.add_to_db()


# Transaktions page
@app.route('/verifikations/<int:statements_id>', methods=['POST', 'GET'])
def transaktions_by_id(statements_id):
    return verifikations.transaktions_list(statements_id)


@app.route('/verifikations/se/<int:statements_id>')
def create_se_file(statements_id):
    return make_SE_file.create_se_file(statements_id)


# Statements list page
@app.route('/bank_statements')
def statements():
    return bank_statements.get_list_of_statements()


@app.route('/bank_statements/<int:statement_id>/delete', methods=['GET'])
def remove_statement(statement_id):
    return clean_db.remove_statement(statement_id)


# Settings page
@app.route('/settings', methods=['POST', 'GET'])
def show_settings():
    return settings.view_settings()


@app.route('/settings/new', methods=['POST', 'GET'])
def new_setting():
    return settings.create_new_filter()


@app.route("/settings/<int:setting_id>/edit/", methods=['GET', 'POST'])
def update_setting(setting_id):
    return settings.update_filter(setting_id)


@app.route('/settings/<int:setting_id>/delete/', methods=['GET', 'POST'])
def delete_setting(setting_id):
    return settings.remove_filter(setting_id)


@app.route('/about')
def about():  # put application's code here
    return render_template("about.html")


@app.route('/vat')
def moms():  # räkna ut moms
    return render_template("moms.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
