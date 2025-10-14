from base.observe.Listener import Listener


class IterableListener(Listener):
    def __init__(self, sub_listener):
        self.sub_listener = sub_listener

    def observe(self, iterable):
        for elem in iterable:
            self.sub_listener.observe(elem)