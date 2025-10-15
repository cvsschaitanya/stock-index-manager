import time

from base.extract.Extractor import Extractor


class RateLimitedExtractor(Extractor):

    def __init__(self, iterable, extractor_supplier, req_per_minute=5):
        super().__init__()
        self.req_per_minute = req_per_minute
        self.extractor_supplier = extractor_supplier
        self.buckets = []
        for i in range(0, len(iterable), self.req_per_minute):
            self.buckets.append(iterable[i:i + self.req_per_minute])

    def _extract(self):
        for bucket in self.buckets:
            print("Waiting for 60 seconds to respect rate limits...")
            time.sleep(60)  # Wait for 60 seconds before the next batch
            for element in bucket:
                print(f"Extracting data for element: {element}")
                extractor = self.extractor_supplier(element)
                extractor.start()
