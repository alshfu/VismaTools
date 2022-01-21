import sys
from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, BankStatement, Transaktions

app = Flask(__name__)
engine = create_engine('sqlite:///vismatools.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/user/<string:name>/<int:hero_id>')
def user(name, hero_id):
    return "Hello " + name + "<br> Your ID number is " + str(hero_id)


@app.route('/about')
def hello_world():  # put application's code here
    return render_template("about.html")


@app.route('/create_transaktion', methods=['POST', 'GET'])
def add_to_db():  # put application's code here
    if request.method == 'POST':
        print(request.form)
        title = request.form['title']
        summary = request.form['summary']
        transaktions = request.form['transaktions']
        statement = BankStatement(title=title, summary=summary)
        session.add(statement)
        session.flush()
        transaktion = Transaktions(text=transaktions, bank_statement_id=statement.bank_statement_id)
        session.add(transaktion)
        session.commit()
        return redirect('/')
        # try:
        #     session.add(statement)
        #     session.add(transaktion)
        #     session.commit()
        #     return redirect('/')
        # except:
        #     return "some Error"
    else:
        return render_template("create_transaktion.html")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', template_folder='../template')
