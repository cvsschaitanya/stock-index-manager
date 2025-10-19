from polygon import StocksClient

from data.polygon.PolygonApiExtractor import PolygonApiExtractor


class PolygonClosePriceExtractor(PolygonApiExtractor):
    def __init__(self, date):
        super().__init__()
        self.client = StocksClient(self.polygon_api_key)
        self.date = date

    def _extract(self):
        response = self.client.get_grouped_daily_bars(self.date)

        print(response)
        price_data = response["results"]

        print(price_data[:5])

        return price_data

