import sys, json, textwrap
from fractions import Fraction

sys.path.insert(0, ".")

from agent_tools.finals_rebuild.math16_ab2d_v2_scaffolds import TASK_SCAFFOLDS_V2
from agent_tools.finals_rebuild.math16_pool import build_pool_tasks
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from core.prompts.domain_function_library import IntegerOps, FractionOps, RadicalOps, PolynomialOps

pool = {t["task_id"]: t for t in build_pool_tasks()}

ok = True
for task_id, scaffold in TASK_SCAFFOLDS_V2.items():
    pool_task = pool[task_id]
    assert scaffold["frozen_literal"] == pool_task["frozen_params"], (
        task_id, scaffold["frozen_literal"], pool_task["frozen_params"]
    )
    ns = {
        "IntegerOps": IntegerOps, "FractionOps": FractionOps,
        "RadicalOps": RadicalOps, "PolynomialOps": PolynomialOps,
        "Fraction": Fraction,
        "frozen": dict(scaffold["frozen_literal"]),
    }
    body = textwrap.dedent(scaffold["full_plan_body"])
    try:
        exec(compile(body, f"<{task_id}>", "exec"), ns)
    except Exception as exc:
        ok = False
        print(f"[EXEC-FAIL] {task_id}: {type(exc).__name__}: {exc}")
        continue
    correct_answer = ns["correct_answer"]
    result = evaluate_math_task_oracle(scaffold["oracle_type"], pool_task["oracle_payload"], correct_answer)
    passed = result.get("is_correct")
    status = "PASS" if passed else "FAIL"
    if not passed:
        ok = False
    print(f"[{status}] {task_id} oracle_type={scaffold['oracle_type']} correct_answer={json.dumps(correct_answer, default=str)}")
    if not passed:
        print("   oracle_result:", result)
    if correct_answer != pool_task["correct_answer"]:
        print(f"   [POOL-MISMATCH] scaffold={correct_answer!r} vs pool.correct_answer={pool_task['correct_answer']!r}")

print()
print("ALL OK" if ok else "SOME FAILED")
