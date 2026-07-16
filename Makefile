SOURCE_FILES ?= $(shell git ls-files "**.py")
ISOLATE ?= 1

ifeq ($(ISOLATE),1)
UNSHARE := unshare -r -n
else
UNSHARE :=
endif

# Override to use uv, e.g. PYTHON_RUN="uv run"
PYTHON_RUN ?=

.PHONY: help
help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: help

.PHONY: init
init: ## Install dependencies using uv
	uv sync

# Detect if pytest-xdist is installed for parallel testing
PYTEST_XDIST := $(shell $(PYTHON_RUN) python3 -c "import xdist" 2>/dev/null && echo "-n auto" || echo "")

.PHONY: test-unit
test-unit: ## Run dynamic tests with coverage report
	$(UNSHARE) $(PYTHON_RUN) py.test $(PYTEST_XDIST) --cov --cov-report=xml --cov-report=term-missing --cov-branch --cov=baremetal_support tests/

.PHONY: test-unit-no-coverage
test-unit-no-coverage: ## Run dynamic tests without coverage analysis
	$(UNSHARE) $(PYTHON_RUN) py.test $(PYTEST_XDIST) tests/

.PHONY: only-test-with-coverage
only-test-with-coverage: test-unit  ## Alias for "test-unit"

.PHONY: check-ruff
check-ruff: ## Run ruff linting and formatting checks
	$(PYTHON_RUN) ruff check
	$(PYTHON_RUN) ruff format --check

.PHONY: tidy
tidy: ## Format code and fix linting issues
	$(PYTHON_RUN) ruff format
	$(PYTHON_RUN) ruff check --fix

.PHONY: check-conventions
check-conventions: ## Check for banned coding patterns
	@if git grep -nE '^\s*@(unittest\.mock\.|mock\.)?patch' tests/; then \
		echo "Error: @patch decorator detected. Avoid to prevent argument ordering bugs."; \
		echo "   Fix: Use the 'mocker' fixture (pytest-mock) or a 'with patch():' context manager."; \
		exit 1; \
	fi

.PHONY: check-types-ty
check-types-ty: ## Run ty type checker
	$(PYTHON_RUN) ty check

.PHONY: check-types
check-types: check-types-ty

# aggregate targets

.PHONY: checkstyle
checkstyle: ## Run fast style and static analysis checks
	@$(MAKE) -j check-ruff check-conventions check-types

.PHONY: test
test: ## Run all tests with coverage analysis and style checks
	@$(MAKE) test-unit checkstyle

.PHONY: test-no-coverage
test-no-coverage: ## Run all tests *without* coverage analysis and style checks (faster)
	@$(MAKE) test-unit-no-coverage checkstyle

.PHONY: test-with-coverage
test-with-coverage: test  ## Alias for "test"
