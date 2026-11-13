.PHONY: all clean pytest coverage ruff format mypy

# Run all the checks which do not change files
all: ruff pytest

# Run the unit tests using `pytest`
pytest:
	poetry run pytest src tests

# Lint the code using `ruff`
ruff:
	poetry run ruff check src tests

# Automatically format the code using `ruff`
format:
	poetry run ruff format src tests
