# Created Date: Tuesday, June 29th 2021, 10:00:00 pm
# Targets
.PHONY: build up down test clean

build:
	docker-compose build --pull

up:
	docker-compose up --build

down:
	docker-compose down


test:
	pip3 install -r requirements.txt
	python3 -m pytest -v

app:
	pip3 install -r requirements.txt
	python3 -m streamlit run ui/streamlit_app.py

clean:
	docker-compose rm -f

