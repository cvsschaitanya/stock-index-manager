from numpy.f2py.auxfuncs import throw_error


class RawDataExtractor:
    def fetch_stocks(self):
        throw_error("Subclasses should implement this method!")