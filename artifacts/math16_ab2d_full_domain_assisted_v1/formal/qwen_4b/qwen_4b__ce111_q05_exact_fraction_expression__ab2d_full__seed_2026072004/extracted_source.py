from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Parse frozen expression: 9/22 + 11/18 - (23/22 - 7/18)
    
    # Step 1: Construct fraction leaves from parts
    f1 = FractionOps.from_parts(9, 22)
    f2 = FractionOps.from_parts(11, 18)
    f3 = FractionOps.from_parts(23, 22)
    f4 = FractionOps.from_parts(7, 18)

    # Step 2: Evaluate expression tree
    # Inner part: (23/22 - 7/18) -> f5
    inner_diff = FractionOps.sub(f3, f4)
    
    # Full expression: 9/22 + 11/18 - result_of_inner_part
    sum_first_two = FractionOps.add(f1, f2)
    final_result = FractionOps.sub(sum_first_two, inner_diff)

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
