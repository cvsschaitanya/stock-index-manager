from data.polygon.PolygonApiExtractor import PolygonApiExtractor


class PolygonTickerExtractor(PolygonApiExtractor):
    def __init__(self, ticker, date):
        super().__init__()
        self.date = date
        self.ticker = ticker

    def _extract(self):
        print(self.ticker)
        response = self.client.get_ticker_details(self.ticker, self.date)
        ticker_data = response["results"]
        ticker_data["date"] = self.date
        return ticker_data


