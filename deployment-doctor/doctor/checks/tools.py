"""Tool-definition checks.

Tool definitions are where agent quality quietly degrades: a vague description
means the model reaches for the wrong tool, and a stale version string is a 400
that only fires on the code path nobody exercises in staging.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .. import knowledge
from ..model import Finding, Fix, Severity
from . import Context, check
from ._common import tools_of

# Anthropic-defined tools are schema-less: declare `type` + `name` only. Defining
# your own tool with one of these names produces a *different* tool with none of
# the built-in behaviour.
_RESERVED_NAMES = {"bash", "str_replace_based_edit_tool", "memory", "code_execution", "web_search"}

_MIN_DESCRIPTION = 25


@check("TOOL_VERSION_STALE", "tools", "Superseded Anthropic-defined tool version")
def stale_tool_version(ctx: Context) -> Iterable[Finding]:
    for site, tool in _iter_tools(ctx):
        type_ = tool.get("type")
        if not isinstance(type_, str):
            continue
        newer = knowledge.TOOL_UPGRADES.get(type_)
        if newer is None:
            continue
        arg = site.get("tools")
        loc = arg.location if arg else site.location
        yield Finding(
            id="TOOL_VERSION_STALE",
            title=f"Stale tool version `{type_}`",
            severity=Severity.MEDIUM,
            location=loc,
            detail=(
                f"`{type_}` is superseded by `{newer}`."
                + (
                    " The `_20260209` web tools add dynamic filtering — Claude filters "
                    "results in code before they reach the context window, which improves "
                    "both accuracy and token efficiency."
                    if newer.startswith(("web_search", "web_fetch"))
                    else ""
                )
            ),
            remedy=f"Update the `type` to `{newer}`."
            + (
                " The text-editor `name` field changes with it — see TOOL_EDITOR_PAIR."
                if newer.startswith("text_editor")
                else ""
            ),
            fix=Fix(loc.path, loc.line, type_, newer, f"{type_} -> {newer}")
            if not newer.startswith("text_editor")
            else None,
        )


@check("TOOL_EDITOR_PAIR", "tools", "text_editor `type` and `name` must move together")
def editor_pair(ctx: Context) -> Iterable[Finding]:
    """The single most common migration slip: bump the `type` to `_20250728`, leave
    `name` as `str_replace_editor`, get a 400."""
    for site, tool in _iter_tools(ctx):
        type_ = tool.get("type")
        name = tool.get("name")
        if not isinstance(type_, str) or not type_.startswith("text_editor_"):
            continue
        expected = knowledge.TEXT_EDITOR_NAMES.get(type_)
        if expected is None or name == expected:
            continue
        arg = site.get("tools")
        yield Finding(
            id="TOOL_EDITOR_PAIR",
            title=f"`{type_}` paired with `name={name!r}`",
            severity=Severity.CRITICAL,
            location=arg.location if arg else site.location,
            detail=(
                f"`{type_}` requires `name=\"{expected}\"`. The `type` and `name` fields are "
                "a matched pair; changing one without the other returns a 400."
            ),
            remedy=f'Set `name="{expected}"`.',
        )


@check("TOOL_DESCRIPTION_THIN", "tools", "Custom tool has a missing or one-word description")
def thin_description(ctx: Context) -> Iterable[Finding]:
    for site, tool in _iter_tools(ctx):
        if "input_schema" not in tool:  # Anthropic-defined tools carry no description
            continue
        name = tool.get("name", "<unnamed>")
        desc = tool.get("description")
        arg = site.get("tools")
        loc = arg.location if arg else site.location
        if not isinstance(desc, str) or not desc.strip():
            yield Finding(
                id="TOOL_DESCRIPTION_THIN",
                title=f"Tool `{name}` has no description",
                severity=Severity.HIGH,
                location=loc,
                detail=(
                    "The description is the entire basis on which the model decides whether "
                    "to call this tool. With none, selection is a coin flip against the "
                    "tool name."
                ),
                remedy=(
                    "Write a description that is prescriptive about *when* to call it, not "
                    'just what it does — "Call this when the user asks about current prices '
                    'or recent events" measurably outperforms "Gets prices".'
                ),
            )
        elif len(desc.strip()) < _MIN_DESCRIPTION:
            yield Finding(
                id="TOOL_DESCRIPTION_THIN",
                title=f"Tool `{name}` description is {len(desc.strip())} characters",
                severity=Severity.MEDIUM,
                location=loc,
                detail=f"Description: {desc.strip()!r}. Too short to encode a trigger condition.",
                remedy="State when the tool applies, not only what it returns.",
                confidence=0.7,
            )


@check("TOOL_SCHEMA_LOOSE", "tools", "Custom tool schema has no property descriptions or required list")
def loose_schema(ctx: Context) -> Iterable[Finding]:
    for site, tool in _iter_tools(ctx):
        schema = tool.get("input_schema")
        if not isinstance(schema, dict):
            continue
        name = tool.get("name", "<unnamed>")
        props = schema.get("properties")
        if not isinstance(props, dict) or not props:
            continue
        arg = site.get("tools")
        loc = arg.location if arg else site.location
        undocumented = [
            k for k, v in props.items() if not (isinstance(v, dict) and v.get("description"))
        ]
        if undocumented:
            yield Finding(
                id="TOOL_SCHEMA_LOOSE",
                title=f"Tool `{name}`: {len(undocumented)} parameter(s) without a description",
                severity=Severity.MEDIUM,
                location=loc,
                detail="Undocumented: " + ", ".join(f"`{k}`" for k in undocumented) + ".",
                remedy="Add a `description` to each property. Parameter descriptions reduce "
                "malformed tool inputs more reliably than retry logic does.",
            )
        if "required" not in schema:
            yield Finding(
                id="TOOL_SCHEMA_LOOSE",
                title=f"Tool `{name}` schema has no `required` list",
                severity=Severity.LOW,
                location=loc,
                detail="Every parameter is implicitly optional, so the model may omit ones "
                "your handler assumes are present.",
                remedy="List genuinely-required parameters in `required`. For a hard "
                "guarantee, add `strict: true` plus `additionalProperties: false`.",
            )


@check("TOOL_NAME_RESERVED", "tools", "Custom tool shadows an Anthropic-defined tool name")
def reserved_name(ctx: Context) -> Iterable[Finding]:
    for site, tool in _iter_tools(ctx):
        name = tool.get("name")
        if name not in _RESERVED_NAMES or "input_schema" not in tool:
            continue
        arg = site.get("tools")
        yield Finding(
            id="TOOL_NAME_RESERVED",
            title=f"Custom tool named `{name}`",
            severity=Severity.MEDIUM,
            location=arg.location if arg else site.location,
            detail=(
                f"`{name}` is an Anthropic-defined, schema-less tool. Declaring a custom "
                "tool with the same name creates a different tool that has none of the "
                "built-in behaviour, while looking in review like the real one."
            ),
            remedy=f"Rename the custom tool, or drop the schema and declare the real one by "
            f"`type` + `name` only.",
        )


@check("TOOL_SEARCH_ALL_DEFERRED", "tools", "Every tool deferred — the request is a 400")
def all_deferred(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        tools = tools_of(site)
        if not tools or not all(isinstance(t, dict) for t in tools):
            continue
        if len(tools) < 2:
            continue
        if not all(t.get("defer_loading") for t in tools):
            continue
        arg = site.get("tools")
        yield Finding(
            id="TOOL_SEARCH_ALL_DEFERRED",
            title="All tools have `defer_loading: true`",
            severity=Severity.CRITICAL,
            location=arg.location if arg else site.location,
            detail="The API returns 400 `All tools have defer_loading set`. The tool-search "
            "tool itself must never be deferred, and at least one tool must be loaded.",
            remedy="Leave the search tool (and at least one other) non-deferred.",
        )


@check("MCP_TOOLSET_MISSING", "tools", "mcp_servers declared without a matching mcp_toolset")
def mcp_pairing(ctx: Context) -> Iterable[Finding]:
    for site in ctx.call_sites:
        servers = site.get("mcp_servers")
        if servers is None or not isinstance(servers.value, list):
            continue
        declared = {
            s.get("name") for s in servers.value if isinstance(s, dict) and s.get("name")
        }
        tools = tools_of(site) or []
        referenced = {
            t.get("mcp_server_name")
            for t in tools
            if isinstance(t, dict) and t.get("type") == "mcp_toolset"
        }
        missing = declared - referenced
        if not missing:
            continue
        yield Finding(
            id="MCP_TOOLSET_MISSING",
            title=f"MCP server(s) {', '.join(sorted(map(str, missing)))} declared but not referenced",
            severity=Severity.CRITICAL,
            location=servers.location,
            detail=(
                "`mcp_servers` and `tools` are two halves of one configuration. Every server "
                "must be referenced by exactly one `{'type': 'mcp_toolset', "
                "'mcp_server_name': ...}` entry, or the request is rejected as a validation "
                "error."
            ),
            remedy="Add an `mcp_toolset` entry per server, and set the "
            "`mcp-client-2025-11-20` beta.",
        )


def _iter_tools(ctx: Context) -> Iterable[tuple[Any, dict]]:
    for site in ctx.call_sites:
        for tool in tools_of(site) or []:
            if isinstance(tool, dict):
                yield site, tool
