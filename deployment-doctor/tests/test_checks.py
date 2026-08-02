from __future__ import annotations

import os
from datetime import date
from pathlib import Path

import pytest

from doctor import checks, report as reportmod
from doctor.cli import analyse
from doctor.extract.javascript import JavaScriptExtractor
from doctor.extract.python import PythonExtractor
from doctor.model import Severity

FIXTURES = Path(__file__).parent / "fixtures"
TODAY = date(2026, 7, 30)


def run_on(filename: str):
    """Analyse a single fixture in isolation."""
    src = (FIXTURES / filename).read_text()
    ctx = checks.Context(root=FIXTURES, today=TODAY, files=[FIXTURES / filename])
    sites, refs = PythonExtractor().extract(filename, src)
    ctx.call_sites, ctx.model_refs = sites, refs
    return ctx, checks.run(ctx)


def ids(findings) -> set[str]:
    return {f.id for f in findings}


# --------------------------------------------------------------------------- #
# extraction
# --------------------------------------------------------------------------- #


def test_extracts_call_sites_and_resolves_module_constants():
    ctx, _ = run_on("sick_app.py")
    assert len(ctx.call_sites) == 4
    # Module-level constants are traced through the `model=MODEL` reference.
    assert {s.model_id() for s in ctx.call_sites} == {
        "claude-opus-4-8",
        "claude-3-opus-20240229",
        "claude-opus-5",
        "claude-opus-4-6-fast",
    }


def test_streaming_detected_from_method_name():
    ctx, _ = run_on("healthy_app.py")
    assert ctx.call_sites[0].streaming is True


def test_ambiguous_constant_is_not_resolved():
    """Two different values for one name must yield no resolution, not a guess."""
    src = (
        "import anthropic\n"
        "M = 'claude-opus-5'\n"
        "M = 'claude-sonnet-5'\n"
        "anthropic.Anthropic().messages.create(model=M, max_tokens=10, messages=[])\n"
    )
    sites, _ = PythonExtractor().extract("t.py", src)
    assert sites[0].model_id() is None


def test_javascript_extractor_reads_literal_args():
    src = """
    const res = await client.messages.create({
      model: "claude-3-opus-20240229",
      max_tokens: 64000,
      temperature: 0.5,
      messages: [{ role: "user", content: q }],
    });
    """
    sites, _ = JavaScriptExtractor().extract("app.ts", src)
    assert len(sites) == 1
    assert sites[0].model_id() == "claude-3-opus-20240229"
    assert sites[0].get("max_tokens").as_int() == 64000
    assert sites[0].get("temperature").value == 0.5


# --------------------------------------------------------------------------- #
# model checks
# --------------------------------------------------------------------------- #


def test_retired_model_via_constant_reports_at_call_site_but_fixes_at_the_constant():
    """`model=LEGACY_MODEL` has no literal to rewrite. The call site is where the
    breakage is; the constant is where the edit goes. Offering a fix on the call
    site would be a promise the patcher can't keep."""
    _, findings = run_on("sick_app.py")
    retired = [f for f in findings if f.id == "MODEL_RETIRED"]
    call_site = [f for f in retired if f.severity is Severity.CRITICAL]
    constant = [f for f in retired if f.severity is not Severity.CRITICAL]

    assert call_site and call_site[0].fix is None
    assert constant and constant[0].fix is not None
    assert constant[0].fix.new == "claude-opus-5"
    assert "live code" in constant[0].detail


def test_retired_model_inline_literal_is_autofixable():
    src = (
        "import anthropic\n"
        "anthropic.Anthropic().messages.create(model='claude-3-opus-20240229',"
        " max_tokens=10, messages=[])\n"
    )
    sites, refs = PythonExtractor().extract("t.py", src)
    ctx = checks.Context(root=Path("."), today=TODAY)
    ctx.call_sites, ctx.model_refs = sites, refs
    retired = [f for f in checks.run(ctx) if f.id == "MODEL_RETIRED"]
    assert len(retired) == 1
    assert retired[0].severity is Severity.CRITICAL
    assert retired[0].fix is not None and retired[0].fix.new == "claude-opus-5"


def test_fast_suffix_flagged_as_silent_fallback():
    _, findings = run_on("sick_app.py")
    fast = [f for f in findings if f.id == "MODEL_FAST_SUFFIX"]
    assert fast and "silently" in fast[0].detail


