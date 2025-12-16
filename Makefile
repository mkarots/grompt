.PHONY: install test lint format clean build publish-test publish

install:
	pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=grompt --cov-report=term-missing

lint:
	ruff check .
	mypy grompt

format:
	black .
	ruff check --fix .

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

build: clean
	python -m build

publish-test: build
	python -m twine upload --repository testpypi dist/*

publish: build
	python -m twine upload dist/*

