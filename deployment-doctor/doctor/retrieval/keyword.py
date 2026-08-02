"""Keyword retrieval (BM25). No API key, no network, no vector database.

BM25 is the algorithm search engines used for decades before embeddings. It
ranks a document higher when it contains the query's words, with two sensible
adjustments:

  * A rare word counts for more than a common one. Matching "budget_tokens"
    tells you far more than matching "the".
  * Repeating a word helps, but with diminishing returns. A page saying
    "caching" nine times isn't nine times more about caching than one saying it
    three times.

That's the whole idea. It is unfashionable and it is very often the right
answer, because for technical documentation the user's words and the
document's words are usually the same words. Reach for embeddings when you can
demonstrate that failing — not before.
"""

from __future__ import annotations

import math
import re
from collections import Counter

from . import Chunk, Hit

_TOKEN = re.compile(r"[a-z0-9_.\-]+")

# BM25 knobs. The published defaults; not worth tuning until you have an eval set.
K1 = 1.5  # how fast repeat matches stop helping
B = 0.75  # how much to penalise long documents

_STOPWORDS = frozenset(
    """a an and are as at be but by do does for from has have how i if in into is it its
    of on or that the their there these they this to was what when where which who why
    will with you your""".split()
)


def tokenize(text: str) -> list[str]:
    """Lowercase, split on non-word characters, drop filler words.

    `.-_` are kept inside tokens on purpose: `budget_tokens`, `claude-opus-5`
    and `output_config.format` are single meaningful terms in this domain, and
    splitting them would lose the exact thing a user is most likely to search
    for.
    """
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOPWORDS and len(t) > 1]


class KeywordRetriever:
    """BM25 over an in-memory list of chunks."""

    def __init__(self) -> None:
        self.chunks: list[Chunk] = []
        self._tokens: list[list[str]] = []
        self._freqs: list[Counter[str]] = []
        self._doc_freq: Counter[str] = Counter()
        self._avg_len: float = 0.0

    def index(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self._tokens = []
        self._freqs = []
        self._doc_freq = Counter()

        for chunk in chunks:
            # The heading trail is indexed alongside the body, so a question
            # phrased in the words of a section title still finds it.
            tokens = tokenize(" ".join(chunk.heading_path) + " " + chunk.text)
            self._tokens.append(tokens)
            freq = Counter(tokens)
            self._freqs.append(freq)
            self._doc_freq.update(freq.keys())

        self._avg_len = (sum(len(t) for t in self._tokens) / len(self._tokens)) if self._tokens else 0.0

    def search(self, query: str, k: int = 5) -> list[Hit]:
        if not self.chunks:
            return []

        query_terms = tokenize(query)
        n = len(self.chunks)
        scored: list[Hit] = []

        for i, chunk in enumerate(self.chunks):
            freq = self._freqs[i]
            length = len(self._tokens[i])
            score = 0.0
            matched: list[str] = []

            for term in set(query_terms):
                tf = freq.get(term, 0)
                if tf == 0:
                    continue
                matched.append(term)
                df = self._doc_freq[term]
                # Rarer term -> larger idf -> bigger contribution.
                idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
                denom = tf + K1 * (1 - B + B * (length / self._avg_len if self._avg_len else 1))
                score += idf * (tf * (K1 + 1)) / denom

            if score > 0:
                scored.append(Hit(chunk=chunk, score=score, matched=tuple(sorted(matched))))

        scored.sort(key=lambda h: (-h.score, h.chunk.doc_id, h.chunk.start_line))
        return scored[:k]
