#!/bin/bash
# this_file: scripts/dev-setup.sh

# Development setup script for keynote-slides-freezer
set -e

echo "🛠️  Setting up development environment for keynote-slides-freezer..."

# Check if Python 3.10+ is available
python_version=$(python --version 2>&1 | awk '{print $2}')
required_version="3.10"

if ! python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
    echo "❌ Python 3.10+ required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Install the package in development mode
echo "📦 Installing package in development mode..."
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

# Install pre-commit hooks (if available)
if command -v pre-commit &> /dev/null; then
    echo "🪝 Installing pre-commit hooks..."
    pre-commit install
fi

# Create basic .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Development environment variables
PYTHONPATH=.
EOF
fi

echo "✅ Development environment setup completed!"
echo ""
echo "🚀 Quick start:"
echo "  Run tests:    ./scripts/test.sh"
echo "  Build:        ./scripts/build.sh"
echo "  Release:      ./scripts/release.sh <version>"
echo ""
echo "💡 Available commands:"
echo "  keynote_freezer --help"