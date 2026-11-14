#!/usr/bin/env python3
"""make.fun news-image-01 entrypoint (stdlib only).

Copies the pre-rendered entry.png from the repo root to the output
directory. Deterministic: same bytes every run. No network, no other
files, no model calls.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)


if __name__ == "__main__":
    main()
