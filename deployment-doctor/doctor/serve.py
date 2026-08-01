"""A local web front end, so the audit runs from a browser instead of a terminal.

The architecture here is the point, and it is the same one every production
agent uses:

    browser  ->  this server (holds the credential)  ->  Anthropic API

A browser cannot call the Anthropic API directly. Two things stop it: the API
sends no CORS headers, so the request is blocked before it leaves the page; and
even if it weren't, the key would have to be embedded in JavaScript that anyone
can read. So the credential stays server-side, and the page talks only to us.

`/api/status` reports *whether* a credential was found and never what it is.

Deliberately stdlib-only, matching the rest of the deterministic path: no Flask,
no FastAPI, no build step. Bound to loopback because it exposes a filesystem
read to whoever can reach it.
"""

from __future__ import annotations

import json
import webbrowser
from datetime import date
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import checks, cli, env as envmod, report as reportmod

PAGE = Path(__file__).resolve().parent / "ui.html"
MAX_BODY = 64 * 1024


class Handler(BaseHTTPRequestHandler):
    server_version = "DeploymentDoctor/1.0"

    def __init__(self, *args, root: Path, **kwargs):
        self.root = root
        super().__init__(*args, **kwargs)

    # ----------------------------------------------------------------- routes

    def do_GET(self) -> None:
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
        elif self.path == "/api/status":
            self._json(200, self._status())
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/api/audit":
            self._json(404, {"error": "not found"})
            return

        length = int(self.headers.get("content-length") or 0)
        if length > MAX_BODY:
            self._json(413, {"error": "request too large"})
            return
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self._json(400, {"error": "body is not valid JSON"})
            return

        try:
            target = self._resolve(str(body.get("path") or "."))
        except ValueError as exc:
            self._json(400, {"error": str(exc)})
            return

        mode = str(body.get("mode") or "static")
        try:
            report = cli.analyse(
                target,
                use_llm=mode in ("llm", "agent"),
                agentic=mode == "agent",
                effort=str(body.get("effort") or "high"),
                today=date.today(),
            )
        except Exception as exc:  # noqa: BLE001 - reported to the page, not swallowed
            self._json(500, {"error": f"{type(exc).__name__}: {exc}"})
            return

        payload = json.loads(reportmod.to_json(report, target=target.name or str(target)))
        payload["mode"] = mode
        payload["llm_note"] = report.llm_note
        payload["skipped"] = report.skipped
        self._json(200, payload)

    # ---------------------------------------------------------------- helpers

    def _resolve(self, raw: str) -> Path:
        """Confine the audit to the directory the server was started in.

        The path arrives from the page, so it is untrusted input even on a
        loopback socket. Same rule as the agent's Workspace: resolve first, then
        prove the result is still inside the root.
        """
        candidate = (self.root / raw).resolve() if not Path(raw).is_absolute() else Path(raw).resolve()
        if not candidate.is_relative_to(self.root):
            raise ValueError(f"path escapes the server root: {raw!r}")
        if not candidate.exists():
            raise ValueError(f"{raw!r} does not exist")
        if not candidate.is_dir():
            raise ValueError(f"{raw!r} is not a directory")
        return candidate

    def _status(self) -> dict:
        import os

        applied = envmod.load(self.root)
        found = next(
            (
                name
                for name in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_PROFILE")
                if os.environ.get(name)
            ),
            None,
        )
        try:
            import anthropic  # noqa: F401

            sdk = True
        except ImportError:
            sdk = False
        return {
            "root": str(self.root),
            "credential": found,  # the variable NAME only, never the value
            "from_env_file": bool(applied),
            "sdk_installed": sdk,
            "checks": len(checks.all_checks()),
        }

    def _json(self, code: int, obj: dict) -> None:
        self._send(code, json.dumps(obj).encode("utf-8"), "application/json")

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("content-type", content_type)
        self.send_header("content-length", str(len(body)))
        self.send_header("cache-control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args) -> None:
        # One tidy line per request instead of the stdlib's noise.
        print(f"  {fmt % args}")


def serve(root: Path, port: int = 8420, open_browser: bool = True) -> None:
    root = root.resolve()
    handler = partial(Handler, root=root)
    httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
    url = f"http://127.0.0.1:{port}"

    print(f"Deployment Doctor — {url}")
    print(f"  serving {root}")
    print("  bound to loopback only. Ctrl-C to stop.\n")
    if open_browser:
        webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()