def test_deprecated_status_is_date_relative():
    """claude-opus-4-1 retires 2026-08-05: deprecated before, retired after."""
    src = (
        "import anthropic\n"
        "anthropic.Anthropic().messages.create(model='claude-opus-4-1',"
        " max_tokens=10, messages=[])\n"
    )
    sites, refs = PythonExtractor().extract("t.py", src)

    before = checks.Context(root=Path("."), today=date(2026, 7, 1))
    before.call_sites, before.model_refs = sites, refs
    assert "MODEL_DEPRECATED" in ids(checks.run(before))

    after = checks.Context(root=Path("."), today=date(2026, 9, 1))
    after.call_sites, after.model_refs = sites, refs
    assert "MODEL_RETIRED" in ids(checks.run(after))


def test_dated_suffix_on_live_alias_is_flagged_with_a_hint():
    src = (
        "import anthropic\n"
        "anthropic.Anthropic().messages.create(model='claude-opus-5-20260101',"
        " max_tokens=10, messages=[])\n"
    )
    sites, refs = PythonExtractor().extract("t.py", src)
    ctx = checks.Context(root=Path("."), today=TODAY)
    ctx.call_sites, ctx.model_refs = sites, refs
    unknown = [f for f in checks.run(ctx) if f.id == "MODEL_UNKNOWN"]
    assert unknown and "claude-opus-5" in unknown[0].detail


# --------------------------------------------------------------------------- #
# correctness checks
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "check_id",
    [
        "PARAM_SAMPLING_REJECTED",
        "PARAM_BUDGET_TOKENS",
        "PARAM_PREFILL",
        "STREAMING_REQUIRED",
        "BETA_HEADER_STALE",
        "TOOL_EDITOR_PAIR",
        "CACHE_INVALIDATOR",
    ],
)
def test_sick_fixture_triggers(check_id):
    _, findings = run_on("sick_app.py")
    assert check_id in ids(findings)


def test_prefill_not_flagged_on_a_model_that_allows_it():
    src = (
        "import anthropic\n"
        "anthropic.Anthropic().messages.create(model='claude-sonnet-4-5', max_tokens=10,\n"
        "  messages=[{'role':'user','content':'x'},{'role':'assistant','content':'{'}])\n"
    )
    sites, _ = PythonExtractor().extract("t.py", src)
    ctx = checks.Context(root=Path("."), today=TODAY)
    ctx.call_sites = sites
    assert "PARAM_PREFILL" not in ids(checks.run(ctx))


def test_thinking_disabled_above_high_effort_is_critical():
    src = (
        "import anthropic\n"
        "anthropic.Anthropic().messages.create(model='claude-opus-5', max_tokens=100,\n"
        "  thinking={'type':'disabled'}, output_config={'effort':'xhigh'}, messages=[])\n"
    )
    sites, _ = PythonExtractor().extract("t.py", src)
    ctx = checks.Context(root=Path("."), today=TODAY)
    ctx.call_sites = sites
    found = [f for f in checks.run(ctx) if f.id == "THINKING_DISABLED_EFFORT"]
    assert found and found[0].severity is Severity.CRITICAL


def test_thinking_disabled_at_high_effort_is_allowed():
    src = (
        "import anthropic\n"
        "anthropic.Anthropic().messages.create(model='claude-opus-5', max_tokens=100,\n"
        "  thinking={'type':'disabled'}, output_config={'effort':'high'}, messages=[])\n"
    )
    sites, _ = PythonExtractor().extract("t.py", src)
    ctx = checks.Context(root=Path("."), today=TODAY)
    ctx.call_sites = sites
    assert "THINKING_DISABLED_EFFORT" not in ids(checks.run(ctx))


def test_output_format_allowed_on_parse_but_not_create():
    parse_src = (
        "import anthropic\n"
        "anthropic.Anthropic().messages.parse(model='claude-opus-5', max_tokens=10,\n"
        "  output_format='X', messages=[])\n"
    )
    create_src = parse_src.replace(".parse(", ".create(")
    for src, expected in ((parse_src, False), (create_src, True)):
        sites, _ = PythonExtractor().extract("t.py", src)
        ctx = checks.Context(root=Path("."), today=TODAY)
        ctx.call_sites = sites
        assert ("PARAM_OUTPUT_FORMAT" in ids(checks.run(ctx))) is expected


# --------------------------------------------------------------------------- #
# caching checks
# --------------------------------------------------------------------------- #


