import pandas as pd

from base.transform.Transformer import Transformer


class PolygonStocksTransformer(Transformer):
    def __init__(self, count=None):
        super().__init__()
        self.count = count

    def _transform(self, data):
        df = pd.DataFrame(data)

        df = df[df['locale'] == 'us']
        df = df[df['type'] == 'CS']

        df = df[['ticker', 'name', 'primary_exchange']]

        # change column names to match database schema
        df = df.rename(columns={'primary_exchange': 'exchange'})

        if self.count:
            df = df.head(self.count)

        return df