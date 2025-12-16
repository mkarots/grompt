.PHONY: install test test-cov test-cov-xml lint format clean build publish-test publish

install:
	@if [ -n "$$CI" ]; then \
		uv pip install --system -e ".[dev]"; \
	else \
		if [ -z "$$VIRTUAL_ENV" ] && [ ! -d ".venv" ]; then \
			echo "Creating virtual environment..."; \
			uv venv; \
		fi; \
		uv pip install -e ".[dev]"; \
	fi

test:
	pytest

test-cov:
	pytest --cov=grompt --cov-report=term-missing

test-cov-xml:
	pytest --cov=grompt --cov-report=xml

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
	uv build

publish-test: build
	uv pip install --system twine
	twine upload --repository testpypi dist/*

publish: build
	uv pip install --system twine
	twine upload dist/*

