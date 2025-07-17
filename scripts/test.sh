#!/bin/bash
# this_file: scripts/test.sh

# Test script for keynote-slides-freezer
set -e

echo "🧪 Running tests for keynote-slides-freezer..."

# Install test dependencies
echo "📦 Installing test dependencies..."
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

# Run code formatting check
echo "🎨 Checking code formatting with black..."
python -m black --check keynote_slides_freezer/ tests/ || {
    echo "❌ Code formatting issues found. Run 'python -m black keynote_slides_freezer/ tests/' to fix."
    exit 1
}

# Run linting
echo "🔍 Running linting with flake8..."
python -m flake8 keynote_slides_freezer/ tests/ --max-line-length=88 --extend-ignore=E203,W503

# Run type checking
echo "🔬 Running type checking with mypy..."
python -m mypy keynote_slides_freezer/ --ignore-missing-imports

# Run tests
echo "🧪 Running pytest..."
python -m pytest tests/ -v

echo "✅ All tests passed!"