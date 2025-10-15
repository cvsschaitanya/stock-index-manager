from datetime import date, timedelta

import sys
from base.extract.Pipeline import Pipeline
from base.observe.LambdaListener import LambdaListener
from config import load_config, config
from data.db.DatabaseExtractor import DatabaseExtractor
from data.db.MetadataDbDispatcher import MetadataDbDispatcher
from data.polygon.PolygonClosePriceExtractor import PolygonClosePriceExtractor
from data.polygon.PolygonClosePriceTransformer import PolygonClosePriceTransformer
from data.polygon.PolygonMetadataExtractor import PolygonMetadataExtractor
from data.polygon.PolygonStocksTransformer import PolygonStocksTransformer
from data.db.RateLimitedExtractor import RateLimitedExtractor
from data.db.TickerDbDispatcher import TickerDbDispatcher
from data.polygon.PolygonMarketCapExtractor import PolygonMarketCapExtractor
from data.polygon.PolygonMarketCapTransformer import PolygonMarketCapTransformer


def ingest_price_data(market_date):
    extractor = Pipeline(PolygonClosePriceExtractor(market_date),
                         PolygonClosePriceTransformer(market_date),
                         TickerDbDispatcher(config['DB_PATH'], "TickerData")
                         )
    extractor.start()


def ingest_ticker_market_cap(market_date, tickers):
    extractor = RateLimitedExtractor(tickers, lambda ticker: Pipeline(
        PolygonMarketCapExtractor(ticker, market_date),
        PolygonMarketCapTransformer(),
        TickerDbDispatcher(config['DB_PATH'], "TickerData")
    )
                                     )
    extractor.start()


def ingest_market_cap(market_date, count=None):
    extractor = DatabaseExtractor(config['DB_PATH'], "SELECT ticker FROM Metadata")
    extractor.add_listener(
        LambdaListener(lambda x: ingest_ticker_market_cap(market_date, [_x[0] for _x in x[:count if count else len(x)]])))
    extractor.start()

def ingest_stock_metadata(count=1000):
    extractor = PolygonMetadataExtractor()
    transformer = PolygonStocksTransformer(count=count)
    stock_dispatcher = MetadataDbDispatcher(config['DB_PATH'], "Metadata")

    extractor.add_listener(transformer)
    transformer.add_listener(stock_dispatcher)

    extractor.start()

def ingest(market_date):
    ingest_stock_metadata(count=100)  # Limit to 100 for testing

    ingest_market_cap(market_date, count=10)

    ingest_price_data(market_date)

def main():
    config_path = sys.argv[1] if len(sys.argv) > 1 else "/Users/cvsschaitanya/code/python/stock-index-manager/config.json"
    market_date = sys.argv[2] if len(sys.argv) > 2 else (date.today() - timedelta(days=2)).isoformat()

    load_config(config_path)
    ingest(market_date)

    # for i in range(20):
    #     md = date.today() - timedelta(days=6+i)
    #     if md.weekday() < 5:  # Only weekdays
    #         print(f"Ingesting data for {md.isoformat()}")
    #         ingest(md.isoformat())

if __name__ == "__main__":
    main()
