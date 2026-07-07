# PGF developer targets. Commands mirror AGENTS.md "Build and test commands".
.PHONY: setup check test

# Create the virtualenv and install the package with dev extras.
setup:
	python3.12 -m venv .venv && . .venv/bin/activate && python -m pip install -e ".[dev]"

# Run all checks, in the order AGENTS.md specifies. Validation is offline.
check:
	ruff check .
	pytest
	python -m pgf check examples/association-board-brief
	python -m pgf materialize examples/association-board-brief

# Run the test suite only.
test:
	pytest
