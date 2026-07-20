"""Record RENDERER/PARSER + think false/true smoke evidence for gate waiver archive."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT
    / "docs/experiments/results/_smoke_nonformal"
    / "qwen_call_layer_gate_waiver_20260720.json"
)
THINK_TAG_RE = re.compile(r"</?think>", re.IGNORECASE)
SMOKE_PROMPT = "print hello"
MODELS = ("qwen3.5:4b", "qwen3.5:9b")


def _show(model: str) -> dict:
    req = urllib.request.Request(
        "http://localhost:11434/api/show",
        data=json.dumps({"model": model}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _modelfile_flags(modelfile: str) -> dict:
    lines = (modelfile or "").splitlines()
    renderer = next((ln.split(None, 1)[1] for ln in lines if ln.startswith("RENDERER ")), None)
    parser = next((ln.split(None, 1)[1] for ln in lines if ln.startswith("PARSER ")), None)
    template = next((ln.split(None, 1)[1] for ln in lines if ln.startswith("TEMPLATE ")), None)
    return {"renderer": renderer, "parser": parser, "template": template}


def _chat(model: str, *, think: bool) -> dict:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": SMOKE_PROMPT}],
        "stream": False,
        "think": think,
        "options": {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 20,
            "num_predict": 256,
            "seed": 2026071301,
        },
    }
    req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _smoke_pair(model: str) -> dict:
    false_body = _chat(model, think=False)
    true_body = _chat(model, think=True)
    f_msg = false_body.get("message") or {}
    t_msg = true_body.get("message") or {}
    f_content = f_msg.get("content") or ""
    f_thinking = f_msg.get("thinking") or ""
    t_content = t_msg.get("content") or ""
    t_thinking = t_msg.get("thinking") or ""
    return {
        "model": model,
        "prompt": SMOKE_PROMPT,
        "think_false": {
            "content_preview": f_content[:300],
            "thinking_empty": not bool(str(f_thinking).strip()),
            "thinking_len": len(f_thinking),
            "has_think_tags": bool(THINK_TAG_RE.search(f_content + f_thinking)),
            "message_keys": sorted(f_msg.keys()),
            "passed": (
                bool(f_content.strip())
                and not str(f_thinking).strip()
                and not THINK_TAG_RE.search(f_content + f_thinking)
            ),
        },
        "think_true": {
            "content_preview": t_content[:200],
            "thinking_len": len(t_thinking),
            "thinking_preview": t_thinking[:300],
            "thinking_nonempty": bool(str(t_thinking).strip()),
            "message_keys": sorted(t_msg.keys()),
            "passed": bool(str(t_thinking).strip()),
        },
    }


def main() -> int:
    ollama_version = subprocess.check_output(
        ["ollama", "--version"], text=True, encoding="utf-8", errors="replace"
    ).strip()
    models = {}
    smokes = {}
    for model in MODELS:
        show = _show(model)
        flags = _modelfile_flags(show.get("modelfile") or "")
        models[model] = {
            "template": show.get("template"),
            "capabilities": show.get("capabilities"),
            "modelfile_flags": flags,
            "renderer_parser_ok": flags["renderer"] == "qwen3.5"
            and flags["parser"] == "qwen3.5",
        }
        smokes[model] = _smoke_pair(model)

    gate = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "ollama_version": ollama_version,
        "gate_policy": {
            "accepted_option": 1,
            "criterion": (
                "RENDERER qwen3.5 + PARSER qwen3.5 + smoke "
                "(think:false no thinking; think:true thinking in message.thinking) "
                "satisfies full chat/think mechanism gate"
            ),
            "literal_template_gate_superseded": True,
            "note": "Old literal TEMPLATE != {{ .Prompt }} gate was based on pre-renderer Ollama.",
        },
        "models": models,
        "smoke_contrast": smokes,
        "all_models_renderer_parser_ok": all(v["renderer_parser_ok"] for v in models.values()),
        "all_smoke_passed": all(
            s["think_false"]["passed"] and s["think_true"]["passed"] for s in smokes.values()
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(gate, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"output": str(OUT), **{k: gate[k] for k in (
        "ollama_version",
        "all_models_renderer_parser_ok",
        "all_smoke_passed",
    )}}, ensure_ascii=False, indent=2))
    return 0 if gate["all_models_renderer_parser_ok"] and gate["all_smoke_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
