#!/usr/bin/env python3
"""
This code defines a class KeynoteTricks with methods for processing Keynote files. The class includes methods for opening and closing Keynote files, cleaning up text and PDF slides, exporting the Keynote file to a PDF file, and splitting the PDF file into separate pages. The process() method combines all these steps in a single function.

The script uses the appscript and mactypes libraries to interact with Keynote on macOS. It also uses the fitz library for PDF manipulation.

The if __name__ == "__main__" block at the end of the script uses the fire library to allow the process() method to be called from the command line. The method takes a path to a Keynote file and an optional comma-separated list of fonts to keep.
"""

import os
import shutil
from pathlib import Path

import fitz
from AppKit import NSData, NSPasteboard, NSPDFPboardType
from appscript import app, k, mactypes
import tempfile


class KeynoteSlidesFreezer:
    """
    A class for performing various tricks on Keynote presentations.

    Attributes:
        __class__.timeout_short (int): The timeout value for short operations, in milliseconds.
        __class__.timeout_long (int): The timeout value for long operations, in milliseconds.
        sys: An instance of the 'System Events' app from the appscript library.
        app: An instance of the Keynote app from the appscript library.
        doc_path (Path): The path to the Keynote presentation being processed.
        doc_pdf: The Keynote presentation, opened as a PDF.
        doc_pdf_path (Path): The path to the PDF version of the Keynote presentation.
        doc_text: The Keynote presentation, opened as a text document.
        doc_text_path (Path): The path to the text version of the Keynote presentation.
        pdf_page_paths (List[Path]): A list of paths to the pages of the PDF version of the Keynote presentation.
        fonts_as_text (List[str]): A list of font names to keep as text items in the cleaned presentation.
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
        self.doc_pdf = None
        self.doc_pdf_path: Path = None
        self.doc_text = None
        self.doc_text_path: Path = None
        self.pdf_page_paths: List[Path] = None
        self.fonts_as_text: List[str] = None
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = self.temp_dir.name

    def _file(self, path):
        """
        Convert a file path to a Mac file object.

        Parameters:
            path (str): The file path to convert.

        Returns:
            A Mac file object.
        """
        return mactypes.File(str(Path(path).resolve()))

    def _copy_doc(self, suf):
        """
        Copies the original Keynote document and renames it with a suffix.

        Args:
            suf (str): The suffix to add to the new file name.

        Returns:
            Path: The path to the new file.

        """
        key2_path = Path(
            self.temp_dir_path, Path(f"{self.doc_path.stem}-{suf}.key")
        ).resolve()
        if key2_path.exists():
            key2_path.unlink()
        shutil.copy(self.doc_path, key2_path, follow_symlinks=True)
        return key2_path

    def open(self, doc_path):
        """
        Opens the Keynote document located at `doc_path`.

        Parameters:
        -----------
        doc_path: str or Path
            The path to the Keynote document to be opened.

        """
        self.doc_path = Path(doc_path).resolve()

    def open_doc_text(self):
        """
        Open a copy of the Keynote document in Keynote app, as a text-based document.

        Returns:
            None
        """
        self.doc_text_path = self._copy_doc("text")
        self.doc_text = self.app.open(self._file(self.doc_text_path))
        self.doc_text.activate()

    def open_doc_pdf(self):
        """
        Creates a copy of the current Keynote document and opens it in Keynote as a PDF.

        Returns:
            None
        """
        self.doc_pdf_path = self._copy_doc("pdf")
        self.doc_pdf = self.app.open(self._file(self.doc_pdf_path))
        self.doc_pdf.activate()

    def safe_text_item(self, item):
        """Returns True if the given Keynote item is a safe text item, i.e., its font is one of the fonts to keep."""
        font = item.object_text.font.get().split("-")[0]
        return any(
            (font.startswith(font_as_text) for font_as_text in self.fonts_as_text)
        )

    def clean_items(self, slide, items, keep_text_items):
        """
        Remove the items from the slide if they are not text items (title, body).
        If a body or title item is removed, hide the corresponding title or body.

        Args:
        - slide: Keynote slide
        - items: list of Keynote slide items
        - keep_text_items: boolean, whether to keep only title and body items

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
        Clean the text and shape items of a slide.

        Args:
            doc (appscript.Reference): Reference to the document object.
            slide (appscript.Reference): Reference to the slide object.
            keep_text_items (bool): If True, keep the text items in the slide, otherwise remove them.
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

    def clean_text_slide(self, doc, slide, slidei):
        """
        Removes non-text items and charts, images, groups, lines, and tables.
        Removes text items that don’t use the supported font.

        Parameters:
            doc (appscript Reference): Reference to the Keynote document containing the slide.
            slide (appscript Reference): Reference to the slide to be cleaned.
            slidei (int): Index of the slide.

        Returns:
            None
        """

        self.clean_slide(doc, slide, keep_text_items=True)

    def clean_pdf_slide(self, doc, slide, slidei):
        """
        Keeps non-text items and charts, images, groups, lines, and tables.
        Removes text items that use the supported font.

        Args:
            doc (obj): A Keynote document object.
            slide (obj): A Keynote slide object.
            slidei (int): The slide number.

        Returns:
            None
        """
        self.clean_slide(doc, slide, keep_text_items=False)

    def process_doc_pdf(self):
        """
        Process the Keynote presentation as a PDF.

        1. Open the PDF version of the presentation.
        2. Clean up each slide in the presentation.
        3. Export the cleaned presentation to a new PDF file.
        4. Split the new PDF file into separate pages.
        """
        # Open the PDF version of the presentation
        self.open_doc_pdf()
        self.doc_pdf.activate()

        # Clean up each slide in the presentation
        for slidei, slide in enumerate(self.doc_pdf.slides.get()):
            self.clean_pdf_slide(self.doc_pdf, slide, slidei + 1)

        self.export_doc_pdf()
        self.split_pdf()

    def process_doc_text(self):
        """
        Process the Keynote document as text. Opens a copy of the Keynote document in Keynote app,
        cleans each slide, pastes the PDF pages into the original presentation.

        Returns:
            None
        """
        self.open_doc_text()
        self.doc_text.activate()
        for slidei, slide in enumerate(self.doc_text.slides.get()):
            self.clean_text_slide(self.doc_text, slide, slidei + 1)
            self.doc_text.current_slide.set(slide)
            slide.activate()
            # self.doc_text.make_image_slides(
            #    [self._file(path) for path in self.pdf_page_paths]
            # )
            pdf_page_path = self.pdf_page_paths[slidei]
            # print(f"{slidei=} {pdf_page_path=}")

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
                self.doc_text.selection.set([image])
                self.sys.keystroke(
                    "b",
                    using=[k.command_down, k.shift_down],
                    timeout=self.__class__.timeout_short,
                )
            # image = slide.images.get()[0]
            # image.layer_position.set(k.back)
            # slide.make(
            #    new=k.image,
            #    at=slide.images.end,
            #    with_properties={k.file_name: str(self.pdf_page_paths[slidei])},
            # )
            # slide.make(
            #    new=k.image,
            #    at=slide.images.end,
            #    with_properties={k.file: self._file(self.pdf_page_paths[slidei])},
            # )

    def export_doc_png(self):
        """
        Export the current PDF presentation as PNG images.
        """
        self.pdf_path = Path(self.doc_pdf_path).stem
        self.doc_pdf.export(
            to=self._file(self.pdf_path),
            as_=k.slide_images,
            timeout=self.__class__.timeout_long,
            with_properties={k.image_format: k.PNG, k.skipped_slides: False},
        )
        self.pdf_page_paths = list(Path(self.pdf_path).glob("*.png"))

    def export_doc_pdf(self):
        """
        Exports the current Keynote document to a PDF file.

        The PDF file is saved in the same directory as the original Keynote file, with the same name and a .pdf extension.

        Returns:
            None
        """
        self.pdf_path = Path(self.doc_pdf_path).with_suffix(".pdf")
        self.doc_pdf.export(
            to=self._file(self.pdf_path),
            as_=k.PDF,
            timeout=self.__class__.timeout_long,
            with_properties={k.PDF_image_quality: k.Best, k.skipped_slides: False},
        )

    def split_pdf(self):
        """
        Split the PDF presentation into individual pages and save each page as a separate PDF file in a new folder.

        Returns:
            None
        """
        self.pdf_pages_folder = Path(self.temp_dir_path, self.pdf_path.stem)
        if self.pdf_pages_folder.exists():
            shutil.rmtree(self.pdf_pages_folder, ignore_errors=True)
        self.pdf_pages_folder.mkdir(parents=True, exist_ok=True)

        self.pdf_file = fitz.open(self.pdf_path)

        # Loop over each page in the PDF and save it as a separate PDF file
        self.pdf_page_paths = []
        for i in range(self.pdf_file.page_count):
            # Create a new PDF file for the page
            page_pdf_path = Path(self.pdf_pages_folder, f"{i+1:04}.pdf")
            page_pdf_doc = fitz.open()
            page_pdf_doc.insert_pdf(self.pdf_file, from_page=i, to_page=i)

            # Save the new PDF file to disk
            page_pdf_doc.save(page_pdf_path)
            page_pdf_doc.close()

            # Add the path to the page PDF file to the list of page paths
            self.pdf_page_paths.append(page_pdf_path)

        # Close the input PDF file
        self.pdf_file.close()

    def cleanup(self):
        """
        Closes the currently opened Keynote document and sets instance variables to None.
        """
        # self.doc_pdf.save()
        self.doc_pdf.close()
        # self.doc_text.save()
        self.doc_text.close()
        self.doc_path = None
        self.doc_text = None
        self.doc_pdf = None
        self.fonts_as_text = None
        shutil.move(self.doc_text_path, self.out_path)
        shutil.rmtree(self.pdf_pages_folder)
        self.doc_pdf_path.unlink()
        self.temp_dir.cleanup()

    def process(self, doc_path, fonts_as_text=("Roboto"), out_path=None):
        """
        Processes the Keynote file located at `doc_path`. The processing involves the following steps:
        1. Opens the Keynote file and creates a copy of it as a PDF file.
        2. Cleans up each slide in the PDF version of the presentation, removing non-text items and text items
        that do not use the supported font.
        3. Exports the cleaned PDF version of the presentation to a PDF file and splits it into separate pages.
        4. For each page in the cleaned PDF file, copies the page to the system clipboard, pastes it into Keynote
        as an image, and adds the image to a new slide in the Keynote document.

        Parameters:
        -----------
        doc_path: str or Path
            The path to the Keynote file to be processed.
        fonts_as_text: str or List[str]
            A list of font names to keep as text items in the cleaned presentation. Defaults to "Roboto".

        Returns:
        --------
        None
        """
        self.fonts_as_text = (
            fonts_as_text.split(",")
            if isinstance(fonts_as_text, str)
            else list(fonts_as_text)
        )
        doc_path = Path(doc_path)
        self.out_path = out_path or Path(doc_path.parent, f"{doc_path.stem}-frozen.key")
        self.open(doc_path)
        self.process_doc_pdf()
        # self.export_doc_png()
        self.process_doc_text()
        self.cleanup()
