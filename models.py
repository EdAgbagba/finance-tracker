from sqlmodel import SQLModel, Field
from datetime import datetime

class Transaction(SQLModel, table=True):
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
    created_at: datetime = Field(default_factory=datetime.now)