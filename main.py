from itertools import permutations

import click
import pandas as pd

from split.base import Currency
from split.utils import downlaod_google_sheet_from_url

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


@click.command()
@click.option("-c", "--target-currency", type=click.STRING, default="JPY")
def main(target_currency: str):
    url = "https://docs.google.com/spreadsheets/d/1WsJNwAh864X8zVSl9Qk8_GxlZPcRnS5KNwrzM7kjH4I/export?format=csv"
    f = "data.csv"

    downlaod_google_sheet_from_url(url, f)
    df = pd.read_csv(f)
    df.fillna("", inplace=True)

    d = {}
    for creditor, debtor in permutations(NAMES, 2):
        d[(creditor, debtor)] = 0

    for _, row in df.iterrows():
        creditor = parse_creditor(row["出錢的"])
        debtors = parse_debtor(row["分攤的人"])
        amount = parse_amount(row["平均"])

        currency = Currency(row["貨幣"])
        if currency != target_currency:
            continue

        len_debtors = len(debtors)
        if len_debtors == 0:
            continue

        for debtor in debtors:
            if creditor == debtor:
                continue

            d[(creditor, debtor)] += float(amount)
            d[(debtor, creditor)] -= float(amount)

    # for (creditor, debtor), amount in d.items():
    #     if amount == 0:
    #         continue

    #     if amount > 0:
    #         # print(f"{creditor} 借 {debtor}: {amount} {target_currency}")
    #         pass
    #     elif amount < 0:
    #         print(f"{creditor} 欠 {debtor}: {-amount} {target_currency}")
    #     else:
    #         continue

    for name in NAMES:
        total = 0
        for (creditor, _), amount in d.items():
            if amount == 0:
                continue

            if creditor == name:
                total += amount
        if total == 0:
            continue
        print(f"{name}: {total} {target_currency}")


if __name__ == "__main__":
    main()
