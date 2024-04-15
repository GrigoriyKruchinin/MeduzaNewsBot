.PHONY: start

start:
	python meduza_news_bot/db.py && python meduza_news_bot/app.py

export_dep:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
