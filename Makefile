.DEFAULT_GOAL := help
.PHONY: coverage deps help lint push test

coverage:  ## Run tests with coverage
	coverage erase
	coverage run --include=twisp/* -m pytest -ra
	coverage report -m

deps:  ## Install dependencies
	pip install black coverage flake8 mccabe mypy pylint pytest tox

lint:  ## Lint and static-check
	flake8 twisp
	pylint twisp
	mypy twisp

push:  ## Push code with tags
	git push && git push --tags

test:  ## Run tests
	pytest -ra