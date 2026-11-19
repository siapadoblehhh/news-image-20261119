#!/usr/bin/env python3
"""Sum up 19 November's world news in one image.

Writes the entry image to /output/entry.png.

The image is a fixed asset held in this repository (entry.png). This program
copies it byte for byte, so every run produces the same file: no network,
no randomness, no clock, no environment input.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET = "/output/entry.png"


def main() -> int:
    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    return 0


if __name__ == "__main__":
    sys.exit(main())
