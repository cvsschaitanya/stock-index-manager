from base.extract.Extractor import Extractor


class Pipeline(Extractor):
    def _extract(self):
        pass

    def __init__(self, *pipes):
        super().__init__()
        self.pipes = pipes
        for i in range(len(self.pipes) - 1):
            self.pipes[i].add_listener(self.pipes[i + 1])

    def start(self):
        if self.pipes:
            self.pipes[0].start()