"""Retrieval: find the few relevant pages in a pile too big to read.

The whole idea in one line: **search your documents, paste the results into the
prompt, ask the question.** That is all "RAG" means.

This package exists because of one real limitation in the tool. `knowledge.py`
is hand-maintained: model IDs, prices, retirement dates. It fits in a prompt, so
it needs no retrieval at all — which is exactly why the main analyser doesn't use
this package. But the moment you want to audit against the *full* documentation
set (every changelog, every migration note, years of release history), the facts
stop fitting, and you need a way to pull out only the handful of paragraphs that
matter for this particular question.

Two ways to do that, and the difference matters more than the code:

  keyword.py    Rank by word overlap. Boring, fast, free, no API key, and it
                beats fancier methods whenever the user's words match the
                document's words — which for technical docs is most of the time.

  embedding.py  Rank by meaning. Handles "how do I cancel" matching a page
                titled "ending your subscription". Costs an API call per
                document up front, plus one per query.

Both implement `Retriever`, so callers never learn which one they got. Start
with keyword; swap only when you can show it failing on real questions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class Chunk:
    """One searchable piece of a document.

    `heading_path` is the fix for the biggest beginner mistake in retrieval.
    Chopping a document into equal-sized blocks destroys the context that made
    each block meaningful — a paragraph reading "the minimum is 4096 tokens"
    is useless once separated from the heading that said which model. So every
    chunk carries the trail of headings above it, and that trail is prepended
    when the chunk is handed to the model.
    """

    doc_id: str
    heading_path: tuple[str, ...]
    text: str
    start_line: int

    @property
    def title(self) -> str:
        return " › ".join(self.heading_path) if self.heading_path else self.doc_id

    def render(self) -> str:
        """What actually gets pasted into the prompt."""
        return f"[{self.doc_id} · {self.title}]\n{self.text}"

    def __str__(self) -> str:
        return f"{self.doc_id}:{self.start_line} ({self.title})"


@dataclass
class Hit:
    chunk: Chunk
    score: float
    # Which query words were responsible. Retrieval is the part of a RAG system
    # that fails silently, so every hit has to be able to explain itself.
    matched: tuple[str, ...] = field(default_factory=tuple)


class Retriever(Protocol):
    """Every retrieval method looks like this from the outside."""

    def index(self, chunks: list[Chunk]) -> None: ...

    def search(self, query: str, k: int = 5) -> list[Hit]: ...
