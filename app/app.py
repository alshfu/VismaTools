import sys
from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, BankStatement, Transaktions
from sqlalchemy import desc

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
    transactions = session.query(BankStatement).get(statements_id)
    print(transactions.title)
    return render_template('transactions.html', transactions=transactions)


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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', template_folder='../template')
