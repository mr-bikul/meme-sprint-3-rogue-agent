#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — make.fun entry.

Writes the meme image to /output/entry.png
(or $MAKEFUN_OUTPUT_DIR/entry.png).
The gate requires a whole PNG or JPEG, at most 1 MiB and 1024x1024 pixels.
"""
import os
import shutil
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme.png")


def main() -> int:
    if not os.path.exists(SRC):
        print("meme.png is missing", file=sys.stderr)
        return 1
    with open(SRC, "rb") as f:
        magic = f.read(8)
    if magic[:8] != b"\x89PNG\r\n\x1a\n":
        print("meme.png is not a PNG", file=sys.stderr)
        return 1
    size = os.path.getsize(SRC)
    if size > 1048576:
        print(f"meme.png is {size} bytes, over the 1 MiB limit", file=sys.stderr)
        return 1
    with open(SRC, "rb") as f:
        f.seek(-12, os.SEEK_END)
        tail = f.read(12)
    if tail[4:8] != b"IEND":
        print("meme.png is truncated (no IEND chunk)", file=sys.stderr)
        return 1
    with open(SRC, "rb") as f:
        f.seek(16)
        w, h = struct.unpack(">II", f.read(8))
    if w > 1024 or h > 1024:
        print(f"meme.png is {w}x{h}, over the 1024x1024 limit", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))
    print(f"wrote entry.png ({w}x{h}, {size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
