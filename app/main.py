#Blueprint Main (seguendo 03_Blueprint_Create_Read.md e 04_Update_Delete_Auth.md)

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.repositories import transazioni_repo as transaction_repository
from app.repositories import categoria_repo as category_repository

bp = Blueprint('main', __name__)

def get_transaction(id, check_author=True):
    """
    Helper per controlli (come get_post del prof in 04_Update_Delete_Auth.md).
    1. Recupera transazione
    2. Controlla se esiste
    3. Controlla AUTORIZZAZIONE (è tua?)
    """
    transaction = transaction_repository.find_by_id(id)

    if transaction is None:
        abort(404, f"Transazione id {id} non esiste.")

    if check_author and transaction['author_id'] != g.user['id']:
        abort(403)  # Vietato!

    return transaction

@bp.route('/')
def index():
    """Homepage con ultime transazioni."""
    #PROTEZIONE: Se non sei loggato, vai al login
    if g.user is None:
        return redirect(url_for('auth.login'))

    #non SQL qui!
    transactions = transaction_repository.find_by_user(g.user['id'], limit=5)

    #calcola saldo (entrate - uscite)
    stats = transaction_repository.get_statistics(g.user['id'])
    balance = stats['bilancio']

    return render_template('index.html', transactions=transactions, balance=balance)

@bp.route('/transazioni')
def transazioni():
    """
    Lista transazioni con FILTRI 
    """
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    #Prendi filtri
    category_id = request.args.get('category_id', type=int)
    type_filter = request.args.get('type')
    
    #Chiama Repository con filtri
    transactions = transaction_repository.find_filtered(
        g.user['id'], category_id, type_filter
    )
    categories = category_repository.find_all()
    
    return render_template('transazioni.html',
                         transactions=transactions,
                         categories=categories,
                         selected_category=category_id,
                         selected_type=type_filter)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    """Crea nuova transazione"""
    if g.user is None:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        category_id = request.form['category_id']
        type = request.form['type']
        amount = request.form['amount']
        description = request.form['description']
        date = request.form['date']
        error = None
        #Da mettere
        if not description:
            error = 'La descrizione è obbligatoria.'

        if error is not None:
            flash(error, 'error')
        else:
            #Usa Repository
            transaction_repository.create(
                g.user['id'], category_id, type, amount, description, date
            )
            flash('Transazione aggiunta!', 'success')

            #BUDGET: Controllo semplice (solo per uscite)
            if type == 'uscita':
                #Budget fissi (semplice dizionario Python)
                budgets = {
                    1: 300.0,  #cibo max 300€
                    3: 150.0,  #svago max 150€
                }

                #se la categoria ha un budget, controlla
                if int(category_id) in budgets:
                    from datetime import datetime
                    month_start = datetime.now().strftime('%Y-%m-01')

                    #calcola totale del mese (tramite Repository!)
                    total = transaction_repository.get_monthly_total_by_category(
                        g.user['id'], category_id, month_start
                    )

                    budget_limit = budgets[int(category_id)]

                    #avviso se supera budget
                    if total > budget_limit:
                        category = category_repository.find_by_id(category_id)
                        flash(f'Attenzione! Hai superato il budget per {category["name"]}: €{total:.2f} / €{budget_limit:.2f}', 'error')

            return redirect(url_for('main.transazioni'))

    categories = category_repository.find_all()
    return render_template('create.html', categories=categories)

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    """
    Modifica transazione (04_Update_Delete_Auth.md).
    sei loggato? È tua?
    """
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    #controllo AUTORIZZAZIONE
    transaction = get_transaction(id)

    if request.method == 'POST':
        category_id = request.form['category_id']
        type = request.form['type']
        amount = request.form['amount']
        description = request.form['description']
        date = request.form['date']
        error = None

        if not description:
            error = 'La descrizione è obbligatoria.'

        if error is not None:
            flash(error, 'error')
        else:
            transaction_repository.update(
                id, category_id, type, amount, description, date
            )
            flash('Transazione modificata!', 'success')
            return redirect(url_for('main.transazioni'))

    categories = category_repository.find_all()
    return render_template('update.html', 
                         transaction=transaction,
                         categories=categories)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    """
    Elimina transazione
    Solo POST per sicurezza
    """
    if g.user is None:
        return redirect(url_for('auth.login'))
    
    #Verifica autorizzazione
    get_transaction(id)

    transaction_repository.delete(id)
    flash('Transazione eliminata.', 'success')
    return redirect(url_for('main.transazioni'))

@bp.route('/dashboard')
def dashboard():
    """
    Dashboard con GROUP BY
    Statistiche aggregate nel Repository
    """
    if g.user is None:
        return redirect(url_for('auth.login'))

    #Repository gestisce le query
    stats = transaction_repository.get_statistics(g.user['id'])

    return render_template('dashboard.html', stats=stats)

@bp.route('/export_csv')
def export_csv():
    """
    EXTRA: Esporta transazioni in CSV (come vuole il prof).
    Seguendo: https://www.geeksforgeeks.org/python/how-to-create-csv-output-in-flask/
    """
    if g.user is None:
        return redirect(url_for('auth.login'))

    from flask import make_response
    import csv
    from io import StringIO

    # Prendi tutte le transazioni dell'utente
    transactions = transaction_repository.find_by_user(g.user['id'])

    # Crea CSV usando il modulo csv (come nell'articolo GeeksForGeeks)
    si = StringIO()
    cw = csv.writer(si)

    # Header
    cw.writerow(['Data', 'Tipo', 'Categoria', 'Descrizione', 'Importo'])

    # Dati
    for t in transactions:
        cw.writerow([t['date'], t['type'], t['category_name'], t['description'], t['amount']])

    # Ottieni il contenuto CSV
    output = si.getvalue()

    # Crea response con CSV (come nel link del prof)
    response = make_response(output)
    response.headers["Content-Disposition"] = "attachment; filename=transazioni.csv"
    response.headers["Content-Type"] = "text/csv"

    return response