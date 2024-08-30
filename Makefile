.PHONY: test lint format install build publish clean

RUN:=poetry run

test: lint
	$(RUN) pytest --cov=pystream_collections --cov-report=xml tests

clean:
	rm -fr dist/
	find . -type d -name __pycache__ | xargs rm -fr {}

lint:
	$(RUN) ruff check src/ tests/
	$(RUN) pyright src/ tests/

format:
	$(RUN) ruff check --fix src/ tests/

install:
	poetry install

build:
	poetry build

publish:
	poetry publish
