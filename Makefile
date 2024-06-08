.PHONY: test lint format install build publish clean

RUN:=poetry run

test: lint
	$(RUN) pytest --cov=pystream_collections src/tests

clean:
	rm -fr dist/

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
