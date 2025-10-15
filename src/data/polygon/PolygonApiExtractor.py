from base.extract.Extractor import Extractor
from config import config


class PolygonApiExtractor(Extractor):
    def __init__(self):
        super().__init__()
        self.polygon_api_key = config["POLYGON_API_KEY"]
