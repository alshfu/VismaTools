from flask import render_template, request, redirect, url_for
from sqlalchemy import desc
from db.database_setup import session, BankStatement, Transaktions


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
                transaktion.moms = request.form.getlist('tr_moms')[index_]
                session.commit()
                print(request.form.getlist('tr_moms')[index_])
            return redirect(url_for('transaktions_by_id', statements_id=statements_id))
        except Exception as e:
            print(e)
            return redirect(url_for('transaktions_by_id', statements_id=statements_id))

    return render_template('transactions.html', statements=statements, transaktions=transaktions)
