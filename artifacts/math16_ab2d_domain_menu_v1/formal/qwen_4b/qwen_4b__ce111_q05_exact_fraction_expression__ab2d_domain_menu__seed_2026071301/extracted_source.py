from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Parse the expression components from frozen_params
    expr = kwargs.get("oracle_payload", {}).get("expression")
    
    # Extract fractions: 9/22 + 11/18 - (23/22 - 7/18)
    # This is equivalent to: 9/22 + 11/18 - 23/22 + 7/18
    
    a = FractionOps.from_parts(9, 22)
    b = FractionOps.from_parts(11, 18)
    
    # The term in parentheses: (23/22 - 7/18)
    c = FractionOps.from_parts(23, 22)
    d = FractionOps.from_parts(7, 18)
    paren_result = FractionOps.sub(c, d)
    
    # Full expression: a + b - (c - d) => a + b - paren_result
    result_step1 = FractionOps.add(a, b)
    final_value = FractionOps.sub(result_step1, paren_result)
    
    question_text = "精確計算\n\\[\n\\frac{9}{22}+\\frac{11}{18}\n-\\left(\\frac{23}{22}-\\frac{7}{18}\\right).\n\\]\n答案須化為最簡分數。"
    
    # Construct correct_answer according to the contract:
    # numerator, denominator (integers), canonical_latex (string)
    num = final_value.numerator
    den = final_value.denominator
    
    latex_str = FractionOps.to_latex(final_value)

    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": int(num),
            "denominator": int(den),
            "canonical_latex": latex_str
        },
        "oracle_payload": kwargs.get("oracle_payload", {"expression": expr}) if isinstance(expr, str) else kwargs.get("oracle_payload") or {}
    }
