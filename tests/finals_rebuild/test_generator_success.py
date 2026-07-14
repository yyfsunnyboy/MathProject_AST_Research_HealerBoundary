from agent_tools.finals_rebuild.generator_success import (
    FAIL, NOT_ASSESSED, NOT_OBSERVED, PASS, composite_outcomes,
    evaluate_math_notation, evaluate_problem_presentation,
)


def test_presentation_cases():
    assert evaluate_problem_presentation("Calculate 2 + 2.")["status"] == PASS
    assert evaluate_problem_presentation(None)["status"] == NOT_OBSERVED
    assert evaluate_problem_presentation("Solve {{value}}.")["status"] == FAIL
    assert evaluate_problem_presentation("Return only Python.")["status"] == FAIL
    assert evaluate_problem_presentation("def generate(): pass")["status"] == FAIL


def test_notation_cases():
    assert evaluate_math_notation("Calculate 2 × 3.")["status"] == PASS
    assert evaluate_math_notation("Calculate $x + 1$.")["status"] == PASS
    assert evaluate_math_notation("Calculate $x + 1.")["status"] == FAIL
    assert evaluate_math_notation(r"Solve \(x+1\).")["status"] == PASS
    assert evaluate_math_notation(r"Solve \[x+1.")["status"] == FAIL
    assert evaluate_math_notation("Trailing slash \\")["status"] == FAIL


def test_composites():
    names = ("g1_evaluability", "g2_executability", "g3_contract_compliance", "g4_semantic_correctness", "g5_problem_presentation", "g6_math_notation")
    gates = {name: {"status": PASS} for name in names}
    assert composite_outcomes(gates)["full_pass"] == PASS
    gates["g4_semantic_correctness"]["status"] = FAIL
    assert composite_outcomes(gates)["technical_pass"] == FAIL
    gates["g4_semantic_correctness"]["status"] = PASS
    gates["g6_math_notation"]["status"] = NOT_OBSERVED
    assert composite_outcomes(gates)["full_pass"] == NOT_OBSERVED
    gates["g1_evaluability"]["status"] = FAIL
    gates["g2_executability"]["status"] = NOT_ASSESSED
    assert composite_outcomes(gates)["technical_pass"] == FAIL
