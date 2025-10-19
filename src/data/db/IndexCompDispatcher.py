from data.db.DatabaseDispatcher import DatabaseDispatcher


class IndexCompDispatcher(DatabaseDispatcher):
    def __init__(self, db_path):
        super().__init__(db_path, "IndexComposition")

    def create_table_query(self):
        return f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            ticker TEXT,
            date TEXT,
            share100 REAL,
            PRIMARY KEY (ticker, date)
        )
        """

    def conflict_key(self):
        return "ticker,date"