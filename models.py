from sqlmodel import SQLModel, Field, DateTime, text
from datetime import datetime


class Transactions(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
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
    created_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        nullable=False,
        sa_column_kwargs={"server_default": text("now()")},
    )


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password: str
    created_at: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        nullable=False,
        sa_column_kwargs={"server_default": text("now()")},
    )
