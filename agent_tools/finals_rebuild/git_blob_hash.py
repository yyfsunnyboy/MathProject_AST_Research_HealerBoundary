"""Canonical freeze-asset hashing: SHA-256 of git blob content (LF).

Working-tree CRLF must not affect freeze hashes. Prefer the git index/HEAD
blob; fall back to LF-normalized disk bytes for untracked paths.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


def normalize_to_lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_git_blob_lf(path: Path, *, repo_root: Path | None = None) -> str:
    """Return SHA-256 of the path's git blob bytes (LF), matching freeze basis."""
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    resolved = path.resolve()
    try:
        rel = resolved.relative_to(root).as_posix()
    except ValueError:
        rel = path.as_posix().replace("\\", "/")

    data: bytes | None = None
    for spec in (f":{rel}", f"HEAD:{rel}"):
        try:
            data = subprocess.check_output(
                ["git", "-C", str(root), "cat-file", "blob", spec],
                stderr=subprocess.DEVNULL,
            )
            break
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    if data is None:
        data = normalize_to_lf(resolved.read_bytes())
    return sha256_bytes(data)


def git_blob_oid(path: Path, *, repo_root: Path | None = None) -> str:
    """Return git object id (`git hash-object`), LF-normalized via git."""
    root = (repo_root or Path(__file__).resolve().parents[2]).resolve()
    return subprocess.check_output(
        ["git", "-C", str(root), "hash-object", str(path)],
        text=True,
    ).strip()
