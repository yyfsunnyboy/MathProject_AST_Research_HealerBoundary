"""Shared helpers for Tier D D3/D1 rules."""

from __future__ import annotations

import ast
from typing import Optional

OPS_NAMES = frozenset({"IntegerOps", "FractionOps", "RadicalOps", "PolynomialOps"})


def is_parseable(source: str) -> bool:
    try:
        ast.parse(source)
    except SyntaxError:
        return False
    return True


def is_compilable(source: str) -> bool:
    try:
        compile(source, "<tier_d>", "exec")
    except SyntaxError:
        return False
    return True


def unique_generate(tree: ast.Module) -> Optional[ast.FunctionDef]:
    gens = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "generate"]
    if len(gens) == 1:
        return gens[0]
    return None


def line_span_source(source: str, start_lineno: int, end_lineno: int) -> str:
    """1-based inclusive line span."""
    lines = source.splitlines(keepends=True)
    return "".join(lines[start_lineno - 1 : end_lineno])


def replace_line_span(source: str, start_lineno: int, end_lineno: int, replacement: str) -> str:
    lines = source.splitlines(keepends=True)
    before = "".join(lines[: start_lineno - 1])
    after = "".join(lines[end_lineno:])
    return before + replacement + after


def comment_out_lines(text: str, *, marker: str = "# TIER_D_QUARANTINE: ") -> str:
    """Comment-out contiguous residue; preserve original newlines."""
    if not text:
        return text
    keepends = text.splitlines(keepends=True)
    out: list[str] = []
    for line in keepends:
        if line.strip() == "":
            out.append(line)
            continue
        # Preserve ending newline
        if line.endswith("\r\n"):
            body, nl = line[:-2], "\r\n"
        elif line.endswith("\n"):
            body, nl = line[:-1], "\n"
        else:
            body, nl = line, ""
        if body.lstrip().startswith("#"):
            out.append(line)
        else:
            out.append(f"{marker}{body}{nl}")
    return "".join(out)


def names_bound_in_module_fragment(tree: ast.AST) -> set[str]:
    bound: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                bound.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    continue
                bound.add(alias.asname or alias.name)
        elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            bound.add(node.name)
        elif isinstance(node, ast.ClassDef):
            bound.add(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    bound.add(t.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            bound.add(node.target.id)
    return bound


def names_loaded_in(tree: ast.AST) -> set[str]:
    return {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
