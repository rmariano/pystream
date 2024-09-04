.PHONY: test lint clean format install build publish release

RUN:=poetry run
VERSION:=$(shell poetry version --short)

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

release:
	@echo "Releasing $(VERSION)"
	gh release create $(VERSION) --generate-notes
