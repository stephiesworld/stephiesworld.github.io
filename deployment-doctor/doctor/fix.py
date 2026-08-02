"""Auto-fixes, applied narrowly and reversibly.

A fix is only emitted when the substitution is mechanical *and* the surrounding
context cannot change its meaning — model ID swaps and tool version strings.
Anything requiring a judgement call (which effort level replaces this
`budget_tokens`? which model replaces this tier?) is reported and left alone.

Fixes are line-scoped and verified before writing: if the line no longer
contains the expected text, the fix is skipped rather than applied to whatever
is there now.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .model import Finding


@dataclass
class FixResult:
    applied: list[str]
    skipped: list[str]


def apply(root: Path, findings: list[Finding], *, dry_run: bool = False) -> FixResult:
    applied: list[str] = []
    skipped: list[str] = []

    by_file: dict[str, list[Finding]] = {}
    for finding in findings:
        if finding.fix is None:
            continue
        by_file.setdefault(finding.fix.path, []).append(finding)

    for rel_path, group in by_file.items():
        path = root / rel_path
        try:
            original = path.read_text(encoding="utf-8")
        except OSError as exc:
            skipped.append(f"{rel_path}: unreadable ({exc})")
            continue

        lines = original.splitlines(keepends=True)
        changed = False
        # Descending line order so earlier edits don't shift later ones.
        for finding in sorted(group, key=lambda f: -f.fix.line):  # type: ignore[union-attr]
            fix = finding.fix
            assert fix is not None
            idx = fix.line - 1
            if not (0 <= idx < len(lines)):
                skipped.append(f"{rel_path}:{fix.line}: line out of range")
                continue
            if fix.old not in lines[idx]:
                skipped.append(
                    f"{rel_path}:{fix.line}: expected {fix.old!r} on this line — "
                    "file changed since analysis, not touching it"
                )
                continue
            lines[idx] = lines[idx].replace(fix.old, fix.new)
            applied.append(f"{rel_path}:{fix.line}  {fix.description}")
            changed = True

        if changed and not dry_run:
            path.write_text("".join(lines), encoding="utf-8")

    return FixResult(applied=applied, skipped=skipped)
