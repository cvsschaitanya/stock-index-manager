from abc import abstractmethod

from base.observe.Listener import Listener
from base.observe.Provider import Provider


class Transformer(Listener, Provider):

    def observe(self, df):
        transformed_df = self._transform(df)
        self._provide(transformed_df)

    @abstractmethod
    def _transform(self, df):
        pass