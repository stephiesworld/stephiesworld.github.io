"""Language-specific extraction, behind one interface.

Every extractor turns source text into `CallSite` + `ModelRef` objects. Checks
never touch a syntax tree directly, so adding a language means adding an
extractor — not touching 8 check modules.
"""

from __future__ import annotations

from typing import Protocol

from ..model import CallSite, ModelRef


class Extractor(Protocol):
    suffixes: tuple[str, ...]

    def extract(self, path: str, source: str) -> tuple[list[CallSite], list[ModelRef]]: ...


def get_extractors() -> list[Extractor]:
    from . import javascript, python

    return [python.PythonExtractor(), javascript.JavaScriptExtractor()]


def for_path(path: str) -> Extractor | None:
    for ex in get_extractors():
        if path.endswith(ex.suffixes):
            return ex
    return None
