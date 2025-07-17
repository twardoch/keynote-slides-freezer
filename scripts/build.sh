#!/bin/bash
# this_file: scripts/build.sh

# Build script for keynote-slides-freezer
set -e

echo "🔧 Building keynote-slides-freezer..."

# Update version from git tags
echo "📝 Updating version from git tags..."
python3 version.py update

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
echo "📦 Installing build dependencies..."
python3 -m pip install --upgrade pip build twine

# Build package
echo "🏗️  Building package..."
python3 -m build

# Verify the build
echo "✅ Verifying build..."
python3 -m twine check dist/*

echo "✨ Build completed successfully!"
echo "📁 Built packages:"
ls -la dist/