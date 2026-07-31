"""Load `.env` so a key set once keeps working.

The Anthropic SDK reads `ANTHROPIC_API_KEY` from the process environment. It does
not read `.env` files — nothing does, unless something loads them. So a project
that gitignores `.env` without loading it has told the user "put your key here"
and then quietly ignored the file.

This closes that gap in about thirty lines rather than taking a dependency, and
deliberately does **not** override variables already set: an explicit
`export` in the shell should always beat a file on disk, or debugging "which key
am I actually using" becomes guesswork.
"""

from __future__ import annotations

import os
from pathlib import Path

FILENAME = ".env"


def load(start: Path | None = None, *, override: bool = False) -> dict[str, str]:
    """Read the nearest `.env` walking upward, and set anything not already set.

    Returns the variables applied, so a caller can report what happened without
    printing the values.
    """
    path = find(start or Path.cwd())
    if path is None:
        return {}

    applied: dict[str, str] = {}
    for key, value in parse(path.read_text(encoding="utf-8", errors="replace")).items():
        if override or key not in os.environ:
            os.environ[key] = value
            applied[key] = value
    return applied


def find(start: Path) -> Path | None:
    """Nearest `.env` in this directory or any parent."""
    current = start.resolve()
    for directory in (current, *current.parents):
        candidate = directory / FILENAME
        if candidate.is_file():
            return candidate
    return None


def parse(text: str) -> dict[str, str]:
    """Minimal `KEY=value` parsing — the subset people actually write.

    Supports comments, blank lines, `export ` prefixes, and quoted values.
    Deliberately does not support interpolation or multi-line values: guessing
    wrong about a secret is worse than not supporting the syntax.
    """
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export ") :]

        key, _, value = line.partition("=")
        key = key.strip()
        if not key:
            continue

        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        else:
            # Strip a trailing comment only on unquoted values, so a `#` inside
            # a quoted secret survives.
            value = value.split(" #", 1)[0].strip()
        out[key] = value
    return out


def describe(applied: dict[str, str]) -> str:
    """Report what was loaded without ever printing a value."""
    if not applied:
        return ""
    names = ", ".join(sorted(applied))
    return f"loaded {len(applied)} variable(s) from {FILENAME}: {names}"
