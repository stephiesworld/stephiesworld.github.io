"""Tests for the agentic reviewer.

The loop is driven by a stub client, so these run offline and deterministically.
This is also the answer to "how do you test an agent?": you don't assert on the
model's choices, you assert that the harness around them is correct — tool
results are paired to their tool_use blocks, errors are handed back rather than
raised, the sandbox holds, and the loop terminates.
"""

from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest

from doctor import agent

FIXTURES = Path(__file__).parent / "fixtures"
FILES = [FIXTURES / "sick_app.py", FIXTURES / "healthy_app.py"]


class Block:
    def __init__(self, **kw):
        self.type = kw.pop("type", "tool_use")
        for k, v in kw.items():
            setattr(self, k, v)


class Response:
    def __init__(self, content, stop_reason="tool_use"):
        self.content = content
        self.stop_reason = stop_reason
        self.usage = types.SimpleNamespace(
            input_tokens=100, output_tokens=50, cache_read_input_tokens=90
        )


def install_stub(monkeypatch, scripted):
    """Replay a scripted list of responses, recording what the loop sent back."""
    sent: list[list[dict]] = []

    class Messages:
        def create(self, **kwargs):
            sent.append(list(kwargs["messages"]))
            if not scripted:
                raise AssertionError("loop made more calls than the script provides")
            return scripted.pop(0)

    class Client:
        def __init__(self, *a, **kw):
            self.beta = types.SimpleNamespace(messages=Messages())

    module = types.ModuleType("anthropic")
    module.Anthropic = Client
    monkeypatch.setitem(sys.modules, "anthropic", module)
    return sent


def submit(findings):
    return Response(
        [Block(id="t9", name="submit_findings", input={"findings": findings})],
        stop_reason="tool_use",
    )


FINDING = {
    "title": "Prompt tells the model to double-check its own work",
    "dimension": "prompt",
    "severity": "medium",
    "file": "sick_app.py",
    "line": 14,
    "detail": "Current models verify unprompted; instructing it causes over-verification.",
    "remedy": "Delete the verification instruction.",
    "confidence": 0.7,
}


def test_loop_runs_tools_then_submits(monkeypatch):
    sent = install_stub(
        monkeypatch,
        [
            Response([Block(id="t1", name="grep", input={"pattern": "messages.create"})]),
            Response([Block(id="t2", name="read_file", input={"path": "sick_app.py"})]),
            submit([FINDING]),
        ],
    )
    result = agent.review(FIXTURES, FILES)

    assert result.error is None
    assert len(result.findings) == 1
    assert result.findings[0].check == "llm-agent"
    assert result.iterations == 3
    # Usage accumulates across turns, not just the last one.
    assert result.input_tokens == 300 and result.cache_read_tokens == 270


def test_tool_results_are_paired_and_batched_into_one_user_message(monkeypatch):
    """Two tool calls in one assistant turn must come back as one user message
    containing both results, each carrying its own tool_use_id."""
    sent = install_stub(
        monkeypatch,
        [
            Response(
                [
                    Block(id="a", name="grep", input={"pattern": "model"}),
                    Block(id="b", name="read_file", input={"path": "healthy_app.py"}),
                ]
            ),
            submit([]),
        ],
    )
    agent.review(FIXTURES, FILES)

    final = sent[-1]
    assert final[-2]["role"] == "assistant"  # the turn holding the tool_use blocks
    results_msg = final[-1]
    assert results_msg["role"] == "user"
    assert [b["tool_use_id"] for b in results_msg["content"]] == ["a", "b"]
    assert all(b["type"] == "tool_result" for b in results_msg["content"])


def test_tool_errors_are_returned_to_the_model_not_raised(monkeypatch):
    sent = install_stub(
        monkeypatch,
        [
            Response([Block(id="a", name="read_file", input={"path": "../../etc/passwd"})]),
            submit([]),
        ],
    )
    result = agent.review(FIXTURES, FILES)

    assert result.error is None  # the loop survived
    block = sent[-1][-1]["content"][0]
    assert block["is_error"] is True
    assert "escapes the repository root" in block["content"]


def test_pause_turn_resumes_without_injecting_a_message(monkeypatch):
    sent = install_stub(
        monkeypatch,
        [
            Response([Block(type="text", text="thinking...")], stop_reason="pause_turn"),
            submit([]),
        ],
    )
    result = agent.review(FIXTURES, FILES)

    assert result.error is None
    # The resumed request ends on the assistant turn — no synthetic "continue".
    assert sent[-1][-1]["role"] == "assistant"


def test_loop_terminates_at_the_iteration_cap(monkeypatch):
    script = [
        Response([Block(id=f"t{i}", name="grep", input={"pattern": "x"})])
        for i in range(agent.MAX_ITERATIONS)
    ]
    install_stub(monkeypatch, script)
    result = agent.review(FIXTURES, FILES)

    assert result.iterations == agent.MAX_ITERATIONS
    assert "cap" in (result.error or "")


def test_stopping_without_submitting_is_an_error_not_a_silent_pass(monkeypatch):
    install_stub(monkeypatch, [Response([Block(type="text", text="looks fine")], "end_turn")])
    result = agent.review(FIXTURES, FILES)

    assert result.findings == []
    assert "without calling submit_findings" in (result.error or "")


def test_refusal_is_handled_before_reading_content(monkeypatch):
    install_stub(monkeypatch, [Response([], stop_reason="refusal")])
    result = agent.review(FIXTURES, FILES)
    assert result.error == "the model declined this request"


# --------------------------------------------------------------------------- #
# sandbox
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "path", ["../secrets.env", "/etc/passwd", "../../doctor/knowledge.py"]
)
def test_workspace_rejects_paths_outside_the_root(path):
    ws = agent.Workspace(FIXTURES, FILES)
    with pytest.raises(ValueError):
        ws.read_file(path)


def test_workspace_rejects_in_root_files_not_in_scope(tmp_path):
    (tmp_path / "app.py").write_text("x = 1\n")
    (tmp_path / "secret.txt").write_text("hunter2\n")
    ws = agent.Workspace(tmp_path, [tmp_path / "app.py"])
    with pytest.raises(ValueError, match="not a source file in scope"):
        ws.read_file("secret.txt")


def test_workspace_read_and_grep():
    ws = agent.Workspace(FIXTURES, FILES)
    body = ws.read_file("healthy_app.py", start_line=1, end_line=3)
    assert body.splitlines()[0].strip().startswith("1 |")

    hits = ws.grep(r"messages\.create", glob="*.py")
    assert "sick_app.py:" in hits
    assert ws.grep("zzz-no-such-pattern") == "(no matches)"


def test_workspace_reports_bad_regex_as_a_tool_error():
    ws = agent.Workspace(FIXTURES, FILES)
    with pytest.raises(ValueError, match="invalid regular expression"):
        ws.grep("([unclosed")
