import os

from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from sqlalchemy import desc
from db.database_setup import session, BankStatement, Transaktions, Settings

UPLOAD_FOLDER = 'app/static/uploads'


def transaktions_list(statements_id):
    filters = session.query(Settings).all()
    statements = session.query(BankStatement).get(statements_id)
    transaktions = session.query(Transaktions).filter_by(bank_statement_id=statements_id).order_by(
        desc(Transaktions.quote_id))

    if request.method == 'POST':
        print(len(request.form))
        try:
            for index_ in range(len(request.form)):
                print(index_)
                tr_id = request.form.getlist('tr_quote_id')[index_]
                tr_name = request.form.getlist('tr_name')[index_]
                konto_s = request.form.getlist('tr_konto_s')[index_]
                tr_file = request.files
                file = tr_file.getlist('tr_file')[index_]
                filename = secure_filename(file.filename)
                transaktion = session.query(Transaktions).filter_by(quote_id=tr_id)
                transaktion = session.query(Transaktions).get(tr_id)
                transaktion.tr_name = tr_name
                transaktion.konto_s = konto_s
                transaktion.moms = request.form.getlist('tr_moms')[index_]
                if len(filename) != 0:
                    filename = str(statements.bank_statement_id) + '_' + str(index_) + '_' + filename
                    print(os.path.join(UPLOAD_FOLDER, filename))
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    transaktion.ver_file = 'static/uploads/' + filename
                session.commit()
            return redirect(url_for('transaktions_by_id', statements_id=statements_id))
        except Exception as e:
            print("!!!")
            print(e)
            return redirect(url_for('transaktions_by_id', statements_id=statements_id))

    return render_template('verifikations.html', statements=statements, transaktions=transaktions, filters=filters)
