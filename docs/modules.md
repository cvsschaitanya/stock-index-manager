# Module-level descriptions

Below are short descriptions of the important modules and what they do.

### `src/api/main.py`

* FastAPI app exposing endpoints to query and build a market-cap based index. Primary functions:

  * `get_connection()` — helper to open SQLite connection to `src/batch/stocks.db`.
  * `get_top_marketcap(start_date, end_date, index_size)` — queries the DB for top tickers by market cap for each date and returns the composition used to build the index.
  * `get_cached_index_data(start_date, end_date)` — fetches already computed index values from DB.
  * `build_index(start_date, end_date, index_size)` — main endpoint flow that computes the index composition for given date range, persists index composition using `IndexCompDispatcher`, and returns the computed frame.
* Uses `pandas`+`sqlite3` for SQL-to-DataFrame workflow and `IndexCompDispatcher` to persist the composition.

### `src/base/extract/Extractor.py`

* Abstract base class for extractors. Defines `start()` and `_extract()` contract. Concrete extractors (Polygon/AlphaVantage/DatabaseExtractor) inherit and implement `_extract`.

### `src/base/extract/Pipeline.py`

* Lightweight pipeline orchestration: chain multiple extractors / transformers / dispatchers and call `start()` to run the first pipe, implicitly passing results down the chain.

### `src/base/dispatch/Dispatcher.py`

* Abstract base class for dispatcher components (the thing that *writes* data somewhere). Concrete subclasses include `DatabaseDispatcher` which upserts rows into SQLite tables.

### `src/base/transform/Transformer.py`

* Abstract Transformer base class that defines a `_transform(df)` hook. Concrete transformers implement `_transform` to convert DataFrame shapes, rename columns, filter tickers, etc.

### `src/base/observe/*` (Provider, Listener, LambdaListener)

* Tiny observer pattern implementation used to broadcast DataFrames to listeners/observers. Used by dispatchers to receive dataframes and act on them.

### `src/data/db/DatabaseDispatcher.py`

* Concrete `Dispatcher` that writes a pandas DataFrame into a SQLite table via `INSERT ... ON CONFLICT ... DO UPDATE`. Handles table creation via `create_table_if_not_exists()` which calls `create_table_query()` implemented by subclasses.

### `src/data/db/DatabaseExtractor.py`

* Extractor that runs a SQL query against a SQLite DB and returns rows. Useful for queries used by the API or downstream processing.

### `src/data/db/IndexCompDispatcher.py`

* Specialization of `DatabaseDispatcher` to persist index composition. Writes to table `IndexComposition` with columns `(ticker, date, share100)` and primary key `(ticker, date)`.

### `src/data/db/IndexPerfDispatcher.py`

* Persists index performance/time-series to a table `IndexPerf` with columns like `(date, value)`.

### `src/data/db/MetadataDbDispatcher.py`

* Persists stock metadata (ticker, name, exchange, etc) into a `TickerMetadata` table.

### `src/data/db/TickerDbDispatcher.py`

* Persists per-ticker daily price data into a `TickerPrice` (or similar) table. See the class for exact column names.

### `src/data/polygon/*`

* `PolygonApiExtractor.py` — small subclass of the general `Extractor` that wires Polygon API key from `config`.
* `PolygonClosePriceExtractor.py` — calls Polygon `StocksClient` (from `polygon` package) to extract daily close prices and shape them into a DataFrame with expected columns: `['ticker', 'date', 'close']` or similar.
* `PolygonClosePriceTransformer.py` — transforms Polygon close price responses into the canonical DataFrame format used by dispatchers.
* `PolygonMarketCapExtractor.py` — obtains market-cap (or shares outstanding) information for tickers from Polygon.
* `PolygonMarketCapTransformer.py` — uses shares outstanding × price or direct market cap fields to compute per-date market capitalization values.
* `PolygonMetadataExtractor.py` and `PolygonStocksTransformer.py` — extract and shape metadata and listing information (ticker name, exchange), and filter tickers to a reasonable set (there's a `filter_tickers` helper).

### `src/data/alphaVantage/AlphaVantageExtractor.py`

* Extractor for AlphaVantage API. Likely fetches time series and returns DataFrame for a ticker (used in tests).

### `src/batch/ingest/*` and `src/batch/ingestion.py`

* `batch/ingest/*.py` — scripts that orchestrate ingestion of price data, metadata and market-cap figures into the local SQLite DB via the extractors, transformers and DB dispatchers.
* `ingestion.py` — top-level helper that computes the date ranges, sets up initial index values and calls ingest functions for daily ranges. Contains `setup()` which seeds `IndexPerf` with a `ROOT_DATE` and `ROOT_INVESTMENT`.

---
