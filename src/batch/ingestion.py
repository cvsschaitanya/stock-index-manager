import sys
from datetime import date, timedelta

from batch.ingest.market_cap_data import ingest_market_cap
from batch.ingest.price_data import ingest_price_data
from batch.ingest.stock_metadata import ingest_stock_metadata
from config import load_config


def ingest(market_date):
    ingest_stock_metadata(count=100)  # Limit to 100 for testing

    ingest_market_cap([market_date], count=10)

    ingest_price_data(market_date)

def main():

    config_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/cvsschaitanya/code/python/stock-index-manager/config.json"
    market_date = sys.argv[2] if len(sys.argv) > 2 else (date.today() - timedelta(days=2)).isoformat()

    load_config(config_path)
    ingest(market_date)


if __name__ == "__main__":
    main()
