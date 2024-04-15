import sqlite3


class DatabaseConnection:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.commit()
            self.conn.close()


def create_headlines_table():
    with DatabaseConnection("news.db") as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS headlines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE
            )
        """
        )


if __name__ == "__main__":
    create_headlines_table()
