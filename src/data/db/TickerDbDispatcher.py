from data.db.DatabaseDispatcher import DatabaseDispatcher


class TickerDbDispatcher(DatabaseDispatcher):
    def __init__(self, db_path):
        super().__init__(db_path, "TickerData")

    def create_table_query(self):
        return f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            ticker TEXT,
            market_cap REAL,
            price REAL,
            date TEXT DEFAULT (date('now')),
            PRIMARY KEY (ticker, date)
        );
        """

    def conflict_key(self):
        return "ticker,date"
