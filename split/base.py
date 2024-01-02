from enum import Enum

from pydantic import BaseModel


class Currency(str, Enum):
    JPY = "JPY"
    TWD = "TWD"


class DebtItem(BaseModel):
    debtor: str
    creditors: list[str]
    description: str
    currency: Currency


class Debt(BaseModel):
    debtor: str
    creditor: str
    amount: float
    currency: Currency
