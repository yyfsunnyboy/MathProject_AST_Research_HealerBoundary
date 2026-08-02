from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Parse components from the expression string to build fractions manually using API
    f1_num, f1_den = 9, 22
    f2_num, f2_den = 11, 18
    f3_num, f3_den = 23, 22
    f4_num, f4_den = 7, 18
    
    # Create fractions using from_parts API as per domain rules (avoiding direct string parsing of '9/22' if possible to ensure canonical form)
    a = FractionOps.from_parts(f1_num, f1_den)
    b = FractionOps.from_parts(f2_num, f2_den)
    c = FractionOps.from_parts(f3_num, f3_den)
    d = FractionOps.from_parts(f4_num, f4_den)
    
    # Compute inner parenthesis: (c - d)
    inner_diff = FractionOps.sub(c, d)
    
    # Compute main expression: a + b - inner_diff
    sum_ab = FractionOps.add(a, b)
    result = FractionOps.sub(sum_ab, inner_diff)
    
    # Prepare correct_answer according to contract
    canonical_latex = FractionOps.to_latex(result)
    
    return {
        "question_text": "\n精確計算\n\\[ \\frac{9}{22}+\\frac{11}{18}-\\left(\\frac{23}{22}-\\frac{7}{18}\\right). \\\\ 答案須化為最簡分數。",
        "correct_answer": {
            "numerator": result.numerator,
            "denominator": result.denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }