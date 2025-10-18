import time

from base.extract.Extractor import Extractor


class RateLimitedExtractor(Extractor):

    def __init__(self, iterable, extractor_supplier, req_per_minute=5, safe=False):
        super().__init__()
        self.safe = safe
        self.req_per_minute = req_per_minute
        self.extractor_supplier = extractor_supplier
        self.buckets = []
        for i in range(0, len(iterable), self.req_per_minute):
            self.buckets.append(iterable[i:i + self.req_per_minute])

    def _extract(self):
        if self.safe:
            print("Waiting for 60 seconds to respect rate limits...")
            time.sleep(60)  # Wait for 60 seconds to account for any prev requests

        for bucket in self.buckets:
            for element in bucket:
                print(f"Extracting data for element: {element}")
                extractor = self.extractor_supplier(element)
                extractor.start()
            print("Waiting for 60 seconds to respect rate limits...")
            time.sleep(60)  # Wait for 60 seconds before the next batch
