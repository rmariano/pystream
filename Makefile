.PHONY: test lint format install build publish

RUN:=poetry run

test: lint
	$(RUN) pytest src/tests

lint:
	$(RUN) ruff check src/
	$(RUN) pyright src/

format:
	$(RUN) ruff check --fix src/

install:
	poetry install

build:
	poetry build

publish:
	poetry publish
