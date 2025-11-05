import sqlite3

def conectar():
    return sqlite3.connect("db.sqlite")

def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ingredientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            nome TEXT,
            quantidade REAL,
            custo_unitario REAL,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            quantidade INTEGER,
            total REAL,
            data TEXT,
            FOREIGN KEY(produto_id) REFERENCES produtos(id)
        )
    """)
    conn.commit()
    conn.close()
