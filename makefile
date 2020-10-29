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

.PHONY: update
update: ## Update the dependency project
	poetry update

