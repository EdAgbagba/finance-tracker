import os
from typing import Annotated
from fastapi import Depends
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel

load_dotenv()

SQL_DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(SQL_DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# dependency for the various functions so they create a new session
SessionDep = Annotated[Session, Depends(get_session)]
