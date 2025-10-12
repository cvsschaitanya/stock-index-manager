from numpy.f2py.auxfuncs import throw_error


class RawDataExtractor:
    def fetch_stocks(self):
        raise Exception("Subclasses should implement this method!")