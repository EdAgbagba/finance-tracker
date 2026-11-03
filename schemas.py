from sqlmodel import SQLModel
from pydantic import EmailStr
from datetime import datetime


class Create_txn(SQLModel):
    message: str


# posts response model
class Txn_response(SQLModel):
    id: int
    provider: str
    type: str
    direction: str | None = None
    amount: float | None = None
    counterparty_name: str | None = None
    counterparty_number: str | None = None
    balance_after: float | None = None
    fee: float | None = None
    transaction_id: str | None = None
    raw_text: str
    created_at: datetime


# input model for creating a user
class Create_user(SQLModel):
    email: EmailStr
    password: str


# response model for when a user is created
class Created_user_response(SQLModel):
    id: int
    email: EmailStr
    created_at: datetime


class User_login(SQLModel):
    email: EmailStr
    password: str


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    id: str | None = None
