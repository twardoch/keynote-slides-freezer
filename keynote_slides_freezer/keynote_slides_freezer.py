#!/usr/bin/env python3
"""
A Python tool for macOS to "freeze" a Keynote slides deck. It keeps only "safe" text objects that use specified fonts as text, and replaces the rest with a PDF.

Useful if you make a Keynote deck that uses many different fonts. If you "freeze" the deck, you can easily convert it to PowerPoint, and optionally upload that to Google Slides, and the custom fonts will not be replaced by random fallback fonts.

The tool is command-line, and uses scripting to process an Apple Keynote `.key` file. It’s not very robust, due to limitations of the AppleScript interface for Keynote.

1. Opens an input `.key` Keynote file and creates two copies in a temp folder, a "vector" and a "text" version.
2. In the "text" version, removes non-text items and text items that use the supported font.
3. In the "vector" version, removes text items that do not use the supported font.
4. Exports the "vector" version to a PDF file, and splits it into separate pages.
5. Pastes each exported separate PDF into the "text" version, and sends it to the back.
6. Removes all files except, keeps the "text" version as the output.

The code defines a `KeynoteSlidesFreezer` class with methods for processing Keynote files in the macOS GUI. The class includes methods for opening and closing Keynote files, cleaning up text and vector slides, exporting the Keynote file to a PDF file, and splitting the PDF file into separate pages, and importing them. The process() method combines all these steps in a single function.

The script uses the `appscript` and `AppKit` libraries to interact with Keynote on macOS. It also uses the `fitz` library for PDF manipulation.
"""

import shutil
import tempfile
from pathlib import Path

import fitz
from AppKit import NSData, NSPasteboard, NSPDFPboardType
from appscript import app, k, mactypes


