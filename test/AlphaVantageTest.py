import unittest
from unittest.mock import mock_open, MagicMock

import numpy as np
import pandas as pd

from ingest.alphaVantage.AlphaVantageExtractor import AlphaVantageExtractor


class MyTestCase(unittest.TestCase):

    @unittest.mock.patch('ingest.alphaVantage.AlphaVantageExtractor.requests.get')
    def test_fetch_stocks(self, mock_get):

        # mock the API call to return a sample dataframe
        fake_data = """symbol,name,exchange,assetType,ipoDate,delistingDate,status
AAPL,Apple Inc,NASDAQ,Stock,1980-12-12,,Active
"""
        fake_response = MagicMock()
        fake_response.text = fake_data
        mock_get.return_value = fake_response

        data_source = AlphaVantageExtractor()
        df = data_source.fetch_stocks()

        pd.testing.assert_frame_equal(df, pd.DataFrame({
            'symbol': ['AAPL'],
            'name': ['Apple Inc'],
            'exchange': ['NASDAQ'],
            'assetType': ['Stock'],
            'ipoDate': ['1980-12-12'],
            'delistingDate': [np.nan],
            'status': ['Active']
        }))


if __name__ == '__main__':
    unittest.main()
