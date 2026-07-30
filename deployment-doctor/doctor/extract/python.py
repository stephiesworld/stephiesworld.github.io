"""Python extractor, built on stdlib `ast`.

Two passes:
  1. Collect module-level constant assignments, so `MODEL = "claude-opus-5"` +
     `model=MODEL` resolves. Real code almost never inlines the ID.
  2. Walk for calls whose attribute chain lands on the Messages API surface.

Anything we can't resolve statically is still recorded, with `resolved=False`,
so checks can distinguish "this is wrong" from "we couldn't see it".
"""

from __future__ import annotations

import ast

from .. import knowledge
from ..model import Arg, CallSite, Location, ModelRef

# Terminal method names we care about, and the surface they belong to.
_TERMINALS = {
    "create",
    "stream",
    "parse",
    "count_tokens",
    "tool_runner",
}

_SURFACE_ROOTS = ("messages", "batches")


def _attr_chain(node: ast.AST) -> list[str]:
    """`client.beta.messages.create` -> ['client','beta','messages','create']"""
    parts: list[str] = []
    cur = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
    elif isinstance(cur, ast.Call):
        parts.append("()")
    parts.reverse()
    return parts


class _Sentinel:
    def __init__(self, name: str) -> None:
        self._name = name

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return self._name


# A value we could not resolve. Distinct from None, which is a legitimate value.
UNRESOLVED = _Sentinel("<unresolved>")
# A name assigned twice with different values. Refusing to pick is the point.
_AMBIGUOUS = _Sentinel("<ambiguous>")

# Guard against `"x" * 10**9` in a constant blowing up the analyser.
_MAX_STRING = 4_000_000


def safe_eval(node: ast.AST, consts: dict[str, object]) -> object:
    """Evaluate what we can, element-wise, and mark the rest UNRESOLVED.

    `ast.literal_eval` is all-or-nothing, which is the wrong shape here: real
    code writes `messages=[{"role": "user", "content": ticket}]`, where `ticket`
    is a parameter. Giving up on the whole list because one leaf is a variable
    would blind every structural check. Instead the dict resolves, `content`
    becomes UNRESOLVED, and the prefill check can still read `role`.
    """
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return [safe_eval(e, consts) for e in node.elts if not isinstance(e, ast.Starred)]

    if isinstance(node, ast.Dict):
        out: dict[object, object] = {}
        for key_node, value_node in zip(node.keys, node.values):
            if key_node is None:  # {**spread} — contents are invisible
                continue
            key = safe_eval(key_node, consts)
            if key is UNRESOLVED or not isinstance(key, (str, int, float, bool, tuple)):
                continue
            out[key] = safe_eval(value_node, consts)
        return out

    if isinstance(node, ast.Name):
        value = consts.get(node.id, UNRESOLVED)
        return UNRESOLVED if value is _AMBIGUOUS else value

    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Mult)):
        left = safe_eval(node.left, consts)
        right = safe_eval(node.right, consts)
        if left is UNRESOLVED or right is UNRESOLVED:
            return UNRESOLVED
        if isinstance(node.op, ast.Mult) and isinstance(left, str) and isinstance(right, int):
            if len(left) * right > _MAX_STRING:
                return UNRESOLVED
        if isinstance(node.op, ast.Mult) and isinstance(right, str) and isinstance(left, int):
            if len(right) * left > _MAX_STRING:
                return UNRESOLVED
        try:
            return left * right if isinstance(node.op, ast.Mult) else left + right  # type: ignore[operator]
        except Exception:  # noqa: BLE001 - any arithmetic failure means "unknown"
            return UNRESOLVED

    return UNRESOLVED


class _ConstantCollector(ast.NodeVisitor):
    """Module-level simple constants only. We deliberately do not do dataflow — a
    wrong resolution is worse than no resolution, because it produces a confident
    finding about code that doesn't exist."""

    def __init__(self) -> None:
        self.consts: dict[str, object] = {}

    def visit_Assign(self, node: ast.Assign) -> None:
        value = safe_eval(node.value, self.consts)
        if value is UNRESOLVED:
            return
        for target in node.targets:
            if isinstance(target, ast.Name):
                # Last write wins; if a name is assigned twice with different
                # values, drop it rather than guess.
                if target.id in self.consts and self.consts[target.id] != value:
                    self.consts[target.id] = _AMBIGUOUS
                else:
                    self.consts[target.id] = value

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if node.value is None or not isinstance(node.target, ast.Name):
            return
        value = safe_eval(node.value, self.consts)
        if value is not UNRESOLVED:
            self.consts[node.target.id] = value


class PythonExtractor:
    suffixes = (".py",)
    language = "python"

    def extract(self, path: str, source: str) -> tuple[list[CallSite], list[ModelRef]]:
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return [], []

        lines = source.splitlines()
        consts = _ConstantCollector()
        consts.visit(tree)

        sites: list[CallSite] = []
        refs: list[ModelRef] = []
        call_lines: set[int] = set()

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            chain = _attr_chain(node.func)
            if len(chain) < 2 or chain[-1] not in _TERMINALS:
                continue
            if not any(root in chain for root in _SURFACE_ROOTS):
                continue

            method = ".".join(chain[1:]) if chain[0] not in _SURFACE_ROOTS else ".".join(chain)
            site = CallSite(
                location=Location(path, node.lineno, node.col_offset),
                method=method,
                language="python",
                source=_slice(lines, node),
            )
            for kw in node.keywords:
                if kw.arg is None:  # **kwargs — we can't see inside
                    continue
                site.args[kw.arg] = self._arg(path, kw.arg, kw.value, lines, consts.consts)
            sites.append(site)
            call_lines.update(range(node.lineno, (node.end_lineno or node.lineno) + 1))

        # Second sweep: bare model-ID strings anywhere in the file. These may be
        # config, registries, or test fixtures — reported separately and never
        # auto-fixed.
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if knowledge.looks_like_model_id(node.value) and node.lineno not in call_lines:
                    refs.append(
                        ModelRef(
                            location=Location(path, node.lineno, node.col_offset),
                            model_id=node.value,
                            context=lines[node.lineno - 1].strip() if node.lineno <= len(lines) else "",
                        )
                    )

        return sites, refs

    def _arg(
        self,
        path: str,
        name: str,
        node: ast.AST,
        lines: list[str],
        consts: dict[str, object],
    ) -> Arg:
        loc = Location(path, getattr(node, "lineno", 0), getattr(node, "col_offset", 0))
        arg = Arg(name=name, raw=_slice(lines, node), location=loc, node=node)
        value = safe_eval(node, consts)
        if value is not UNRESOLVED:
            arg.value = value
            arg.resolved = True
        return arg


def _slice(lines: list[str], node: ast.AST) -> str:
    start = getattr(node, "lineno", 1)
    end = getattr(node, "end_lineno", start) or start
    return "\n".join(lines[start - 1 : end])


def walk_calls(node: ast.AST):
    """Yield dotted names of every call inside an expression — used by the cache
    check to spot `datetime.now()` buried in an f-string argument."""
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call):
            chain = _attr_chain(sub.func)
            if chain:
                yield ".".join(chain)


def contains_fstring(node: ast.AST) -> bool:
    return any(isinstance(sub, ast.JoinedStr) for sub in ast.walk(node))
