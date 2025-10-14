import pandas as pd

from base.transform.Transformer import Transformer


class PolygonTickerTransformer(Transformer):
    def _transform(self, df):
        df = pd.DataFrame([df])
        df = df[['ticker', 'date', 'market_cap']]
        print(df)
        return df