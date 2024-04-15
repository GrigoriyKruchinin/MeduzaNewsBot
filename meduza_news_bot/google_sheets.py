import json
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Количество строк записей, после которых будет выполнена задержка
WRITE_BATCH_SIZE = 26
# Время задержки в секундах
DELAY_SECONDS = 60


def authenticate(credentials_file, scope=None):
    """
    Аутентифицирует сервисный аккаунт и возвращает объект клиента
    для взаимодействия с Google Sheets API.

    Args:
        credentials_file (str): Путь к файлу с учетными данными для аутентификации.
        scope (list, optional): Список разрешений OAuth 2.0.

    Returns:
        gspread.client.Client: Объект клиента для взаимодействия с Google Sheets API.
    """
    if scope is None:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
    # Загрузить credentials.json
    with open(credentials_file) as f:
        credentials = json.load(f)
    # Аутентифицировать сервисный аккаунт
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    return gspread.authorize(creds)


def open_worksheet(client, sheet_name):
    """
    Открывает Google Таблицу по названию. Записывает заголовки для колонок.

    Args:
        client (gspread.client.Client): Объект клиента для взаимодействия с Google API.
        sheet_name (str): Название листа Google Таблицы.
    Returns:
        gspread.models.Worksheet: Объект листа Google Таблицы.
    """
    # Открыть Google Таблицу по названию
    sheet = client.open(sheet_name)

    # Получить объект листа
    worksheet = sheet.get_worksheet(0)  # 0 для первого листа

    # Если таблица пустая, записать заголовки для колонок
    if not worksheet.col_values(1):
        worksheet.update_cell(1, 1, "Время занесения")
        worksheet.update_cell(1, 2, "Заголовок")
    return worksheet


def write_data_to_worksheet(worksheet, data):
    """
    Записывает данные в Google Таблицу.

    Args:
        worksheet: Объект листа Google Таблицы, в который будут записываться данные.
        data: Список данных, которые будут записаны в таблицу.
    """
    # Начать запись данных со следующей строки
    next_row = len(worksheet.col_values(1)) + 1

    for i, value in enumerate(data):
        # Записать дату и время в первую ячейку новой строки
        worksheet.update_cell(next_row, 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # Записать заголовок новости в отдельную ячейку
        worksheet.update_cell(next_row, 2, value)
        next_row += 1  # Увеличение номера строки для следующей записи

        # Если достигнуто количество записей для задержки
        if (i + 1) % WRITE_BATCH_SIZE == 0:
            # Задержка перед следующей итерацией
            print(
                "Достигнута квота на количество записей. Через минуту квота обновится."
            )
            time.sleep(DELAY_SECONDS)


def write_to_google_sheet(data, sheet_name, credentials_file):
    """
    Аутентифицирует сервисный аккаунт, открывает Google Таблицу
    и записывает в нее данные.

    Args:
        data: Список данных, которые будут записаны в таблицу.
        sheet_name: Название листа Google Таблицы, куда будут записываться данные.
        credentials_file: Путь к файлу с учетными данными для аутентификации.
    """
    client = authenticate(credentials_file)
    worksheet = open_worksheet(client, sheet_name)
    write_data_to_worksheet(worksheet, data)
