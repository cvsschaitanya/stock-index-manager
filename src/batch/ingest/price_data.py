from base.extract.Pipeline import Pipeline
from config import config
from data.db.TickerDbDispatcher import TickerDbDispatcher
from data.polygon.PolygonClosePriceExtractor import PolygonClosePriceExtractor
from data.polygon.PolygonClosePriceTransformer import PolygonClosePriceTransformer


def ingest_price_data(market_date):
    extractor = Pipeline(PolygonClosePriceExtractor(market_date),
                         PolygonClosePriceTransformer(market_date),
                         TickerDbDispatcher(config['DB_PATH'], "TickerData")
                         )
    extractor.start()
