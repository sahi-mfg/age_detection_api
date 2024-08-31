# Created Date: Tuesday, June 29th 2021, 10:00:00 pm
# Targets
.PHONY: build up down test clean

build:
	docker-compose build --pull

up:
	docker-compose up --build

down:
	docker-compose down

restart: down up


test:
	docker-compose run --rm test

streamlit:
	docker-compose run --rm app poetry run streamlit run ui/streamlit_app.py

clean:
	docker-compose rm -f
