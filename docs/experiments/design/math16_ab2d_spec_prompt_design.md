# Math16 Ab2d+Spec Prompt Design

This document details the design specifications and structural rules for the `Ab2d+spec` treatment in the Pilot-02 phase.

## Prompt Composition Formula

The `Ab2d+spec` prompt is constructed as follows:

```text
Ab2d+spec
= frozen task contract
+ Ab2g prefix
+ compact Domain Scaffold
+ one matching Task Guardrails card
+ compact Final Check
```

## Key Architectural Principles

1. **Parallel Execution with Ab2d+api**:
   - `Ab2d+api` and `Ab2d+spec` are parallel treatments representing distinct levels/types of domain-specific constraints. They are NOT stacked or accumulated (i.e. `Ab2d+spec` does not build on top of `Ab2d+api`).
   - `Ab2d+spec` replaces the domain API exposure block entirely with the compact Domain Scaffold, rather than adding to it.

2. **Integer Native-Only Restriction**:
   - All four tasks in the Integer family for Pilot-02 are classified as **native-only**.
   - The generated programs for these tasks must NOT import, reference, or call the `IntegerOps` API.

3. **Reference Shell vs. Compact Scaffold**:
   - The reference file (`Example_Program_Research_Math16_Ab2d_Spec_Reference.py`) is for **researcher-facing reference only** and must never be injected into model prompts.
   - The compact scaffold (`integer_domain_scaffold_compact.py`) is the only scaffold code structure injected directly into the model's prompt.

4. **Task-Specific Isolation**:
   - Each prompt must contain exactly one matching Task Guardrail card, restricted to the card corresponding to that specific task. Stacking multiple guardrail cards is strictly prohibited.

5. **Data Dependencies and Boundary Controls**:
   - The prompt construction may utilize the target math question, the runtime contract, and frozen historical evidence/parameters.
   - It is strictly forbidden to use any raw responses or rating results from any other conditions within the same Pilot-02 run.
   - All `Ab2d+spec` prompts must be completed and frozen prior to the first Pilot-02 model call.
