import pandas as pd

from base.transform.Transformer import Transformer


class PolygonClosePriceTransformer(Transformer):
    def __init__(self, date):
        super().__init__()
        self.date = date

    def _transform(self, data):
        df = pd.DataFrame(data)

        # change column names to match database schema
        df.rename(columns={'T': 'ticker', 'c': 'price'}, inplace=True)
        df = df[['ticker', 'price']]
        df['date'] = self.date

        print(df)

        return df