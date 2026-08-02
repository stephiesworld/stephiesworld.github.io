"""The agentic reviewer — v2 of the judgement pass.

`llm.py` makes ONE call: we assemble every relevant file up front and ask for a
verdict. That works because we know what the reviewer needs to read.

This module is what you build when you *don't*. The reviewer gets tools and
decides for itself what to look at: it sees `handle_tool_call(name, input)`
referenced in the file it's reading, and goes and reads the handler. You cannot
assemble that payload in advance, because which file matters depends on what the
model finds — so you need a loop.

That is the entire difference between a workflow and an agent, and it is worth
being precise about it: not "the agent is smarter", but "the set of steps is not
known until the work is underway."

The loop below is deliberately written by hand rather than using the SDK's
tool runner, because the loop is the thing worth reading. In production, prefer
`client.beta.messages.tool_runner(...)` — it does exactly this, with per-turn
hooks for approval and interception.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .llm import MODEL, _SCHEMA, _to_finding
from .model import Finding

MAX_ITERATIONS = 14
MAX_FILE_BYTES = 200_000
MAX_GREP_HITS = 60

SYSTEM = """\
You are auditing a codebase's Claude API integration for the engineers who own \
it. A deterministic static analyser has already covered every \
mechanically checkable defect — retired model IDs, parameters that 400, cache \
placement, tool version strings, missing evals. Do not repeat any of that.

Your job is the judgement the analyser cannot make, and your advantage over it \
is that you can follow references. When a request builds its prompt from a \
constant defined elsewhere, read that file. When a tool is declared in one place \
and handled in another, read the handler and check they agree — a tool whose \
description promises something its implementation does not do is a defect no \
schema check can find. When an agent loop is spread across modules, read enough \
of it to say whether it terminates.

Work in this order:
  1. `grep` for the API call sites to orient yourself.
  2. `read_file` the ones that look substantive, following references outward.
  3. Stop reading once further files would not change your findings.
  4. Call `submit_findings` exactly once. That ends the review.

