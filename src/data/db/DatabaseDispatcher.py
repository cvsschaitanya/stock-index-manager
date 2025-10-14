import sqlite3
from abc import abstractmethod

from base.dispatch.Dispatcher import Dispatcher


class DatabaseDispatcher(Dispatcher):
    def __init__(self, sqlite_db_filename, table):
        # Create sqlite connection from file name
        self.conn = sqlite3.connect(sqlite_db_filename)

        self.table = table

    def _dispatch(self, df):
        self.create_table_if_not_exists()

        columns = [col.lower() for col in df.columns]
        placeholders = ",".join(["?"] * len(columns))
        col_names = ",".join(columns)

        query = (
                f"INSERT INTO {self.table} ({col_names}) "
                f"VALUES ({placeholders}) "
                f"ON CONFLICT({self.conflict_key()}) DO UPDATE SET "
                + ", ".join(f"{col}=excluded.{col}" for col in columns)
        )

        for row in df.itertuples(index=False, name=None):
            with self.conn:
                self.conn.execute(query, row)

    def create_table_if_not_exists(self):
        with self.conn:
            self.conn.execute(self.create_table_query())

    @abstractmethod
    def create_table_query(self):
        pass

    @abstractmethod
    def conflict_key(self):
        pass
