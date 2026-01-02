#Blueprint Auth (seguendo 03_Form_e_Auth.md)
#Gestione: Registrazione, Login, Logout, Sessione

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.repositories import user_repo

# url_prefix='/auth' → tutte le route iniziano con /auth
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    """
    Middleware del prof (03_Form_e_Auth.md)
    Eseguita PRIMA di ogni richiesta
    Carica l'utente dalla sessione e lo mette in g.user
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = user_repo.get_user_by_id(user_id)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Registrazione nuovo utente."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username obbligatorio.'
        elif not password:
            error = 'Password obbligatoria.'

        if error is None:
            #Hasho la password (MAI salvarla in chiaro sennò ciao conto)
            hashed_pwd = generate_password_hash(password)

            #Chiamo il Repository
            success = user_repo.create_user(username, hashed_pwd)
            
            if success:
                flash('Registrazione completata!', 'success')
                return redirect(url_for('auth.login'))
            else:
                error = f"L'utente {username} è già registrato."

        flash(error, 'error')

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Login utente."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        #Cerco l'utente nel DB
        user = user_repo.get_user_by_username(username)

        if user is None:
            error = 'Username non corretto.'
        #Verifico la password
        elif not check_password_hash(user['password'], password):
            error = 'Password non corretta.'

        if error is None:
            #SESSIONE: salvo l'id dell'utente nella sessione
            session.clear()
            session['user_id'] = user['id']
            
            flash('Login effettuato!', 'success')
            return redirect(url_for('main.index'))

        flash(error, 'error')

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """Logout: tagliamo il braccialetto."""
    session.clear()
    flash('Logout effettuato.', 'success')
    return redirect(url_for('auth.login'))