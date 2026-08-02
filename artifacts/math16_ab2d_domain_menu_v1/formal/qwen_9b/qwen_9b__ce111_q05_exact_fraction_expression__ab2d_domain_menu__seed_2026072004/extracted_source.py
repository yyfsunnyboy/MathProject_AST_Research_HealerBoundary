from core.prompts.domain_function_library import FractionOps, Fraction

def generate(level=1, **kwargs):
    # Parse the expression components from frozen_params logic implied by task description
    # Expression: 9/22 + 11/18 - (23/22 - 7/18)
    
    term_a = FractionOps.from_parts(9, 22)
    term_b = FractionOps.from_parts(11, 18)
    term_c = FractionOps.from_parts(23, 22)
    term_d = FractionOps.from_parts(7, 18)

    # Calculate inner parenthesis: (term_c - term_d)
    inner_parenthesis = FractionOps.sub(term_c, term_d)

    # Calculate full expression: term_a + term_b - inner_parenthesis
    partial_sum = FractionOps.add(term_a, term_b)
    result = FractionOps.sub(partial_sum, inner_parenthesis)

    # Prepare correct_answer according to contract
    numerator = int(result.numerator)
    denominator = int(result.denominator)
    
    question_text = "精確計算 \\[\\frac{9}{22}+\\frac{11}{18}-\\left(\\frac{23}{22}-\\frac{7}{18}\\right).\\] 答案須化為最簡分數。"

    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": FractionOps.to_latex(result)
        },
        "oracle_payload": {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    }