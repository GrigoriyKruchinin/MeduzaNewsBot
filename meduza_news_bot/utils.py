import sqlite3
import gspread


STICKER_DOG = "CAACAgIAAxkBAAELIitlnrqebILw4fRZ1TxmDvhm6SFo6AACfwEAAj0N6AS98XKpqDIlKDQE"


def sanitize_string(string):
    """
    Очищает строку от лишних пробелов и символов.

    Args:
        text (str): Строка для очистки.

    Returns:
        str: Очищенная строка.
    """
    return string.strip().replace("\xa0", " ")


class ParsingError(Exception):
    """
    Исключение, возникающее при ошибке парсинга данных.
    """

    pass


def handle_error(bot, message, e):
    """
    Обработка ошибок.

    Args:
        bot: Экземпляр бота.
        message: Сообщение для отправки пользователю.
        e: Объект ошибки.
    """
    if isinstance(e, sqlite3.Error):
        # Ошибка SQLite
        bot.send_message(
            message.chat.id, "Произошла ошибка при работе с базой данных SQLite."
        )
    elif isinstance(e, gspread.exceptions.APIError) and e.response.status_code == 429:
        # Ошибка квоты Google Таблиц
        bot.send_message(
            message.chat.id,
            "Квота на запись информации в Google Таблицу исчерпана. \n"
            "Подождите пару минут и повторите попытку.",
        )
    elif isinstance(e, ParsingError):
        # Ошибка парсинга данных
        bot.send_message(message.chat.id, str(e))
    else:
        # Отправка сообщения о другой ошибке
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
