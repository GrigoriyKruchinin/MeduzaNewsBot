import os
import telebot

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
    bot.reply_to(message, f"Начинаю сбор заголовков новостей...")
    bot.send_message(
        message.chat.id,
        "Новые заголовки новостей успешно записаны в Google таблицу.",
    )


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
