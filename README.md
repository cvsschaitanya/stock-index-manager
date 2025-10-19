# stock-index-manager

A small, pragmatic toolkit (and a little chaotic) to ingest stock data, compute market-cap-based index compositions and track index performance over time. It provides a set of extractors for external data (Polygon, AlphaVantage), dispatchers that write to a local SQLite DB used in `src/batch/stocks.db`, and a tiny FastAPI server to expose index-building and query endpoints.

> Quick note: this repo expects a local SQLite database file at `src/batch/stocks.db` (a sample/backup is included under `src/batch/`). API keys (Polygon/AlphaVantage) are read from `config`.

---

## Assumptions / scope

- FREE-API has a rate limit, so mostly assumed index of size 5 within a universe of 10 stocks
- More focussed on code structure, modularity, and testability than performance/optimization
- SQLite is used as the local DB for simplicity
- More focus on the ingestion part than the API part
---


## Quick links

* Assignment brief: `Assignment.pdf`
* Data ingestion notes: `docs/Ingestion.md`
* Start API helper: `start_api.sh`
* Local DB sample: `src/batch/stocks.db.liq` and `src/batch/stocks.db.bak`

## Modules

See the [Modules documentation](docs/modules.md) for details.


---

## Install & run (developer quickstart)

1. Create a virtual environment and install dependencies from `requirements.txt`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Ensure config is present (or set env vars). `config` module is expected under `src/config`. Edit `config/__init__.py` or use your own loader (the repo contains a `config` package skeleton).

3. Ensure DB is available at `src/batch/stocks.db` (you can use the included sample `src/batch/stocks.db.liq` or run the ingestion script to create/populate it).

4. Start the API (uses FastAPI/Uvicorn):

```bash
./start_api.sh  # convenience script in repo root
# or
uvicorn src.api.main:app --reload --port 8000
```

---

## High-level responsibilities (what each top-level package does)

* `src/api` — FastAPI endpoints and helpers to query top market-cap tickers, build index composition and persist it to DB.
* `src/base` — abstract base classes and framework pieces (Extractors, Transformers, Dispatchers, Providers/Listeners) used by concrete implementations. Think of it as the small in-house ETL mini-framework.
* `src/data` — concrete data extraction/transform/transporter implementations for data sources (Polygon, AlphaVantage) and SQLite DB dispatchers.
* `src/batch` — batch ingestion scripts that stitch together extractors and dispatchers to populate the local SQLite DB.
* `src/config` — configuration loader and constants (API keys, DB_PATH, etc).

---


## Database schema
Most of the column names are self-explanatory. Primary keys are indicated.
- Metadata: key(ticker)
    - ticker
    - name
    - exchange
- TickerData: key(ticker, date)
    - ticker
    - date
    - market_cap
    - price
- IndexComposition: key(ticker, date)
    - ticker
    - date
    - share100 - How many(can be fractional) shares of the ticker are present in $100 worth investment on this day?
- IndexPerformance: key(date)
    - date
    - value - Index value on this date assuming $100,000 initial investment on a ROOT_DAY(say 2025-10-06) 
---

## Config

Takes a config.json file with the following structure:

```json
{
  "POLYGON_API_KEY": "your_polygon_api_key",
  "DB_PATH": "src/batch/stocks.db",
  "ROOT_DATE": "2025-10-06",
  "ROOT_INVESTMENT": 100000
}
```

--

## How to run

* Run ingestion for a date range:

```bash
export PYTHONPATH=/Users/cvsschaitanya/code/python/stock-index-manager/src && python src/batch/ingestion.py --config /Users/cvsschaitanya/code/python/stock-index-manager/config.json --to_date 2025-10-19 --from_date 2025-10-06
```

* Run api

```bash
./start_api.sh
```
