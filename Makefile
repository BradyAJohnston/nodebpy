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
	cd docs && uv run quartodoc build
	cd docs && uv run quartodoc interlinks
	cd docs && uv run quarto render

# List upstream node-arrange commits not yet ported into the vendored copy
# (see src/nodebpy/lib/nodearrange/VENDORED.md).
vendor-check:
	@rev=$$(sed -n 's/.*Last sync:\*\* upstream commit `\([0-9a-f]*\)`.*/\1/p' src/nodebpy/lib/nodearrange/VENDORED.md); \
	tmp=$$(mktemp -d); \
	git clone --quiet --filter=blob:none https://github.com/Leonardo-Pike-Excell/node-arrange $$tmp; \
	git -C $$tmp log --oneline $$rev..HEAD -- source/arrange source/config.py source/utils.py \
		&& echo "(no output above = vendored copy is up to date with upstream)"; \
	rm -rf $$tmp
