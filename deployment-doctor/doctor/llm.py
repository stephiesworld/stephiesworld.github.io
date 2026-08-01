"""The one agentic step.

Everything in `checks/` is deterministic: an AST walk, zero tokens, perfectly
reproducible. This module handles the part no rule can decide — whether a prompt
is any good, whether a tool description will actually trigger, whether the
architecture fits the task. That split is the whole design: static analysis
where the shape is known, model judgement where it isn't.

The request below deliberately uses the features the checks look for, so the
tool is its own first patient: current model ID, adaptive thinking, prompt
caching on the static rubric, structured outputs, streaming, refusal handling,
and server-side fallbacks.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from .model import Finding, Location, Severity

MODEL = "claude-opus-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"
MAX_PAYLOAD_CHARS = 120_000

_SEVERITY_BY_NAME = {s.name.lower(): s for s in Severity}

# Kept as a module-level constant on purpose: this is the cached prefix. Any
# per-run value interpolated in here would invalidate the cache on every call —
# the exact defect CACHE_INVALIDATOR reports.
RUBRIC = """\
You are reviewing a codebase's integration with the Claude API, on behalf of an \
AI deployment manager preparing findings for the customer who wrote it.

The caller has already run a deterministic static analyser over this code. It has \
covered — completely and correctly — everything mechanically checkable: retired and \
deprecated model IDs, parameters that return a 400 (sampling parameters, \
`budget_tokens`, assistant prefill), streaming requirements at high `max_tokens`, \
cache-control placement and minimum prefix sizes, cache invalidators, stale beta \
headers, tool version strings, MCP pairing, and the absence of evals.

DO NOT REPORT ANY OF THE ABOVE. Repeating a mechanical finding is worse than \
silence: it makes the report longer without making it more useful, and it trains \
the reader to skim. Your entire value is the judgement the analyser cannot make.

Report only on these dimensions:

1. PROMPT QUALITY. Is the system prompt doing work, or is it vibes? Look for: \
instructions that contradict each other; aggressive all-caps directives \
("CRITICAL: YOU MUST") that overtrigger on current models, which follow \
instructions far more literally than the models those prompts were written for; \
verification scaffolding ("double-check your answer", "add a final verification \
step") that current models now do unprompted and which causes over-verification \
when told; forced progress-update scaffolding ("summarise after every 3 tool \
calls") that is now redundant; and missing scope discipline where the model is \
likely to expand the task beyond what was asked.

2. TOOL SURFACE DESIGN. Are the tools the right decomposition? A single \
do-everything tool and fifteen near-duplicate tools are both smells. Does each \
description state *when* to call it, not only what it does? Are there overlapping \
tools the model must disambiguate on vibes? Is anything a tool that should have \
been a code path?

3. ARCHITECTURE FIT. Is the tier right for the task — a single API call, a \
code-controlled workflow, or an agentic loop? A common failure is an agentic loop \
where a workflow would be cheaper, faster, and testable, because the steps were \
actually known in advance. The reverse also happens: a rigid chain of calls where \
the work genuinely has unknown shape. Flag either.

4. CONTEXT AND STATE. In multi-turn or long-running code: is history growing \
unbounded with no compaction or context editing? Is state that should persist \
across sessions being rebuilt every turn? Is a fork/subagent call rebuilding the \
parent's system prompt and tools slightly differently, so it misses the parent's \
cache entirely?

5. FAILURE HANDLING BEYOND ERROR CODES. What happens on a partial response, a \
`max_tokens` stop, a tool that returns nothing, a malformed tool input? Is there \
an unbounded agentic loop with no iteration cap?

