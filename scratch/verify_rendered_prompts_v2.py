import re, sys, json
from fractions import Fraction

sys.path.insert(0, ".")

from agent_tools.finals_rebuild.math16_pool import build_pool_tasks
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from core.prompts.domain_function_library import IntegerOps, FractionOps, RadicalOps, PolynomialOps

pool = {t["task_id"]: t for t in build_pool_tasks()}

ok_all = True
for task_id, task in pool.items():
    path = f"docs/experiments/prompts/ab2d_full_v2/prompts/{task_id}.txt"
    text = open(path, encoding="utf-8").read()
    fences = re.findall(r"```python\n(.*?)```", text, re.S)
    code = fences[-1]  # last fence = the full-plan task-specific scaffold
    ns = {
        "IntegerOps": IntegerOps, "FractionOps": FractionOps,
        "RadicalOps": RadicalOps, "PolynomialOps": PolynomialOps,
        "Fraction": Fraction,
    }
    try:
        exec(compile(code, f"<{task_id}>", "exec"), ns)
        value = ns["generate"]()
    except Exception as exc:
        ok_all = False
        print(f"[EXEC-FAIL] {task_id}: {type(exc).__name__}: {exc}")
        continue
    if set(value) != {"question_text", "correct_answer", "oracle_payload"}:
        ok_all = False
        print(f"[SCHEMA-FAIL] {task_id}: keys={set(value)}")
        continue
    if value["oracle_payload"] != task["frozen_params"]:
        ok_all = False
        print(f"[ORACLE-PAYLOAD-FAIL] {task_id}: {value['oracle_payload']} != {task['frozen_params']}")
        continue
    result = evaluate_math_task_oracle(task["oracle_type"], task["oracle_payload"], value["correct_answer"])
    passed = result.get("is_correct")
    if not passed:
        ok_all = False
    print(f"[{'PASS' if passed else 'FAIL'}] {task_id}")

print()
print("ALL RENDERED-PROMPT SCAFFOLDS OK" if ok_all else "SOME FAILED")
