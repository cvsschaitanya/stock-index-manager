from config import config
from data.db.MetadataDbDispatcher import MetadataDbDispatcher
from data.polygon.PolygonMetadataExtractor import PolygonMetadataExtractor
from data.polygon.PolygonStocksTransformer import PolygonStocksTransformer


def ingest_stock_metadata(count=1000):
    extractor = PolygonMetadataExtractor()
    transformer = PolygonStocksTransformer(count=count)
    stock_dispatcher = MetadataDbDispatcher(config['DB_PATH'])

    extractor.add_listener(transformer)
    transformer.add_listener(stock_dispatcher)

    extractor.start()
