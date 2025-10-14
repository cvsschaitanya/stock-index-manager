from base.observe.Listener import Listener


class LambdaListener(Listener):
    def __init__(self, fn):
        self.fn = fn
    def observe(self, df):
        self.fn(df)
