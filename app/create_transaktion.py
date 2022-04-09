from flask import render_template, request, redirect, url_for

from db.database_setup import session, BankStatement, Settings, Transaktions


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
            return redirect(url_for('bank_statements'))
        except Exception as e:
            print(e)
            return render_template("csv_reader.html")
    else:
        return render_template("csv_reader.html", filters=filters)
