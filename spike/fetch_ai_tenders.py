"""AP2-Spike: KI-Ausschreibungen der letzten 7 Tage von TED abholen.

Wegwerf-Code. Der saubere, getestete Client entsteht in AP4.

Ablauf:
1. Suche (Search API, Seitenmodus) -> Liste der Bekanntmachungen (Protokoll unter data/runs/).
2. Pro Bekanntmachung das XML laden -> unverändert nach data/raw/<datum>/<nummer>.xml.
3. Messwerte ausgeben (Treffer, pro Tag, Seiten, Laufzeit, Fehler).

Aufruf: uv run python spike/fetch_ai_tenders.py [--days 7] [--data-dir data]
"""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import httpx

SEARCH_URL = "https://api.ted.europa.eu/v3/notices/search"
PAGE_SIZE = 250  # Maximum im Seitenmodus
MIN_INTERVAL_S = 1.0  # höchstens 1 Anfrage pro Sekunde
TIMEOUT_S = 30.0
MAX_RETRIES = 3
RETRY_STATUS = {429, 500, 502, 503, 504}

# EU-27 (ISO 3166-1 alpha-3, wie TED es in buyer-country liefert)
EU27 = [
    "AUT",
    "BEL",
    "BGR",
    "HRV",
    "CYP",
    "CZE",
    "DNK",
    "EST",
    "FIN",
    "FRA",
    "DEU",
    "GRC",
    "HUN",
    "IRL",
    "ITA",
    "LVA",
    "LTU",
    "LUX",
    "MLT",
    "NLD",
    "POL",
    "PRT",
    "ROU",
    "SVK",
    "SVN",
    "ESP",
    "SWE",
]

# „Künstliche Intelligenz“ in den 24 EU-Amtssprachen + Machine Learning.
# TED-Volltext normalisiert Beugungen und Akzente (gemessen für de, pl, ro),
# daher reicht je Sprache die Grundform.
TERMS = [
    "изкуствен интелект",  # bg
    "umělá inteligence",  # cs
    "kunstig intelligens",  # da
    "künstliche Intelligenz",  # de
    "τεχνητή νοημοσύνη",  # el
    "artificial intelligence",  # en
    "inteligencia artificial",  # es
    "tehisintellekt",  # et
    "tekoäly",  # fi
    "intelligence artificielle",  # fr
    "intleacht shaorga",  # ga
    "umjetna inteligencija",  # hr
    "mesterséges intelligencia",  # hu
    "intelligenza artificiale",  # it
    "dirbtinis intelektas",  # lt
    "mākslīgais intelekts",  # lv
    "intelliġenza artifiċjali",  # mt
    "kunstmatige intelligentie",  # nl
    "sztuczna inteligencja",  # pl
    "inteligência artificial",  # pt
    "inteligență artificială",  # ro
    "umelá inteligencia",  # sk
    "umetna inteligenca",  # sl
    "artificiell intelligens",  # sv
    "machine learning",
    "maschinelles Lernen",
]


def build_query(start: date, end: date) -> str:
    terms = " OR ".join(f'FT~("{t}")' for t in TERMS)
    return (
        "notice-type IN (cn-standard)"
        f" AND buyer-country IN ({' '.join(EU27)})"
        f" AND publication-date>={start:%Y%m%d} AND publication-date<={end:%Y%m%d}"
        f" AND ({terms})"
    )


class Client:
    """Minimaler HTTP-Client mit Rate-Limit, Timeout und Retries mit Backoff."""

    def __init__(self) -> None:
        self.http = httpx.Client(timeout=TIMEOUT_S, headers={"User-Agent": "tender-ingest-spike"})
        self.last_request = 0.0
        self.requests = 0
        self.retries = 0

    def _wait(self) -> None:
        pause = MIN_INTERVAL_S - (time.monotonic() - self.last_request)
        if pause > 0:
            time.sleep(pause)
        self.last_request = time.monotonic()

    def request(self, method: str, url: str, **kwargs) -> httpx.Response:
        for attempt in range(MAX_RETRIES + 1):
            self._wait()
            self.requests += 1
            try:
                resp = self.http.request(method, url, **kwargs)
                if resp.status_code not in RETRY_STATUS:
                    resp.raise_for_status()
                    return resp
                reason = f"HTTP {resp.status_code}"
            except httpx.TransportError as exc:
                reason = type(exc).__name__
            if attempt == MAX_RETRIES:
                raise RuntimeError(f"{method} {url} fehlgeschlagen: {reason}")
            self.retries += 1
            backoff = 2**attempt  # 1 s, 2 s, 4 s
            print(f"  Wiederholung {attempt + 1}/{MAX_RETRIES} in {backoff}s ({reason})")
            time.sleep(backoff)
        raise AssertionError("unreachable")


def search_all(client: Client, query: str, run_dir: Path) -> list[dict]:
    notices: list[dict] = []
    page = 1
    while True:
        body = {
            "query": query,
            "fields": ["publication-number", "publication-date"],
            "limit": PAGE_SIZE,
            "page": page,
            "paginationMode": "PAGE_NUMBER",
        }
        data = client.request("POST", SEARCH_URL, json=body).json()
        (run_dir / f"search-page-{page}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        batch = data.get("notices", [])
        notices.extend(batch)
        total = data.get("totalNoticeCount") or 0
        print(f"Seite {page}: {len(batch)} Treffer (gesamt laut API: {total})")
        if len(batch) < PAGE_SIZE or len(notices) >= total:
            return notices
        page += 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    args = parser.parse_args()

    started = time.monotonic()
    end = date.today() - timedelta(days=1)  # letzter vollständiger Tag
    start = end - timedelta(days=args.days - 1)
    query = build_query(start, end)

    run_dir = args.data_dir / "runs" / datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "query.txt").write_text(query + "\n", encoding="utf-8")
    print(f"Zeitraum: {start} bis {end}")

    client = Client()
    notices = search_all(client, query, run_dir)

    per_day: Counter[str] = Counter()
    new, skipped, errors = 0, 0, []
    for n in notices:
        number = n["publication-number"]
        day = n["publication-date"][:10]
        per_day[day] += 1
        target = args.data_dir / "raw" / day / f"{number}.xml"
        if target.exists():
            skipped += 1
            continue
        try:
            xml_url = n["links"]["xml"]["MUL"]
            resp = client.request("GET", xml_url)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(resp.content)  # unverändert, Bytes wie geliefert
            new += 1
        except (KeyError, RuntimeError, httpx.HTTPStatusError) as exc:
            errors.append(f"{number}: {exc}")

    duration = time.monotonic() - started
    metrics = {
        "zeitraum": f"{start} bis {end}",
        "treffer": len(notices),
        "pro_tag": dict(sorted(per_day.items())),
        "xml_neu": new,
        "xml_schon_vorhanden": skipped,
        "fehler": len(errors),
        "fehlerquote": round(len(errors) / len(notices), 3) if notices else 0.0,
        "anfragen": client.requests,
        "wiederholungen": client.retries,
        "laufzeit_s": round(duration, 1),
    }
    (run_dir / "metrics.json").write_text(
        json.dumps(metrics | {"fehlerliste": errors}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    for e in errors:
        print("FEHLER", e)


if __name__ == "__main__":
    main()
