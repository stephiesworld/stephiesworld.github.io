"""Rendering. The report is the deliverable — treat it like one."""

from __future__ import annotations

import json
from collections import Counter, defaultdict

from . import knowledge
from .checks import DIMENSIONS, all_checks
from .model import Report, Severity

_ICON = {
    Severity.CRITICAL: "🔴",
    Severity.HIGH: "🟠",
    Severity.MEDIUM: "🟡",
    Severity.LOW: "⚪",
    Severity.INFO: "·",
}

# Weight per finding, subtracted from 100 per dimension.
_WEIGHT = {
    Severity.CRITICAL: 40,
    Severity.HIGH: 20,
    Severity.MEDIUM: 8,
    Severity.LOW: 2,
    Severity.INFO: 0,
}


def _dimension_of(check_id: str) -> str:
    for registered in all_checks():
        if registered.id == check_id:
            return registered.dimension
    return "correctness"


def scores(report: Report) -> dict[str, int]:
    out = {d: 100 for d in DIMENSIONS}
    for finding in report.findings:
        if finding.check == "llm-review":
            dim = {"LLM_PROMPT": "correctness", "LLM_TOOLS": "tools"}.get(
                finding.id, "correctness"
            )
        else:
            dim = _dimension_of(finding.check)
        out[dim] = max(0, out[dim] - _WEIGHT[finding.severity])
    return out


def _bar(score: int, width: int = 20) -> str:
    filled = round(score / 100 * width)
    return "█" * filled + "░" * (width - filled)


def markdown(report: Report, *, target: str) -> str:
    findings = report.sorted_findings()
    counts = report.by_severity()
    dim_scores = scores(report)
    overall = round(sum(dim_scores.values()) / len(dim_scores))

    out: list[str] = []
    out.append(f"# Deployment Doctor — `{target}`\n")
    out.append(
        f"**{overall}/100** across {report.files_scanned} file(s), "
        f"{len(report.call_sites)} API call site(s). "
        f"Model catalog as of {knowledge.KNOWLEDGE_AS_OF}.\n"
    )

    if not findings:
        out.append(
            "> No findings. Either this integration is in good shape, or the analyser "
            "could not resolve enough statically — check the coverage note below before "
            "reading this as a clean bill of health.\n"
        )

    # --- summary ------------------------------------------------------------
    out.append("| Severity | Count | What it means |")
    out.append("| --- | ---: | --- |")
    meanings = {
        Severity.CRITICAL: "Rejected by the API. Fails today.",
        Severity.HIGH: "Silently wrong, expensive, or truncated.",
        Severity.MEDIUM: "Real cost or quality on the table.",
        Severity.LOW: "Cleanup.",
    }
    for sev in (Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW):
        if counts[sev]:
            out.append(f"| {_ICON[sev]} {sev.label} | {counts[sev]} | {meanings[sev]} |")
    out.append("")

    # --- scorecard ----------------------------------------------------------
    out.append("## Scorecard\n")
    out.append("| Dimension | Score | |")
    out.append("| --- | ---: | --- |")
    for dim in DIMENSIONS:
        out.append(f"| {dim.title()} | {dim_scores[dim]} | `{_bar(dim_scores[dim])}` |")
    out.append("")

    # --- findings -----------------------------------------------------------
    if findings:
        out.append("## Findings\n")
        by_sev: dict[Severity, list] = defaultdict(list)
        for finding in findings:
            by_sev[finding.severity].append(finding)

        for sev in (Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW):
            group = by_sev.get(sev)
            if not group:
                continue
            out.append(f"### {_ICON[sev]} {sev.label}\n")
            for finding in group:
                out.append(f"#### {finding.title}")
                out.append("")
                out.append(f"`{finding.location}` · `{finding.id}`" + _confidence_note(finding))
                out.append("")
                out.append(finding.detail)
                out.append("")
                out.append(f"**Fix:** {finding.remedy}")
                if finding.cost_signal:
                    out.append("")
                    out.append(f"**Cost:** {finding.cost_signal}")
                if finding.fix:
                    out.append("")
                    out.append(
                        f"*Auto-fixable* — `--fix` rewrites `{finding.fix.old}` → "
                        f"`{finding.fix.new}`."
                    )
                out.append("")

    # --- coverage -----------------------------------------------------------
    out.append("## Coverage\n")
    out.append(_coverage(report))

    if report.llm_error:
        out.append("")
        out.append(f"> Judgement pass did not run: {report.llm_error}")
    elif report.llm_ran:
        n = sum(1 for f in report.findings if f.check in ("llm-review", "llm-agent"))
        note = f" ({report.llm_note})" if report.llm_note else ""
        out.append("")
        out.append(f"> Judgement pass ran and contributed {n} finding(s).{note}")

    return "\n".join(out) + "\n"


