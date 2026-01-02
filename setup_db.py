# setup_db.py
# Script per creare il database (come insegna il prof in 02_DB_e_Repository.md)

import sqlite3
import os

# Crea cartella instance se non esiste
if not os.path.exists('instance'):
    os.makedirs('instance')

db_path = os.path.join('instance', 'walletwise.sqlite')

# Connessione (crea il file se non esiste)
connection = sqlite3.connect(db_path)

# Leggi ed esegui schema.sql (con encoding UTF-8 per le emoji)
with open('app/schema.sql', encoding='utf-8') as f:
    connection.executescript(f.read())

print("Database creato con successo in:", db_path)
connection.close()