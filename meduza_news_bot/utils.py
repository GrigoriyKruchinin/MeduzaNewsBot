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
