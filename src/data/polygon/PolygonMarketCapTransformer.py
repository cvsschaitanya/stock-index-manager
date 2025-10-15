import pandas as pd

from base.transform.Transformer import Transformer


class PolygonMarketCapTransformer(Transformer):
    def _transform(self, data):
        df = pd.DataFrame([data])
        df = df[['ticker', 'date', 'market_cap']]
        print(df)
        return df