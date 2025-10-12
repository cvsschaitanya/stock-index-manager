from abc import abstractmethod, ABC

from observe.Provider import Provider


class Extractor(ABC, Provider):

    def start(self):
        df = self._extract()
        self._notify(df)

    @abstractmethod
    def _extract(self):
        raise Exception("Subclasses should implement this method!")