"""A2: TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1."""

from __future__ import annotations

import re
from typing import Any

from agent_tools.finals_rebuild.aggressive_healer_tier_a.common import (
    is_parseable,
    parse_error,
    split_line_comment,
    source_sha,
)
from agent_tools.finals_rebuild.aggressive_healer_tier_a.types import RuleResult

RULE_ID = "TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1"
SEQUENCE_INDEX = 2

_CLOSING = (")", "]", "}")

_DELIMITER_ERR_RE = re.compile(
    r"never closed|unmatched|unexpected EOF|EOF while parsing|was never closed",
    re.IGNORECASE,
)

_EMPTY_SUITE_ERR_RE = re.compile(
    r"expected an indented block|IndentationError",
    re.IGNORECASE,
)


def _is_delimiter_error(msg: str) -> bool:
    if _EMPTY_SUITE_ERR_RE.search(msg):
        return False
    return bool(_DELIMITER_ERR_RE.search(msg))


def _enumerate_closing_inserts(source: str, lineno: int) -> list[dict[str, Any]]:
    lines = source.splitlines(keepends=True)
    if lineno < 1 or lineno > len(lines):
        return []
    err_line = lines[lineno - 1]
    code_part, comment_part = split_line_comment(err_line)
    # Preserve newline belonging to the physical line on comment_part / rebuild.
    # code_part may include trailing spaces before '#'; strip only for insert
    # scanning over the code characters excluding the kept newline.
    nl = ""
    body = code_part
    if body.endswith("\r\n"):
        nl = "\r\n"
        body = body[:-2]
    elif body.endswith("\n"):
        nl = "\n"
        body = body[:-1]
    # If comment_part absorbed the newline, recover.
    if not nl and comment_part:
        if comment_part.endswith("\r\n"):
            nl = "\r\n"
            comment_part = comment_part[:-2]
        elif comment_part.endswith("\n"):
            nl = "\n"
            comment_part = comment_part[:-1]
    if not nl:
        nl = "\n"

    candidates: list[dict[str, Any]] = []
    for pos in range(len(body) + 1):
        for ch in _CLOSING:
            trial_body = body[:pos] + ch + body[pos:]
            trial_line = trial_body + comment_part + nl
            trial_lines = list(lines)
            trial_lines[lineno - 1] = trial_line
            # Preserve files that had no trailing newline on last line.
            if lineno == len(lines) and not lines[-1].endswith(("\n", "\r\n")):
                trial_lines[lineno - 1] = trial_body + comment_part
            trial_source = "".join(trial_lines)
            if is_parseable(trial_source):
                candidates.append(
                    {
                        "lineno": lineno,
                        "pos": pos,
                        "delimiter_char": ch,
                        "fixed_source": trial_source,
                    }
                )
    return candidates


def apply_once(source: str) -> RuleResult:
    pre_sha = source_sha(source)
    err, lineno = parse_error(source)
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

    if lineno is None:
        result.abstained = True
        result.abstention_reason = "missing_line_number"
        result.outcome_taxonomy = "abstain"
        result.trigger_evidence = err
        return result

    if not _is_delimiter_error(err):
        result.abstained = True
        result.abstention_reason = "syntax_error_not_delimiter"
        result.outcome_taxonomy = "abstain"
        result.trigger_evidence = err
        return result

    candidates = _enumerate_closing_inserts(source, lineno)
    if len(candidates) == 0:
        result.abstained = True
        result.abstention_reason = "no_unique_closing_insert"
        result.outcome_taxonomy = "abstain"
        result.trigger_evidence = err
        return result
    if len(candidates) > 1:
        result.abstained = True
        result.abstention_reason = f"ambiguous_closing_inserts_count_{len(candidates)}"
        result.outcome_taxonomy = "abstain"
        result.trigger_evidence = err
        result.extras["candidate_count"] = len(candidates)
        return result

    cand = candidates[0]
    fixed = cand["fixed_source"]
    result.triggered = True
    result.applied = True
    result.edit_count = 1
    result.edit_scope = "single_closing_delimiter_insert"
    result.source_out = fixed
    result.post_source_sha = source_sha(fixed)
    result.post_parseable = True
    result.trigger_evidence = err
    result.ast_node_location = {
        "lineno": cand["lineno"],
        "pos": cand["pos"],
    }
    result.extras.update(
        {
            "delimiter_char": cand["delimiter_char"],
            "insert_location": {
                "lineno": cand["lineno"],
                "pos": cand["pos"],
            },
            "uniqueness_proof": True,
        }
    )
    result.outcome_taxonomy = "repaired"
    return result
