import glob
import os
import sys
from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, BankStatement, Transaktions, Settings
from sqlalchemy.inspection import inspect
from sqlalchemy import desc
from flask import send_file

app = Flask(__name__)
engine = create_engine('sqlite:///vismatools.db?check_same_thread=False')
Base.metadata.bind = engine
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/transactions/<int:statements_id>')
def transaktions_list(statements_id):
    statements = session.query(BankStatement).get(statements_id)
    transaktions = session.query(Transaktions).filter_by(bank_statement_id=statements_id)
    print(statements.title)
    print(transaktions[0])
    return render_template('transactions.html', statements=statements, transaktions=transaktions)


@app.route('/transactions/se/<int:statements_id>')
def create_se_file(statements_id):
    statements = session.query(BankStatement).get(statements_id)
    transaktions = session.query(Transaktions).filter_by(bank_statement_id=statements_id)
    file_header = f'''#FLAGGA 0
#FORMAT PC8
#SIETYP 4
#PROGRAM "Visma Administration 2000" 2020.3
#GEN 20211229 
#FNAMN "{statements.title}"
#TAXAR 2022 
#VALUTA SEK'''
    print(file_header)
    i = 1
    try:
        f = open('SE/' + statements.title + '.SE', 'w')
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
                f.write(f"""#VER A {i} {s_date} {transaktion.tr_name} {tr_date}
{{
   #TRANS {transaktion.konto_p} {{}} {amount_p}
   #TRANS {transaktion.konto_s} {{}} {amount_s}
}}
""")
                i = i + 1
            except:
                pass

        f.close()
    except FileNotFoundError:
        print("The 'docs' directory does not exist")

    return send_file(f"""SE/{statements.title}.SE""", as_attachment=True)


@app.route('/bank_statements')
def get_list_of_statements():
    statements = session.query(BankStatement).order_by(desc(BankStatement.bank_statement_id)).all()
    print(statements)
    # statements = session.query(BankStatement).all().sort(key=BankStatement.date, reverse=True))
    return render_template('bank_statements.html', statements=statements)


@app.route('/user/<string:name>/<int:hero_id>')
def user(name, hero_id):
    return "Hello " + name + "<br> Your ID number is " + str(hero_id)


@app.route('/about')
def hello_world():  # put application's code here
    return render_template("about.html")


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    # # TODO utföra kontroll av duplicering i konto_n   så att de kopplas ihop
    # # ---------------------------------------------
    # result = checkIfDuplicates_1(konto_list)
    # if result:
    #     import collections
    #     print('Yes, list contains duplicates')
    #     print([item for item, count in collections.Counter(konto_list).items() if count > 1])
    #     for key in range(0, len(konto_list)):
    #         print(key)
    #
    # else:
    #     print('No duplicates found in list')
    #
    # # ----------------------------------------------
    # def checkIfDuplicates_1(listOfElems):
    #     ''' Check if given list contains any duplicates '''
    #     if len(listOfElems) == len(set(listOfElems)):
    #         return False
    #     else:
    #         return True
    if request.method == 'POST':
        konto_list = request.form.getlist('konto_n')
        filter_list = request.form.getlist('filter_list')
        settings_table = Settings
        for i in range(0, len(konto_list)):
            print(f"konto nummer => {konto_list[i]} => {filter_list[i]} ")
            settings_table = Settings(konto=konto_list[i], filter=filter_list[i])
            session.add(settings_table)
            session.commit()
        try:
            print(request.form)
            return render_template("settings.html")
        except:
            pass
    else:
        try:
            settings_list = session.query(Settings).get(all)
            print(settings_list)
        except:
            settings_list = 'Inget att visa'
        return render_template('settings.html', settings=settings_list)


@app.route('/create_transaktion', methods=['POST', 'GET'])
def add_to_db():  # put application's code here
    if request.method == 'POST':
        title = request.form['title']
        summary = request.form['summary']
        print(f'title: {title} and summary{summary}')
        i = 0
        statement = BankStatement(title=title, summary=summary)
        session.add(statement)
        session.flush()
        try:
            for i in range(0, len(request.form.getlist('tr_id'))):
                tr_date = request.form.getlist('tr_date')[i]
                tr_name = request.form.getlist('tr_name')[i]
                tr_amount = request.form.getlist('tr_amount')[i]
                konto_p = request.form.getlist('konto_p')[i]
                konto_s = request.form.getlist('konto_s')[i]
                string = f'Id:{i} Date:{tr_date} Name:{tr_name} Amount: {tr_amount} konto_p {konto_p} konto_s {konto_s}'
                print(string)
                transaktion = Transaktions(bank_statement_id=statement.bank_statement_id,
                                           tr_date=tr_date,
                                           tr_name=tr_name,
                                           tr_amount=tr_amount,
                                           konto_s=konto_s,
                                           konto_p=konto_p)
                session.add(transaktion)
                session.commit()

            return render_template("create_transaktion.html")
        except:
            print('some error')
        return render_template("create_transaktion.html")
    else:
        return render_template("create_transaktion.html")


def clean_se_folder():
    files = glob.glob('/SE/*')
    for f in files:
        print(f)
        os.remove(f)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', template_folder='../template')
