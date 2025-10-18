from fastapi import FastAPI, HTTPException, Query
from typing import List
import sqlite3
import pandas as pd

app = FastAPI(title="Market Cap API")

DB_PATH = "src/batch/stocks.db"


def get_connection():
    # fastapi lifespan uses per-request connection
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/top_marketcap")
def get_top_marketcap(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    limit: int = Query(10, description="Number of top tickers to return (default 10)"),
):
    """Return top tickers by market cap for a given date."""
    try:
        conn = get_connection()
        query = """
            SELECT TickerData.ticker, market_cap, price
            FROM TickerData, Metadata
            WHERE TickerData.ticker = Metadata.ticker
            AND date = ?
            ORDER BY market_cap DESC
            LIMIT ?
        """
        df = pd.read_sql_query(query, conn, params=(date, limit))
        print(df)
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data for {date}")
        resp = df.to_dict(orient="records")
        print(resp)
        return resp

    finally:
        conn.close()
