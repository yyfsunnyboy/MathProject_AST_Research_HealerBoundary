# -*- coding: utf-8 -*-
"""Math16 Ab2d V2 formal runner: ab2d_domain_menu_v2 / qwen_4b."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.math16_ab2d_v2_formal_cli import run_cli

if __name__ == "__main__":
    raise SystemExit(run_cli("ab2d_domain_menu_v2", "qwen_4b"))
