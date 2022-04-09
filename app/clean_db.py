from flask import request, redirect, url_for
from db.database_setup import session, BankStatement, Transaktions


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
        return redirect(url_for('statements'))
    else:
        return redirect(url_for('statements'))
