ARTIFACT_DIR := $(if $(ARTIFACT_DIR),$(ARTIFACT_DIR),tests/test_results)
PATH_TO_PLANTUML := ~/bin


run: ## Run the service locally
	python src/lightspeed_stack.py

test-unit: ## Run the unit tests
	@echo "Running unit tests..."
	@echo "Reports will be written to ${ARTIFACT_DIR}"
	COVERAGE_FILE="${ARTIFACT_DIR}/.coverage.unit" pdm run pytest tests/unit --cov=src --cov-report term-missing --cov-report "json:${ARTIFACT_DIR}/coverage_unit.json" --junit-xml="${ARTIFACT_DIR}/junit_unit.xml" --cov-fail-under=60

test-integration: ## Run integration tests tests
	@echo "Running integration tests..."
	@echo "Reports will be written to ${ARTIFACT_DIR}"
	COVERAGE_FILE="${ARTIFACT_DIR}/.coverage.integration" pdm run pytest tests/integration --cov=src --cov-report term-missing --cov-report "json:${ARTIFACT_DIR}/coverage_integration.json" --junit-xml="${ARTIFACT_DIR}/junit_integration.xml" --cov-fail-under=10

check-types: ## Checks type hints in sources
	pdm run mypy --explicit-package-bases --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs --ignore-missing-imports --disable-error-code attr-defined src/

security-check: ## Check the project for security issues
	bandit -c pyproject.toml -r src tests

format: ## Format the code into unified format
	pdm run black .
	pdm run ruff check . --fix

schema:	## Generate OpenAPI schema file
	pdm run scripts/generate_openapi_schema.py docs/openapi.json

requirements.txt:	pyproject.toml pdm.lock ## Generate requirements.txt file containing hashes for all non-devel packages
	pdm export --prod --format requirements --output requirements.txt --no-extras --without evaluation

docs/config.puml: ## Generate PlantUML class diagram for configuration
	pyreverse src/models/config.py --output puml --output-directory=docs/
	mv docs/classes.puml docs/config.puml

docs/config.png:	docs/config.puml ## Generate an image with configuration graph
	pushd docs && \
	java -jar ${PATH_TO_PLANTUML}/plantuml.jar --theme rose config.puml && \
	mv classes.png config.png && \
	popd

shellcheck: ## Run shellcheck
	wget -qO- "https://github.com/koalaman/shellcheck/releases/download/stable/shellcheck-stable.linux.x86_64.tar.xz" | tar -xJv \
	shellcheck --version
	shellcheck -- */*.sh

black:
	pdm run black --check .

pylint:
	pdm run pylint src

pyright:
	pdm run pyright src

docstyle:
	pdm run pydocstyle -v .

ruff:
	pdm run ruff check . --per-file-ignores=tests/*:S101 --per-file-ignores=scripts/*:S101

verify:
	$(MAKE) black
	$(MAKE) pylint
	$(MAKE) pyright
	$(MAKE) ruff
	$(MAKE) docstyle
	$(MAKE) check-types
