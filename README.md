# keynote-slides-freezer

A Python tool to "freeze" a Keynote slideshow. Keeps only "safe" text objects that use specified fonts as text, exports to PDF slides from the rest and builds a new deck that has the PDFs plus the "safe" text boxes.

Runs on macOS and uses scripting to process an Apple Keynote `.key` file: 

1. Opens the Keynote file and creates two copies in a temp folder, a "PDF" and a "text" version.
2. In the "text" version, removes non-text items and text items that use the supported font. 
3. In the "PDF" version, removes text items that do not use the supported font. 
4. Exports the "PDF" version to a PDF file and splits it into separate pages. 
5. Pastes the separate pages into the "text" version and sends it to the back. 
6. Removes all files except the "text" version.

## Installation

```
python3 -m pip install --upgrade git+https://github.com/twardoch/keynote-slides-freezer
```

## Usage

In Terminal:

```
keynote_freezer INPUT_KEY_FILE -f SAFE_FONTS -o OUTPUT_KEY_FILE
```

`SAFE_FONTS` is a comma-separated list of font family name prefixes, by default `Roboto`. 

If `OUTPUT_KEY_FILE` is not specified, saves the processed version in the same folder as the `INPUT_KEY_FILE`, with `-frozen` added to the base filename. 

