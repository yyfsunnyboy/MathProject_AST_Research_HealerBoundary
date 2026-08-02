from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Parse the expression components from frozen_params
    expr = kwargs.get("oracle_payload", {}).get("expression")
    
    # Extract fractions: 9/22 + 11/18 - (23/22 - 7/18)
    # This corresponds to: a + b - c where 
    # a = 9/22, b = 11/18, c = 23/22, d = 7/18
    
    term_a_num, term_a_den = FractionOps.from_parts(9, 22)
    term_b_num, term_b_den = FractionOps.from_parts(11, 18)
    
    # The expression is: a + b - (c - d) which equals a + b - c + d
    
    term_c_num, term_c_den = FractionOps.from_parts(23, 22)
    term_d_num, term_d_den = FractionOps.from_parts(7, 18)

    # Calculate step by step: 
    # result = (a + b) - c + d
    
    sum_ab = FractionOps.add(term_a_num, term_b_num)
    
    diff_cd = FractionOps.sub(term_c_num, term_d_num)
    
    final_result = FractionOps.sub(sum_ab, diff_cd)

    return {
        "question_text": kwargs.get("oracle_payload", {}).get("expression"),
        "correct_answer": {
            "numerator": int(final_result.numerator),
            "denominator": int(final_result.denominator),
            "canonical_latex": FractionOps.to_exact(final_result)
        },
        "oracle_payload": kwargs.get("oracle_payload", {})
    }
