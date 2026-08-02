from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {
        "expression": "9/22 + 11/18 - (23/22 - 7/18)"
    }
    
    # Parse components from the expression string to build fractions manually
    # Expression: 9/22 + 11/18 - (23/22 - 7/18)
    # Let a = 9/22, b = 11/18, c = 23/22, d = 7/18
    
    term_a_num, term_a_den = 9, 22
    term_b_num, term_b_den = 11, 18
    term_c_num, term_c_den = 23, 22
    term_d_num, term_d_den = 7, 18
    
    a = FractionOps.from_parts(term_a_num, term_a_den)
    b = FractionOps.from_parts(term_b_num, term_b_den)
    c = FractionOps.from_parts(term_c_num, term_c_den)
    d = FractionOps.from_parts(term_d_num, term_d_den)
    
    # Calculate inner parenthesis: (c - d)
    inner_parenthesis = FractionOps.sub(c, d)
    
    # Full expression: a + b - inner_parenthesis
    result_part1 = FractionOps.add(a, b)
    final_result = FractionOps.sub(result_part1, inner_parenthesis)
    
    question_text = "精確計算\n\\[ \\frac{9}{22}+\\frac{11}{18}-\\left(\\frac{23}{22}-\\frac{7}{18}\\right). \\]\n答案須化為最簡分數。"
    
    correct_answer = {
        "numerator": final_result.numerator,
        "denominator": final_result.denominator,
        "canonical_latex": FractionOps.to_latex(final_result)
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }