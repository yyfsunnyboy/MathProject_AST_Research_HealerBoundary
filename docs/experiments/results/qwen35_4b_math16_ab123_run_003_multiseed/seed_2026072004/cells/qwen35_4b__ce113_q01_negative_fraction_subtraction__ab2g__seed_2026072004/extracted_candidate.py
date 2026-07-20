def generate(level=1, **kwargs):
    import math
    
    # Frozen sampled parameters from task specification
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    question_text = r"Compute the difference: $\frac{3}{7} - \left(-\frac{1}{4}\right)$."
    
    # Calculate correct answer manually for 3/7 - (-1/4)
    # 3/7 + 1/4 = (3*4)/(7*4) + (1*7)/(4*7) = 12/28 + 7/28 = 19/28
    
    numerator = 19
    denominator = 28
    
    # Verify irreducibility and canonical form for positive fractions > 0
    if denominator != 0:
        gcd_val = math.gcd(numerator, abs(denominator))
        n_final = numerator // gcd_val
        d_final = denominator // gcd_val
        
        # Ensure standard representation (positive denominator)
        if d_final < 0:
            n_final *= -1
            d_final *= -1
            
    correct_answer_str = f"{numerator}/{denominator}"
    
    canonical_latex = r"\frac{19}{28}"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": n_final,
            "denominator": d_final,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }