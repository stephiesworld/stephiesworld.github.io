"""Command line entry point."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from . import agent, checks, extract, fix as fixmod, llm, report as reportmod
from .model import Report, Severity

_SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
    ".next",
    "site-packages",
}

_EXIT_CLEAN = 0
_EXIT_FINDINGS = 1
_EXIT_ERROR = 2


def discover(root: Path) -> list[Path]:
    out: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in _SKIP_DIRS for part in path.parts):
            continue
        if extract.for_path(path.name) is not None:
            out.append(path)
    return out


def analyse(
    root: Path,
    *,
    use_llm: bool,
    effort: str,
    today: date,
    agentic: bool = False,
) -> Report:
    report = Report()
    ctx = checks.Context(root=root, today=today)
    files = discover(root)
    ctx.files = files

    for path in files:
        extractor = extract.for_path(path.name)
        if extractor is None:
            continue
        rel = ctx.rel(path)
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            report.skipped.append(rel)
            continue
        report.files_scanned += 1
        sites, refs = extractor.extract(rel, source)
        ctx.call_sites.extend(sites)
        ctx.model_refs.extend(refs)

    report.call_sites = ctx.call_sites
    report.model_refs = ctx.model_refs
    report.findings.extend(checks.run(ctx))

    if use_llm and ctx.call_sites:
        if agentic:
            # The reviewer picks its own reading order, so it needs the loop.
            agent_result = agent.review(root, files, effort=effort)
            report.llm_error = agent_result.error
            report.findings.extend(agent_result.findings)
            report.llm_ran = bool(agent_result.findings) or not agent_result.error
            report.llm_note = agent_result.cost_note
        else:
            result = llm.review(llm.build_payload(ctx), effort=effort)
            report.llm_ran = not result.error or bool(result.findings)
            report.llm_error = result.error
            report.findings.extend(result.findings)

    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="deployment-doctor",
        description="Audit a codebase's Claude API integration.",
    )
    parser.add_argument("path", nargs="?", default=".", help="repository or directory to audit")
    parser.add_argument(
        "--format",
        choices=("terminal", "markdown", "json"),
        default="terminal",
    )
    parser.add_argument("-o", "--out", type=Path, help="write the report to a file")
    parser.add_argument(
        "--llm",
        action="store_true",
        help="run the judgement pass (needs ANTHROPIC_API_KEY or an `ant auth login` profile)",
    )
    parser.add_argument(
        "--llm-agent",
        action="store_true",
        help="run the judgement pass as an agent loop: the reviewer gets grep/read_file "
        "tools and chooses what to read. Implies --llm.",
    )
    parser.add_argument(
        "--effort",
        default="high",
        choices=("low", "medium", "high", "xhigh", "max"),
        help="effort for the judgement pass (default: high)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="apply mechanical fixes (model IDs, tool versions) in place",
    )
    parser.add_argument("--dry-run", action="store_true", help="with --fix, show but don't write")
    parser.add_argument(
        "--fail-on",
        choices=("critical", "high", "medium", "low", "never"),
        default="high",
        help="exit non-zero at this severity or above (default: high)",
    )
    parser.add_argument("--list-checks", action="store_true", help="print the check catalog")
    args = parser.parse_args(argv)

    if args.list_checks:
        for registered in checks.all_checks():
            print(f"{registered.dimension:<12} {registered.id:<28} {registered.summary}")
        return _EXIT_CLEAN

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"error: {root} does not exist", file=sys.stderr)
        return _EXIT_ERROR

    report = analyse(
        root,
        use_llm=args.llm or args.llm_agent,
        effort=args.effort,
        today=date.today(),
        agentic=args.llm_agent,
    )

    if args.fix:
        result = fixmod.apply(root, report.findings, dry_run=args.dry_run)
        verb = "would apply" if args.dry_run else "applied"
        print(f"{verb} {len(result.applied)} fix(es)")
        for line in result.applied:
            print(f"  + {line}")
        for line in result.skipped:
            print(f"  ! {line}")
        print()

    target = root.name or str(root)
    if args.format == "json":
        rendered = reportmod.to_json(report, target=target)
    elif args.format == "markdown":
        rendered = reportmod.markdown(report, target=target)
    else:
        rendered = reportmod.terminal(report, target=target)

    if args.out:
        args.out.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(rendered)

    if args.fail_on == "never":
        return _EXIT_CLEAN
    threshold = Severity[args.fail_on.upper()]
    if any(f.severity >= threshold for f in report.findings):
        return _EXIT_FINDINGS
    return _EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(main())
