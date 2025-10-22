install:
	uv sync

test:
	uv run pytest -v tests/

run:
	uv run uvicorn app.main:app --reload


lint:
	uv run ruff check .

format:
	uv run ruff format .
