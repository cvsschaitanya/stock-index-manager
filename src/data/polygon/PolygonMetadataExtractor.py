import pandas as pd
from polygon import ReferenceClient

from data.polygon.PolygonApiExtractor import PolygonApiExtractor


class PolygonMetadataExtractor(PolygonApiExtractor):

    def __init__(self, count=1000):
        super().__init__()
        self.client = ReferenceClient(self.polygon_api_key)
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

        return response["results"]
