from data.db.DatabaseDispatcher import DatabaseDispatcher


class MetadataDbDispatcher(DatabaseDispatcher):
    def __init__(self, db_path):
        super().__init__(db_path, "Metadata")

    def create_table_query(self):
        return f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            ticker TEXT PRIMARY KEY,
            name TEXT,
            exchange TEXT
        );
        """

    def conflict_key(self):
        return "ticker"
