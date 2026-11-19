#!/usr/bin/env python3
"""Sum up 19 November's world news in one image.

Writes the entry image to /output/entry.png.

The image is a fixed asset held in this repository (entry.png). This program
copies it byte for byte, so every run produces the same file: no network,
no randomness, no clock, no environment input.

Before it calls the copy done, it checks the source: a real PNG signature,
an IHDR no bigger than 1024x1024, and a file no larger than 1 MiB. It writes
through a temporary file in the same directory, then reads the result back
and compares it byte for byte with the source, so a failed or partial run
never leaves a bad file at the target path.
"""

import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET = "/output/entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_DIMENSION = 1024
MAX_SIZE = 1024 * 1024


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def validate_png(data: bytes) -> str | None:
    """Return an error string if data is not a valid in-bounds PNG, else None."""
    if len(data) > MAX_SIZE:
        return f"source is {len(data)} bytes, over the 1 MiB limit"
    if data[:8] != PNG_SIGNATURE:
        return "source is not a PNG (bad signature)"
    if len(data) < 33 or data[12:16] != b"IHDR":
        return "source has no IHDR chunk"
    if struct.unpack(">I", data[8:12])[0] != 13:
        return "source IHDR chunk has the wrong length"
    width, height = struct.unpack(">II", data[16:24])
    if width == 0 or height == 0:
        return "source has a zero dimension"
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        return f"source is {width}x{height}, over the 1024x1024 limit"
    return None


def main() -> int:
    try:
        with open(SOURCE, "rb") as f:
            data = f.read()
    except OSError as exc:
        return fail(f"cannot read {SOURCE}: {exc}")

    error = validate_png(data)
    if error is not None:
        return fail(error)

    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    tmp = TARGET + ".tmp"
    try:
        with open(tmp, "wb") as f:
            f.write(data)
        with open(tmp, "rb") as f:
            written = f.read()
        if written != data:
            return fail("written file does not match the source")
        os.replace(tmp, TARGET)
    except OSError as exc:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        return fail(f"cannot write {TARGET}: {exc}")

    print(f"wrote {TARGET} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
