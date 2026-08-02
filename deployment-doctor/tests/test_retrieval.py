"""Tests for the retrieval layer.

These double as the honest record of what keyword search can and cannot do.
The failure tests matter more than the success tests: a retrieval system that
is never shown failing is one nobody knows the limits of.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from doctor.retrieval import Chunk
from doctor.retrieval.corpus import MAX_CHARS, chunk_markdown, load_corpus
from doctor.retrieval.embedding import (
    EmbeddingRetriever,
    HashingEmbedder,
    overfetch_and_filter,
)
from doctor.retrieval.keyword import KeywordRetriever, tokenize

CORPUS = Path(__file__).parent.parent / "corpus"


@pytest.fixture(scope="module")
def retriever() -> KeywordRetriever:
    r = KeywordRetriever()
    r.index(load_corpus(CORPUS))
    return r


# --------------------------------------------------------------------------- #
# chunking
# --------------------------------------------------------------------------- #


def test_chunks_carry_their_heading_trail():
    """The whole point of splitting on headings. A chunk saying 'the minimum is
    4096 tokens' is useless without the heading that said which model."""
    doc = "# Guide\n\nintro\n\n## Caching\n\n### Minimums\n\nThe minimum is 4096 tokens.\n"
    chunks = chunk_markdown("guide.md", doc)
    deepest = [c for c in chunks if "4096" in c.text]
    assert deepest
    assert deepest[0].heading_path == ("Guide", "Caching", "Minimums")
    assert deepest[0].title == "Guide › Caching › Minimums"


def test_sibling_heading_replaces_rather_than_nests():
    doc = "# Top\n\n## A\n\nalpha\n\n## B\n\nbeta\n"
    chunks = chunk_markdown("d.md", doc)
    paths = {c.text.strip(): c.heading_path for c in chunks}
    assert paths["alpha"] == ("Top", "A")
    assert paths["beta"] == ("Top", "B")  # not ("Top", "A", "B")


def test_long_sections_split_but_keep_context():
    body = "\n\n".join(f"Paragraph {i}. " + ("filler " * 40) for i in range(12))
    chunks = chunk_markdown("big.md", f"# Doc\n\n## Section\n\n{body}\n")
    assert len(chunks) > 1
    # Every piece still knows which section it came from.
    assert all(c.heading_path == ("Doc", "Section") for c in chunks)
    assert all(len(c.text) <= MAX_CHARS + 400 for c in chunks)


def test_rendered_chunk_includes_its_source_and_title():
    chunk = Chunk(doc_id="a.md", heading_path=("Top", "Sub"), text="body", start_line=3)
    assert chunk.render() == "[a.md · Top › Sub]\nbody"


def test_corpus_loads():
    chunks = load_corpus(CORPUS)
    assert len(chunks) > 10
    assert {c.doc_id for c in chunks} >= {"models.md", "prompt-caching.md", "breaking-changes.md"}


# --------------------------------------------------------------------------- #
# tokenizing
# --------------------------------------------------------------------------- #


def test_domain_terms_survive_tokenizing():
    """`budget_tokens` and `claude-opus-5` are single terms here. Splitting them
    on punctuation would destroy exactly what people search for."""
    tokens = tokenize("Remove budget_tokens from claude-opus-5 and output_config.format")
    assert "budget_tokens" in tokens
    assert "claude-opus-5" in tokens
    assert "output_config.format" in tokens


def test_filler_words_are_dropped():
    assert tokenize("what is the and of") == []


# --------------------------------------------------------------------------- #
# keyword search — where it works
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("query", "expected_doc"),
    [
        ("minimum cacheable prefix tokens", "prompt-caching.md"),
        ("budget_tokens removed", "breaking-changes.md"),
        ("claude-opus-5 pricing", "models.md"),
        ("retired model 404", "models.md"),
        ("assistant prefill 400", "breaking-changes.md"),
    ],
)
def test_finds_the_right_document_when_words_match(retriever, query, expected_doc):
    hits = retriever.search(query, k=3)
    assert hits, f"no hits for {query!r}"
    assert any(h.chunk.doc_id == expected_doc for h in hits)


def test_every_hit_can_explain_itself(retriever):
    """Retrieval fails silently. A hit that can't say which words matched is a
    hit nobody can debug."""
    for hit in retriever.search("prompt caching minimum", k=5):
        assert hit.matched
        assert hit.score > 0


def test_results_are_ranked_and_capped(retriever):
    hits = retriever.search("caching", k=3)
    assert len(hits) <= 3
    assert [h.score for h in hits] == sorted((h.score for h in hits), reverse=True)


def test_empty_index_returns_nothing():
    assert KeywordRetriever().search("anything") == []


# --------------------------------------------------------------------------- #
# keyword search — where it fails, which matters more
# --------------------------------------------------------------------------- #


def test_paraphrased_question_retrieves_junk(retriever):
    """The honest limitation, pinned so it can't quietly change.

    "my bill went up after upgrading" is really about the cache-minimum trap.
    Keyword search cannot know that: it matches the filler words 'went' and
    'after' and returns unrelated sections with confident-looking scores.

    This is the case that justifies meaning-based search — and the reason to
    keep a written set of real questions rather than trusting a demo query.
    """
    hits = retriever.search("my bill went up after upgrading", k=3)
    assert hits, "expected junk hits, not zero hits — that's the point"
    matched = {word for hit in hits for word in hit.matched}
    # It matched on filler, not on anything meaningful.
    assert matched <= {"went", "after", "up", "my", "bill", "upgrading"}
    assert "cacheable" not in matched


def test_no_shared_vocabulary_means_no_results(retriever):
    assert retriever.search("photosynthesis chlorophyll") == []


# --------------------------------------------------------------------------- #
# k
# --------------------------------------------------------------------------- #


def test_k_is_a_guess_you_make_before_you_know_the_answer(retriever):
    """Small k cuts off the answer you needed, and nothing tells you.

    Someone asking about token counts could mean either the cache-minimum table
    or the tokenizer change — two different documents. At k=1 they get only the
    first, with no signal that the other exists. This is why "what should k be"
    has no answer without a written set of real questions.
    """
    query = "tokens"
    narrow = {h.chunk.doc_id for h in retriever.search(query, k=1)}
    wide = {h.chunk.doc_id for h in retriever.search(query, k=5)}

    assert narrow == {"prompt-caching.md"}
    assert "breaking-changes.md" in wide, "widening k surfaces what k=1 cut off"
    assert narrow < wide


def test_overfetch_and_filter_removes_the_guess(retriever):
    """The practical answer to picking k: fetch generously, then judge.

    The judge here is a stub predicate so the test runs offline. In production
    it is a small model call per candidate — the point is the shape, not this
    particular rule.
    """
    query = "cache minimum"

    def judge(_q, chunk) -> bool:
        return "minimum" in chunk.text.lower()

    raw = overfetch_and_filter(retriever, query, fetch=20)
    kept = overfetch_and_filter(retriever, query, fetch=20, judge=judge)

    assert len(kept) < len(raw), "the filter should discard something"
    assert all("minimum" in h.chunk.text.lower() for h in kept)


# --------------------------------------------------------------------------- #
# the embedding path
# --------------------------------------------------------------------------- #


def test_embedding_retriever_runs_end_to_end():
    """Exercises the plumbing with an offline stand-in. HashingEmbedder is NOT
    semantic — this proves the code path works, not that it retrieves well."""
    r = EmbeddingRetriever(HashingEmbedder(dims=128))
    r.index(load_corpus(CORPUS))
    hits = r.search("prompt caching minimum", k=3)
    assert len(hits) == 3
    assert all(-1.0001 <= h.score <= 1.0001 for h in hits)


def test_embedding_retriever_handles_an_empty_corpus():
    r = EmbeddingRetriever(HashingEmbedder())
    r.index([])
    assert r.search("anything") == []


def test_both_retrievers_satisfy_the_same_interface():
    """Callers never learn which one they got — that's what makes swapping one
    for the other a one-line change rather than a rewrite."""
    chunks = load_corpus(CORPUS)
    for r in (KeywordRetriever(), EmbeddingRetriever(HashingEmbedder(dims=64))):
        r.index(chunks)
        hits = r.search("caching", k=2)
        assert len(hits) <= 2
        assert all(hasattr(h, "chunk") and hasattr(h, "score") for h in hits)
