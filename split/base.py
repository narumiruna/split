from enum import Enum

from pydantic import BaseModel


class Currency(str, Enum):
    JPY = "JPY"
    TWD = "TWD"


class DebtItem(BaseModel):
    creditor: str  # 出錢的
    debtors: list[str]  # 欠錢的
    description: str
    currency: Currency
    total_amount: float


class Debt(BaseModel):
    creditor: str  # 出錢的
    debtor: str  # 欠錢的
    amount: float
    currency: Currency
