from abc import abstractmethod

from base.observe.Listener import Listener


class Dispatcher(Listener):

    def observe(self, df):
        self._dispatch(df)

    @abstractmethod
    def _dispatch(self, df):
        pass