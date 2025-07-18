.PHONY: build dev install install-dev

build:
	alembic upgrade head  # Run database migrations

dev:
	uvicorn main:app --reload  # Start FastAPI with auto-reload

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

.PHONY: format lint check

format:
	black .
	isort .

lint:
	flake8 . --count

check:
	pre-commit run --all-files

.PHONY: test coverage

test:
	pytest

coverage:
	pytest --cov=app --cov-report=term --cov-report=html

.PHONY: clean tags bump

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .pytest_cache .mypy_cache dist

tags:
	git tag -l

bump:
	bumpversion patch  # or minor / major

.PHONY: ci

ci: install-dev format lint test
