#!/bin/bash
# this_file: scripts/build-binary.sh

# Binary build script for keynote-slides-freezer
set -e

echo "🏗️  Building binary for keynote-slides-freezer..."

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Binary build is only supported on macOS"
    exit 1
fi

# Update version from git tags
echo "📝 Updating version from git tags..."
python version.py update

# Install PyInstaller if not present
echo "📦 Installing PyInstaller..."
python -m pip install --upgrade pyinstaller

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/

# Build binary
echo "🔨 Building binary with PyInstaller..."
pyinstaller --onefile \
    --name keynote_freezer \
    --add-data "keynote_slides_freezer:keynote_slides_freezer" \
    --hidden-import=keynote_slides_freezer.cli \
    --hidden-import=keynote_slides_freezer.keynote_slides_freezer \
    keynote_slides_freezer/cli.py

# Test the binary
echo "🧪 Testing binary..."
./dist/keynote_freezer --help

# Get version for packaging
VERSION=$(python version.py)
echo "📦 Packaging version: $VERSION"

# Create binary package
echo "📁 Creating binary package..."
mkdir -p binary-release
cp dist/keynote_freezer binary-release/
cp README.md binary-release/
cp LICENSE binary-release/

# Create installation script
cat > binary-release/install.sh << 'EOF'
#!/bin/bash
# Installation script for keynote_freezer binary

INSTALL_DIR="/usr/local/bin"
BINARY_NAME="keynote_freezer"

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This binary is only compatible with macOS"
    exit 1
fi

# Check if user has write permissions to install directory
if [[ ! -w "$INSTALL_DIR" ]]; then
    echo "🔐 Installing to $INSTALL_DIR requires sudo permissions"
    sudo cp "$BINARY_NAME" "$INSTALL_DIR/"
    sudo chmod +x "$INSTALL_DIR/$BINARY_NAME"
else
    cp "$BINARY_NAME" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/$BINARY_NAME"
fi

echo "✅ keynote_freezer installed to $INSTALL_DIR"
echo "🚀 You can now run: keynote_freezer --help"
EOF

chmod +x binary-release/install.sh

# Create README for binary release
cat > binary-release/README-BINARY.md << 'EOF'
# keynote_freezer Binary Release

This is a standalone binary release of keynote_freezer for macOS.

## Installation

### Option 1: Automatic installation
```bash
./install.sh
```

### Option 2: Manual installation
1. Copy the `keynote_freezer` binary to a directory in your PATH (e.g., `/usr/local/bin`)
2. Make it executable: `chmod +x /usr/local/bin/keynote_freezer`

## Usage

```bash
keynote_freezer --help
keynote_freezer your-presentation.key
```

## Requirements

- macOS 10.15 or later
- Apple Keynote installed

## Support

For support and documentation, visit: https://github.com/twardoch/keynote-slides-freezer
EOF

# Create archive
cd binary-release
tar -czf ../keynote_freezer-$VERSION-macos.tar.gz *
cd ..

echo "✅ Binary build completed!"
echo "📦 Binary package: keynote_freezer-$VERSION-macos.tar.gz"
echo "🚀 To install locally: cd binary-release && ./install.sh"