Rules for every finding you report:
- Point at a real line in the code you were given. Never invent a location.
- State the concrete failure: which input, what goes wrong. If you cannot name a \
failure, it is a preference, not a finding — drop it.
- Be specific to THIS code. Generic advice that would apply to any codebase is \
noise; the reader has read the docs.
- Give a remedy the author could apply today, not a direction to explore.
- Prefer five real findings to twenty padded ones. An empty list is a valid and \
respectable answer for well-built code, and you should return one rather than \
manufacture findings to look thorough.
- Severity: `critical` = broken in production; `high` = silently wrong, silently \
expensive, or silently truncated; `medium` = real quality or cost left on the \
table; `low` = cleanup.
"""

_SCHEMA = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "One line, the claim itself."},
                    "dimension": {
                        "type": "string",
                        "enum": ["prompt", "tools", "architecture", "context", "failure"],
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"],
                    },
                    "file": {"type": "string", "description": "Repo-relative path as given."},
                    "line": {"type": "integer", "description": "1-indexed line in that file."},
                    "detail": {
                        "type": "string",
                        "description": "The concrete failure: which input, what goes wrong.",
                    },
                    "remedy": {"type": "string", "description": "What to change, specifically."},
                    "confidence": {"type": "number"},
                },
                "required": [
                    "title",
                    "dimension",
                    "severity",
                    "file",
                    "line",
                    "detail",
                    "remedy",
                    "confidence",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["findings"],
    "additionalProperties": False,
}


@dataclass
class LLMResult:
    findings: list[Finding]
    error: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0


def review(payload: str, *, effort: str = "high", model: str = MODEL) -> LLMResult:
    """Run the judgement pass. Never raises — a failure here degrades the report,
    it does not fail the run.

    `model` is a parameter rather than a constant so the eval harness can hold
    the prompt fixed and vary only the model. That is the whole comparison: if
    the rubric changed between runs, the numbers would not be comparable.
    """
    try:
        import anthropic
    except ImportError:
        return LLMResult([], error="`anthropic` is not installed — run `pip install anthropic`.")

    if len(payload) > MAX_PAYLOAD_CHARS:
        payload = payload[:MAX_PAYLOAD_CHARS] + "\n\n[... truncated for length ...]"

    try:
        client = anthropic.Anthropic()
    except Exception as exc:  # noqa: BLE001 - surfaced to the user, not swallowed
        return LLMResult([], error=f"could not construct client: {exc}")

    try:
        with client.beta.messages.stream(
            model=model,
            max_tokens=16000,
            betas=[FALLBACK_BETA],
            fallbacks="default",
            thinking={"type": "adaptive"},
            output_config={
                "effort": effort,
                "format": {"type": "json_schema", "schema": _SCHEMA},
            },
            # The rubric is the cached prefix; the payload varies per run and sits
            # after it, which is the whole point.
            system=[{"type": "text", "text": RUBRIC, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": payload}],
        ) as stream:
            response = stream.get_final_message()
    except Exception as exc:  # noqa: BLE001
        return LLMResult([], error=f"{type(exc).__name__}: {exc}")

    usage = getattr(response, "usage", None)
    result = LLMResult(
        findings=[],
        input_tokens=getattr(usage, "input_tokens", 0) or 0,
        output_tokens=getattr(usage, "output_tokens", 0) or 0,
        cache_read_tokens=getattr(usage, "cache_read_input_tokens", 0) or 0,
    )

    # Branch on stop_reason before touching content — a refusal is a 200 with an
    # empty or partial content array, not an exception. (Branch on stop_reason,
    # not stop_details: the latter can be null even on a refusal.)
    if getattr(response, "stop_reason", None) == "refusal":
        result.error = "the model declined this request; no judgement findings returned"
        return result
    if getattr(response, "stop_reason", None) == "max_tokens":
        result.error = "response hit max_tokens — findings may be incomplete"

    text = next(
        (b.text for b in response.content if getattr(b, "type", None) == "text"),
        None,
    )
    if not text:
        result.error = result.error or "no text block in response"
        return result

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        result.error = f"could not parse structured output: {exc}"
        return result

    for raw in parsed.get("findings", []):
        finding = _to_finding(raw)
        if finding is not None:
            result.findings.append(finding)
    return result


def _to_finding(raw: dict) -> Finding | None:
    try:
        severity = _SEVERITY_BY_NAME[str(raw["severity"]).lower()]
        location = Location(str(raw["file"]), int(raw["line"]))
    except (KeyError, ValueError, TypeError):
        return None
    return Finding(
        id=f"LLM_{str(raw.get('dimension', 'review')).upper()}",
        title=str(raw.get("title", "")).strip() or "(untitled)",
        severity=severity,
        location=location,
        detail=str(raw.get("detail", "")).strip(),
        remedy=str(raw.get("remedy", "")).strip(),
        check="llm-review",
        confidence=float(raw.get("confidence", 0.6)),
    )


def build_payload(ctx) -> str:
    """Assemble the varying half of the prompt: the code the reviewer should read.

    Only files that actually contain a call site are included — sending the whole
    repository would bury the signal and cost a fortune.
    """
    parts: list[str] = []
    paths = sorted({site.location.path for site in ctx.call_sites})
    for path in paths:
        source = ctx.read(path)
        if source is None:
            continue
        numbered = "\n".join(
            f"{i:>5} | {line}" for i, line in enumerate(source.splitlines(), start=1)
        )
        parts.append(f"<file path={path!r}>\n{numbered}\n</file>")
    header = (
        f"Review the following {len(paths)} file(s). Line numbers are prefixed; cite them "
        "exactly as shown.\n\n"
    )
    return header + "\n\n".join(parts)
