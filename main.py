#!/usr/bin/env python3
"""Monday Morning Punchlines — one joke about Monday mornings.

Writes the entry joke to ``$MAKEFUN_OUTPUT_DIR/entry.txt``
(default ``/output/entry.txt``), then reads it back and verifies the
bytes match exactly, so what the judge sees is what we wrote.
"""

import os
import sys

ENTRY = "I asked Monday for a rain check, and it rained deadlines instead."

MAX_CHARS = 200
TERMINAL_PUNCTUATION = ".!?"


def validate(text: str) -> None:
    """Enforce the competition gate before writing anything."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) != len(text.strip()):
        raise ValueError("entry must not have leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text[-1] not in TERMINAL_PUNCTUATION:
        raise ValueError("entry must end with terminal punctuation")
    # One sentence: no sentence-ending punctuation mid-text.
    body = text[:-1]
    if any(ch in TERMINAL_PUNCTUATION for ch in body):
        raise ValueError("entry must be a single sentence")
    if "monday" not in text.lower():
        raise ValueError("entry must be about Monday")


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.txt")
    # MAKEFUN_OUTPUT_DIR is a directory in the harness; tolerate being
    # given the full file path instead.
    if out_dir.endswith("entry.txt"):
        out_path = out_dir
    else:
        out_path = os.path.join(out_dir, "entry.txt")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    data = ENTRY.encode("utf-8")
    with open(out_path, "wb") as fh:
        fh.write(data)
    with open(out_path, "rb") as fh:
        written = fh.read()
    if written != data:
        raise SystemExit("read-back mismatch: entry.txt bytes differ")
    print("wrote %d characters to %s" % (len(ENTRY), out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
