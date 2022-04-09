from flask import render_template

from sqlalchemy import desc

from db.database_setup import session, BankStatement


def get_list_of_statements():
    statements = session.query(BankStatement).order_by(desc(BankStatement.bank_statement_id)).all()
    return render_template('bank_statements.html', statements=statements)
