import sqlite3

from base.extract.Extractor import Extractor


class DatabaseExtractor(Extractor):
    def __init__(self, sqlite_db_filename, query):
        super().__init__()
        self.conn = sqlite3.connect(sqlite_db_filename)
        self.query = query

    def _extract(self):
        rows = []
        with self.conn:
            rows = self.conn.execute(self.query).fetchall()

        return rows