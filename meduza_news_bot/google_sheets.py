import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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
