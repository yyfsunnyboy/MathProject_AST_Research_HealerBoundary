"""Shared helpers for Aggressive Healer Tier A v1."""

from __future__ import annotations

import ast
import builtins
from typing import Optional

from agent_tools.finals_rebuild.artifacts import sha256_text


_BUILTIN_NAMES = set(dir(builtins))


def source_sha(source: str) -> str:
    return sha256_text(source)


def is_parseable(source: str) -> bool:
    try:
        ast.parse(source)
    except SyntaxError:
        return False
    return True


def parse_error(source: str) -> tuple[Optional[str], Optional[int]]:
    try:
        ast.parse(source)
    except SyntaxError as exc:
        return str(exc), exc.lineno
    return None, None


def split_line_comment(line: str) -> tuple[str, str]:
    """Split a physical line into (code_part, comment_part) respecting quotes."""
    in_single = False
    in_double = False
    in_triple_single = False
    in_triple_double = False
    idx = 0
    n = len(line)
    while idx < n:
        if idx + 2 < n and line[idx : idx + 3] == "'''":
            if not in_double and not in_triple_double:
                in_triple_single = not in_triple_single
            idx += 3
            continue
        if idx + 2 < n and line[idx : idx + 3] == '"""':
            if not in_single and not in_triple_single:
                in_triple_double = not in_triple_double
            idx += 3
            continue
        ch = line[idx]
        if ch == "\\" and idx + 1 < n:
            idx += 2
            continue
        if ch == "'" and not in_double and not in_triple_double:
            in_single = not in_single
        elif ch == '"' and not in_single and not in_triple_single:
            in_double = not in_double
        elif (
            ch == "#"
            and not in_single
            and not in_double
            and not in_triple_single
            and not in_triple_double
        ):
            return line[:idx], line[idx:]
        idx += 1
    return line, ""


def newline_of(line: str) -> str:
    if line.endswith("\r\n"):
        return "\r\n"
    if line.endswith("\n"):
        return "\n"
    return "\n"


def indent_width(line: str) -> int:
    width = 0
    for ch in line:
        if ch == " ":
            width += 1
        elif ch == "\t":
            width += 4
        else:
            break
    return width


def is_blank(line: str) -> bool:
    return line.strip() == ""


def is_comment_only(line: str) -> bool:
    return line.strip().startswith("#")


def builtin_names() -> set[str]:
    return set(_BUILTIN_NAMES)
