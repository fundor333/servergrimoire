# You can set these variables from the command line.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

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

view:
	open build/html/index.html

clean: ## Clean Sphinx output
	-rm -rf $(BUILDDIR)/*

html: clean ## Build documentation
	poetry run $(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

publish: test html
	poetry publish --build
