#!/usr/bin/env python3

"""The setup script."""

import re
from pathlib import Path
from setuptools import find_packages, setup

NAME = "keynote_slides_freezer"


def get_version(*args):
    verstrline = open(Path(NAME, "__init__.py"), "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    return mo[1] if (mo := re.search(VSRE, verstrline, re.M)) else "undefined"


requirements = []

test_requirements = []

setup(
    author="Adam Twardoch",
    author_email="adam+github@twardoch.com",
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    description="Python tool to 'freeze' a Keynote slidehow: keeps only text objects that use specified fonts as text, exports to PDF slides from the rest and builds a new deck that has the PDFs plus the 'safe' text boxes",
    entry_points={
        "console_scripts": [
            "keynote_freezer=keynote_slides_freezer.cli:main",
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=open(
        Path(Path(__file__).parent, "README.md"), "r", encoding="utf-8"
    ).read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords=[
        "apple",
        "keynote",
        "macos",
    ],
    name=f"{NAME}",
    packages=find_packages(include=["keynote_slides_freezer"]),
    url="https://github.com/twardoch/keynote-slides-freezer",
    version=get_version(),
    zip_safe=False,
)
