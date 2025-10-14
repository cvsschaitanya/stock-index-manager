from base.extract.Extractor import Extractor
from polygon.reference_apis import ReferenceClient

from config import config


class PolygonApiExtractor(Extractor):
    def __init__(self):
        super().__init__()
        self.client = ReferenceClient(config["POLYGON_API_KEY"])
