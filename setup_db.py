
#Script per creare il database (02_DB_e_Repository.md)

import sqlite3
import os

# Crea cartella instance se non esiste
if not os.path.exists('instance'):
    os.makedirs('instance')

db_path = os.path.join('instance', 'walletwise.sqlite')

# Connessione (crea il file se non esiste)
connection = sqlite3.connect(db_path)

# Leggi ed esegui schema.sql
with open('app/schema.sql') as f:
    connection.executescript(f.read())

print("Database creato con successo in:", db_path)
connection.close()
