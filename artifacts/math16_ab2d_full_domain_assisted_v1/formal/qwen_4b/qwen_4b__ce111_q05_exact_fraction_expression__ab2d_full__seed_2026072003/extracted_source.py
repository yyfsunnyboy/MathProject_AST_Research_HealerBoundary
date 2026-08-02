from core.prompts.domain_function_library import FractionOps, from_parts

def generate(level=1, **kwargs):
    # Parse expression: 9/22 + 11/18 - (23/22 - 7/18)
    # Step 1: Create fractions
    f1 = FractionOps.from_parts(9, 22)
    f2 = FractionOps.from_parts(11, 18)
    f3 = FractionOps.from_parts(23, 22)
    f4 = FractionOps.from_parts(7, 18)

    # Step 2: Evaluate expression tree
    # Inner parenthesis first: (f3 - f4)
    inner_diff = FractionOps.sub(f3, f4)
    
    # Then add/sub from left to right as per standard order of operations for + and - at same level
    # Expression is: f1 + f2 - inner_diff
    step_add = FractionOps.add(f1, f2)
    final_result = FractionOps.sub(step_add, inner_diff)

    # Step 3: Assemble correct_answer according to contract
    canonical_latex = FractionOps.to_latex(final_result)
    
    return {
        "question_text": r"精確計算\n\[\frac{9}{22}+\frac{11}{18}-\left(\frac{23}{22}-\frac{7}{18}\right).\n答案須化為最簡分數。",
        "correct_answer": {
            "numerator": final_result.numerator,
            "denominator": final_result.denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": kwargs.get("frozen_params") or {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }
