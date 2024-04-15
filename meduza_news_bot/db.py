import sqlite3


class DatabaseConnection:
    """
    Класс для управления подключением к базе данных SQLite.

    Attributes:
        db_name (str): Имя файла базы данных.
        conn (Connection): Объект подключения к базе данных.
        cursor (Cursor): Объект курсора для выполнения SQL-запросов.
    """

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
    """
    Создание таблицы для хранения заголовков новостей, если ее еще нет.
    """
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
    """
    Фильтрация новых заголовков и сохранение в базу данных.

    Args:
        news_headlines: Список заголовков новостей.

    Returns:
        new_headlines: Список новых заголовков, которые были добавлены в базу данных.
    """
    new_headlines = []
    with DatabaseConnection("news.db") as cursor:
        for headline in news_headlines:
            # Вставка нового заголовка, игнорируя дубликаты
            cursor.execute(
                """
                INSERT OR IGNORE INTO headlines (title) VALUES (?)
            """,
                (headline,),
            )
            # Проверка, была ли вставлена новая запись
            if cursor.rowcount > 0:
                # Если да, добавляем заголовок в список новых заголовков
                new_headlines.append(headline)
    return new_headlines


if __name__ == "__main__":
    create_headlines_table()
