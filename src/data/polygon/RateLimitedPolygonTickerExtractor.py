import time
from base.extract.Extractor import Extractor
from base.extract.Pipeline import Pipeline
from config import config
from data.db.TickerDbDispatcher import TickerDbDispatcher
from data.polygon.PolygonTickerExtractor import PolygonTickerExtractor
from data.polygon.PolygonTickerTransformer import PolygonTickerTransformer


class RateLimitedPolygonTickerExtractor(Extractor):
    REQ_PER_MINUTE = 5

    def __init__(self, tickers, date):
        super().__init__()
        self.date = date
        self.buckets = []
        for i in range(0, len(tickers), self.REQ_PER_MINUTE):
            self.buckets.append(tickers[i:i + self.REQ_PER_MINUTE])

    def _extract(self):
        for bucket in self.buckets:
            print("Waiting for 60 seconds to respect rate limits...")
            time.sleep(60)  # Wait for 60 seconds before the next batch
            for ticker in bucket:
                print(f"Fetching data for ticker: {ticker}")
                extractor = Pipeline(
                    PolygonTickerExtractor(ticker, self.date),
                    PolygonTickerTransformer(),
                    TickerDbDispatcher(config['DB_PATH'], "TickerData")
                )
                extractor.start()
