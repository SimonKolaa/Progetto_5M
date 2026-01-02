#Repository delle transazioni con JOIN (come i post in 02_Repository_dei_Post.md)
#Relazione: molte transazioni per un utente (molti-a-uno)

from app.db import get_db

def find_all():
    """
    Recupera tutte le transazioni
    JOIN con user per username e con categories per nome.
    """
    db = get_db()
    query = """
        SELECT t.*, u.username, c.name as category_name, c.icon
        FROM transactions t
        JOIN user u ON t.author_id = u.id
        JOIN categories c ON t.category_id = c.id
        ORDER BY t.date DESC, t.created DESC
    """
    return db.execute(query).fetchall()

def find_by_user(user_id, limit=None):
    """Recupera transazioni di un utente specifico."""
    db = get_db()
    query = """
        SELECT t.*, c.name as category_name, c.icon
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.author_id = ?
        ORDER BY t.date DESC, t.created DESC
    """
    if limit:
        query += f' LIMIT {limit}'
    return db.execute(query, (user_id,)).fetchall()

def find_by_id(transaction_id):
    """Recupera una singola transazione con JOIN"""
    db = get_db()
    query = """
        SELECT t.*, u.username, c.name as category_name, c.icon
        FROM transactions t
        JOIN user u ON t.author_id = u.id
        JOIN categories c ON t.category_id = c.id
        WHERE t.id = ?
    """
    return db.execute(query, (transaction_id,)).fetchone()

def find_filtered(user_id, category_id=None, type_filter=None):
    """
    LIVELLO 2: Filtra transazioni per categoria e/o tipo
    Query dinamica
    """
    db = get_db()
    query = """
        SELECT t.*, c.name as category_name, c.icon
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.author_id = ?
    """
    params = [user_id]

    if category_id:
        query += ' AND t.category_id = ?'
        params.append(category_id)
    if type_filter:
        query += ' AND t.type = ?'
        params.append(type_filter)

    query += ' ORDER BY t.date DESC, t.created DESC'

    return db.execute(query, params).fetchall()

def create(author_id, category_id, type, amount, description, date):
    """Crea una nuova transazione (come create_post del prof)"""
    db = get_db()
    db.execute(
        '''INSERT INTO transactions
           (author_id, category_id, type, amount, description, date)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (author_id, category_id, type, amount, description, date)
    )
    db.commit()

def update(transaction_id, category_id, type, amount, description, date):
    """Aggiorna una transazione (come update_post del prof)"""
    db = get_db()
    db.execute(
        '''UPDATE transactions
           SET category_id=?, type=?, amount=?, description=?, date=?
           WHERE id = ?''',
        (category_id, type, amount, description, date, transaction_id)
    )
    db.commit()

def delete(transaction_id):
    """Elimina una transazione (come delete_post del prof)"""
    db = get_db()
    db.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    db.commit()

def get_balance(user_id):
    """
    Calcola saldo corrente (funzionalità wallet)
    """
    db = get_db()
    
    #totale entrate
    result_entrate = db.execute(
        'SELECT SUM(amount) as total FROM transactions WHERE author_id = ? AND type = "entrata"',
        (user_id,)
    ).fetchone()
    entrate = result_entrate['total'] if result_entrate['total'] else 0
    
    #totale uscite
    result_uscite = db.execute(
        'SELECT SUM(amount) as total FROM transactions WHERE author_id = ? AND type = "uscita"',
        (user_id,)
    ).fetchone()
    uscite = result_uscite['total'] if result_uscite['total'] else 0
    
    return entrate - uscite

def get_statistics(user_id, start_date=None, end_date=None):
    """
    SUM semplice, >= e <= per le date.
    """
    db = get_db()
    
    #Query
    base_where = 'WHERE author_id = ?'
    params_entrate = [user_id]
    params_uscite = [user_id]
    params_categoria = [user_id]
    
    #FILTRO DATA (solo >= e <=)
    date_filter = ''
    if start_date and end_date:
        date_filter = ' AND date >= ? AND date <= ?'
        params_entrate.extend([start_date, end_date])
        params_uscite.extend([start_date, end_date])
        params_categoria.extend([start_date, end_date])
    
    #totale entrate (SUM)
    result_entrate = db.execute(
        f'''SELECT SUM(amount) as total 
           FROM transactions 
           {base_where} AND type = "entrata"{date_filter}''',
        params_entrate
    ).fetchone()
    entrate = result_entrate['total'] if result_entrate['total'] else 0
    
    #totale uscite (SUM)
    result_uscite = db.execute(
        f'''SELECT SUM(amount) as total 
           FROM transactions 
           {base_where} AND type = "uscita"{date_filter}''',
        params_uscite
    ).fetchone()
    uscite = result_uscite['total'] if result_uscite['total'] else 0
    
    #spese per categoria con GROUP BY 
    per_categoria = db.execute(
        f'''SELECT c.name, c.icon, SUM(t.amount) as total
           FROM categories c
           LEFT JOIN transactions t ON c.id = t.category_id 
               AND t.author_id = ? AND t.type = "uscita"{date_filter}
           GROUP BY c.id
           HAVING total > 0
           ORDER BY total DESC''',
        params_categoria
    ).fetchall()
    
    return {
        'entrate': entrate,
        'uscite': uscite,
        'bilancio': entrate - uscite,
        'per_categoria': per_categoria,
        'start_date': start_date,
        'end_date': end_date
    }