from datetime import date

from base.observe.LambdaListener import LambdaListener
from config import load_config, config
from data.db.DatabaseDispatcher import DatabaseDispatcher
from data.db.DatabaseExtractor import DatabaseExtractor
from data.db.MetadataDbDispatcher import MetadataDbDispatcher
from data.polygon.PolygonStocksExtractor import PolygonStocksExtractor
from data.polygon.PolygonStocksTransformer import PolygonStocksTransformer
from data.polygon.RateLimitedPolygonTickerExtractor import RateLimitedPolygonTickerExtractor


def ingest_ticker_data(ticker):
    extractor = RateLimitedPolygonTickerExtractor(ticker, date.today().isoformat())
    extractor.start()


def ingest_stock_market_data(count=None):
    extractor = DatabaseExtractor(config['DB_PATH'], "SELECT ticker FROM Metadata")
    extractor.add_listener(
        LambdaListener(lambda x: ingest_ticker_data([_x[0] for _x in x[:count if count else len(x)]])))
    extractor.start()


def main():
    load_config("config.json")

    # ingest_stock_metadata(count=100)  # Limit to 100 for testing

    ingest_stock_market_data(count=10)


def ingest_stock_metadata(count=1000):
    extractor = PolygonStocksExtractor()
    transformer = PolygonStocksTransformer(count=count)
    stock_dispatcher = MetadataDbDispatcher(config['DB_PATH'], "Metadata")

    extractor.add_listener(transformer)
    transformer.add_listener(stock_dispatcher)

    extractor.start()


if __name__ == "__main__":
    main()
