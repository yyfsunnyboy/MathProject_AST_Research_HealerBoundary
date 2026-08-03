# -*- coding: utf-8 -*-
"""Contract-Aware Aggressive Healer v2 (first stage; proof-carrying; fail-closed).

Stacks on top of the existing Aggressive Healer packages without modifying them.
Does not write into V1/V2 formal cell artifacts.
"""
from __future__ import annotations

from agent_tools.finals_rebuild.aggressive_healer_contract_v2.pipeline import (
    apply_contract_aware_v2,
    run_frozen_validation_bundle,
)
from agent_tools.finals_rebuild.aggressive_healer_contract_v2.contracts import (
    CONDITIONS,
    build_all_contracts,
    load_contract,
)

__all__ = [
    "CONDITIONS",
    "apply_contract_aware_v2",
    "build_all_contracts",
    "load_contract",
    "run_frozen_validation_bundle",
]