def test_cache_absent_on_large_uncached_prefix():
    src = (
        "import anthropic\n"
        "SYSTEM = 'word ' * 4000\n"
        "anthropic.Anthropic().messages.create(model='claude-opus-5', max_tokens=100,\n"
        "  system=SYSTEM, messages=[])\n"
    )
    sites, _ = PythonExtractor().extract("t.py", src)
    ctx = checks.Context(root=Path("."), today=TODAY)
    ctx.call_sites = sites
    assert "CACHE_ABSENT" in ids(checks.run(ctx))


def test_cache_below_minimum_is_model_specific():
    """Same prompt, same marker: silently uncached on Opus 4.6 (4096-token
    minimum), fine on Opus 5 (512)."""
    template = (
        "import anthropic\n"
        "anthropic.Anthropic().messages.create(model={m!r}, max_tokens=100,\n"
        # ~750 tokens: comfortably over Opus 5's 512 minimum, well under 4.6's 4096.
        "  system=[{{'type':'text','text':'word '*600,"
        "'cache_control':{{'type':'ephemeral'}}}}], messages=[])\n"
    )
    results = {}
    for model in ("claude-opus-4-6", "claude-opus-5"):
        sites, _ = PythonExtractor().extract("t.py", template.format(m=model))
        ctx = checks.Context(root=Path("."), today=TODAY)
        ctx.call_sites = sites
        results[model] = "CACHE_BELOW_MINIMUM" in ids(checks.run(ctx))
    assert results == {"claude-opus-4-6": True, "claude-opus-5": False}


def test_too_many_breakpoints_is_critical():
    blocks = ",".join(
        "{'type':'text','text':'x','cache_control':{'type':'ephemeral'}}" for _ in range(5)
    )
    src = (
        "import anthropic\n"
        f"anthropic.Anthropic().messages.create(model='claude-opus-5', max_tokens=10,\n"
        f"  system=[{blocks}], messages=[])\n"
    )
    sites, _ = PythonExtractor().extract("t.py", src)
    ctx = checks.Context(root=Path("."), today=TODAY)
    ctx.call_sites = sites
    found = [f for f in checks.run(ctx) if f.id == "CACHE_TOO_MANY_BREAKPOINTS"]
    assert found and found[0].severity is Severity.CRITICAL


# --------------------------------------------------------------------------- #
# tool checks
# --------------------------------------------------------------------------- #


def test_thin_tool_description_and_undocumented_params():
    _, findings = run_on("sick_app.py")
    assert "TOOL_DESCRIPTION_THIN" in ids(findings)
    assert "TOOL_SCHEMA_LOOSE" in ids(findings)


def test_mcp_server_without_toolset_is_critical():
    src = (
        "import anthropic\n"
        "anthropic.Anthropic().beta.messages.create(model='claude-opus-5', max_tokens=10,\n"
        "  mcp_servers=[{'type':'url','name':'linear','url':'https://mcp.linear.app/mcp'}],\n"
        "  tools=[], messages=[])\n"
    )
    sites, _ = PythonExtractor().extract("t.py", src)
    ctx = checks.Context(root=Path("."), today=TODAY)
    ctx.call_sites = sites
    found = [f for f in checks.run(ctx) if f.id == "MCP_TOOLSET_MISSING"]
    assert found and found[0].severity is Severity.CRITICAL


# --------------------------------------------------------------------------- #
# repo-level
# --------------------------------------------------------------------------- #


def test_healthy_fixture_has_no_critical_or_high_findings():
    ctx, findings = run_on("healthy_app.py")
    # EVAL_NONE is repo-level and expected when analysing one file in isolation.
    serious = [
        f for f in findings if f.severity >= Severity.HIGH and f.id != "EVAL_NONE"
    ]
    assert serious == [], [(f.id, f.title, str(f.location)) for f in serious]


def test_full_run_produces_a_report_without_the_llm_pass():
    report = analyse(FIXTURES, use_llm=False, effort="high", today=TODAY)
    assert report.files_scanned >= 2
    assert report.llm_ran is False
    md = reportmod.markdown(report, target="fixtures")
    assert "Deployment Doctor" in md
    assert "## Scorecard" in md
    assert "## Coverage" in md


def test_scores_drop_with_severity():
    report = analyse(FIXTURES, use_llm=False, effort="high", today=TODAY)
    scores = reportmod.scores(report)
    assert scores["correctness"] < 100
    assert all(0 <= v <= 100 for v in scores.values())


