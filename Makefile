# Makefile for keynote-slides-freezer

.PHONY: help install test build clean release binary dev-setup format lint

help:  ## Show this help message
	@echo "📋 Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install package in development mode
	python -m pip install -e ".[dev]"

dev-setup:  ## Set up development environment
	./scripts/dev-setup.sh

test:  ## Run tests
	./scripts/test.sh

format:  ## Format code
	python -m black keynote_slides_freezer/ tests/

lint:  ## Run linting
	python -m flake8 keynote_slides_freezer/ tests/ --max-line-length=88 --extend-ignore=E203,W503

build:  ## Build package
	./scripts/build.sh

binary:  ## Build binary
	./scripts/build-binary.sh

clean:  ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/ .coverage htmlcov/ binary-release/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

release:  ## Release package (usage: make release VERSION=1.0.0)
	@if [ -z "$(VERSION)" ]; then \
		echo "❌ Usage: make release VERSION=1.0.0"; \
		exit 1; \
	fi
	./scripts/release.sh $(VERSION)

version:  ## Show current version
	@python version.py

update-version:  ## Update version from git tags
	python version.py update