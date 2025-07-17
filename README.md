# keynote-slides-freezer

**`keynote-slides-freezer` is a Python tool for macOS designed to "freeze" Apple Keynote slide decks. It intelligently processes your presentation, converting most content into PDF objects while preserving specified text elements as editable text. This is particularly useful for presentations rich in custom fonts, ensuring visual fidelity when converting to PowerPoint or Google Slides.**

This tool addresses a common challenge: when Keynote presentations with unique or non-standard fonts are opened in other applications like PowerPoint or imported into Google Slides, these fonts are often substituted, leading to a broken layout and a compromised visual presentation. `keynote-slides-freezer` helps maintain your design by "baking in" the appearance of most slide elements.

## Table of Contents

- [Who is this tool for?](#who-is-this-tool-for)
- [Why is it useful?](#why-is-it-useful)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Interface (CLI)](#command-line-interface-cli)
  - [Programmatic Usage](#programmatic-usage)
- [Technical Details](#technical-details)
  - [How it Works](#how-it-works)
  - [Core Components](#core-components)
  - [Key Dependencies](#key-dependencies)
  - [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Who is this tool for?

This tool is for anyone who uses Apple Keynote on macOS and needs to share their presentations in formats like PowerPoint or Google Slides, especially when:

*   You use many custom or non-standard fonts.
*   You want to ensure that the visual layout and typography are preserved as much as possible across different platforms and applications.
*   You are preparing a deck for wider distribution where recipients might not have your specific fonts installed.

## Why is it useful?

*   **Preserves Visual Fidelity:** Prevents font substitution issues when converting Keynote files, so your slides look as intended.
*   **Cross-Platform Compatibility:** Makes Keynote decks more portable to PowerPoint and Google Slides.
*   **Saves Time:** Automates the process of selectively rasterizing or vectorizing slide content, which would be tedious to do manually.
*   **Maintains Editability for Key Text:** Allows you to specify fonts that should remain as editable text, offering a balance between visual preservation and future edits for essential content.

## Installation

`keynote-slides-freezer` can be installed in several ways:

### Option 1: Install from PyPI (Recommended)

```bash
pip install keynote-slides-freezer
```

### Option 2: Install from GitHub

```bash
pip install git+https://github.com/twardoch/keynote-slides-freezer
```

### Option 3: Binary Release (macOS)

Download the latest binary release from the [releases page](https://github.com/twardoch/keynote-slides-freezer/releases):

```bash
# Download and extract
curl -L -o keynote_freezer-macos.tar.gz https://github.com/twardoch/keynote-slides-freezer/releases/latest/download/keynote_freezer-*-macos.tar.gz
tar -xzf keynote_freezer-macos.tar.gz
cd keynote_freezer-*-macos

# Install
./install.sh
```

### Requirements

- macOS 10.15 or later
- Python 3.10 or newer (for pip installation)
- Apple Keynote installed

After installation, the command-line tool `keynote_freezer` will be available in your path.

## Usage

`keynote-slides-freezer` can be used both as a command-line tool and programmatically in your Python scripts. **Note:** This tool interacts with the Keynote application GUI, so Keynote must be installed, and you may see it open and process files during operation.

### Command-Line Interface (CLI)

The primary way to use the tool is via the `keynote_freezer` command in your Terminal.

**Basic Syntax:**

```bash
keynote_freezer INPUT_KEY_FILE [OPTIONS]
```

**Arguments and Options:**

*   `INPUT_KEY_FILE`: (Required) The path to the Keynote file (`.key`) you want to process.
*   `-f SAFE_FONTS` or `--fonts_as_text SAFE_FONTS`: (Optional) A comma-separated list of font family name prefixes to keep as editable text.
    *   Default: `"Roboto"`
    *   Example: `-f "Helvetica Neue,Arial,MyCustomFont"`
*   `-o OUTPUT_KEY_FILE` or `--out_path OUTPUT_KEY_FILE`: (Optional) The full path for the processed output Keynote file.
    *   Default: If not specified, the processed version is saved in the same folder as the `INPUT_KEY_FILE`, with `-frozen` appended to the original filename (e.g., `MySlides.key` becomes `MySlides-frozen.key`).

**Examples:**

1.  Process `MyPresentation.key` using the default safe font ("Roboto") and save it as `MyPresentation-frozen.key`:
    ```bash
    keynote_freezer "MyPresentation.key"
    ```

2.  Process `ConferenceDeck.key`, keeping text formatted with "Arial" or "Times New Roman" as editable text, and save to a specific path:
    ```bash
    keynote_freezer "ConferenceDeck.key" -f "Arial,Times New Roman" -o "/Users/yourname/Desktop/ConferenceDeck_Frozen.key"
    ```

### Programmatic Usage

You can also use `keynote-slides-freezer` within your Python scripts for more complex workflows.

```python
from pathlib import Path
from keynote_slides_freezer import KeynoteSlidesFreezer

# Initialize the freezer
freezer = KeynoteSlidesFreezer()

# Define input and output paths
input_file = Path("path/to/your/input.key")
output_file = Path("path/to/your/output-frozen.key") # Optional

# Specify fonts to keep as text (can be a list or a comma-separated string)
safe_fonts = ["Arial", "Helvetica Neue", "MyCustomFont"]
# or safe_fonts = "Arial,Helvetica Neue,MyCustomFont"

try:
    # Process the Keynote file
    if output_file:
        freezer.process(doc_path=input_file, fonts_as_text=safe_fonts, out_path=output_file)
    else:
        # If out_path is None, it will save with "-frozen" suffix in the same directory
        freezer.process(doc_path=input_file, fonts_as_text=safe_fonts)
    print(f"Successfully processed {input_file}")
except Exception as e:
    print(f"An error occurred: {e}")

```

The `process()` method takes the following arguments:
*   `doc_path` (str or Path): The path to the input Keynote file.
*   `fonts_as_text` (str or List[str], optional): A list or comma-separated string of font names to keep as text items. Defaults to `"Roboto"`.
*   `out_path` (str or Path, optional): The path for the output Keynote file. If `None` or not provided, the output file is created in the same folder as the input file, with `-frozen` added to the base filename.

## Technical Details

This section describes how `keynote-slides-freezer` works under the hood.

### How it Works

The tool automates a multi-step process using AppleScript to control Keynote and other libraries for file manipulation. It's important to note that due to the reliance on AppleScript for GUI interaction, the process might not be perfectly robust for all complex Keynote files.

The core workflow is as follows:

1.  **Initialization & Duplication:**
    *   The input `.key` Keynote file is identified.
    *   Two copies of this file are created in a temporary folder:
        *   A "vector" version (e.g., `input-pdf.key`)
        *   A "text" version (e.g., `input-text.key`)

2.  **Processing the "Text" Version:**
    *   The "text" version is opened in Keynote.
    *   For each slide:
        *   Non-text items (images, shapes that are not text boxes, charts, tables, groups, lines) are deleted.
        *   Text items that use fonts *not* in the user-specified `SAFE_FONTS` list are also deleted.
        *   Only text items using the `SAFE_FONTS` remain.

3.  **Processing the "Vector" Version:**
    *   The "vector" version is opened in Keynote.
    *   For each slide:
        *   Text items that *do* use one of the `SAFE_FONTS` are deleted.
        *   The goal is to keep all visual elements and text that will be converted to an image/vector object.

4.  **PDF Export and Splitting:**
    *   The modified "vector" version (containing non-safe-font text and all graphical elements) is exported from Keynote as a single PDF file (with best quality settings).
    *   This PDF is then split into individual PDF files, one for each slide, using the `fitz` (PyMuPDF) library.

5.  **Reconstructing the Final Deck:**
    *   The "text" version (containing only the "safe" text items) is brought to the front.
    *   For each slide in the "text" version:
        *   The corresponding individual PDF page (generated in step 4) is pasted onto the slide.
        *   This pasted PDF object (which now represents the visual background and non-safe text) is sent to the back, appearing behind the "safe" text items.

6.  **Cleanup and Output:**
    *   The original "vector" and intermediate PDF files are deleted from the temporary folder.
    *   The modified "text" version, now containing the safe text overlaid on PDF representations of everything else, is saved to the specified output path (or the default `-frozen` path).
    *   The temporary folder is cleaned up.

### Core Components

*   **`KeynoteSlidesFreezer` Class (in `keynote_slides_freezer.py`):**
    *   This is the main class orchestrating the entire process.
    *   `__init__()`: Initializes connections to Keynote and System Events via `appscript`, and sets up a temporary directory.
    *   `process(doc_path, fonts_as_text, out_path)`: The main public method that drives the freezing workflow.
    *   `_copy_doc()`: Handles copying the Keynote file.
    *   `open_txtdoc()`, `open_vecdoc()`: Open the respective temporary Keynote files.
    *   `safe_text_item(item)`: Checks if a Keynote item's font is in the `fonts_as_text` list.
    *   `clean_items(slide, items, keep_text_items)`: Deletes items from a slide based on whether they are safe text or not.
    *   `clean_slide(doc, slide, keep_text_items)`: Orchestrates the cleaning of a whole slide.
    *   `process_vecdoc()`: Manages the cleaning of the vector document and its export to PDF.
    *   `process_txtdoc()`: Manages the cleaning of the text document and the pasting of PDF pages.
    *   `export_vecdoc()`: Exports the vector document to PDF using Keynote's export functionality.
    *   `split_pdf()`: Splits the exported multi-page PDF into single-page PDFs using `fitz`.
    *   `cleanup()`: Closes Keynote documents, moves the final result, and removes temporary files.

*   **`cli.py`:**
    *   Provides the command-line interface using the `fire` library.
    *   The `main()` function initializes `KeynoteSlidesFreezer` and exposes its `process` method to the CLI.

### Key Dependencies

*   **`appscript`**: A Python bridge to AppleScript / Open Scripting Architecture, enabling control of scriptable macOS applications like Keynote.
*   **`PyMuPDF (fitz)`**: A Python binding for MuPDF, used here for its robust PDF manipulation capabilities, specifically splitting PDF files.
*   **`python-fire`**: A library for automatically generating command-line interfaces (CLIs) from Python objects.
*   **`AppKit`**: Part of Python's PyObjC bridge, used here for interacting with the macOS pasteboard (`NSPasteboard`) to copy and paste PDF data.

### Limitations

*   **macOS Only:** This tool relies on Apple Keynote and macOS-specific technologies (AppleScript, AppKit), so it only runs on macOS.
*   **Keynote Installation Required:** Apple Keynote must be installed on the system.
*   **GUI Interaction:** The tool controls the Keynote GUI. You will see Keynote windows open and files being processed. This means it's not suitable for headless server environments.
*   **Robustness:** As mentioned in the original documentation, controlling GUI applications via scripting can sometimes be fragile. Complex slides or unexpected Keynote dialogs might interrupt the process.
*   **Font Name Specificity:** The `SAFE_FONTS` matching is based on font family name *prefixes*. This is generally effective but be mindful if you have fonts with very similar names.
*   **Unsupported Elements:** While it aims to handle common slide elements, very complex or unusual Keynote objects might not be processed as expected.

## Contributing

Contributions are welcome and greatly appreciated! Whether it's reporting a bug, suggesting an enhancement, or writing code, your help makes this project better.

**Ways to Contribute:**

*   **Report Bugs:** If you find a bug, please open an issue on the [GitHub Issues page](https://github.com/twardoch/keynote-slides-freezer/issues). Include your OS version, Keynote version, steps to reproduce, and any error messages.
*   **Suggest Features:** Have an idea for a new feature or an improvement? File an issue to discuss it.
*   **Write Code:**
    *   Fix bugs or implement new features. Look for issues tagged "bug" or "enhancement."
    *   Improve documentation (docstrings, this README).
*   **Submit Feedback:** Share your experience or suggestions by opening an issue.

### Development Setup

```bash
# Clone repository
git clone https://github.com/twardoch/keynote-slides-freezer.git
cd keynote-slides-freezer

# Set up development environment
make dev-setup

# Run tests
make test

# Build package
make build
```

For detailed development instructions, see [DEVELOPMENT.md](./DEVELOPMENT.md).

### Pull Request Guidelines

- Write tests for new functionality
- Update documentation if necessary
- Follow the existing code style (Black formatting)
- Ensure all tests pass: `make test`

## License

`keynote-slides-freezer` is licensed under the Apache License 2.0. You can find the full license text in the [LICENSE](./LICENSE) file.
