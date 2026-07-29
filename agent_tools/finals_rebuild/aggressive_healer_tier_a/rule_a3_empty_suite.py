"""A3: TIER_A_EMPTY_SUITE_INSERT_PASS_V1."""

from __future__ import annotations

import re
from typing import Any

from agent_tools.finals_rebuild.aggressive_healer_tier_a.common import (
    indent_width,
    is_blank,
    is_comment_only,
    is_parseable,
    newline_of,
    parse_error,
    source_sha,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_a.types import RuleResult

RULE_ID = "TIER_A_EMPTY_SUITE_INSERT_PASS_V1"
SEQUENCE_INDEX = 3

_HEADER_RE = re.compile(
    r"^([ \t]*)(?:if|elif|else|for|while|try|except|finally|with|def|class|match|case)\b"
    r"[^:\n]*:\s*(#.*)?$"
)

_EMPTY_SUITE_ERR_RE = re.compile(
    r"expected an indented block|expected 'except'|unexpected EOF",
    re.IGNORECASE,
)


def _find_empty_suite_sites(source: str) -> list[dict[str, Any]]:
    lines = source.splitlines(keepends=True)
    sites: list[dict[str, Any]] = []
    i = 0
    while i < len(lines):
        logical = lines[i].rstrip("\r\n")
        match = _HEADER_RE.match(logical)
        if not match:
            i += 1
            continue

        header_indent = indent_width(logical)
        # Determine kind token.
        kind_m = re.match(
            r"^[ \t]*(if|elif|else|for|while|try|except|finally|with|def|class|match|case)\b",
            logical,
        )
        kind = kind_m.group(1) if kind_m else "unknown"

        j = i + 1
        saw_exec = False
        comment_indent = None
        while j < len(lines):
            suite_logical = lines[j].rstrip("\r\n")
            if is_blank(suite_logical):
                j += 1
                continue
            suite_indent = indent_width(suite_logical)
            if suite_indent <= header_indent:
                break
            if is_comment_only(suite_logical):
                if comment_indent is None:
                    comment_indent = suite_indent
                j += 1
                continue
            saw_exec = True
            break

        if saw_exec:
            i += 1
            continue

        # Empty (blank and/or comment-only) suite.
        suite_indent = (
            comment_indent if comment_indent is not None else header_indent + 4
        )
        sites.append(
            {
                "header_index": i,
                "header_lineno": i + 1,
                "suite_end_index": j,
                "insert_after_index": i,
                "suite_indent": suite_indent,
                "suite_owner_kind": kind,
            }
        )
        i += 1
    return sites


def _insert_pass(source: str, site: dict[str, Any]) -> str:
    lines = source.splitlines(keepends=True)
    idx = int(site["insert_after_index"])
    header = lines[idx]
    nl = newline_of(header)
    indent = " " * int(site["suite_indent"])
    pass_line = f"{indent}pass{nl}"
    return "".join(lines[: idx + 1] + [pass_line] + lines[idx + 1 :])


def apply_once(source: str) -> RuleResult:
    pre_sha = source_sha(source)
    err, _lineno = parse_error(source)
    pre_parse = err is None
    result = RuleResult(
        rule_id=RULE_ID,
        sequence_index=SEQUENCE_INDEX,
        pre_source_sha=pre_sha,
        pre_parseable=pre_parse,
        source_out=source,
        post_source_sha=pre_sha,
        post_parseable=pre_parse,
    )

    if err is None:
        result.abstained = True
        result.abstention_reason = "source_already_parses"
        result.outcome_taxonomy = "noop"
        return result

    # Prefer empty-suite shaped errors; still allow site scan if message is weak
    # but require trial uniqueness.
    sites = _find_empty_suite_sites(source)
    if not sites:
        result.abstained = True
        result.abstention_reason = "no_empty_suite_site"
        result.outcome_taxonomy = "abstain"
        result.trigger_evidence = err
        return result

    # Spec eligibility: empty suite site must be unique before mutation.
    if len(sites) > 1:
        result.abstained = True
        result.abstention_reason = f"ambiguous_empty_suites_count_{len(sites)}"
        result.outcome_taxonomy = "abstain"
        result.trigger_evidence = err
        result.extras["candidate_count"] = len(sites)
        return result

    successful: list[dict[str, Any]] = []
    for site in sites:
        trial = _insert_pass(source, site)
        if is_parseable(trial):
            successful.append({"site": site, "fixed_source": trial})

    if len(successful) == 0:
        result.abstained = True
        result.abstention_reason = "empty_suite_insert_pass_still_unparseable"
        result.outcome_taxonomy = "abstain"
        result.trigger_evidence = err
        return result
    if len(successful) > 1:
        result.abstained = True
        result.abstention_reason = f"ambiguous_empty_suites_count_{len(successful)}"
        result.outcome_taxonomy = "abstain"
        result.trigger_evidence = err
        result.extras["candidate_count"] = len(successful)
        return result

    # If the parse error does not look like empty-suite and we somehow found a
    # unique fix, still require empty-suite shaped error to avoid unrelated repairs.
    if not _EMPTY_SUITE_ERR_RE.search(err) and "indented block" not in err.lower():
        # Python 3.12+ often: "expected an indented block after 'if' statement"
        if "indented" not in err.lower() and "unexpected EOF" not in err.lower():
            result.abstained = True
            result.abstention_reason = "syntax_error_not_empty_suite"
            result.outcome_taxonomy = "abstain"
            result.trigger_evidence = err
            return result

    site = successful[0]["site"]
    fixed = successful[0]["fixed_source"]
    result.triggered = True
    result.applied = True
    result.edit_count = 1
    result.edit_scope = "single_empty_suite_insert_pass"
    result.source_out = fixed
    result.post_source_sha = source_sha(fixed)
    result.post_parseable = True
    result.trigger_evidence = err
    result.ast_node_location = {
        "header_lineno": site["header_lineno"],
        "insert_lineno": site["header_lineno"] + 1,
    }
    result.extras.update(
        {
            "suite_owner_kind": site["suite_owner_kind"],
            "insert_lineno": site["header_lineno"] + 1,
            "suite_indent": site["suite_indent"],
        }
    )
    result.outcome_taxonomy = "repaired"
    return result