Judge on: prompt quality (contradictions, aggressive directives that overtrigger \
on current models, verification scaffolding those models no longer need), tool \
surface design (does each description say *when* to call it, do any two \
overlap), architecture fit (agentic loop where a workflow would do, or the \
reverse), context and state handling (unbounded history, forks that rebuild the \
parent's prefix slightly differently and miss its cache), and failure handling \
beyond error codes (partial responses, unbounded loops, tools returning nothing).

Every finding must cite a real file and line you actually read, and name a \
concrete failure: which input, what goes wrong. If you cannot name the failure, \
it is a preference — drop it. An empty findings list is a respectable answer for \
well-built code; do not manufacture findings to look thorough.
"""

TOOLS = [
    {
        "name": "grep",
        "description": (
            "Search the codebase with a regular expression. Call this first to locate "
            "API call sites, prompt definitions, or tool handlers before reading whole "
            "files. Returns matching lines with their file and line number."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Python regular expression."},
                "glob": {
                    "type": "string",
                    "description": "Optional filename filter, e.g. '*.py'. Defaults to all source files.",
                },
            },
            "required": ["pattern"],
            "additionalProperties": False,
        },
    },
    {
        "name": "read_file",
        "description": (
            "Read a source file with line numbers. Call this when you need the full "
            "context around something grep surfaced, or to follow a reference — an "
            "imported prompt constant, a tool handler, a helper that builds the request. "
            "Prefer a line range on large files."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Repo-relative path."},
                "start_line": {"type": "integer", "description": "1-indexed, inclusive."},
                "end_line": {"type": "integer", "description": "1-indexed, inclusive."},
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    },
    {
        "name": "submit_findings",
        "description": (
            "Submit the completed review. Call this exactly once, when further reading "
            "would not change your conclusions. Calling it ends the review."
        ),
        "input_schema": _SCHEMA,
    },
]


@dataclass
class AgentResult:
    findings: list[Finding] = field(default_factory=list)
    error: str | None = None
    iterations: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    transcript: list[str] = field(default_factory=list)

    @property
    def cost_note(self) -> str:
        return (
            f"{self.iterations} turn(s), {self.input_tokens:,} in / "
            f"{self.output_tokens:,} out, {self.cache_read_tokens:,} cached"
        )


class Workspace:
    """The tool implementations. Every path the model supplies is untrusted input:
    resolve it and confirm it is still inside the root before touching disk."""

    def __init__(self, root: Path, allowed: list[Path]) -> None:
        self.root = root.resolve()
        self.allowed = {p.resolve() for p in allowed}

    def _resolve(self, rel: str) -> Path:
        candidate = (self.root / rel).resolve()
        if not candidate.is_relative_to(self.root):
            raise ValueError(f"path escapes the repository root: {rel!r}")
        if candidate not in self.allowed:
            raise ValueError(
                f"{rel!r} is not a source file in scope. Use grep to find files in scope."
            )
        return candidate

    def read_file(self, path: str, start_line: int | None = None, end_line: int | None = None) -> str:
        target = self._resolve(path)
        text = target.read_text(encoding="utf-8", errors="replace")
        if len(text) > MAX_FILE_BYTES and start_line is None:
            raise ValueError(
                f"{path} is {len(text):,} bytes. Request a line range instead."
            )
        lines = text.splitlines()
        lo = max(1, start_line or 1)
        hi = min(len(lines), end_line or len(lines))
        return "\n".join(f"{i:>5} | {lines[i - 1]}" for i in range(lo, hi + 1))

    def grep(self, pattern: str, glob: str | None = None) -> str:
        import fnmatch
        import re

        try:
            regex = re.compile(pattern)
        except re.error as exc:
            raise ValueError(f"invalid regular expression: {exc}") from exc

        hits: list[str] = []
        for path in sorted(self.allowed):
            rel = str(path.relative_to(self.root))
            if glob and not fnmatch.fnmatch(rel, glob) and not fnmatch.fnmatch(path.name, glob):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for n, line in enumerate(text.splitlines(), start=1):
                if regex.search(line):
                    hits.append(f"{rel}:{n}: {line.strip()[:200]}")
                    if len(hits) >= MAX_GREP_HITS:
                        hits.append(f"... truncated at {MAX_GREP_HITS} matches")
                        return "\n".join(hits)
        return "\n".join(hits) if hits else "(no matches)"


def review(root: Path, files: list[Path], *, effort: str = "high") -> AgentResult:
    """Run the agentic review. Never raises — a failure degrades the report."""
    try:
        import anthropic
    except ImportError:
        return AgentResult(error="`anthropic` is not installed — run `pip install anthropic`.")

    try:
        client = anthropic.Anthropic()
    except Exception as exc:  # noqa: BLE001
        return AgentResult(error=f"could not construct client: {exc}")

    workspace = Workspace(root, files)
    result = AgentResult()

    messages: list[dict] = [
        {
            "role": "user",
            "content": (
                f"Audit the Claude API integration in this repository. It has "
                f"{len(files)} source file(s). Start by grepping for `messages.create` "
                "or `messages.stream` to find the call sites."
            ),
        }
    ]

    for iteration in range(1, MAX_ITERATIONS + 1):
        result.iterations = iteration
        try:
            response = client.beta.messages.create(
                model=MODEL,
                max_tokens=16000,
                betas=["context-management-2025-06-27"],
                thinking={"type": "adaptive"},
                output_config={"effort": effort},
                # Context management (#4): the API clears tool results that have
                # aged out, so a long review doesn't re-send every file it read
                # on turn 2. Without this, input tokens grow quadratically.
                context_management={"edits": [{"type": "clear_tool_uses_20250919"}]},
                # Prompt caching: system + tools are byte-identical every turn, so
                # they bill at ~10% from turn 2 onward. The marker goes on the last
                # stable block — never on the conversation, which changes each turn.
                system=[
                    {"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}
                ],
                tools=TOOLS,
                messages=messages,
            )
        except Exception as exc:  # noqa: BLE001
            result.error = f"{type(exc).__name__}: {exc}"
            return result

        usage = getattr(response, "usage", None)
        result.input_tokens += getattr(usage, "input_tokens", 0) or 0
        result.output_tokens += getattr(usage, "output_tokens", 0) or 0
        result.cache_read_tokens += getattr(usage, "cache_read_input_tokens", 0) or 0

        stop = getattr(response, "stop_reason", None)
        if stop == "refusal":
            result.error = "the model declined this request"
            return result

        # Append the assistant turn BEFORE handling tools, so tool_use blocks stay
        # paired with their results. The API rejects a tool_result whose tool_use
        # is missing from the history.
        messages.append({"role": "assistant", "content": response.content})

        # A server-side tool hit its iteration limit. Re-send to resume; do NOT
        # add a "continue" message — the API detects the pending block itself.
        if stop == "pause_turn":
            continue

        tool_uses = [b for b in response.content if getattr(b, "type", None) == "tool_use"]
        if not tool_uses:
            result.error = (
                f"the reviewer stopped after {iteration} turn(s) without calling "
                "submit_findings"
            )
            return result

        tool_results = []
        for block in tool_uses:
            if block.name == "submit_findings":
                for raw in (block.input or {}).get("findings", []):
                    finding = _to_finding(raw)
                    if finding is not None:
                        finding.check = "llm-agent"
                        result.findings.append(finding)
                return result

            result.transcript.append(f"{block.name}({json.dumps(block.input)[:120]})")
            try:
                if block.name == "read_file":
                    output = workspace.read_file(**block.input)
                elif block.name == "grep":
                    output = workspace.grep(**block.input)
                else:
                    raise ValueError(f"unknown tool {block.name!r}")
                is_error = False
            except Exception as exc:  # noqa: BLE001
                # Hand the error back rather than crashing: the model recovers from
                # a bad path far more reliably than your retry logic will.
                output = f"error: {exc}"
                is_error = True

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                    "is_error": is_error,
                }
            )

        # All results go back in ONE user message. Splitting them across several
        # trains the model to stop making parallel tool calls.
        messages.append({"role": "user", "content": tool_results})

    result.error = f"hit the {MAX_ITERATIONS}-turn cap without a verdict"
    return result
