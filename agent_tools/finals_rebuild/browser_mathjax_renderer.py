"""Offline MathJax browser renderer using local Chrome/Edge + CDP.

Loads the vendored MathJax tex-svg.js via file:// only. Counts remote network
requests through CDP; report builds must keep network_calls == 0.
"""
from __future__ import annotations

import asyncio
import json
import os
import socket
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.request import urlopen

VENDOR_MATHJAX = Path(__file__).resolve().parent / "vendor" / "mathjax" / "tex-svg.js"

MATHJAX_CONFIG_JS = r"""
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    macros: {
      dfrac: ['{\\displaystyle\\frac{#1}{#2}}', 2]
    }
  },
  svg: { fontCache: 'global' },
  startup: { typeset: false }
};
"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8"/>
<title>G6b MathJax Render Probe</title>
<style>
html, body {{ margin: 0; padding: 0; background: #fff; color: #111;
  font-family: "Segoe UI", "Noto Sans TC", sans-serif; }}
.probe-root {{ width: 720px; max-width: 720px; padding: 16px; box-sizing: border-box; overflow: hidden; }}
.probe-block {{ margin: 12px 0; padding: 8px; border: 1px solid #ddd; overflow: auto; max-height: 480px; }}
.probe-label {{ font-size: 12px; color: #555; margin-bottom: 4px; }}
pre.raw {{ white-space: pre-wrap; word-break: break-word; background: #f7f7f7;
  border: 1px solid #eee; padding: 8px; font-size: 12px; }}
.mjx-target {{ font-size: 18px; line-height: 1.5; min-height: 1.5em; }}
</style>
<script>{mathjax_config}</script>
<script src="{mathjax_src}"></script>
</head>
<body>
<div class="probe-root" id="root">
  <div class="probe-block" id="question-wrap">
    <div class="probe-label">question</div>
    <div class="mjx-target" id="question-render"></div>
    <pre class="raw" id="question-raw"></pre>
  </div>
  <div class="probe-block" id="answer-wrap">
    <div class="probe-label">answer</div>
    <div class="mjx-target" id="answer-render"></div>
    <pre class="raw" id="answer-raw"></pre>
  </div>
</div>
<script>
window.__G6B_RESULT__ = null;
window.__G6B_ERROR__ = null;

function leftoverLatexSignals(el) {{
  const clone = el.cloneNode(true);
  clone.querySelectorAll('mjx-container, mjx-assistive-mml, script').forEach(n => n.remove());
  const visible = (clone.textContent || '');
  const hits = [];
  // Require TeX-like commands (2+ letters) or math delimiters. Avoid single-letter
  // false positives from ordinary prose/file fragments.
  const re = /\\\\[A-Za-z]{{2,}}|\\$\\$|\\$(?!\\$)|\\\\\\(|\\\\\\)|\\\\\\[|\\\\\\]/g;
  let m;
  while ((m = re.exec(visible)) !== null) {{
    hits.push(m[0]);
    if (hits.length >= 20) break;
  }}
  return hits;
}}

function rectInfo(el) {{
  const r = el.getBoundingClientRect();
  return {{
    width: r.width,
    height: r.height,
    top: r.top,
    left: r.left,
    bottom: r.bottom,
    right: r.right,
    scroll_width: el.scrollWidth,
    scroll_height: el.scrollHeight,
    client_width: el.clientWidth,
    client_height: el.clientHeight,
    overflow_x: el.scrollWidth > el.clientWidth + 1,
    overflow_y: el.scrollHeight > el.clientHeight + 1
  }};
}}

function overlap(a, b) {{
  return !(a.right <= b.left || a.left >= b.right || a.bottom <= b.top || a.top >= b.bottom);
}}

function inspectTarget(kind, el, wrap) {{
  const errors = Array.from(el.querySelectorAll('mjx-merror')).map(node => ({{
    text: (node.textContent || '').trim(),
    title: node.getAttribute('title') || null
  }}));
  const containers = Array.from(el.querySelectorAll('mjx-container'));
  const leftover = leftoverLatexSignals(el);
  const metrics = rectInfo(el);
  const wrapMetrics = rectInfo(wrap);
  // Overlap among mjx-container boxes is evidence/warning only — nested/adjacent
  // MathJax layout can touch without being a presentation failure.
  let overlap_hit = false;
  const rects = containers.map(node => node.getBoundingClientRect());
  for (let i = 0; i < rects.length; i++) {{
    for (let j = i + 1; j < rects.length; j++) {{
      if (overlap(rects[i], rects[j])) {{ overlap_hit = true; }}
    }}
  }}
  // Clipping threshold: wrap scroll overflow OR content box exceeds wrap client size by >2px.
  const CLIP_PX = 2;
  const clipped = wrapMetrics.overflow_x || wrapMetrics.overflow_y ||
    metrics.width > wrapMetrics.client_width + CLIP_PX ||
    metrics.height > wrapMetrics.client_height + CLIP_PX;
  const status = (errors.length || leftover.length || clipped) ? 'FAIL' : 'PASS';
  return {{
    kind,
    status,
    renderer_errors: errors,
    leftover_latex_commands: leftover,
    mjx_container_count: containers.length,
    metrics,
    wrap_metrics: wrapMetrics,
    clipping: !!clipped,
    clipping_threshold_px: CLIP_PX,
    overlap: overlap_hit,
    overlap_is_warning_only: true,
    rendered_html: el.innerHTML.slice(0, 8000),
    dom_text: (el.textContent || '').slice(0, 2000)
  }};
}}

async function runProbe(payload) {{
  const qEl = document.getElementById('question-render');
  const aEl = document.getElementById('answer-render');
  const qRaw = document.getElementById('question-raw');
  const aRaw = document.getElementById('answer-raw');
  const qWrap = document.getElementById('question-wrap');
  const aWrap = document.getElementById('answer-wrap');
  qRaw.textContent = payload.question_text == null ? 'NOT_AVAILABLE' : String(payload.question_text);
  aRaw.textContent = payload.answer_text == null ? 'NOT_AVAILABLE' : String(payload.answer_text);
  qEl.textContent = '';
  aEl.textContent = '';
  if (payload.question_text != null) {{ qEl.innerHTML = String(payload.question_text); }}
  if (payload.answer_text != null) {{ aEl.innerHTML = String(payload.answer_text); }}
  await MathJax.startup.promise;
  await MathJax.typesetPromise([qEl, aEl]);
  const question = payload.question_text == null
    ? {{ kind: 'question', status: 'NOT_OBSERVED', reason: 'actual_question_text_unavailable' }}
    : inspectTarget('question', qEl, qWrap);
  const answer = payload.answer_text == null
    ? {{ kind: 'answer', status: 'NOT_OBSERVED', reason: 'correct_answer_unavailable' }}
    : inspectTarget('answer', aEl, aWrap);
  return {{
    question,
    answer,
    mathjax_version: (MathJax && MathJax.version) ? MathJax.version : 'unknown',
    ready: true
  }};
}}

window.__G6B_RUN__ = async function(payload) {{
  try {{
    window.__G6B_RESULT__ = await runProbe(payload);
    window.__G6B_ERROR__ = null;
  }} catch (err) {{
    window.__G6B_RESULT__ = null;
    window.__G6B_ERROR__ = String(err && err.stack ? err.stack : err);
  }}
  return window.__G6B_RESULT__;
}};
</script>
</body>
</html>
"""


