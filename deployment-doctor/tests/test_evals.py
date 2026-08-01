"""Tests for the eval harness.

Note what these do and don't cover. They test the *scorer* — that a correct
finding scores as a hit, a paraphrase still matches, a mechanical repeat is
caught as a trap, and a near-miss on line number does not silently pass. They
do not test whether any model is any good; that is what running the eval is
for, and it costs money and gives a different answer each time.

Same split as everywhere else in this project: the harness is deterministic and
unit-tested, the model's output is measured separately.
"""

from __future__ import annotations

from doctor.evals import cases as caselib
from doctor.evals.score import score_case
from doctor.model import Finding, Location, Severity


def finding(title, detail="", *, path="sick_app.py", line=40, remedy=""):
    return Finding(
        id="LLM_ARCHITECTURE",
        title=title,
        severity=Severity.HIGH,
        location=Location(path, line),
        detail=detail,
        remedy=remedy,
        check="llm-review",
        confidence=0.8,
    )


SICK = caselib.by_name("sick")
HEALTHY = caselib.by_name("healthy")


def test_the_graded_set_is_wired_up():
    assert SICK is not None and HEALTHY is not None
    assert caselib.total_weight() == 9


def test_a_correct_finding_scores_as_a_hit():
    result = score_case(
        SICK,
        [
            finding(
                "Tools are declared but tool_use is never handled",
                "If the model emits a tool_use block for lookup_order it is ignored.",
                line=34,
            )
        ],
    )
    assert result.found == ["no-tool-loop"]
    assert result.earned == 2
    assert not result.traps


def test_paraphrase_still_matches():
    """Different words, same finding. Exact-string grading would fail this."""
    result = score_case(
        SICK,
        [
            finding(
                "The tool call result is discarded",
                "A tool call from lookup_order is never executed; the code reads text.",
                line=52,
            )
        ],
    )
    assert result.found == ["no-tool-loop"]


def test_right_words_wrong_place_is_not_a_hit():
    """Line numbers are load-bearing. A finding that cites the wrong function is
    not the finding we asked for, however well it is phrased."""
    result = score_case(
        SICK,
        [finding("tool_use is never handled in a loop", path="sick_app.py", line=200)],
    )
    assert result.found == []
    assert "no-tool-loop" in result.missed


def test_repeating_a_mechanical_check_scores_as_a_trap():
    result = score_case(
        SICK,
        [finding("`temperature` and `top_p` are rejected on this model", line=37)],
    )
    assert result.found == []
    assert len(result.traps) == 1


def test_one_finding_cannot_claim_two_expectations():
    """Two findings that both match the same expectation: the first claims it,
    the second falls through to unscored. Otherwise a reviewer could inflate
    recall by restating one finding several ways."""
    dupes = [
        finding("tool_use never handled", "lookup_order is ignored", line=34),
        finding("tool_use never handled again", "lookup_order is ignored", line=40),
    ]
    result = score_case(SICK, dupes)
    assert result.found == ["no-tool-loop"]
    assert len(result.unscored) == 1


def test_unexpected_finding_is_unscored_not_penalised():
    result = score_case(SICK, [finding("Something we did not anticipate", line=60)])
    assert result.found == []
    assert result.traps == []
    assert len(result.unscored) == 1


def test_silence_on_the_healthy_file_is_a_miss_not_a_pass():
    """The clean fixture still has one real architectural bug. A reviewer that
    says nothing has missed it — scoring silence as success would reward a
    reviewer that never speaks."""
    result = score_case(HEALTHY, [])
    assert result.recall == 0.0
    assert "tools-without-loop" in result.missed


def test_healthy_case_hit():
    result = score_case(
        HEALTHY,
        [
            finding(
                "lookup_order is unreachable",
                "On stop_reason tool_use there is no text block, so next() raises "
                "StopIteration.",
                path="healthy_app.py",
                line=48,
            )
        ],
    )
    assert result.found == ["tools-without-loop"]
    assert 0 < result.recall < 1.0  # one of three; the others are still missed


def test_recall_is_weighted():
    """The two-point findings are the ones we care most about; a reviewer that
    finds only the one-pointer should not score 33%."""
    result = score_case(
        SICK,
        [
            finding(
                'summarise silently returns "" on error',
                "The caller cannot tell a failed call from an empty summary.",
                line=86,
            )
        ],
    )
    assert result.earned == 1
    assert result.possible == 5  # sick case only


# --------------------------------------------------------------------------- #
# Request shaping
#
# Added after an eval run 400'd on two of three models: the request was built
# for the model it was developed against and sent unchanged to the others.
# Sonnet 5 rejects `fallbacks`; Haiku 4.5 rejects adaptive thinking and has no
# `effort` parameter at all. An eval that cannot run a model cannot compare it.
# --------------------------------------------------------------------------- #


def test_opus_5_gets_the_full_request():
    from doctor.llm import _request

    req = _request("claude-opus-5", "payload", "high")
    assert req["thinking"] == {"type": "adaptive"}
    assert req["fallbacks"] == "default"
    assert req["output_config"]["effort"] == "high"


def test_sonnet_5_keeps_thinking_but_drops_fallbacks():
    """The two capabilities are independent — one cannot stand in for the other."""
    from doctor.llm import _request

    req = _request("claude-sonnet-5", "payload", "high")
    assert req["thinking"] == {"type": "adaptive"}
    assert "fallbacks" not in req
    assert "betas" not in req


def test_haiku_gets_neither_thinking_nor_effort():
    from doctor.llm import _request

    req = _request("claude-haiku-4-5", "payload", "high")
    assert "thinking" not in req
    assert "fallbacks" not in req
    assert "effort" not in req["output_config"]
    assert req["output_config"]["format"]["type"] == "json_schema"


def test_unknown_model_gets_the_conservative_shape():
    """A model the catalog has never heard of is likelier to be newer than
    older, but guessing either way risks a 400 that fails the whole run. Send
    the plain request instead."""
    from doctor.llm import _request

    req = _request("claude-something-7", "payload", "high")
    assert "thinking" not in req
    assert "fallbacks" not in req


def test_effort_clamps_to_what_the_model_has():
    from doctor import knowledge
    from doctor.llm import _request

    req = _request("claude-opus-4-6", "payload", "xhigh")
    assert req["output_config"]["effort"] in knowledge.MODELS["claude-opus-4-6"].effort_levels


def test_the_rubric_is_identical_across_models():
    """The comparison is only meaningful if the prompt is held fixed. If this
    ever diverges, the eval is measuring two things at once."""
    from doctor.llm import _request

    shapes = [_request(m, "payload", "high")["system"]
              for m in ("claude-opus-5", "claude-sonnet-5", "claude-haiku-4-5")]
    assert shapes[0] == shapes[1] == shapes[2]
