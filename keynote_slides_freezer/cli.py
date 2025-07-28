#!/usr/bin/env python3

import fire

from .keynote_slides_freezer import KeynoteSlidesFreezer


def main():
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    key = KeynoteSlidesFreezer()
    fire.Fire(key.process)


if __name__ == "__main__":
    main()
