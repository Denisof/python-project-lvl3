install:
	poetry install 

page-loader:
	poetry run page-loader

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl

lint:
	poetry run flake8 page_loader

test:
	poetry run coverage run -m  pytest

test-coverage:
	poetry run coverage xml --include=page_loader/*