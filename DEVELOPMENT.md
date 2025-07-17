# Development Guide

This guide covers how to develop, test, and release keynote-slides-freezer.

## Quick Start

```bash
# Set up development environment
make dev-setup

# Run tests
make test

# Build package
make build

# Build binary
make binary

# Release (example)
make release VERSION=1.0.0
```

## Development Setup

### Prerequisites

- macOS 10.15 or later
- Python 3.10 or later
- Apple Keynote installed
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/twardoch/keynote-slides-freezer.git
   cd keynote-slides-freezer
   ```

2. **Set up development environment**
   ```bash
   make dev-setup
   ```

   This will:
   - Install the package in development mode
   - Install all development dependencies
   - Set up pre-commit hooks (if available)

## Version Management

This project uses **git-tag-based semantic versioning**:

- **Version Format**: `MAJOR.MINOR.PATCH` (e.g., `1.0.0`)
- **Git Tags**: `v1.0.0`, `v1.1.0`, `v2.0.0`, etc.
- **Development Versions**: `1.0.0.dev3+a1b2c3d` (auto-generated)

### Version Commands

```bash
# Show current version
make version

# Update version from git tags
make update-version
```

## Testing

### Run All Tests

```bash
make test
```

This runs:
- Code formatting check (Black)
- Linting (Flake8)
- Type checking (MyPy)
- Unit tests (pytest)
- Coverage reporting

### Individual Test Commands

```bash
# Format code
make format

# Run linting
make lint

# Run only unit tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=keynote_slides_freezer --cov-report=html
```

## Building

### Build Python Package

```bash
make build
```

Output: `dist/keynote_slides_freezer-VERSION-py3-none-any.whl` and `dist/keynote_slides_freezer-VERSION.tar.gz`

### Build Binary

```bash
make binary
```

Output: `keynote_freezer-VERSION-macos.tar.gz`

The binary includes:
- Standalone executable
- Installation script
- Documentation
- License

## Release Process

### Automated Release (Recommended)

1. **Create and push a git tag**
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

2. **GitHub Actions will automatically:**
   - Run tests on multiple Python versions
   - Build Python packages
   - Build binary releases
   - Create GitHub release with assets
   - Upload to PyPI

### Manual Release

```bash
# Run tests and build
make test
make build

# Create release (with dry-run option)
make release VERSION=1.0.0 --dry-run

# Actual release
make release VERSION=1.0.0
```

## GitHub Actions

### CI Pipeline (`.github/workflows/ci.yml`)

**Triggers**: Push/PR to `main` or `develop`

**Jobs**:
- Test on Python 3.10, 3.11, 3.12
- Code quality checks
- Build package
- Upload build artifacts

### Release Pipeline (`.github/workflows/release.yml`)

**Triggers**: Push git tag `v*`

**Jobs**:
- Run full test suite
- Build and publish to PyPI
- Create GitHub release
- Upload package assets

### Binary Release Pipeline (`.github/workflows/binary-release.yml`)

**Triggers**: Push git tag `v*`

**Jobs**:
- Build macOS binary with PyInstaller
- Create binary package
- Upload to GitHub release

## Project Structure

```
keynote-slides-freezer/
├── keynote_slides_freezer/     # Main package
│   ├── __init__.py
│   ├── cli.py                  # Command-line interface
│   └── keynote_slides_freezer.py  # Core functionality
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_imports.py
│   └── test_version.py
├── scripts/                    # Build and release scripts
│   ├── build.sh
│   ├── build-binary.sh
│   ├── dev-setup.sh
│   ├── release.sh
│   └── test.sh
├── .github/workflows/          # GitHub Actions
│   ├── ci.yml
│   ├── release.yml
│   └── binary-release.yml
├── pyproject.toml              # Python project configuration
├── version.py                  # Version management
├── Makefile                    # Common development tasks
└── ...
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite: `make test`
6. Submit a pull request

## Troubleshooting

### Common Issues

1. **Version not updating**: Run `make update-version`
2. **Tests failing**: Check Python version (3.10+ required)
3. **Binary build failing**: Ensure you're on macOS with Keynote installed
4. **Import errors**: Run `make dev-setup` to reinstall dependencies

### Debug Commands

```bash
# Check Python version
python --version

# Check package installation
pip list | grep keynote

# Check git tags
git tag -l

# Verbose test output
python -m pytest tests/ -v -s
```

## Release Checklist

Before releasing a new version:

- [ ] Update `CHANGELOG.md` with changes
- [ ] Run full test suite: `make test`
- [ ] Build and test locally: `make build`
- [ ] Test binary: `make binary`
- [ ] Create and push git tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
- [ ] Monitor GitHub Actions for successful deployment
- [ ] Verify PyPI upload
- [ ] Test installation: `pip install keynote-slides-freezer==X.Y.Z`