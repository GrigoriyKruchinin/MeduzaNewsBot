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


def filter_and_save_new_headlines(news_headlines):
    new_headlines = []
    with DatabaseConnection("news.db") as cursor:
        for headline in news_headlines:
            cursor.execute(
                """
                INSERT OR IGNORE INTO headlines (title) VALUES (?)
            """,
                (headline,),
            )
            if cursor.rowcount > 0:
                new_headlines.append(headline)
    return new_headlines


if __name__ == "__main__":
    create_headlines_table()
