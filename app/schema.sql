
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS user;

-- Tabella utenti
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- Tabella categorie (relazione 1-N)
CREATE TABLE categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  icon TEXT NOT NULL
);

-- Tabella transazioni (come post, ma per le spese)
-- Relazione molti-a-uno: molte transazioni per un utente
CREATE TABLE transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  category_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  type TEXT NOT NULL CHECK(type IN ('entrata', 'uscita')),
  amount REAL NOT NULL,
  description TEXT NOT NULL,
  date DATE NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (category_id) REFERENCES categories (id)
);

-- Categorie predefinite
INSERT INTO categories (name) VALUES 
    ('Cibo'),
    ('Trasporti'),
    ('Svago'),
    ('Altro'),
    ('Stipendio');