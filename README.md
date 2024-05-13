# Meduza News Bot

Этот проект представляет собой Telegram бота, который позволяет получать заголовки новостей с сайта meduza.io и записывать их в Google Sheets.

***

## Предупреждение о безопасности

В целях сохранения безопасности, файлы .env и credentials.json не должны находиться в репозитории. Однако, в данном проекте это условие сознательно проигнорировано, чтобы облегчить его запуск.

***


## Запуск проекта

Для запуска проекта выполните следующие шаги:

1. Склонируйте репозиторий на локальную машину:

```
git clone https://github.com/GrigoriyKruchinin/MeduzaNewsBot.git
```

2. Перейдите в каталог проекта:

```
cd MeduzaNewsBot
```

3. Создайте виртуальное окружение и установите зависимостей с помощью Poetry (если установлен Poetry):

```
# Создание и активация виртуального окружения с помощью Poetry
poetry shell

# Установка зависимостей с использованием Poetry
poetry install
```

или используйте Pip:

```
# Создание виртуального окружения
python3 -m venv .venv

# Активация виртуального окружения
source .venv/bin/activate

# Установка зависимостей из файла requirements.txt
pip install -r requirements.txt
```

4. Укажите путь до интерпретатора Python из виртуального окружения в настройках вашего IDE.

5. Запустите проект с помощью команды make start:
```
make start
```

6. Проверьте работоспособности бота, используя следующие ссылки:

- [Google Sheets](https://docs.google.com/spreadsheets/d/1hxaZ_sDSovhidfzjrQ-Zejpfr--jY6pLTeHsxX2h3Kk/edit?usp=sharing)


- [Meduza News Bot](https://t.me/MeduzaNewBot)


***
## Контакты
- Автор: Grigoriy Kruchinin
- [GitHub](https://github.com/GrigoriyKruchinin)
- [Email](gkruchinin75@gmail.com)
- [LinkedIn](https://www.linkedin.com/in/grigoriy-kruchinin/)
***
