from sqlmodel import SQLModel, create_engine, Session
from models import Transaction  # import so SQLModel knows this table exists

DATABASE_URL = "sqlite:///kasuku.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session