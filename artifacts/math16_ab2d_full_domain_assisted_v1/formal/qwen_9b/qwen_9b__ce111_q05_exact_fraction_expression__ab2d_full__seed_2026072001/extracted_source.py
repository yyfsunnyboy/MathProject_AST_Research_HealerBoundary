from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Construct fraction leaves from frozen_params expression components
    f_9_22 = FractionOps.from_parts(9, 22)
    f_11_18 = FractionOps.from_parts(11, 18)
    f_23_22 = FractionOps.from_parts(23, 22)
    f_7_18 = FractionOps.from_parts(7, 18)

    # Evaluate inner parenthesis: (23/22 - 7/18)
    inner_diff = FractionOps.sub(f_23_22, f_7_18)

    # Evaluate full expression: 9/22 + 11/18 - inner_diff
    left_sum = FractionOps.add(f_9_22, f_11_18)
    result = FractionOps.sub(left_sum, inner_diff)

    return {
        "question_text": r"精確計算 \[\frac{9}{22}+\frac{11}{18}-\left(\frac{23}{22}-\frac{7}{18}\right).\ 答案須化為最簡分數。",
        "correct_answer": {
            "numerator": result.numerator,
            "denominator": result.denominator,
            "canonical_latex": FractionOps.to_latex(result)
        },
        "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }