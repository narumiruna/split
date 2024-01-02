from pathlib import Path

import requests


def downlaod_google_sheet_from_url(url: str, f: str) -> None:
    resp = requests.get(url)

    with Path(f).open("wb") as fp:
        fp.write(resp.content)