@dataclass(frozen=True)
class BrowserInfo:
    path: Path
    name: str
    version: str


def _read_file_version(path: Path) -> str:
    try:
        import ctypes
        from ctypes import wintypes

        size = ctypes.windll.version.GetFileVersionInfoSizeW(str(path), None)
        if not size:
            return "unknown"
        buf = ctypes.create_string_buffer(size)
        if not ctypes.windll.version.GetFileVersionInfoW(str(path), 0, size, buf):
            return "unknown"
        length = wintypes.UINT()
        pointer = ctypes.c_void_p()
        if not ctypes.windll.version.VerQueryValueW(buf, r"\\", ctypes.byref(pointer), ctypes.byref(length)):
            return "unknown"
        fixed = ctypes.cast(pointer, ctypes.POINTER(ctypes.c_uint32 * 13)).contents
        # VS_FIXEDFILEINFO: [0]=signature [1]=struc [2]=fileMS [3]=fileLS
        ms = fixed[2]
        ls = fixed[3]
        return f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
    except Exception:  # noqa: BLE001
        return "unknown"


def discover_browsers(*, override: str | Path | None = None) -> list[BrowserInfo]:
    """Discover local Chrome/Edge. Optional override: path or HEALER_G6B_BROWSER."""
    env_override = os.environ.get("HEALER_G6B_BROWSER")
    chosen = override or env_override
    found: list[BrowserInfo] = []
    seen: set[Path] = set()

    def add(path: Path, name: str | None = None) -> None:
        if not path.is_file():
            return
        resolved = path.resolve()
        if resolved in seen:
            return
        seen.add(resolved)
        label = name or ("chrome" if "chrome" in resolved.name.lower() else "edge" if "edge" in resolved.name.lower() else resolved.stem)
        found.append(BrowserInfo(path=resolved, name=label, version=_read_file_version(resolved)))

    if chosen:
        add(Path(chosen))
        return found

    candidates = [
        (Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"), "chrome"),
        (Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"), "chrome"),
        (Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"), "edge"),
        (Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"), "edge"),
    ]
    for path, name in candidates:
        add(path, name)
    return found


def require_mathjax_vendor() -> Path:
    if not VENDOR_MATHJAX.is_file():
        raise FileNotFoundError(
            f"vendored MathJax missing: {VENDOR_MATHJAX}. "
            "Offline G6b requires agent_tools/finals_rebuild/vendor/mathjax/tex-svg.js"
        )
    return VENDOR_MATHJAX.resolve()


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _http_json(url: str) -> Any:
    with urlopen(url, timeout=10) as resp:  # noqa: S310 — loopback CDP only
        return json.loads(resp.read().decode("utf-8"))


def _http_text(url: str) -> str:
    with urlopen(url, timeout=10) as resp:  # noqa: S310 — loopback CDP only
        return resp.read().decode("utf-8", errors="replace")


class _CdpSession:
    def __init__(self, ws_url: str) -> None:
        self.ws_url = ws_url
        self._id = 0
        self._ws = None
        self.network_request_urls: list[str] = []

    async def __aenter__(self) -> "_CdpSession":
        import websockets

        self._ws = await websockets.connect(self.ws_url, max_size=16 * 1024 * 1024)
        await self.call("Network.enable")
        return self

    async def __aexit__(self, *exc: Any) -> None:
        if self._ws is not None:
            await self._ws.close()

    async def call(self, method: str, params: dict[str, Any] | None = None, timeout: float = 60.0) -> Any:
        assert self._ws is not None
        self._id += 1
        msg_id = self._id
        await self._ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"CDP timeout waiting for {method}")
            raw = await asyncio.wait_for(self._ws.recv(), timeout=remaining)
            data = json.loads(raw)
            if data.get("method") == "Network.requestWillBeSent":
                req = data.get("params", {}).get("request", {})
                url = req.get("url")
                if isinstance(url, str):
                    self.network_request_urls.append(url)
            if data.get("id") == msg_id:
                if "error" in data:
                    raise RuntimeError(f"CDP {method} failed: {data['error']}")
                return data.get("result")


def _write_probe_page(workdir: Path) -> Path:
    mathjax = require_mathjax_vendor()
    html = PAGE_TEMPLATE.format(
        mathjax_config=MATHJAX_CONFIG_JS,
        mathjax_src=mathjax.as_uri(),
    )
    path = workdir / "g6b_probe.html"
    path.write_text(html, encoding="utf-8")
    return path


def _classify_network(urls: list[str]) -> dict[str, Any]:
    remote: list[str] = []
    local: list[str] = []
    for url in urls:
        if url.startswith(("file:", "data:", "about:", "blob:")):
            local.append(url)
        elif url.startswith("http://127.0.0.1") or url.startswith("http://localhost"):
            # CDP loopback traffic is tooling, not content network.
            local.append(url)
        else:
            remote.append(url)
    return {
        "network_calls": len(remote),
        "remote_urls": remote,
        "local_urls": local,
        "total_requests_observed": len(urls),
    }


def _wait_for_browser(port: int, *, timeout_s: float) -> None:
    deadline = time.monotonic() + timeout_s
    last_err: Exception | None = None
    while time.monotonic() < deadline:
        try:
            _http_json(f"http://127.0.0.1:{port}/json/version")
            return
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            time.sleep(0.1)
    raise RuntimeError(f"browser CDP not ready on port {port}: {last_err}")


def _open_page_ws(port: int, page_uri: str) -> str:
    # Prefer /json/new when available; fall back to first page target + navigate.
    try:
        created = _http_json(f"http://127.0.0.1:{port}/json/new?{page_uri}")
        ws = created.get("webSocketDebuggerUrl")
        if isinstance(ws, str) and ws:
            return ws
    except Exception:  # noqa: BLE001
        pass
    targets = _http_json(f"http://127.0.0.1:{port}/json/list")
    if isinstance(targets, list):
        for target in targets:
            if target.get("type") == "page" and target.get("webSocketDebuggerUrl"):
                return str(target["webSocketDebuggerUrl"])
    raise RuntimeError("no page CDP websocket available")


async def _probe_on_page(
    session: _CdpSession,
    *,
    page_uri: str,
    question_text: str | None,
    answer_text: str | None,
    timeout_s: float,
    already_navigated: bool,
) -> dict[str, Any]:
    await session.call("Page.enable")
    await session.call("Runtime.enable")
    if not already_navigated:
        await session.call("Page.navigate", {"url": page_uri})

    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        ready = await session.call(
            "Runtime.evaluate",
            {"expression": "Boolean(window.MathJax && window.__G6B_RUN__)", "returnByValue": True},
        )
        if ready and ready.get("result", {}).get("value") is True:
            break
        await asyncio.sleep(0.1)
    else:
        raise TimeoutError("MathJax probe page did not become ready")

    payload = {"question_text": question_text, "answer_text": answer_text}
    evaluated = await session.call(
        "Runtime.evaluate",
        {
            "expression": f"window.__G6B_RUN__({json.dumps(payload, ensure_ascii=False)})",
            "awaitPromise": True,
            "returnByValue": True,
        },
        timeout=timeout_s + 5,
    )
    value = evaluated.get("result", {}).get("value")
    if value is None:
        err = await session.call(
            "Runtime.evaluate",
            {"expression": "window.__G6B_ERROR__", "returnByValue": True},
        )
        raise RuntimeError(f"G6b probe failed: {err.get('result', {}).get('value')}")
    out = dict(value)
    out["network"] = _classify_network(session.network_request_urls)
    out["model_calls"] = 0
    out["healer_calls"] = 0
    return out


def render_texts_with_mathjax(
    *,
    question_text: str | None,
    answer_text: str | None,
    browser: BrowserInfo | None = None,
    browser_path: str | Path | None = None,
    timeout_s: float = 60.0,
) -> dict[str, Any]:
    """Insert question/answer into DOM, typeset with vendored MathJax, return evidence.

    If no Chrome/Edge is available, returns status BLOCKED (G6b FAIL) — never falls
    back to regex-only validation.
    """
    browsers = discover_browsers(override=browser_path)
    if browser is None:
        if not browsers:
            blocked = {
                "status": "FAIL",
                "reason": "browser_unavailable",
                "blocked": True,
                "renderer_errors": [{"text": "browser_unavailable", "title": "BLOCKED"}],
                "leftover_latex_commands": [],
                "clipping": False,
                "overlap": False,
                "overlap_is_warning_only": True,
            }
            return {
                "question": {"kind": "question", **blocked},
                "answer": {"kind": "answer", **blocked},
                "mathjax_version": None,
                "mathjax_vendor": str(require_mathjax_vendor()),
                "network": {"network_calls": 0, "remote_urls": [], "local_urls": [], "total_requests_observed": 0},
                "model_calls": 0,
                "healer_calls": 0,
                "blocked": True,
                "status": "BLOCKED",
                "browser": None,
                "ready": False,
            }
        browser = browsers[0]

    port = _free_port()
    with tempfile.TemporaryDirectory(prefix="g6b_mathjax_") as tmp:
        workdir = Path(tmp)
        page = _write_probe_page(workdir)
        page_uri = page.resolve().as_uri()
        user_data = workdir / "chrome-profile"
        user_data.mkdir()
        args = [
            str(browser.path),
            f"--remote-debugging-port={port}",
            f"--user-data-dir={user_data}",
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-sync",
            "--disable-default-apps",
            "--disable-component-update",
            "--disable-features=Translate,BackForwardCache",
            "--allow-file-access-from-files",
            "about:blank",
        ]
        proc = subprocess.Popen(  # noqa: S603 — local browser path only
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            _wait_for_browser(port, timeout_s=timeout_s)
            page_ws = _open_page_ws(port, page_uri)
            # /json/new may already navigate; always ensure navigate inside probe.
            already = False
            result = asyncio.run(
                _run(page_ws, page_uri, question_text, answer_text, timeout_s, already)
            )
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

    result["browser"] = {
        "name": browser.name,
        "path": str(browser.path),
        "version": browser.version,
    }
    result["mathjax_vendor"] = str(require_mathjax_vendor())
    return result


async def _run(
    page_ws: str,
    page_uri: str,
    question_text: str | None,
    answer_text: str | None,
    timeout_s: float,
    already_navigated: bool,
) -> dict[str, Any]:
    async with _CdpSession(page_ws) as session:
        return await _probe_on_page(
            session,
            page_uri=page_uri,
            question_text=question_text,
            answer_text=answer_text,
            timeout_s=timeout_s,
            already_navigated=already_navigated,
        )
