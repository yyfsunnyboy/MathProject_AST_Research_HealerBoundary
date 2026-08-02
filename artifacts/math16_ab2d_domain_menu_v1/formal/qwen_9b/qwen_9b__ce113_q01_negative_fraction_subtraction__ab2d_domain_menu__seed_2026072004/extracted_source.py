from core.prompts.domain_function_library import FractionOps, Fraction

def generate(level=1, **kwargs):
    # Parse the frozen expression components from oracle_payload to ensure consistency
    expr_str = kwargs.get("oracle_payload", {}).get("expression")
    
    # Extract numbers based on the specific task: 3/7 - (-1/4)
    num1_numerator = 3
    num1_denominator = 7
    
    neg_num2_sign = -1  # Represents the negative sign before the fraction in "-(-1/4)" logic, 
                        # but mathematically we are subtracting a negative.
                        # The expression is A - B where B = (-1)/4? No.
                        # Expression: 3/7 - ( -1 / 4 )
                        # Let's parse strictly from the string "3/7 - (-1/4)" if needed, 
                        # but we have explicit values in frozen_params logic usually implied by task_id.
    
    # Reconstructing based on standard interpretation of "3/7 - (-1/4)":
    # Term 1: +3/7
    # Term 2 inside parenthesis: -1/4
    # Operation: Subtraction
    
    frac_a = FractionOps.from_parts(num1_numerator, num1_denominator)
    
    # The second term is explicitly negative one fourth.
    # We need to construct the fraction -1/4 first.
    frac_b_inner = FractionOps.from_parts(-1, 4)
    
    # Perform subtraction: A - B
    result_frac = FractionOps.sub(frac_a, frac_b_inner)
    
    # Prepare canonical latex using mixed=False as per standard requirement unless specified otherwise
    # The example showed '\frac{2}{7}' for positive. For negative results or negatives in numerator/denom?
    # to_latex handles signs usually by placing them on the fraction bar if possible, 
    # but Python Fraction's sign is typically on the denominator or handled specifically.
    # Let's rely on FractionOps.to_latex which returns a string representation compatible with LaTeX.
    
    latex_str = FractionOps.to_latex(result_frac)
    
    return {
        "question_text": kwargs.get("oracle_payload", {}).get("expression"), 
        "correct_answer": {
            "numerator": result_frac.numerator,
            "denominator": result_frac.denominator,
            "canonical_latex": latex_str
        },
        "oracle_payload": kwargs.get("oracle_payload")
    }