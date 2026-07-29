# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen sampled parameters defined directly as per task specification
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Parse the first fraction: 3/7
    frac_a_str = "3/7"
    frac_b_str = "-(-1/4)"  # The expression includes a unary minus before the second fraction
    
    try:
        # Create fractions from string representations handled by FractionOps.create
        f_a = FractionOps.create(frac_a_str)
        
        # Handle the negative sign in front of the second fraction manually for logic clarity, 
        # but rely on create to parse "-1/4" correctly. The expression is "3/7 - (-1/4)".
        # We need to subtract a negative number: 3/7 - (-1/4) = 3/7 + 1/4.
        
        f_b_inner = FractionOps.create("-1/4")
        
        # Logic for subtraction based on expression structure "A - B" where B is "-(-1/4)"? 
        # Actually, the string provided in frozen_params is "3/7 - (-1/4)".
        # This implies we are subtracting the value of (-1/4).
        # So operation: f_a.sub(f_b_inner) -> 3/7 - (-1/4) = 3/7 + 1/4.
        
        result_fraction = f_a.sub(f_b_inner)
    except Exception as e:
        # Fallback if string parsing fails, construct manually using from_parts for robustness in this specific case
        numerator_1, denominator_1 = 3, 7
        numerator_2, denominator_2 = -1, 4
        
        f_a_manual = FractionOps.from_parts(numerator_1, denominator_1)
        f_b_manual = FractionOps.from_parts(numerator_2, denominator_2)
        
        # Perform subtraction: A - B
        result_fraction = f_a_manual.sub(f_b_manual)

    # Extract components for correct_answer
    num = result_fraction.numerator
    den = result_fraction.denominator
    
    # Construct canonical LaTeX string using the numerator and denominator directly from Fraction object
    if den < 0:
        latex_num = "-" + str(-num)
        latex_den = str(-den)
    else:
        latex_num = str(num)
        latex_den = str(den)
    
    # Format canonical_latex as \frac{...}{...} or integer if den is 1 (though here it won't be)
    canonical_latex = f"\\frac{{{latex_num}}}{{{{{latex_den}}}}}"

    correct_answer = {
        "numerator": num,
        "denominator": den,
        "canonical_latex": canonical_latex
    }

    question_text = r"The value of the expression $3/7 - (-1/4)$ is:"

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }