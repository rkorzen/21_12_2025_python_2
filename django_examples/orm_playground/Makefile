PYTHON ?= python3
UV ?= uv

.PHONY: init migrate makemigrations seed run test lint format check

init:
	$(UV) sync --extra dev --extra postgres

migrate:
	$(UV) run $(PYTHON) manage.py migrate

makemigrations:
	$(UV) run $(PYTHON) manage.py makemigrations

seed:
	$(UV) run $(PYTHON) manage.py seed --seed 123 --reset

run:
	$(UV) run $(PYTHON) manage.py runserver

test:
	$(UV) run pytest

lint:
	$(UV) run ruff check .
	$(UV) run black --check .

format:
	$(UV) run ruff check . --fix
	$(UV) run black .

check: lint test
