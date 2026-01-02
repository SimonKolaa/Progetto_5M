# WalletWise - Gestione Spese Personali fatto da Simon Kola

**Progetto Flask - Natale 2025**

---

## Descrizione
Applicazione web per gestire entrate e uscite personali con categorie e statistiche.

## Funzionalità
- **Livello 1:** Autenticazione (Register/Login) + CRUD completo delle transazioni
- **Livello 2:** Relazione 1-N (Categorie → Transazioni) + Filtri dinamici
- **BONUS:** Dashboard con statistiche aggregate (GROUP BY, SUM, LEFT JOIN)

---

## Architettura

- **Application Factory** (`__init__.py`)
- **Blueprints** (`auth.py`, `main.py`)
- **Repository Pattern** (`repositories/`) - TUTTO il SQL qui!
- **Jinja2 Templates** con ereditarietà
- **Sicurezza:** sessioni, hashing password, autorizzazione

---

## Schema Database
```sql
user (id, username, password)
categories (id, name, icon)
transactions (id, author_id FK, category_id FK, type, amount, description, date)
```
**Relazione molti-a-uno:** molte transazioni per un utente

---

## Installazione

```bash
# 1. Crea ambiente virtuale
python -m venv .venv

# 2. Attiva (Windows)
.venv\Scripts\activate

# 3. Installa dipendenze
pip install -r requirements.txt

# 4. Crea database
python setup_db.py

# 5. Avvia l'applicazione
python run.py
```

Vai su: **http://127.0.0.1:5000**

---

## Struttura File

```
Progetto_5M/
├── app/
│   ├── __init__.py                    # Application Factory
│   ├── db.py                          # Connessione DB
│   ├── auth.py                        # Blueprint Autenticazione
│   ├── main.py                        # Blueprint Main
│   ├── schema.sql                     # Schema Database
│   ├── repositories/                  # REPOSITORY PATTERN
│   │   ├── user_repo.py               # Repository Utenti
│   │   ├── categoria_repo.py          # Repository Categorie
│   │   └── transazioni_repo.py        # Repository Transazioni
│   └── templates/
│       ├── base.html                  # Template base
│       ├── index.html                 # Homepage
│       ├── auth/
│       │   ├── login.html             # Pagina login
│       │   └── register.html          # Pagina registrazione
│       ├── create.html                # Crea nuova transazione
│       ├── transazioni.html           # Elenco transazioni
│       ├── update.html                # Modifica transazione
│       └── dashboard.html             # Dashboard con statistiche
├── app_prof/                          # File di esempio del professore
│   ├── __init___prof.py
│   ├── main_prof.py
│   ├── templates_prof/
│   │   ├── base_prof.html
│   │   ├── index_prof.html
│   │   └── about_prof.html
│   └── run_prof.py
├── setup_db.py                        # Script inizializzazione DB
├── run.py                             # Entry point applicazione
└── requirements.txt                   # Dipendenze Python
```

---

## Tecnologie
- **Flask 3.0** - Web Framework
- **SQLite3** - Database
- **Jinja2** - Template Engine
- **Werkzeug** - Password Hashing

---

##  Autore
**Simon Kola** - Classe 5^M Informatica

