from datetime import date

from base.extract.Pipeline import Pipeline
from base.observe.LambdaListener import LambdaListener
from config import config
from data.db.DatabaseExtractor import DatabaseExtractor
from data.db.RateLimitedExtractor import RateLimitedExtractor
from data.db.TickerDbDispatcher import TickerDbDispatcher
from data.polygon.PolygonMarketCapExtractor import PolygonMarketCapExtractor
from data.polygon.PolygonMarketCapTransformer import PolygonMarketCapTransformer


def ingest_ticker_market_cap(dates, tickers):
    dates = [d for d in dates if date.fromisoformat(d).weekday() < 5]

    queries = [{'ticker': ticker, 'market_date': date} for ticker in tickers for date in dates]
    extractor = RateLimitedExtractor(queries, lambda q: Pipeline(
        PolygonMarketCapExtractor(q['ticker'], q['market_date']),
        PolygonMarketCapTransformer(),
        TickerDbDispatcher(config['DB_PATH'], "TickerData")
    ), safe=True)
    extractor.start()


def ingest_market_cap(dates, count=None):
    extractor = DatabaseExtractor(config['DB_PATH'], "SELECT ticker FROM Metadata")
    extractor.add_listener(
        LambdaListener(lambda x: ingest_ticker_market_cap(dates, [_x[0] for _x in x[:count if count else len(x)]])))
    extractor.start()
