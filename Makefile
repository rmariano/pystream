.PHONY: test lint clean format install build publish release new-version

RUN:=poetry run
VERSION:=$(shell poetry version --short)
NEW_VERSION_TYPE:=patch

test: lint
	$(RUN) pytest --cov=pystream_collections --cov-report=xml --cov-report=term-missing tests

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

new-version:
	./scripts/new-version.sh $(NEW_VERSION_TYPE)
