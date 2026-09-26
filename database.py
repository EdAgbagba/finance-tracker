# from sqlmodel import SQLModel, create_engine, Session
# from models import Transaction  # import so SQLModel knows this table exists

# DATABASE_URL = "sqlite:///kasuku.db"
# engine = create_engine(DATABASE_URL, echo=True)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

# def get_session():
#     with Session(engine) as session:
#         yield session


import sqlite3

conn = sqlite3.connect(database="kasuku.db", autocommit=True)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def create_database():
    cursor.execute("""CREATE TABLE  IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    provider TEXT NOT NULL,
    type TEXT NOT NULL,
    direction TEXT,
    amount FLOAT,
    counterparty_name TEXT,
    counterparty_number TEXT,
    balance_after FLOAT,
    fee FLOAT,
    transaction_id TEXT,
    raw_text TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")

def insert_transaction(data: dict):
    cursor.execute("""
        INSERT INTO transactions
        (provider, type, direction, 
        amount, counterparty_name, 
        counterparty_number, balance_after, 
        fee, transaction_id, raw_text)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING *""", (
        data.get("provider"),
        data.get("type"),
        data.get("direction"),
        data.get("amount"),
        data.get("counterparty_name"),
        data.get("counterparty_number"),
        data.get("balance_after"),
        data.get("fee"),
        data.get("transaction_id"),
        data.get("raw_text"),
    ))
    return dict(cursor.fetchone())