from core.prompts.domain_function_library import FractionOps, Fraction

def generate(level=1, **kwargs):
    # Parse the frozen expression components from kwargs or defaults if needed.
    # The task specifies: 3/7 - (-1/4)
    # This is equivalent to (3/7) + (1/4).
    
    # Define operands based on the specific math problem provided in 'frozen_params' logic
    # Term A: 3/7
    num_a = 3
    den_a = 7
    
    # Term B: -(-1/4) which becomes +1/4. 
    # The expression is "3/7 - (-1/4)". 
    # We construct the two fractions involved in the operation before simplification logic if needed,
    # but FractionOps handles arithmetic directly.
    
    frac_a = FractionOps.from_parts(num_a, den_a)
    frac_b_neg = FractionOps.from_parts(-1, 4)  # Represents -1/4
    
    # The expression is A - B where B is (-1/4). 
    # So we compute: frac_a - frac_b_neg.
    
    result_frac = FractionOps.sub(frac_a, frac_b_neg)
    
    # Prepare the canonical answer components
    numerator = int(result_frac.numerator)
    denominator = int(result_frac.denominator)
    latex_str = FractionOps.to_latex(result_frac)
    
    return {
        "question_text": r"精確計算 \[\frac{3}{7}-\left(-\frac{1}{4}\right).\] 答案須化為最簡分數。",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": latex_str
        },
        "oracle_payload": {"expression": "3/7 - (-1/4)"}
    }