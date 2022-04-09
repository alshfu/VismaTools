import os

from flask import redirect, url_for, send_file
from sqlalchemy import desc
from db.database_setup import session, BankStatement, Transaktions


def create_se_file(statements_id):
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
            tr_date = transaktion.tr_date[0:10].replace('-', '')
            amount_p = transaktion.tr_amount
            moms = transaktion.moms
            # TO do moms kalkbyl
            try:
                if float(amount_p) < 0:
                    amount_s = amount_p.replace('-', '')
                    if moms == "1":
                        vat = float(amount_s) * 0.2
                        vat = round(vat, 2)
                        ex_vat = float(amount_s) - vat
                        print(f"amount = {amount_s} moms = {vat} amount.ex.moms = {ex_vat}")
                else:
                    amount_s = f"""-{amount_p}"""
                    if moms == "1":
                        vat = float(amount_p) * 0.2
                        vat = round(vat, 2)
                        ex_vat = float(amount_p) * 0.8
                        print(f"amount = {amount_p} moms = {vat} amount.ex.moms = {ex_vat}")
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
