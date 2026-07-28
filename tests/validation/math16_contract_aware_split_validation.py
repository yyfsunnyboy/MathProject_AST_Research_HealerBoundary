#!/usr/bin/env python3
"""
Validation Script for Math16 Contract-Aware 40/120 Task-Level Split

Reads the split manifest and performs read-only integrity checks:
1. Cell counts (40 dev, 120 eval, 160 total)
2. Task mutual exclusion and completeness
3. Condition consistency (ab2d, ab2d_spec_v2 only)
4. Seed completeness (all 5 per task-condition)
5. No cross-split cell leakage
6. Prior exposure classification consistency
"""

import json
import sys
from collections import defaultdict

def validate_split_manifest(manifest_path):
    """Perform comprehensive validation of the split manifest."""

    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    print("=" * 80)
    print("Math16 Contract-Aware 40/120 Task-Level Split Validation")
    print("=" * 80)

    errors = []
    warnings = []

    # Extract sections
    metadata = manifest.get('metadata', {})
    split_def = manifest.get('split_definition', {})
    dev_cells = manifest.get('cells', {}).get('development', [])
    eval_cells = manifest.get('cells', {}).get('evaluation', [])
    prior_exposure = manifest.get('prior_exposure_summary', {})

    # ========== CHECK 1: Cell Counts ==========
    print("\n[1] Cell Count Validation")
    print("-" * 80)

    expected_dev = 40
    expected_eval = 120
    expected_total = 160

    actual_dev = len(dev_cells)
    actual_eval = len(eval_cells)
    actual_total = actual_dev + actual_eval

    print(f"Development cells:  {actual_dev} (expected {expected_dev})")
    if actual_dev != expected_dev:
        errors.append(f"Development cell count mismatch: {actual_dev} != {expected_dev}")
    else:
        print("  ✓ PASS")

    print(f"Evaluation cells:   {actual_eval} (expected {expected_eval})")
    if actual_eval != expected_eval:
        errors.append(f"Evaluation cell count mismatch: {actual_eval} != {expected_eval}")
    else:
        print("  ✓ PASS")

    print(f"Total cells:        {actual_total} (expected {expected_total})")
    if actual_total != expected_total:
        errors.append(f"Total cell count mismatch: {actual_total} != {expected_total}")
    else:
        print("  ✓ PASS")

    # ========== CHECK 2: Task Mutual Exclusion ==========
    print("\n[2] Task Mutual Exclusion")
    print("-" * 80)

    dev_tasks = set(c['task_id'] for c in dev_cells)
    eval_tasks = set(c['task_id'] for c in eval_cells)

    print(f"Development tasks: {len(dev_tasks)}")
    print(f"Evaluation tasks:  {len(eval_tasks)}")

    intersection = dev_tasks & eval_tasks
    if intersection:
        errors.append(f"Tasks present in both cohorts: {intersection}")
        print(f"  ✗ FAIL: Tasks in both cohorts: {intersection}")
    else:
        print("  ✓ PASS: No task overlap")

    # ========== CHECK 3: Task Completeness ==========
    print("\n[3] Development Task Completeness")
    print("-" * 80)

    expected_dev_tasks = {
        'ce111_q08_polynomial_factor_parameter_recovery',
        'ce111_nonchoice_q01_part1_exponential_growth',
        'ce111_q05_exact_fraction_expression',
        'ce111_q10_ordered_quadratic_roots_radical',
    }

    if dev_tasks == expected_dev_tasks:
        print(f"  ✓ PASS: Development tasks match exactly ({len(dev_tasks)} tasks)")
        for task in sorted(dev_tasks):
            print(f"    - {task}")
    else:
        missing = expected_dev_tasks - dev_tasks
        extra = dev_tasks - expected_dev_tasks
        if missing:
            errors.append(f"Missing development tasks: {missing}")
            print(f"  ✗ Missing: {missing}")
        if extra:
            errors.append(f"Extra development tasks: {extra}")
            print(f"  ✗ Extra: {extra}")

    print("\n[4] Evaluation Task Count")
    print("-" * 80)

    expected_eval_count = 12
    if len(eval_tasks) == expected_eval_count:
        print(f"  ✓ PASS: {len(eval_tasks)} evaluation tasks")
    else:
        errors.append(f"Evaluation task count: {len(eval_tasks)} != {expected_eval_count}")
        print(f"  ✗ FAIL: {len(eval_tasks)} != {expected_eval_count}")

    # ========== CHECK 5: Condition Consistency ==========
    print("\n[5] Condition Consistency")
    print("-" * 80)

    expected_conditions = {'ab2d', 'ab2d_spec_v2'}

    dev_conditions = set(c['condition'] for c in dev_cells)
    eval_conditions = set(c['condition'] for c in eval_cells)

    print(f"Development conditions: {dev_conditions}")
    if dev_conditions != expected_conditions:
        errors.append(f"Development conditions mismatch: {dev_conditions} != {expected_conditions}")
        print("  ✗ FAIL")
    else:
        print("  ✓ PASS")

    print(f"Evaluation conditions:  {eval_conditions}")
    if eval_conditions != expected_conditions:
        errors.append(f"Evaluation conditions mismatch: {eval_conditions} != {expected_conditions}")
        print("  ✗ FAIL")
    else:
        print("  ✓ PASS")

    # ========== CHECK 6: Seed Completeness ==========
    print("\n[6] Seed Completeness")
    print("-" * 80)

    expected_seeds = {2026071301, 2026072001, 2026072002, 2026072003, 2026072004}
    expected_seeds_per_task_condition = 5

    # Check development
    dev_by_task_cond = defaultdict(set)
    for cell in dev_cells:
        key = (cell['task_id'], cell['condition'])
        dev_by_task_cond[key].add(cell['seed'])

    dev_seed_pass = True
    for (task, cond), seeds in sorted(dev_by_task_cond.items()):
        if seeds != expected_seeds:
            errors.append(f"Dev task {task} cond {cond}: seeds {seeds} != {expected_seeds}")
            dev_seed_pass = False

    if dev_seed_pass:
        print("  ✓ PASS: All development task-condition pairs have all 5 seeds")
    else:
        print("  ✗ FAIL: Some development task-condition pairs missing seeds")

    # Check evaluation (spot check a few)
    eval_by_task_cond = defaultdict(set)
    for cell in eval_cells:
        key = (cell['task_id'], cell['condition'])
        eval_by_task_cond[key].add(cell['seed'])

    eval_seed_pass = True
    for (task, cond), seeds in sorted(eval_by_task_cond.items()):
        if seeds != expected_seeds:
            errors.append(f"Eval task {task} cond {cond}: seeds {seeds} != {expected_seeds}")
            eval_seed_pass = False

    if eval_seed_pass:
        print("  ✓ PASS: All evaluation task-condition pairs have all 5 seeds")
    else:
        print("  ✗ FAIL: Some evaluation task-condition pairs missing seeds")

    # ========== CHECK 7: No Cross-Split Leakage ==========
    print("\n[7] Cross-Split Cell Leakage Check")
    print("-" * 80)

    dev_cell_ids = set(c['cell_id'] for c in dev_cells)
    eval_cell_ids = set(c['cell_id'] for c in eval_cells)

    cell_id_overlap = dev_cell_ids & eval_cell_ids
    if cell_id_overlap:
        errors.append(f"Cell ID overlap between cohorts: {cell_id_overlap}")
        print(f"  ✗ FAIL: {len(cell_id_overlap)} cells in both cohorts")
    else:
        print("  ✓ PASS: No cell ID overlap")

    print(f"Total unique cells: {len(dev_cell_ids) + len(eval_cell_ids)}")

    # ========== CHECK 8: Prior Exposure Classification ==========
    print("\n[8] Prior Exposure Classification Consistency")
    print("-" * 80)

    # Check development prior exposure
    guard_related = prior_exposure.get('guard_related_exposure', [])
    provenance_uncertain = prior_exposure.get('cohort_level_provenance_uncertain', [])
    no_exposure = prior_exposure.get('no_documented_design_exposure', [])

    print(f"Guard-related:           {len(guard_related)} tasks")
    print(f"Provenance uncertain:    {len(provenance_uncertain)} tasks")
    print(f"No documented exposure:  {len(no_exposure)} tasks")

    # Verify each cell has a classification
    for cell in dev_cells:
        if 'prior_exposure_classification' not in cell:
            errors.append(f"Dev cell {cell['cell_id']} missing prior_exposure_classification")

    for cell in eval_cells:
        if 'prior_exposure_classification' not in cell:
            errors.append(f"Eval cell {cell['cell_id']} missing prior_exposure_classification")

    if not errors or all('prior_exposure_classification' in c for c in dev_cells + eval_cells):
        print("  ✓ PASS: All cells have prior_exposure_classification field")
    else:
        print("  ✗ FAIL: Some cells missing prior_exposure_classification")

    # ========== SUMMARY ==========
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)

    if errors:
        print(f"\n✗ VALIDATION FAILED with {len(errors)} error(s):\n")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        return False
    else:
        print("\n✓ ALL VALIDATION CHECKS PASSED")
        print("\nSplit manifest is valid and consistent:")
        print(f"  - 4 development tasks × 2 conditions × 5 seeds = 40 cells")
        print(f"  - 12 evaluation tasks × 2 conditions × 5 seeds = 120 cells")
        print(f"  - Total: 160 cells")
        print(f"  - Mutual exclusion: ✓")
        print(f"  - Condition consistency: ✓")
        print(f"  - Seed completeness: ✓")
        print(f"  - Prior exposure classification: ✓")
        return True

if __name__ == '__main__':
    manifest_path = '/tmp/math16_contract_aware_40_120_split_manifest.json'
    success = validate_split_manifest(manifest_path)
    sys.exit(0 if success else 1)
