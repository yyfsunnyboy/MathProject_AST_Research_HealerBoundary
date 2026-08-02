from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Construct fractions from frozen_params expression: "9/22 + 11/18 - (23/22 - 7/18)"
    f1 = FractionOps.from_parts(9, 22)   # 9/22
    f2 = FractionOps.from_parts(11, 18)  # 11/18
    f3 = FractionOps.from_parts(23, 22)  # 23/22
    f4 = FractionOps.from_parts(7, 18)   # 7/18

    # Evaluate inner parenthesis: (f3 - f4)
    inner_diff = FractionOps.sub(f3, f4)

    # Evaluate outer expression: f1 + f2 - inner_diff
    left_sum = FractionOps.add(f1, f2)
    result = FractionOps.sub(left_sum, inner_diff)

    return {
        "question_text": r"精確計算 \[\frac{9}{22}+\frac{11}{18}-\left(\frac{23}{22}-\frac{7}{18}\right).\ 答案須化為最簡分數。",
        "correct_answer": {
            "numerator": result.numerator,
            "denominator": result.denominator,
            "canonical_latex": FractionOps.to_latex(result),
        },
        "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"},
    }