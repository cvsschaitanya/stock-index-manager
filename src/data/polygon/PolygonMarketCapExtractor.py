from polygon import ReferenceClient

from data.polygon.PolygonApiExtractor import PolygonApiExtractor


class PolygonMarketCapExtractor(PolygonApiExtractor):
    def __init__(self, ticker, date):
        super().__init__()
        self.client = ReferenceClient(self.polygon_api_key)
        self.date = date
        self.ticker = ticker

    def _extract(self):
        print(self.ticker)
        response = self.client.get_ticker_details(self.ticker, self.date)
        print(response)

        ticker_data = response["results"]
        ticker_data["date"] = self.date
        return ticker_data


