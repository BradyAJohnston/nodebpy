generate:
	uv run python -m gen
	make format

# Refresh the repository-root copy of the agent skill from the package source.
.PHONY: skills
skills:
	rm -rf skills/nodebpy
	mkdir -p skills
	cp -r src/nodebpy/skills/nodebpy skills/nodebpy

# Regenerate the socket draw-order table from Blender's node declarations
# (network: sparse-clones the tag matching the installed bpy).
socket-order:
	uv run python -m gen.socket_order
	uv run ruff format src/nodebpy/builder/_socket_order.py

test:
	uv run pytest -n 4

# Type-check the built wheel as a consumer with every major type checker.
typecheck:
	./tests/typing/run.sh

format:
	uv run ruff format
	uv run ruff check --fix
	uv run ty check --fix src
	uv run ruff format

docs:
	cd docs && uv run quartodoc build
	cd docs && uv run quartodoc interlinks
	cd docs && uv run quarto render

# Arrange a corpus of trees and print layout-quality metrics; see
# tests/layout/report.py for comparing runs and drawing the trees.
layout-report:
	uv run python -m tests.layout.report --essentials

# Recompute the layouts stored in tests/layout/corpus/ after a deliberate
# change to the layout; it prints what changed in each layout's counts.
layout-corpus:
	uv run python -m tests.layout.corpus --update
