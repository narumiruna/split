from itertools import permutations
from pathlib import Path

import pandas as pd

from split.base import Currency

NAMES = [
    # 棒子四人組
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


def normalize(s: str) -> str:
    return s.strip().lower()


def parse_creditor(s: str) -> str:
    s = s.strip().lower()
    if s == "":
        return ""

    if s not in NAMES:
        raise ValueError(f"Invalid creditor name: {s}")
    return s


def parse_debtor(raw: str) -> list[str]:
    res = []

    if not isinstance(raw, str):
        raise ValueError(f"Invalid debtor name: {raw}")

    if raw == "":
        return res

    for s in raw.split(","):
        s = s.strip().lower()
        if s not in NAMES:
            raise ValueError(f"Invalid debtor name: {s}")
        res.append(s)
    return res


def parse_amount(raw: str) -> float:
    if raw == "":
        return 0
    return float(raw.replace(",", ""))


def main():
    f = Path("/Users/narumi/Downloads/2023日本仙台債務表 - 債務列表.csv")
    df = pd.read_csv(f)
    df.fillna("", inplace=True)

    d = {}
    for creditor, debtor in permutations(NAMES, 2):
        d[(creditor, debtor)] = 0

    for _, row in df.iterrows():
        creditor = parse_creditor(row["出錢的"])
        debtors = parse_debtor(row["分攤的人"])
        total_amount = parse_amount(row["總金額"])

        currency = Currency(row["貨幣"])

        if currency != Currency.JPY:
            continue

        len_debtors = len(debtors)
        if len_debtors == 0:
            continue

        amount = total_amount / len_debtors
        for debtor in debtors:
            if creditor == debtor:
                continue

            d[(creditor, debtor)] += float(amount)
            d[(debtor, creditor)] -= float(amount)

    for (creditor, debtor), amount in d.items():
        if amount == 0:
            continue

        if amount > 0:
            print(f"{creditor} 借 {debtor}: {amount} yen")
        elif amount < 0:
            print(f"{creditor} 欠 {debtor}: {-amount} yen")
        else:
            continue


if __name__ == "__main__":
    main()
