# -*- coding: utf-8 -*-
from __future__ import annotations

import ast
from typing import Any, Optional


OPS_CLASS_NAMES = frozenset({"IntegerOps", "FractionOps", "RadicalOps", "PolynomialOps"})


def is_parseable(source: str) -> bool:
    try:
        ast.parse(source)
        return True
    except SyntaxError:
        return False


def parse_tree(source: str) -> Optional[ast.Module]:
    try:
        return ast.parse(source)
    except SyntaxError:
        return None


def count_generate_defs(tree: ast.AST) -> int:
    return sum(
        1
        for n in getattr(tree, "body", [])
        if isinstance(n, ast.FunctionDef) and n.name == "generate"
    )


def iter_ops_calls(tree: ast.AST) -> list[ast.Call]:
    out: list[ast.Call] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            if func.value.id in OPS_CLASS_NAMES or func.value.id.endswith("Ops"):
                out.append(node)
    return out


def fqname(call: ast.Call) -> str:
    assert isinstance(call.func, ast.Attribute)
    assert isinstance(call.func.value, ast.Name)
    return f"{call.func.value.id}.{call.func.attr}"


def unparse(node: ast.AST) -> str:
    try:
        return ast.unparse(node)
    except Exception:
        return type(node).__name__


def node_loc(node: ast.AST) -> dict[str, Any]:
    return {
        "lineno": getattr(node, "lineno", None),
        "end_lineno": getattr(node, "end_lineno", None),
        "col_offset": getattr(node, "col_offset", None),
        "end_col_offset": getattr(node, "end_col_offset", None),
        "type": type(node).__name__,
    }


def source_fingerprint_excluding_span(
    source: str, node: ast.AST
) -> tuple[str, str]:
    """Return (before_full, region) for certificate snippets (region = node source)."""
    try:
        region = ast.get_source_segment(source, node) or unparse(node)
    except Exception:
        region = unparse(node)
    return source, region


def replace_node_span(source: str, node: ast.AST, new_text: str) -> Optional[str]:
    if not all(
        getattr(node, a, None) is not None
        for a in ("lineno", "col_offset", "end_lineno", "end_col_offset")
    ):
        return None
    lines = source.splitlines(keepends=True)
    # Compute byte offsets via character rebuild
    start_line = node.lineno - 1
    end_line = node.end_lineno - 1
    if start_line == end_line:
        line = lines[start_line]
        new_line = line[: node.col_offset] + new_text + line[node.end_col_offset :]
        lines[start_line] = new_line
        return "".join(lines)
    prefix = lines[start_line][: node.col_offset]
    suffix = lines[end_line][node.end_col_offset :]
    mid = new_text
    new_lines = lines[:start_line] + [prefix + mid + suffix] + lines[end_line + 1 :]
    return "".join(new_lines)


def expr_name(node: ast.AST) -> Optional[str]:
    if isinstance(node, ast.Name):
        return node.id
    return None


def is_call_ops(node: ast.AST, cls: str, meth: str) -> bool:
    if not isinstance(node, ast.Call):
        return False
    f = node.func
    return (
        isinstance(f, ast.Attribute)
        and isinstance(f.value, ast.Name)
        and f.value.id == cls
        and f.attr == meth
    )
