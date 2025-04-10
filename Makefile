run:
	@uvicorn dio_blog.main:app --reload
precommit-install:
	@poetry run pre-commit install
format:
	isort .
	black .
	autopep8 --in-place --recursive .
lint:
	flake8 .
	pylint $(find . -name "*.py")
type-check:
	mypy --explicit-package-bases .
	bandit -r .
test_ex1:
	poetry run pytest -v
test_ex2:
	poetry run pytest -vvv
test:
	pytest
test-matching:
	pytest -s -rx -k $(K) --pdb ./tests/
add_dev:
	poetry add '$(K)=*' --group dev
add:
	poetry add '$(K)=*'
run_gunicorn:
	poetry run gunicorn mysite.wsgi:application
