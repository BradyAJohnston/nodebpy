generate:
	 uv run generate.py && uv run ruff format && uv run ruff check --fix && uv run ty check --fix src && uv run ruff format

test:
	uv run pytest -n 4

docs:
	cd docs && uv run quartodoc build && uv run quartodoc interlinks && uv run quarto render
