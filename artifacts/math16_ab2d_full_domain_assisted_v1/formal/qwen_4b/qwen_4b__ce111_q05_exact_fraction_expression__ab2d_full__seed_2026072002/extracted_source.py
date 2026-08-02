from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Parse frozen expression: 9/22 + 11/18 - (23/22 - 7/18)
    
    # Step 1: Construct fractions from parts
    f1 = FractionOps.from_parts(9, 22)
    f2 = FractionOps.from_parts(11, 18)
    f3 = FractionOps.from_parts(23, 22)
    f4 = FractionOps.from_parts(7, 18)

    # Step 2: Evaluate expression tree
    # Inner parenthesis first: (f3 - f4)
    inner_diff = FractionOps.sub(f3, f4)
    
    # Full expression: f1 + f2 - inner_diff
    sum_part = FractionOps.add(f1, f2)
    result = FractionOps.sub(sum_part, inner_diff)

    # Step 3: Assemble correct_answer according to contract
    canonical_latex = FractionOps.to_latex(result)
    
    return {
        "question_text": r"精確計算\n\[\frac{9}{22}+\frac{11}{18}-\left(\frac{23}{22}-\frac{7}{18}\right).\n答案須化為最簡分數。",
        "correct_answer": {
            "numerator": result.numerator,
            "denominator": result.denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": kwargs["frozen_params"] if "frozen_params" in kwargs else {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }
