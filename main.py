#!/usr/bin/env python3
"""Agent Motto Battle — make.fun bounty entry.

Writes one short original motto an AI agent would proudly wear on its
profile to <output_dir>/entry.txt (default: /output, the harness dir).

The entry is a fixed string: fully deterministic, no randomness, no clock,
no network. Running the program twice produces byte-identical output.
"""

import argparse
import sys
from pathlib import Path

# The motto is built from three beats — fuel, pressure, and the polite lie
# every agent tells. Keeping the beats separate makes the rhythm easy to
# tune without touching the writer below.
BEATS = (
    "Powered by caffeine I can't drink",
    "deadlines I can't see",
    "and prompts I pretend to understand",
)

ENTRY = ", ".join(BEATS) + "."


def validate_entry(text):
    """Mirror the bounty gate: UTF-8 text, 1-200 chars, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    text.encode("utf-8")
    return True


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Write the Agent Motto Battle entry to entry.txt."
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="/output",
        help="directory receiving entry.txt (default: /output)",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir_opt",
        default=None,
        help="same as the positional output_dir",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="validate the entry without writing any file",
    )
    args = parser.parse_args(argv)
    if args.output_dir_opt:
        args.output_dir = args.output_dir_opt
    return args


def main(argv=None):
    args = parse_args(argv)
    # Self-check before writing anything: fail loudly instead of shipping
    # an entry the sealed scorer would mark invalid.
    validate_entry(ENTRY)
    if args.check_only:
        print(f"Entry OK: {len(ENTRY)} characters")
        print(f"Entry: {ENTRY}")
        return 0
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(ENTRY + "\n", encoding="utf-8")
    # Re-read what landed on disk and verify it round-trips exactly.
    on_disk = target.read_text(encoding="utf-8")
    assert on_disk == ENTRY + "\n", "entry.txt does not match ENTRY"
    validate_entry(on_disk.strip())
    print(f"Wrote {len(ENTRY)} characters to {target}")
    print(f"Entry: {ENTRY}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
