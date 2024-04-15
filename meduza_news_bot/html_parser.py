import requests
from bs4 import BeautifulSoup

from meduza_news_bot.utils import ParsingError, sanitize_string


# Заголовки для имитации запроса от браузера
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
}


def get_news_headlines(url, tag, class_):
    """
    Получает заголовки новостей с указанного URL.

    Args:
        url (str): URL, с которого будут получены заголовки новостей.
        tag (str): Тег HTML, который содержит заголовки новостей.
        class_ (str): Класс HTML элементов, содержащих заголовки новостей.

    Returns:
        list: Список заголовков новостей.

    Raises:
        ParsingError: Ошибка при парсинге данных.
    """
    try:
        # Отправить GET запрос к указанному URL
        response = requests.get(url, headers=HEADERS)

        # Проверить, успешно ли был выполнен запрос
        if response.status_code == 200:
            # Создать объект BeautifulSoup для парсинга HTML
            soup = BeautifulSoup(response.text, "lxml")

            # Нахождение всех элементов с указанным тегом и классом
            headlines = soup.find_all(tag, class_)

            # Извлечь текст заголовков, очистить их и добавить в список
            news_headlines = [sanitize_string(headline.text) for headline in headlines]

            return news_headlines
    except Exception as e:
        raise ParsingError(f"Ошибка при парсинге данных: {str(e)}")
