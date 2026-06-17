generate:
	uv run python -m nodebpy.assets
	uv run python -m gen
	make format

test:
	uv run pytest -n 4

format:
	uv run ruff format
	uv run ruff check --fix
	uv run ty check --fix src
	uv run ruff format

docs:
	cd docs
	uv run quartodoc build
	uv run quartodoc interlinks
	uv run quarto render
