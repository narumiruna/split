import requests


def rate(source: str, target: str) -> float:
    url = "https://wise.com/rates/live"

    params = {"source": source, "target": target}
    resp = requests.get(url, params=params)
    data = resp.json()
    return float(data["value"])


def main():
    print(rate("JPY", "TWD"))


if __name__ == "__main__":
    main()
