from datetime import date

from base.extract.Pipeline import Pipeline
from config import config, load_config
from data.db.RateLimitedExtractor import RateLimitedExtractor
from data.db.TickerDbDispatcher import TickerDbDispatcher
from data.polygon.PolygonClosePriceExtractor import PolygonClosePriceExtractor
from data.polygon.PolygonClosePriceTransformer import PolygonClosePriceTransformer


def ingest_price_data(dates):
    dates = [d for d in dates if date.fromisoformat(d).weekday() < 5]

    extractor = RateLimitedExtractor(dates,
                                     lambda d: Pipeline(PolygonClosePriceExtractor(d),
                                                        PolygonClosePriceTransformer(d),
                                                        TickerDbDispatcher(config['DB_PATH'])
                                                        ))
    extractor.start()
