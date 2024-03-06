# Created Date: Tuesday, June 29th 2021, 10:00:00 pm
# Targets
.PHONY: build run stop clean

build:
	docker-compose build --pull

up:
	docker-compose up --build

down:
	docker-compose down


test:
	pip3 install -r requirements.txt
	python3 -m pytest -v

clean:
	docker-compose rm -f

