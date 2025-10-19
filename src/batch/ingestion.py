import sys
from datetime import date, timedelta

import pandas as pd

from batch.ingest.market_cap_data import ingest_market_cap
from batch.ingest.price_data import ingest_price_data
from batch.ingest.stock_metadata import ingest_stock_metadata
from config import load_config, config
from data.db.IndexPerfDispatcher import IndexPerfDispatcher


def get_all_dates_between(from_date, to_date):
    start_date = date.fromisoformat(from_date)
    end_date = date.fromisoformat(to_date)

    delta = end_date - start_date

    all_dates = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        all_dates.append(day.isoformat())

    return all_dates


ROOT_DATE = "2025-10-06"
ROOT_INVESTMENT = 1000_000.0
def setup():
    dispatcher = IndexPerfDispatcher(config['DB_PATH'])
    dispatcher.observe(pd.DataFrame({
        'date': [ROOT_DATE],
        'value': [ROOT_INVESTMENT]
    }))

def ingest(from_date, to_date):
    setup()

    ingest_stock_metadata(count=100)  # Limit to 100 for testing

    ingest_market_cap(get_all_dates_between(from_date, to_date), count=10)

    ingest_price_data(get_all_dates_between(from_date, to_date))

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Stock index tracker")

    parser.add_argument(
        "--config",
        default="/Users/cvsschaitanya/code/python/stock-index-manager/config.json",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--from_date",
        default=date.today().isoformat(),
        help="Start date in YYYY-MM-DD format"
    )
    parser.add_argument(
        "--to_date",
        default=date.today().isoformat(),
        help="End date in YYYY-MM-DD format"
    )

    return parser.parse_args()

def main():

    args = parse_args()

    load_config(args.config)
    ingest(args.from_date, args.to_date)


if __name__ == "__main__":
    main()
