install:
	uv sync

test:
	uv run pytest -v tests/

run:
	uv run uvicorn app.main:app --reload

run-prod:
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

lint:
	uv run ruff check .

format:
	uv run ruff format .
