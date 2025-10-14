class Provider:
    def __init__(self):
        self.observers = []

    def add_listener(self, observer):
        self.observers.append(observer)

    def _provide(self, df):
        for observer in self.observers:
            observer.observe(df)