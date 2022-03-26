import os
import re

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker

from database_setup import Base, BankStatement, Transaktions, Settings

app = Flask(__name__)
engine = create_engine('sqlite:///vismatools.db?check_same_thread=False')
Base.metadata.bind = engine
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# Home Page
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/create_transaktion', methods=['POST', 'GET'])
def add_to_db():  # put application's code here
    filters = session.query(Settings).all()
    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        statement = BankStatement(title=title, summary=summary)
        session.add(statement)
        session.flush()
        try:
            for id_ in request.form.getlist('tr_id'):
                id_ = int(id_)
                tr_date = request.form.getlist('tr_date')[id_]
                tr_name = request.form.getlist('tr_name')[id_]
                tr_amount = request.form.getlist('tr_amount')[id_]
                konto_p = request.form.getlist('konto_p')[id_]
                konto_s = request.form.getlist('konto_s')[id_]
                transaktion = Transaktions(bank_statement_id=statement.bank_statement_id,
                                           tr_date=tr_date,
                                           tr_name=tr_name,
                                           tr_amount=tr_amount,
                                           konto_s=konto_s,
                                           konto_p=konto_p)
                session.add(transaktion)
                session.commit()
            return redirect(url_for('get_list_of_statements'))
        except Exception as e:
            print(e)
            return render_template("create_transaktion.html")
    else:
        return render_template("create_transaktion.html", filters=filters)


# Transaktions page
@app.route('/transactions/<int:statements_id>', methods=['POST', 'GET'])
def transaktions_list(statements_id):
    statements = session.query(BankStatement).get(statements_id)
    transaktions = session.query(Transaktions).filter_by(bank_statement_id=statements_id).order_by(
        desc(Transaktions.quote_id))

    if request.method == 'POST':
        try:
            for index_ in range(len(request.form.getlist('tr_quote_id'))):
                tr_id = request.form.getlist('tr_quote_id')[index_]
                tr_name = request.form.getlist('tr_name')[index_]
                konto_s = request.form.getlist('tr_konto_s')[index_]
                # transaktion = session.query(Transaktions).filter_by(quote_id=tr_id)
                transaktion = session.query(Transaktions).get(tr_id)
                transaktion.tr_name = tr_name
                transaktion.konto_s = konto_s
                session.commit()
            return redirect(url_for('transaktions_list', statements_id=statements_id))
        except Exception as e:
            print(e)
            return redirect(url_for('transaktions_list', statements_id=statements_id))

    return render_template('transactions.html', statements=statements, transaktions=transaktions)


@app.route('/transactions/se/<int:statements_id>')
def create_se_file(statements_id):
    import os
    cwd = os.getcwd() + "/app/SE"  # Get the current working directory (cwd)
    # cwd = "SE"  # For Windows 2019 Server
    statements = session.query(BankStatement).get(statements_id)
    transaktions = session.query(Transaktions).filter_by(bank_statement_id=statements_id).order_by(
        desc(Transaktions.quote_id))
    file_header = f'''#FLAGGA 0
#FORMAT PC8
#SIETYP 4
#PROGRAM "Visma Administration 2000" 2020.3
#GEN 20211229 
#FNAMN "{statements.title}"
#TAXAR 2022 
#VALUTA SEK'''
    i = 1
    try:
        file_name = f"""{cwd}/{statements.title.replace(' ', '')}.SE"""
        print(file_name)
        f = open(file_name, 'w')
        f.write(file_header)
        for transaktion in transaktions:
            s_date = statements.date[0:10].replace('-', '')
            tr_date = transaktion.tr_date[0:10].replace('-', '')
            amount_p = transaktion.tr_amount
            try:
                if float(amount_p) < 0:
                    amount_s = amount_p.replace('-', '')
                else:
                    amount_s = f"""-{amount_p}"""
                f.write(f"""#VER A {i} {tr_date} {transaktion.tr_name} {tr_date}
{{
   #TRANS {transaktion.konto_p} {{}} {amount_p}
   #TRANS {transaktion.konto_s} {{}} {amount_s}
}}
""")
                i = i + 1
            except Exception as e:
                print(e)
        f.close()
        return send_file(file_name, as_attachment=True)
    except Exception as e:
        print(e)
        return redirect(url_for('get_list_of_statements'))


# Statements list page
@app.route('/bank_statements')
def get_list_of_statements():
    statements = session.query(BankStatement).order_by(desc(BankStatement.bank_statement_id)).all()
    return render_template('bank_statements.html', statements=statements)


@app.route('/bank_statements/<int:statement_id>/delete', methods=['GET'])
def remove_statement(statement_id):
    statement_to_delete = session.query(BankStatement).filter_by(bank_statement_id=statement_id).one()
    if request.method == 'GET':
        import os
        cwd = os.getcwd() + "/app/SE"
        file_name = f"""{cwd}/{statement_to_delete.title.replace(' ', '')}.SE"""
        print(file_name)
        if os.path.exists(file_name):
            print(file_name)
            os.remove(file_name)
        session.delete(statement_to_delete)
        session.commit()
        return redirect(url_for('get_list_of_statements'))
    else:
        return redirect(url_for('get_list_of_statements'))


# Settings page
@app.route('/settings', methods=['POST', 'GET'])
def show_settings():
    settings_list = session.query(Settings).all()
    # # TODO utföra kontroll av duplicering i konto_n   så att de kopplas ihop
    return render_template('settings.html', settings=settings_list)


@app.route('/settings/new', methods=['POST', 'GET'])
def new_setting():
    # TODO utföra kontroll av duplicering i konto_n   så att de kopplas ihop
    if request.method == 'POST':
        new_filter = Settings(konto=request.form['konto_n'], filter=request.form['filter_list'])
        session.add(new_filter)
        session.commit()
        return redirect(url_for('show_settings'))
    else:
        return render_template('settings.html')


@app.route("/settings/<int:setting_id>/edit/", methods=['GET', 'POST'])
def update_setting(setting_id):
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


@app.route('/settings/<int:setting_id>/delete/', methods=['GET', 'POST'])
def delete_setting(setting_id):
    setting_to_delete = session.query(Settings).filter_by(quote_id=setting_id).one()
    if request.method == 'GET':
        session.delete(setting_to_delete)
        session.commit()
        return redirect(url_for('show_settings'))
    else:
        return redirect(url_for('show_settings'))


@app.route('/about')
def about():  # put application's code here
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
