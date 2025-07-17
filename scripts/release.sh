#!/bin/bash
# this_file: scripts/release.sh

# Release script for keynote-slides-freezer
set -e

# Check if version tag is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <version> [--dry-run]"
    echo "Example: $0 1.0.0"
    echo "Example: $0 1.0.0 --dry-run"
    exit 1
fi

VERSION=$1
DRY_RUN=${2:-}

# Validate version format (basic semver)
if ! echo "$VERSION" | grep -E "^[0-9]+\.[0-9]+\.[0-9]+$" > /dev/null; then
    echo "❌ Invalid version format. Use semantic versioning (e.g., 1.0.0)"
    exit 1
fi

echo "🚀 Preparing release $VERSION..."

# Check if we're on the main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "❌ Releases must be made from the main branch. Current branch: $CURRENT_BRANCH"
    exit 1
fi

# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Working directory is not clean. Please commit or stash changes."
    exit 1
fi

# Check if tag already exists
if git tag -l | grep -q "^v$VERSION$"; then
    echo "❌ Tag v$VERSION already exists"
    exit 1
fi

# Run tests
echo "🧪 Running tests..."
./scripts/test.sh

# Build package
echo "🏗️  Building package..."
./scripts/build.sh

if [ "$DRY_RUN" = "--dry-run" ]; then
    echo "🔍 DRY RUN: Would create tag v$VERSION and push to repository"
    echo "🔍 DRY RUN: Would upload to PyPI"
    echo "✅ Dry run completed successfully!"
else
    # Create and push tag
    echo "📝 Creating git tag v$VERSION..."
    git tag -a "v$VERSION" -m "Release v$VERSION"
    
    echo "📤 Pushing tag to repository..."
    git push origin "v$VERSION"
    
    # Upload to PyPI
    echo "📦 Uploading to PyPI..."
    python -m twine upload dist/*
    
    echo "✅ Release $VERSION completed successfully!"
    echo "🎉 Package uploaded to PyPI and tag pushed to repository"
fi