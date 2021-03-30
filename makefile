.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: test
test: ## Testing the app
	poetry run python -m unittest tests

.PHONY: install
install: ## Install the env
	poetry install
	poetry run pre-commit install
	poetry run pre-commit autoupdate

.PHONY: update
update: ## Update the dependency project
	poetry update

.PHONY: docs
docs:  ## Previewing as you write documentation
	poetry run mkdocs build --clean

.PHONY: html
html: docs## Serve the docs
	poetry run mkdocs serve

prepublish: test docs ## Code for the prepublish

publish: prepublish ## Testing and publish the paackage
	poetry publish --build
