#Repository per le categorie (seguendo il pattern del prof)

from app.db import get_db

def find_all():
    """Recupera tutte le categorie."""
    db = get_db()
    return db.execute('SELECT * FROM categories ORDER BY name').fetchall()

def find_by_id(category_id):
    """Trova una categoria per ID."""
    db = get_db()
    return db.execute(
        'SELECT * FROM categories WHERE id = ?', 
        (category_id,)
    ).fetchone()