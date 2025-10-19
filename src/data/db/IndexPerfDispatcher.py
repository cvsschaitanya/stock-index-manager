from data.db.DatabaseDispatcher import DatabaseDispatcher


class IndexPerfDispatcher(DatabaseDispatcher):
    def __init__(self, db_path):
        super().__init__(db_path, "IndexPerformance")

    def create_table_query(self):
        return f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            date TEXT,
            value REAL,
            PRIMARY KEY (date)
        )
        """

    def conflict_key(self):
        return "date"
