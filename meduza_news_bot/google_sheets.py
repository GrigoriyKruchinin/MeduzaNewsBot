import json
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Количество строк записей, после которых будет выполнена задержка
WRITE_BATCH_SIZE = 28
# Время задержки в секундах
DELAY_SECONDS = 60


def authenticate(credentials_file, scope=None):
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
    # Открыть Google Таблицу по названию
    sheet = client.open(sheet_name)

    # Получить объект листа
    worksheet = sheet.get_worksheet(0)  # 0 для первого листа

    # Если таблица пустая, записать заголовки
    if not worksheet.col_values(1):
        # Записать структуру данных
        worksheet.update_cell(1, 1, "Время занесения")
        worksheet.update_cell(1, 2, "Заголовок")
    return worksheet


def write_data_to_worksheet(worksheet, data):
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
    client = authenticate(credentials_file)
    worksheet = open_worksheet(client, sheet_name)
    write_data_to_worksheet(worksheet, data)
