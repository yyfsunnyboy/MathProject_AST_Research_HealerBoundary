"""Write Math16-LaTeX-v1 pool manifest (no model calls)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_pool import write_pool_manifest


def main() -> None:
    manifest = write_pool_manifest(ROOT)
    print(f"pool_id={manifest['pool_id']}")
    print(f"tasks={len(manifest['tasks'])}")
    print(f"domain_ops={manifest['domain_ops_distribution']}")
    print(f"pool_identity_hash={manifest['pool_identity_hash']}")
    print(f"manifest_content_sha256={manifest['manifest_content_sha256']}")
    print(f"task_freeze_hash={manifest['task_freeze_hash']}")


if __name__ == "__main__":
    main()
