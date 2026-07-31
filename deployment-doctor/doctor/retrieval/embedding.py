"""Meaning-based retrieval — the thing people usually mean by "RAG".

The idea: turn every chunk into a list of numbers ("a vector") that represents
what it's *about*. Turn the question into numbers the same way. Then return the
chunks whose numbers point in the most similar direction. Because it compares
meaning rather than spelling, "how do I cancel" can find a page titled "ending
your subscription" — which keyword search would miss completely.

Two honest notes, both of which matter more than the code:

**1. This does not include a bundled embedding provider.** Anthropic's
documented API surface is the Messages API; embeddings come from a separate
provider you choose. So `EmbeddingRetriever` takes an `embed` function and does
not care where the numbers come from. Plug in whatever you already use. This is
also just better design — the swappable part stays swappable.

**2. Do not reach for this first.** It costs an API call per chunk to build the
index, plus one per query, plus somewhere to store the vectors. Keyword search
costs nothing and, for technical documentation, usually wins — because the words
in the question are the words in the docs. Use `KeywordRetriever` until you have
a written-down set of real questions it demonstrably fails, then switch. "We
used embeddings because that's what RAG means" is how teams end up maintaining a
vector database that performs worse than `grep`.
"""

from __future__ import annotations

import hashlib
import math
import re
from collections.abc import Callable, Sequence

from . import Chunk, Hit
from .keyword import tokenize

# Turns a batch of texts into a batch of vectors.
EmbedFn = Callable[[Sequence[str]], list[list[float]]]


class EmbeddingRetriever:
    """Cosine-similarity search over vectors from an `embed` function you supply."""

    def __init__(self, embed: EmbedFn) -> None:
        self.embed = embed
        self.chunks: list[Chunk] = []
        self._vectors: list[list[float]] = []

    def index(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        if not chunks:
            self._vectors = []
            return
        # The heading trail is embedded with the body for the same reason it is
        # indexed with the body in keyword search: a chunk stripped of its
        # section title has lost most of what made it meaningful.
        texts = [f"{c.title}\n{c.text}" for c in chunks]
        self._vectors = [_normalise(v) for v in self.embed(texts)]

    def search(self, query: str, k: int = 5) -> list[Hit]:
        if not self.chunks:
            return []
        query_vec = _normalise(self.embed([query])[0])
        hits = [
            Hit(chunk=chunk, score=_dot(query_vec, vec))
            for chunk, vec in zip(self.chunks, self._vectors)
        ]
        hits.sort(key=lambda h: (-h.score, h.chunk.doc_id, h.chunk.start_line))
        return hits[:k]


class HashingEmbedder:
    """A deterministic, offline stand-in for a real embedding provider.

    ⚠️ This is **not semantic**. It hashes words into buckets, so it behaves
    roughly like keyword matching wearing a vector costume. It exists so the
    embedding code path can be tested without a network call or an API key —
    never because it is a good retriever. If you ship this to production you
    have built a slower keyword search.
    """

    def __init__(self, dims: int = 256) -> None:
        self.dims = dims

    def __call__(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._one(t) for t in texts]

    def _one(self, text: str) -> list[float]:
        vec = [0.0] * self.dims
        for token in tokenize(text):
            digest = hashlib.blake2b(token.encode(), digest_size=8).digest()
            bucket = int.from_bytes(digest[:4], "big") % self.dims
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vec[bucket] += sign
        return vec


def _normalise(vec: Sequence[float]) -> list[float]:
    length = math.sqrt(sum(x * x for x in vec))
    return [x / length for x in vec] if length else list(vec)


def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


# --------------------------------------------------------------------------- #
# The answer to "how do I pick k"
# --------------------------------------------------------------------------- #

_RELEVANT = re.compile(r"^\s*(yes|relevant|keep)\b", re.IGNORECASE)


def overfetch_and_filter(
    retriever,
    query: str,
    *,
    fetch: int = 20,
    judge: Callable[[str, Chunk], bool] | None = None,
) -> list[Hit]:
    """Grab many, keep the ones that survive a second look.

    Picking k in advance is a guess: too small and the answer is missing, too
    large and it drowns in noise. This removes the guess. Fetch generously, then
    let a cheap judgement pass throw out what isn't actually relevant, and keep
    whatever is left — however many that turns out to be.

    `judge` is any predicate. In production it is usually a small, fast model
    call per candidate ("does this passage help answer the question? yes/no"),
    which is why it is injected rather than hardcoded: it keeps this function
    testable offline, and lets you start with a cheap heuristic before paying
    for a model.
    """
    candidates = retriever.search(query, k=fetch)
    if judge is None:
        return candidates
    return [hit for hit in candidates if judge(query, hit.chunk)]
