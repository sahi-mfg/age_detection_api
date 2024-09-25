install:
	pipenv install --dev

test:
	pipenv run pytest --cov=app --cov-report=term-missing -v

run:
	pipenv run uvicorn app.main:app --reload

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

lint:
	pipenv run ruff check .

format:
	pipenv run ruff format .

.PHONY: all
all: clean install lint test docs
