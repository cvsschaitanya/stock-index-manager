import pandas as pd
import os
import requests
from io import StringIO

from extract.RawDataExtractor import RawDataExtractor


class AlphaVantageExtractor(RawDataExtractor):
    def fetch_stocks(self):
        alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        url = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={alpha_vantage_api_key}"
        # make request
        response = requests.get(url)
        print(response.text)
        df = pd.read_csv(StringIO(response.text))
        return df