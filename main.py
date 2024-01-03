import io
from enum import Enum
from itertools import permutations
from pathlib import Path

import pandas as pd
import requests

NAMES = [
    #
    "narumi",
    "david",
    "dogiko",
    "alex",
    #
    "ben",
    "angie",
    #
    "moo",
    "charissa",
    #
    "john",
    "cindy",
    #
    "mia",
    "sam",
]

# 匯率
JPYTWD = 0.216345


# Google Sheet
url = "https://docs.google.com/spreadsheets/d/1WsJNwAh864X8zVSl9Qk8_GxlZPcRnS5KNwrzM7kjH4I/export?format=csv"


class Currency(str, Enum):
    JPY = "JPY"
    TWD = "TWD"


def downlaod_google_sheet_from_url(url: str, f: str) -> None:
    # 從 Google Sheet 下載 CSV 檔案
    resp = requests.get(url)

    with Path(f).open("wb") as fp:
        fp.write(resp.content)


def read_csv_from_google_sheet(url: str) -> pd.DataFrame:
    resp = requests.get(url)
    df = pd.read_csv(io.BytesIO(resp.content))
    df.fillna(0, inplace=True)
    return df


def normalize(s: str) -> str:
    # 去除空白，轉成小寫
    return s.strip().lower()


def parse_name(s: str) -> str:
    s = normalize(s)

    # 如果是空字串，直接回傳
    if s == "":
        msg = f"invalid name: {s}"
        raise ValueError(msg)

    return s


def parse_names(raw: str) -> list[str]:
    res = []

    if raw == "":
        raise ValueError("empty string")

    for s in raw.split(","):
        res += [parse_name(s)]

    return res


def parse_float(s: str) -> float:
    if s == "":
        return 0
    return float(s.replace(",", ""))


def parse_currency(s: str) -> Currency:
    s = s.strip().upper()
    if s not in list(Currency):
        msg = f"invalid currency: {s}"
        raise ValueError(msg)

    return Currency(s)


def check_name(s: str) -> None:
    if s not in NAMES:
        msg = f"invalid name: {s}"
        raise ValueError(msg)


df = read_csv_from_google_sheet(url)

# (債權人, 債務人) -> 金額
d = {}
for creditor, debtor in permutations(NAMES, 2):
    d[(creditor, debtor)] = 0

for _, row in df.iterrows():
    creditor = parse_name(row["出錢的"])
    debtors = parse_names(row["分攤的人"])
    amount = parse_float(row["平均"])

    # 把台幣轉換成日幣
    currency = parse_currency(row["貨幣"])
    if currency == Currency.JPY:
        amount = amount * JPYTWD

    # 檢查名字是國手
    check_name(creditor)
    for debtor in debtors:
        check_name(debtor)

    # 計算誰欠誰多少錢
    for debtor in debtors:
        # 夫妻合併
        # ("ben", "angie") 指 angie 的債務和債權都丟給 ben
        pairs = [
            ("ben", "angie"),
            ("moo", "charissa"),
            ("john", "cindy"),
            ("mia", "sam"),
        ]
        for x, y in pairs:
            if creditor == y:
                creditor = x
            if debtor == y:
                debtor = x
        # 不用計算自己欠自己多少錢
        if creditor == debtor:
            continue

        d[(creditor, debtor)] += float(amount)
        d[(debtor, creditor)] -= float(amount)

# 計算結算後每個人帳戶的增減
for name in NAMES:
    balance = 0
    for (creditor, _), amount in d.items():
        if amount == 0:
            continue

        if creditor == name:
            balance += amount

    if balance == 0:
        continue

    print(f"{name}:\t {balance:.2f} TWD")
