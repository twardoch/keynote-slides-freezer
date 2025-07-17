# Deployment Guide

This document describes how to deploy and release keynote-slides-freezer using the automated CI/CD system.

## Quick Reference

### For Regular Releases

1. **Create and push a git tag:**
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

2. **GitHub Actions will automatically:**
   - Run tests on multiple Python versions
   - Build packages (wheel + source)
   - Create GitHub release with assets
   - Upload to PyPI
   - Build and attach binary releases

### For Local Development

```bash
# Quick setup
make dev-setup

# Run tests
make test

# Build locally
make build

# Build binary
make binary

# Manual release (if needed)
make release VERSION=1.0.0
```

## Prerequisites

### GitHub Repository Setup

1. **PyPI API Token**: Add `PYPI_API_TOKEN` to repository secrets
2. **GitHub Token**: Automatically available as `GITHUB_TOKEN`

### Local Development Setup

1. **macOS**: Required for binary builds and full testing
2. **Python 3.10+**: For development and testing
3. **Git**: For version management

## Release Process

### 1. Prepare Release

```bash
# Ensure you're on main branch
git checkout main
git pull origin main

# Update CHANGELOG.md with release notes
# Update version in any docs if needed

# Commit changes
git add -A
git commit -m "Prepare release v1.0.0"
git push origin main
```

### 2. Create Release Tag

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0"

# Push tag (this triggers the release)
git push origin v1.0.0
```

### 3. Monitor Release

1. **GitHub Actions**: Watch the workflows at `/actions`
2. **PyPI**: Verify package at `https://pypi.org/project/keynote-slides-freezer/`
3. **GitHub Release**: Check assets at `/releases`

## CI/CD Workflows

### CI Workflow (`.github/workflows/ci.yml`)

**Triggered by**: Push/PR to main/develop

**Steps**:
1. Run tests on Python 3.10, 3.11, 3.12
2. Code quality checks (Black, Flake8, MyPy)
3. Build package
4. Upload artifacts

### Release Workflow (`.github/workflows/release.yml`)

**Triggered by**: Git tag push (`v*`)

**Steps**:
1. Run full test suite
2. Build packages
3. Create GitHub release
4. Upload to PyPI
5. Attach package assets

### Binary Release Workflow (`.github/workflows/binary-release.yml`)

**Triggered by**: Git tag push (`v*`)

**Steps**:
1. Build macOS binary with PyInstaller
2. Create installation package
3. Attach to GitHub release

## Version Management

### Semantic Versioning

- **Format**: `MAJOR.MINOR.PATCH`
- **Git Tags**: `v1.0.0`, `v1.1.0`, `v2.0.0`
- **Development**: `1.0.0.dev3+a1b2c3d` (auto-generated)

### Version Sources

1. **Git Tags**: Primary source for releases
2. **Development**: Auto-generated from commits ahead of tag
3. **Fallback**: `0.0.0+unknown` if no git info

### Version Commands

```bash
# Show current version
python3 version.py

# Update __init__.py with git version
python3 version.py update

# Via Makefile
make version
make update-version
```

## Package Distribution

### PyPI Package

- **Name**: `keynote-slides-freezer`
- **Installation**: `pip install keynote-slides-freezer`
- **Formats**: Wheel (`.whl`) and Source (`.tar.gz`)

### Binary Release

- **Platform**: macOS only
- **Format**: `.tar.gz` with installer
- **Installation**: Extract and run `./install.sh`

## Troubleshooting

### Common Issues

1. **PyPI Upload Fails**
   - Check `PYPI_API_TOKEN` secret
   - Verify version doesn't already exist
   - Check package metadata

2. **Binary Build Fails**
   - Ensure running on macOS
   - Check PyInstaller dependencies
   - Verify imports work

3. **Tests Fail**
   - Check Python version compatibility
   - Verify dependencies are installed
   - Review platform-specific tests

### Debug Commands

```bash
# Check package build
python3 -m build
python3 -m twine check dist/*

# Test package installation
pip install dist/*.whl

# Verify CLI works
keynote_freezer --help

# Check version consistency
python3 version.py
python3 -c "import keynote_slides_freezer; print(keynote_slides_freezer.__version__)"
```

## Manual Recovery

### If Automated Release Fails

1. **Build locally**:
   ```bash
   make build
   ```

2. **Upload to PyPI**:
   ```bash
   python3 -m twine upload dist/*
   ```

3. **Create GitHub release**:
   ```bash
   gh release create v1.0.0 dist/* --title "Release v1.0.0"
   ```

### Rollback Process

1. **Delete PyPI release**: Contact PyPI support
2. **Delete GitHub release**: Use GitHub UI or API
3. **Delete git tag**:
   ```bash
   git tag -d v1.0.0
   git push origin --delete v1.0.0
   ```

## Security Considerations

1. **API Tokens**: Store in GitHub secrets, never commit
2. **Signed Releases**: Consider GPG signing for releases
3. **Dependencies**: Regular security updates
4. **Permissions**: Limit repository access

## Monitoring

### Success Indicators

- ✅ All GitHub Actions workflows pass
- ✅ Package available on PyPI
- ✅ Binary attached to GitHub release
- ✅ Version numbers consistent
- ✅ Installation works: `pip install keynote-slides-freezer`

### Metrics to Track

- Release frequency
- CI/CD success rate
- Download statistics
- Issue resolution time
- Test coverage percentage