def _confidence_note(finding) -> str:
    if finding.confidence >= 0.9:
        return ""
    return f" · confidence {finding.confidence:.0%}"


def _coverage(report: Report) -> str:
    """Say plainly what was and wasn't analysed. A report that hides its blind
    spots reads as a clean bill of health, which is worse than no report."""
    lines: list[str] = []
    resolved = sum(1 for s in report.call_sites if s.model_id())
    total = len(report.call_sites)
    lines.append(
        f"- {total} call site(s) found; the model ID resolved statically on {resolved}. "
        + (
            f"The other {total - resolved} pass the model through a variable or config the "
            "analyser cannot trace, so model-specific checks were skipped there."
            if resolved < total
            else "Model-specific checks ran on all of them."
        )
    )
    langs = Counter(s.language for s in report.call_sites)
    if langs.get("javascript"):
        lines.append(
            f"- {langs['javascript']} JS/TS call site(s) were read heuristically, not parsed. "
            "Identifiers, spreads, and imported constants are invisible there — treat "
            "absence of findings in those files as absence of evidence."
        )
    if report.model_refs:
        lines.append(
            f"- {len(report.model_refs)} model-ID string(s) found outside call sites "
            "(constants, config, registries, fixtures). These are reported but never "
            "auto-fixed: a registry that *serves* a model legitimately keeps the old ID."
        )
    if report.skipped:
        lines.append(f"- {len(report.skipped)} file(s) skipped (unreadable or unparseable).")
    lines.append(
        "- Not checked: runtime behaviour, actual token counts, actual cache hit rates, "
        "or output quality. Those need the live API and an eval set."
    )
    return "\n".join(lines)


def to_json(report: Report, *, target: str) -> str:
    return json.dumps(
        {
            "target": target,
            "knowledge_as_of": str(knowledge.KNOWLEDGE_AS_OF),
            "files_scanned": report.files_scanned,
            "call_sites": len(report.call_sites),
            "scores": scores(report),
            "llm_ran": report.llm_ran,
            "llm_error": report.llm_error,
            "findings": [
                {
                    "id": f.id,
                    "check": f.check,
                    "title": f.title,
                    "severity": f.severity.name.lower(),
                    "file": f.location.path,
                    "line": f.location.line,
                    "detail": f.detail,
                    "remedy": f.remedy,
                    "confidence": f.confidence,
                    "cost_signal": f.cost_signal,
                    "autofixable": f.fix is not None,
                }
                for f in report.sorted_findings()
            ],
        },
        indent=2,
    )


def terminal(report: Report, *, target: str) -> str:
    """Compact view for the shell. The markdown report is the artifact; this is
    for the iteration loop."""
    lines = [f"Deployment Doctor — {target}"]
    dim_scores = scores(report)
    overall = round(sum(dim_scores.values()) / len(dim_scores))
    lines.append(f"  score {overall}/100 · {len(report.findings)} finding(s)")
    lines.append("")
    for finding in report.sorted_findings():
        lines.append(f"  {_ICON[finding.severity]} {finding.location}  {finding.title}")
        lines.append(f"      {finding.id}  →  {finding.remedy.splitlines()[0][:96]}")
    if report.llm_error:
        lines.append("")
        lines.append(f"  judgement pass skipped: {report.llm_error}")
    return "\n".join(lines)
