import sqlite3

from dispatch.Dispatcher import Dispatcher


class DatabaseDispatcher(Dispatcher):
    def __init__(self, sqlite_db_filename, db, table):
        # Create sqlite connection from file name
        self.conn = sqlite3.connect(sqlite_db_filename)

        self.db = db
        self.table = table

    def _dispatch(self, df):
        self.create_table_if_not_exists()

        columns = [col.lower() for col in df.columns]

        query = f" INSERT INTO {self.table}"
        query += f" VALUES ({','.join('?' * len(columns))})"
        query += " ON CONFLICT DO UPDATE SET"
        query += " ,".join([
            f" {col}=excluded.{col}" for col in columns
        ])

        for row in df.itertuples(index=False, name=None):
            with self.conn:
                self.conn.execute(query, row)

    def create_table_if_not_exists(self):
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            symbol TEXT PRIMARY KEY,
            name TEXT,
            exchange TEXT,
            assetType TEXT,
            ipoDate TEXT,
            delistingDate TEXT,
            status TEXT
        );
        """
        with self.conn:
            self.conn.execute(create_table_query)
