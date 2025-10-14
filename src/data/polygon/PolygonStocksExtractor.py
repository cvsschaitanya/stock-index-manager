import pandas as pd

from data.polygon.PolygonApiExtractor import PolygonApiExtractor


class PolygonStocksExtractor(PolygonApiExtractor):

    def __init__(self, count=1000):
        super().__init__()
        self.count = count

    def _extract(self):
        response = self.client.get_tickers(
            market="stocks",
            active="true",
            limit=self.count,
            verbose=True,
            sort="ticker",
        )

        # print(response)

        # TODO: handle validation

        df = pd.DataFrame(response["results"])

        return df
