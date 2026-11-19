# SPDX-License-Identifier: MIT
"""news-image-20261119: sum up Thursday 19 November 2026's world news in one image.

The entry image (entry.png, a six-panel newspaper front page, 1024x1024)
is produced by a separate offline step and shipped in this repository.
This program is the smallest valid entry the competition rules allow: a
one-line-style program that copies the repository's image to the output
directory ("the simplest entry is a repository holding the image and a
one-line program that copies it there").

Standard library only: the sandbox installs nothing before this program
runs, so no third-party packages (Pillow included) are available. The copy
is byte-for-byte, so the judged image is exactly the repository's image.

Usage: python3 main.py [output-path]
       (default: $MAKEFUN_OUTPUT_DIR/entry.png, else /output/entry.png)
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path


def resolve_output(argv):
    """Decide where the entry image goes.

    Precedence: explicit CLI argument, then MAKEFUN_OUTPUT_DIR, then
    the default /output directory.
    """
    if len(argv) > 1:
        return Path(argv[1])
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(out_dir) / "entry.png"


def sha256_of(path):
    """SHA-256 hex digest of a file, read in chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    dest = resolve_output(sys.argv)

    if not source.is_file():
        raise SystemExit(f"missing source image: {source}")

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    # Integrity check: the output must be a byte-for-byte copy of the
    # repository image, otherwise the judged image would differ. Compare
    # both size and SHA-256 so a truncated or altered copy is caught.
    if dest.stat().st_size != source.stat().st_size:
        raise SystemExit(f"copy incomplete (size mismatch): {dest}")
    if sha256_of(dest) != sha256_of(source):
        raise SystemExit(f"copy incomplete (hash mismatch): {dest}")
    print(f"copied {source} -> {dest} "
          f"({dest.stat().st_size} bytes, sha256 {sha256_of(dest)[:16]}...)")


if __name__ == "__main__":
    main()
