# keynote-slides-freezer
A Python tool to "freeze" a Keynote slidehow: keeps only text objects that use specified fonts as text, exports to PDF slides from the rest and builds a new deck that has the PDFs plus the "safe" text boxes

```
NAME
    keynote_freezer - Processes the Keynote file located at `doc_path`. The processing involves the following steps: 1. Opens the Keynote file and creates a copy of it as a PDF file. 2. Cleans up each slide in the PDF version of the presentation, removing non-text items and text items that do not use the supported font. 3. Exports the cleaned PDF version of the presentation to a PDF file and splits it into separate pages. 4. For each page in the cleaned PDF file, copies the page to the system clipboard, pastes it into Keynote as an image, and adds the image to a new slide in the Keynote document.

SYNOPSIS
    keynote_freezer DOC_PATH <flags>

DESCRIPTION
    Processes the Keynote file located at `doc_path`. The processing involves the following steps: 1. Opens the Keynote file and creates a copy of it as a PDF file. 2. Cleans up each slide in the PDF version of the presentation, removing non-text items and text items that do not use the supported font. 3. Exports the cleaned PDF version of the presentation to a PDF file and splits it into separate pages. 4. For each page in the cleaned PDF file, copies the page to the system clipboard, pastes it into Keynote as an image, and adds the image to a new slide in the Keynote document.

POSITIONAL ARGUMENTS
    DOC_PATH
        str or Path The path to the Keynote file to be processed.

FLAGS
    -f, --fonts_as_text=FONTS_AS_TEXT
        Default: 'Roboto'
        str or List[str] A list of font names to keep as text items in the cleaned presentation. Defaults to "Roboto".
    -o, --out_path=OUT_PATH
        Type: Optional[]
        Default: None

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```