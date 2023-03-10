# keynote-slides-freezer

A Python tool for macOS to "freeze" a Keynote slides deck. It keeps only "safe" text objects that use specified fonts as text, and replaces the rest with a PDF.

Useful if you make a Keynote deck that uses many different fonts. If you "freeze" the deck, you can easily convert it to PowerPoint, and optionally upload that to Google Slides, and the custom fonts will not be replaced by random fallback fonts. 

## Functionality

The tool is command-line, and uses scripting to process an Apple Keynote `.key` file. It’s not very robust, due to limitations of the AppleScript interface for Keynote.

1. Opens an input `.key` Keynote file and creates two copies in a temp folder, a "vector" and a "text" version.
2. In the "text" version, removes non-text items and text items that use the supported font. 
3. In the "vector" version, removes text items that do not use the supported font. 
4. Exports the "vector" version to a PDF file, and splits it into separate pages. 
5. Pastes each exported separate PDF into the "text" version, and sends it to the back. 
6. Removes all files except, keeps the "text" version as the output.

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

## Background

The code defines a `KeynoteSlidesFreezer` class with methods for processing Keynote files in the macOS GUI. The class includes methods for opening and closing Keynote files, cleaning up text and vector slides, exporting the Keynote file to a PDF file, and splitting the PDF file into separate pages and importing them. The `process()` method combines all these steps in a single function. 

The script uses the `appscript` and `AppKit` libraries to interact with Keynote on macOS. It also uses the `fitz` library for PDF manipulation.

## License

- [Apache 2.0](./LICENSE)