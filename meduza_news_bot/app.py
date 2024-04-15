import os
import telebot

from meduza_news_bot.html_parser import get_news_headlines
from meduza_news_bot.utils import STICKER_DOG, handle_error
from meduza_news_bot.db import filter_and_save_new_headlines
from meduza_news_bot.google_sheets import write_to_google_sheet

from dotenv import load_dotenv

# Распаковка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE")
SHEET_NAME = os.getenv("SHEET_NAME")

# Настройки парсинга данных
URL = "https://meduza.io/"
DEFAULT_TAG = "h2"
DEFAULT_CLASS = "BlockTitle-module-root"

# Создание экземпляра бота
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    """
    Отправляет приветственное сообщение при запуске бота.

    Args:
        message: Сообщение от пользователя, содержащее команду /start.
    """
    bot.reply_to(
        message,
        f"Привет! Я бот для сбора заголовков новостей c сайта {URL} "
        "и записи их в Google таблицу.",
    )
    bot.send_message(
        message.chat.id,
        "Обратите внимание, что в Google Sheets есть ограничение на "
        "количество записей в минуту. Поэтому процесс записи может занять "
        "некоторое время, особенно если на сайте много новостей 🫣",
    )
    bot.send_message(
        message.chat.id,
        "Введите /news чтобы записать заголовки в вашу таблицу.",
    )


@bot.message_handler(commands=["news"])
def collect_and_write_headlines_to_sheets(message):
    """
    Собирает заголовки новостей при получении команды /news и записывает
    их в Google Sheets

    Args:
        message: Сообщение от пользователя, содержащее команду /news.
    """
    # Отправка сообщения о начале процесса
    bot.reply_to(message, f"Начинаю сбор заголовков новостей...")
    bot.send_message(message.chat.id, "Мне может потребоваться несколько минут...")
    try:
        # Получение заголовков новостей
        news_headlines = get_news_headlines(URL, DEFAULT_TAG, DEFAULT_CLASS)

        # Фильтрация новых заголовков и сохранение в базу данных
        new_headlines = filter_and_save_new_headlines(news_headlines)

        if new_headlines:
            # Запись новых заголовков в таблицу
            write_to_google_sheet(new_headlines, SHEET_NAME, CREDENTIALS_FILE)
            # Отправка сообщения об успешном добавлении
            bot.send_message(
                message.chat.id,
                "Новые заголовки новостей успешно записаны в Google таблицу.",
            )
            bot.send_sticker(message.chat.id, STICKER_DOG)
        else:
            bot.send_message(
                message.chat.id, "Новых заголовков новостей не обнаружено 🙄"
            )

    except Exception as e:
        # Обработка ошибок
        handle_error(bot, message, e)


@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    """
    Обрабатывает все остальные текстовые сообщения и отправляет пользователю инструкции.

    Args:
        message: Сообщение от пользователя, не содержащее команды /start или /news.
    """
    bot.reply_to(
        message,
        "Пока я умею обрабатывать только сообщения: /start и /news.",
    )
    bot.send_message(
        message.chat.id,
        "Воспользуйтесь одной из вышеуказанных команд 😉",
    )


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
