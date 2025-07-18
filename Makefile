VENV = env
PIP = $(VENV)/bin/pip

.PHONY: build dev install install-dev format lint test clean ci

build:
	$(VENV)/bin/alembic upgrade head

dev:
	$(VENV)/bin/uvicorn main:app --reload

install:
	$(PIP) install -r requirements.txt

install-dev:
	$(PIP) install -r requirements.txt -r requirements-dev.txt

format:
	$(VENV)/bin/black .
	$(VENV)/bin/isort .

lint:
	$(VENV)/bin/flake8 . --count

test:
	$(VENV)/bin/pytest

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .pytest_cache .mypy_cache dist htmlcov

ci: install-dev format lint test
