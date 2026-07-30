"""JavaScript / TypeScript extractor.

Deliberately heuristic. A real TS parser (tree-sitter, or shelling out to the
TypeScript compiler) would be more accurate, but pulling either in trades a
stdlib-only tool for a build step. The scan below brace-matches the request
object and reads *top-level literal* keys, which covers the parameters every
check actually needs: `model`, `max_tokens`, `temperature`, `stream`, `betas`,
`thinking`, `system`.

What it deliberately does NOT do:
  - resolve identifiers or imported constants (`model: MODEL` is unresolved)
  - see into spreads (`...baseParams`)
  - understand nested object shapes beyond a shallow read

Unresolved args are recorded with `resolved=False`, so checks stay quiet rather
than guessing. Findings from this extractor carry lower confidence.
"""

from __future__ import annotations

import json
import re

from .. import knowledge
from ..model import Arg, CallSite, Location, ModelRef

_CALL = re.compile(
    r"(?P<chain>(?:\w+\s*\.\s*)*(?:beta\s*\.\s*)?messages\s*\.\s*"
    r"(?P<terminal>create|stream|parse|countTokens|toolRunner))\s*\(",
)

_STRING = re.compile(r"""^\s*(?P<q>["'`])(?P<val>(?:\\.|(?!\1).)*)(?P=q)\s*$""")
_NUMBER = re.compile(r"^\s*(?P<val>-?\d+(?:_\d+)*(?:\.\d+)?)\s*$")
_MODEL_STR = re.compile(r"""["'`](?P<val>(?:anthropic\.)?claude-[A-Za-z0-9._-]+)["'`]""")


class JavaScriptExtractor:
    suffixes = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs")
    language = "javascript"

    def extract(self, path: str, source: str) -> tuple[list[CallSite], list[ModelRef]]:
        sites: list[CallSite] = []
        covered: set[int] = set()

        for match in _CALL.finditer(source):
            open_paren = match.end() - 1
            body, end = _balanced(source, open_paren, "(", ")")
            if body is None:
                continue
            obj, _ = _balanced(body, body.find("{"), "{", "}") if "{" in body else (None, None)
            line = source.count("\n", 0, match.start()) + 1
            terminal = match.group("terminal")
            chain = re.sub(r"\s+", "", match.group("chain"))
            method = _normalise_method(chain, terminal)

            site = CallSite(
                location=Location(path, line),
                method=method,
                language="javascript",
                source=source[match.start() : end or match.end()],
            )
            if obj is not None:
                base_line = line + body[: body.find("{")].count("\n")
                for key, raw, offset in _top_level_pairs(obj):
                    site.args[key] = _make_arg(
                        path, key, raw, base_line + obj[:offset].count("\n")
                    )
            sites.append(site)
            covered.update(range(line, source.count("\n", 0, end or match.end()) + 2))

        refs: list[ModelRef] = []
        for match in _MODEL_STR.finditer(source):
            line = source.count("\n", 0, match.start()) + 1
            if line in covered:
                continue
            value = match.group("val")
            if knowledge.looks_like_model_id(value):
                refs.append(
                    ModelRef(
                        location=Location(path, line),
                        model_id=value,
                        context=source.splitlines()[line - 1].strip(),
                    )
                )
        return sites, refs


def _normalise_method(chain: str, terminal: str) -> str:
    prefix = "beta." if ".beta.messages" in chain or chain.startswith("beta.") else ""
    mapped = {"countTokens": "count_tokens", "toolRunner": "tool_runner"}.get(terminal, terminal)
    return f"{prefix}messages.{mapped}"


def _balanced(text: str, start: int, open_ch: str, close_ch: str) -> tuple[str | None, int | None]:
    """Return the contents between a matched pair, skipping strings and comments."""
    if start < 0 or start >= len(text) or text[start] != open_ch:
        return None, None
    depth = 0
    i = start
    quote: str | None = None
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'`":
            quote = ch
        elif text.startswith("//", i):
            i = text.find("\n", i)
            if i == -1:
                break
            continue
        elif text.startswith("/*", i):
            close = text.find("*/", i)
            if close == -1:
                break
            i = close + 2
            continue
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return text[start + 1 : i], i + 1
        i += 1
    return None, None


def _top_level_pairs(obj: str):
    """Yield (key, raw_value, offset) for depth-0 `key: value` entries."""
    depth = 0
    quote: str | None = None
    i = 0
    key: str | None = None
    key_end = 0
    seg_start = 0
    while i < len(obj):
        ch = obj[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "\"'`":
            quote = ch
        elif ch in "{[(":
            depth += 1
        elif ch in "}])":
            depth -= 1
        elif depth == 0 and ch == ":" and key is None:
            raw_key = obj[seg_start:i].strip().strip("\"'`")
            if re.fullmatch(r"[A-Za-z_$][\w$]*", raw_key):
                key = raw_key
                key_end = i + 1
        elif depth == 0 and ch == "," and key is not None:
            yield key, obj[key_end:i], key_end
            key = None
            seg_start = i + 1
        i += 1
    if key is not None:
        yield key, obj[key_end:], key_end


def _make_arg(path: str, key: str, raw: str, line: int) -> Arg:
    arg = Arg(name=key, raw=raw.strip(), location=Location(path, line))
    text = raw.strip()
    if m := _STRING.match(text):
        arg.value = m.group("val")
        arg.resolved = True
    elif m := _NUMBER.match(text):
        num = m.group("val").replace("_", "")
        arg.value = float(num) if "." in num else int(num)
        arg.resolved = True
    elif text in ("true", "false"):
        arg.value = text == "true"
        arg.resolved = True
    elif text.startswith("{") or text.startswith("["):
        # Try a JSON read for the simple object/array literals that appear in
        # `thinking: {...}` and `betas: [...]`. Quoting is usually JS-style, so
        # this fails often — that's fine, it stays unresolved.
        try:
            arg.value = json.loads(_jsonish(text))
            arg.resolved = True
        except (ValueError, TypeError):
            pass
    return arg


def _jsonish(text: str) -> str:
    text = re.sub(r"'([^']*)'", r'"\1"', text)
    text = re.sub(r"([{,]\s*)([A-Za-z_$][\w$]*)(\s*:)", r'\1"\2"\3', text)
    text = re.sub(r",\s*([}\]])", r"\1", text)
    return text
