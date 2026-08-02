"""Turn a folder of Markdown into searchable chunks.

Chunking is where most retrieval systems are quietly ruined, so this file is
worth reading even though it's short.

The naive approach — cut every 500 characters — is fast to write and produces a
system that confidently retrieves the wrong thing. Two reasons:

  1. It cuts mid-sentence and mid-table, so a chunk can contain half a fact.
  2. It throws away structure. "The minimum is 4096 tokens" is a useless
     sentence once it's been separated from the heading that said which model
     it applies to. The retriever will happily return it for a question about a
     completely different model, and the answer will read as authoritative.

So this splits on headings instead, and every chunk remembers the trail of
headings above it. Long sections are split further, and each piece keeps the
same heading trail — so the context survives the split.
"""

from __future__ import annotations

import re
from pathlib import Path

from . import Chunk

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")

# Chunks bigger than this get split. Roughly a screenful — big enough to hold a
# complete thought, small enough that five of them don't flood the prompt.
MAX_CHARS = 1400
# Overlap between split pieces, so a fact sitting on the boundary appears whole
# in at least one of them.
OVERLAP_CHARS = 200


def load_corpus(root: Path, suffixes: tuple[str, ...] = (".md", ".markdown", ".txt")) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in suffixes:
            doc_id = str(path.relative_to(root))
            chunks.extend(chunk_markdown(doc_id, path.read_text(encoding="utf-8", errors="replace")))
    return chunks


def chunk_markdown(doc_id: str, text: str) -> list[Chunk]:
    lines = text.splitlines()
    chunks: list[Chunk] = []

    heading_stack: list[tuple[int, str]] = []  # (level, title)
    buffer: list[str] = []
    buffer_start = 1

    def flush(end_line: int) -> None:
        body = "\n".join(buffer).strip()
        if not body:
            return
        path = tuple(title for _, title in heading_stack)
        for piece, offset in _split_long(body):
            chunks.append(
                Chunk(doc_id=doc_id, heading_path=path, text=piece, start_line=buffer_start + offset)
            )

    for i, line in enumerate(lines, start=1):
        match = _HEADING.match(line)
        if not match:
            buffer.append(line)
            continue

        # A heading closes the previous section.
        flush(i)
        buffer = []
        buffer_start = i

        level = len(match.group(1))
        title = match.group(2).strip()
        # Pop headings at the same or deeper level: a new "## B" replaces "## A"
        # but stays underneath "# Top".
        while heading_stack and heading_stack[-1][0] >= level:
            heading_stack.pop()
        heading_stack.append((level, title))

    flush(len(lines) + 1)
    return chunks


def _split_long(body: str) -> list[tuple[str, int]]:
    """Split an oversized section on paragraph boundaries, with overlap."""
    if len(body) <= MAX_CHARS:
        return [(body, 0)]

    paragraphs = body.split("\n\n")
    pieces: list[tuple[str, int]] = []
    current: list[str] = []
    line_offset = 0
    current_offset = 0

    for para in paragraphs:
        candidate = "\n\n".join(current + [para])
        if current and len(candidate) > MAX_CHARS:
            joined = "\n\n".join(current)
            pieces.append((joined, current_offset))
            # Carry the tail forward so a fact on the seam survives in one piece.
            tail = joined[-OVERLAP_CHARS:]
            current = [tail, para] if tail.strip() else [para]
            current_offset = line_offset
        else:
            current.append(para)
        line_offset += para.count("\n") + 2

    if current:
        pieces.append(("\n\n".join(current), current_offset))
    return pieces
