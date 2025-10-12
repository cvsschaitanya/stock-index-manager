from abc import ABC, abstractmethod

class Listener(ABC):
    @abstractmethod
    def observe(self, df):
        pass