def test_every_check_declares_a_valid_dimension():
    for registered in checks.all_checks():
        assert registered.dimension in checks.DIMENSIONS
        assert registered.summary


def test_model_registry_suppresses_per_entry_noise():
    """A file listing many model IDs is a catalog, not a caller. It legitimately
    keeps retired IDs — one summary beats twenty wrong alarms."""
    catalog = "\n".join(
        f"    {name!r}: 1,"
        for name in [
            "claude-3-opus-20240229",
            "claude-3-5-sonnet-20241022",
            "claude-2.1",
            "claude-opus-5",
            "claude-sonnet-5",
            "claude-haiku-4-5",
            "claude-opus-4-8",
        ]
    )
    src = f"PRICES = {{\n{catalog}\n}}\n"
    sites, refs = PythonExtractor().extract("registry.py", src)
    ctx = checks.Context(root=Path("."), today=TODAY)
    ctx.call_sites, ctx.model_refs = sites, refs
    findings = checks.run(ctx)

    assert "MODEL_REGISTRY" in ids(findings)
    assert "MODEL_RETIRED" not in ids(findings)
    summary = next(f for f in findings if f.id == "MODEL_REGISTRY")
    assert summary.severity is Severity.INFO
    assert "claude-2.1" in summary.detail


def test_below_the_registry_threshold_entries_are_still_reported():
    src = "A = 'claude-3-opus-20240229'\nB = 'claude-opus-5'\n"
    sites, refs = PythonExtractor().extract("config.py", src)
    ctx = checks.Context(root=Path("."), today=TODAY)
    ctx.call_sites, ctx.model_refs = sites, refs
    findings = checks.run(ctx)
    assert "MODEL_RETIRED" in ids(findings)
    assert "MODEL_REGISTRY" not in ids(findings)


def test_coverage_distinguishes_found_from_reported_model_refs():
    """The coverage section must not claim every reference was reported when the
    catalog heuristic collapsed most of them."""
    report = analyse(Path.cwd(), use_llm=False, effort="high", today=TODAY)
    coverage = reportmod.markdown(report, target="self")
    assert "collapsed into one summary each" in coverage
    assert "are reported individually" in coverage


# --------------------------------------------------------------------------- #
# .env loading
# --------------------------------------------------------------------------- #


def test_env_parses_the_forms_people_actually_write():
    from doctor.env import parse

    parsed = parse(
        "\n".join(
            [
                "# a comment",
                "",
                "ANTHROPIC_API_KEY=sk-ant-plain",
                "export EXPORTED=yes",
                'QUOTED="has spaces"',
                "SINGLE='single'",
                "TRAILING=value # trailing comment",
                'HASH_IN_SECRET="abc#def"',
                "not a pair",
            ]
        )
    )
    assert parsed == {
        "ANTHROPIC_API_KEY": "sk-ant-plain",
        "EXPORTED": "yes",
        "QUOTED": "has spaces",
        "SINGLE": "single",
        "TRAILING": "value",
        # A `#` inside a quoted value is part of the secret, not a comment.
        "HASH_IN_SECRET": "abc#def",
    }


def test_env_does_not_override_an_explicit_export(tmp_path, monkeypatch):
    """A key exported in the shell must beat a file on disk, or 'which key am I
    using' becomes guesswork."""
    from doctor import env as envmod

    (tmp_path / ".env").write_text("ANTHROPIC_API_KEY=from-file\nOTHER=from-file\n")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "from-shell")
    monkeypatch.delenv("OTHER", raising=False)

    applied = envmod.load(tmp_path)

    assert os.environ["ANTHROPIC_API_KEY"] == "from-shell"
    assert os.environ["OTHER"] == "from-file"
    assert set(applied) == {"OTHER"}


def test_env_is_found_in_a_parent_directory(tmp_path, monkeypatch):
    from doctor import env as envmod

    (tmp_path / ".env").write_text("FOUND_UPWARD=1\n")
    nested = tmp_path / "a" / "b"
    nested.mkdir(parents=True)
    monkeypatch.delenv("FOUND_UPWARD", raising=False)

    assert envmod.find(nested) == tmp_path / ".env"
    assert envmod.load(nested) == {"FOUND_UPWARD": "1"}


def test_env_describe_never_prints_a_value():
    from doctor.env import describe

    note = describe({"ANTHROPIC_API_KEY": "sk-ant-supersecret"})
    assert "ANTHROPIC_API_KEY" in note
    assert "supersecret" not in note
    assert describe({}) == ""