class KeynoteSlidesFreezer:
    """
    KeynoteSlidesFreezer class for freezing the Keynote slides deck.

    Attributes:
        __class__.timeout_short (int): The timeout value for short operations, in milliseconds.
        __class__.timeout_long (int): The timeout value for long operations, in milliseconds.
        sys: An instance of the `System Events` app from the`appscript` library.
        app: An instance of the `Keynote` app from the `appscript` library.
        doc_path (Path): The path to the Keynote deck being processed.
        out_path (Path): The path to the output deck file. If not provided, the output file will be created in the same folder as the input file, with `-frozen` added to the base filename.
        vecdoc: A copy of the Keynote deck where vector art will be kept.
        vecdoc_path (Path): The path to the `vecdoc` in a temporary folder.
        txtdoc: A copy of the Keynote deck where text items with supported fonts will be kept, and where the PDF pages will be pasted.
        txtdoc_path (Path): The path to the `txtdoc` in a temporary folder.
        pdf_pages_paths (List[Path]): A list of paths to the pages of the PDF version of the Keynote deck.
        fonts_as_text (List[str]): A list of font names to keep as text items in the cleaned deck.
    """

    timeout_short = 5000
    timeout_long = 12000

    def __init__(self):
        """
        Initializes a new KeynoteTricks instance.
        """
        self.sys = app("System Events")
        self.app = app("Keynote")
        self.app.activate()
        self.doc_path: Path = None
        self.out_path: Path = None
        self.vecdoc = None
        self.vecdoc_path: Path = None
        self.txtdoc = None
        self.txtdoc_path: Path = None
        self.pdf_pages_folder: Path = None
        self.pdf_pages_paths: List[Path] = None
        self.fonts_as_text: List[str] = None
        self.temp_folder = tempfile.TemporaryDirectory()
        self.temp_folder_path = self.temp_folder.name

    def _file(self, path):
        """
        Convert a file path to an `appscript` file object.

        Parameters:
            path (str): The file path to convert.

        Returns:
            An `appscript` file object.
        """
        return mactypes.File(str(Path(path).resolve()))

    def _copy_doc(self, suf):
        """
        Copies a Keynote deck and renames it with a suffix.

        Args:
            suf (str): The suffix to add to the new file name.

        Returns:
            Path: The path to the new file.

        """
        doc2_path = Path(
            self.temp_folder_path, Path(f"{self.doc_path.stem}-{suf}.key")
        ).resolve()
        if doc2_path.exists():
            doc2_path.unlink()
        shutil.copy(self.doc_path, doc2_path, follow_symlinks=True)
        return doc2_path

    def open_txtdoc(self):
        """
        Opens the text-specific deck in Keynote.

        Returns:
            None
        """
        self.txtdoc_path = self._copy_doc("text")
        self.txtdoc = self.app.open(self._file(self.txtdoc_path))
        self.txtdoc.activate()

    def open_vecdoc(self):
        """
        Opens the vector-specific deck in Keynote.

        Returns:
            None
        """
        self.vecdoc_path = self._copy_doc("pdf")
        self.vecdoc = self.app.open(self._file(self.vecdoc_path))
        self.vecdoc.activate()

    def safe_text_item(self, item):
        """Returns True if the given Keynote item is a safe text item, i.e., its font is one of the supported fonts."""
        font = item.object_text.font.get().split("-")[0]
        return any(font.startswith(font_as_text) for font_as_text in self.fonts_as_text)

    def clean_items(self, slide, items, keep_text_items):
        """
        Deletes or hides items from the slide.

        Args:
        - slide: Keynote slide
        - items: list of Keynote slide items
        - keep_text_items: boolean, if True, deletes or hides vector items and text items with unsupported fonts, if False, deletes or hides text items with supported fonts.

        Returns:
        - None
        """

        items_to_delete = []
        for item in items:
            item_to_delete = self.safe_text_item(item) != keep_text_items
            if item_to_delete:
                if "default_body_item" in repr(item):
                    if slide.body_showing.get():
                        slide.body_showing.set(not item_to_delete)
                    item_to_delete = False
                elif "default_title_item" in repr(item):
                    if slide.title_showing.get():
                        slide.title_showing.set(not item_to_delete)
                    item_to_delete = False
            if item_to_delete:
                items_to_delete.append(item)
        items_to_delete.reverse()
        for item in items_to_delete:
            if not item.locked.get():
                item.delete()

    def clean_slide(self, doc, slide, keep_text_items):
        """
        Cleans text and vector items of a slide.

        Args:
            - doc (appscript.Reference): Reference to the deck object.
            - slide (appscript.Reference): Reference to the slide object.
            - keep_text_items: boolean, if True, deletes or hides vector items and text items with unsupported fonts, if False, deletes or hides text items with supported fonts.
        """

        doc.current_slide.set(slide)
        self.clean_items(slide, slide.text_items.get(), keep_text_items)
        self.clean_items(slide, slide.shapes.get(), keep_text_items)
        if keep_text_items:
            slide.charts.delete()
            slide.images.delete()
            slide.groups.delete()
            slide.lines.delete()
            slide.tables.delete()

    def process_vecdoc(self):
        """
        Processes the vector-specific Keynote deck: removes text items that use supported fonts from each slide, exports the deck to PDF, splits the PDF into separate pages.
        """
        # Open the PDF version of the deck
        self.open_vecdoc()
        self.vecdoc.activate()

        # Clean up each slide in the deck
        for slide in self.vecdoc.slides.get():
            self.clean_slide(self.vecdoc, slide, keep_text_items=False)

        self.export_vecdoc()
        self.split_pdf()

    def process_txtdoc(self):
        """
        Processes the text-specific Keynote deck: removes vector items and text items that use unsupported fonts from each slide, pastes the PDF pages and sends them to back.

        Returns:
            None
        """
        self.open_txtdoc()
        self.txtdoc.activate()
        for slidei, slide in enumerate(self.txtdoc.slides.get()):
            self.clean_slide(self.txtdoc, slide, keep_text_items=True)

            self.txtdoc.current_slide.set(slide)
            slide.activate()
            pdf_page_path = self.pdf_pages_paths[slidei]

            pdf_data = NSData.dataWithContentsOfFile_(str(pdf_page_path))
            pasteboard = NSPasteboard.generalPasteboard()
            pasteboard.clearContents()
            pasteboard.setData_forType_(pdf_data, NSPDFPboardType)
            self.sys.keystroke(
                "v", using=[k.command_down], timeout=self.__class__.timeout_long
            )
            images = slide.images.get()
            if len(images):
                image = images[0]
                self.txtdoc.selection.set([image])
                self.sys.keystroke(
                    "b",
                    using=[k.command_down, k.shift_down],
                    timeout=self.__class__.timeout_short,
                )

    def export_doc_png(self):
        """
        Exports the deck as PNG images (not used).
        """
        self.pdf_path = Path(self.vecdoc_path).stem
        self.vecdoc.export(
            to=self._file(self.pdf_path),
            as_=k.slide_images,
            timeout=self.__class__.timeout_long,
            with_properties={k.image_format: k.PNG, k.skipped_slides: False},
        )
        self.pdf_pages_paths = list(Path(self.pdf_path).glob("*.png"))

    def export_vecdoc(self):
        """
        Exports the deck to a PDF file.

        Returns:
            None
        """
        self.pdf_path = Path(self.vecdoc_path).with_suffix(".pdf")
        self.vecdoc.export(
            to=self._file(self.pdf_path),
            as_=k.PDF,
            timeout=self.__class__.timeout_long,
            with_properties={k.PDF_image_quality: k.Best, k.skipped_slides: False},
        )

    def split_pdf(self):
        """
        Splits the exported PDF individual pages.

        Returns:
            None
        """
        self.pdf_pages_folder = Path(self.temp_folder_path, self.pdf_path.stem)
        if self.pdf_pages_folder.exists():
            shutil.rmtree(self.pdf_pages_folder, ignore_errors=True)
        self.pdf_pages_folder.mkdir(parents=True, exist_ok=True)

        self.pdf_file = fitz.open(self.pdf_path)

        # Loop over each page in the PDF and save it as a separate PDF file
        self.pdf_pages_paths = []
        for i in range(self.pdf_file.page_count):
            # Create a new PDF file for the page
            page_pdf_path = Path(self.pdf_pages_folder, f"{i + 1:04}.pdf")
            page_pdf_doc = fitz.open()
            page_pdf_doc.insert_pdf(self.pdf_file, from_page=i, to_page=i)

            # Save the new PDF file to disk
            page_pdf_doc.save(page_pdf_path)
            page_pdf_doc.close()

            # Add the path to the page PDF file to the list of page paths
            self.pdf_pages_paths.append(page_pdf_path)

        # Close the input PDF file
        self.pdf_file.close()

    def cleanup(self):
        """
        Closes the decks and removes temporary files.
        """
        self.vecdoc.close()
        self.txtdoc.close()
        self.doc_path = None
        self.txtdoc = None
        self.vecdoc = None
        self.fonts_as_text = None
        shutil.move(self.txtdoc_path, self.out_path)
        shutil.rmtree(self.pdf_pages_folder)
        self.vecdoc_path.unlink()
        self.temp_folder.cleanup()

    def process(self, doc_path, fonts_as_text=("Roboto"), out_path=None):
        """
        1. Opens the Keynote deck specified in `doc_path`
        2. Creates a vector-specific and a text-specific copy of the deck.
        2. In the vector-specific deck, removes all text items that use supported fonts, exports the deck as PDF and splits that into separate pages.
        4. In the text-specific deck, removes all vector items and text items that use unsupported fonts, places the PDF pages and sends them into background.

        Parameters:
        -----------
        doc_path: str or Path
            The path to the input Keynote file.
        fonts_as_text: str or List[str]
            A list of font names to keep as text items in the cleaned deck. Defaults to `Roboto`.
        out_path: str or Path
            The path to the output Keynote.

        Returns:
        --------
        None
        """
        self.fonts_as_text = (
            fonts_as_text.split(",")
            if isinstance(fonts_as_text, str)
            else list(fonts_as_text)
        )
        self.doc_path = Path(doc_path).resolve()
        self.out_path = out_path or Path(
            self.doc_path.parent, f"{self.doc_path.stem}-frozen.key"
        )
        self.process_vecdoc()
        self.process_txtdoc()
        self.cleanup()
