from datetime import date

import numpy as np
from fastapi import FastAPI, HTTPException, Query
from typing import List
import sqlite3
import pandas as pd

from data.db.IndexCompDispatcher import IndexCompDispatcher

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

INDEX_SIZE = 5


def get_cached_index_data(start_date, end_date):
    """Retrieve cached index data if available."""
    conn = get_connection()
    try:
        query = """
        SELECT DISTINCT date FROM IndexComp
        WHERE date BETWEEN ? AND ?
        ORDER BY date;
        """
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        available_dates = set(df['date'].tolist())

        requested_dates = pd.date_range(start=start_date, end=end_date).strftime('%Y-%m-%d').tolist()
        missing_dates = [d for d in requested_dates if d not in available_dates]

        if len(missing_dates) > 0:
            print(f"Missing dates in cache: {missing_dates}")
            return None

        return df

    finally:
        conn.close()


@app.get("/build_index")
def build_index(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(date.today().isoformat(), description="End date in YYYY-MM-DD format"),
):
    """Build index of top tickers by market cap for each date in the range."""
    df = persist_composition(end_date, start_date)
    # persist_performance(df, start_date, end_date)
    return df.to_dict(orient="records")

def persist_composition(end_date: str, start_date: str):
    try:
        conn = get_connection()
        query_last_available_date = """
        SELECT date, value FROM IndexPerformance
        where date = (
            SELECT MAX(date) FROM IndexPerformance
        );
        """

        df = pd.read_sql_query(query_last_available_date, conn)
        last_available_date = str(df['date'].iloc[0])

        query_top_marketcap = """
        SELECT ticker, date, 20.0/price as share100 FROM (
            SELECT T.ticker, date, market_cap, price,
                ROW_NUMBER() OVER(PARTITION BY date ORDER BY market_cap DESC ) AS rn 
            FROM TickerData T, Metadata M 
            WHERE T.ticker = M.ticker 
            AND date >= ?
            AND date <= ?
        ) AS ranked 
        WHERE rn <= ? ORDER BY date, rn;
        """
        df = pd.read_sql_query(query_top_marketcap, conn, params=(last_available_date, end_date, INDEX_SIZE))

        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data between {start_date} and {end_date}")

        dispatcher = IndexCompDispatcher(DB_PATH)
        print(df[['ticker', 'date', 'share100']])
        dispatcher.observe(df[['ticker', 'date', 'share100']])
        return df

    finally:
        conn.close()
