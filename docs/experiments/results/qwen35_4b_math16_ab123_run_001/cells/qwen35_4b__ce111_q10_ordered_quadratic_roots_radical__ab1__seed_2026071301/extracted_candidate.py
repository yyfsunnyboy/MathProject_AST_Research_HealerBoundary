def generate(level=1, **kwargs):
    import re
    from sympy import sqrt
    
    # Frozen sampled parameters for this specific task instance
    oracle_payload = {
        "equation": "(x-2)^2=3", 
        "order": "a>b", 
        "target": "2a+b"
    }
    
    # Parse the equation: (x-2)^2 = 3 => x^2 - 4x + 4 = 3 => x^2 - 4x + 1 = 0
    # Coefficients for ax^2 + bx + c = 0 are a=1, b=-4, c=1.
    # Roots: x = [4 +/- sqrt(16-4)] / 2 = [4 +/- sqrt(12)] / 2 = 2 +/- (sqrt(12))/2 
    # Simplify sqrt(12): sqrt(4*3) = 2*sqrt(3).
    # Roots: 2 +/- (2*sqrt(3))/2 => 2 +/- sqrt(3).
    
    a_val, b_val, c_val = 1, -4, 1
    
    # Calculate discriminant
    delta = b_val**2 - 4*a_val*c_val
    
    # Determine roots using formula: (-b ± sqrt(delta)) / (2a)
    # Simplified form for presentation based on task "ordered quadratic roots radical"
    # x1 = (-b + sqrt(delta))/(2a), x2 = (-b - sqrt(delta))/(2a)
    
    numerator_positive = -b_val + sqrt(delta)
    denominator = 2 * a_val
    
    root_positive = numerator_positive / denominator
    root_negative = (numerator_positive / denominator) # Same logic applied to negative branch conceptually but we need the specific simplified form asked for. 
    # Actually, standard simplification: x = -b/2a +/- sqrt(delta)/(2a).
    # Here delta=12. sqrt(12)=sqrt(4*3)=2*sqrt(3).
    # Term to add/subtract is (2*sqrt(3))/2 = sqrt(3).
    
    rational_part = -b_val / denominator
    
    simplified_radical_term = 0
    
    if delta > 0:
        from sympy import sqrt, Rational
        
        d_int = int(delta) # Delta must be a perfect square for clean roots in many contexts but here it's not? 
        # Wait, x^2 -4x +1=0. Roots are (4 +/- sqrt(16-4))/2 = 2 +/- sqrt(3).
        # So the radical term is just sqrt(3). The coefficient of the root part outside the bracket doesn't have a common factor with denominator after simplification? 
        # Let's re-calculate carefully.
        # x = (4 + sqrt(12)) / 2 = 2 + sqrt(12)/2 = 2 + sqrt(3).
        # So rational part is 2, radical coefficient is 1, radicand is 3.
        
        term_radicant_val = int(delta) if delta.is_integer else None
        
        # Sympy simplification for presentation
        simplified_root_plus = root_positive.simplify()
        simplified_root_minus = root_negative.simplify()
    else:
        return {
            "question_text": r"$$\frac{-b \pm \sqrt{d}}{2a}$$", 
            "correct_answer": {"rational_coefficient": 0, "radical_coefficient": None, "radicand": None},
            "oracle_payload": oracle_payload
        }

    # Format the LaTeX question text with formal delimiters
    latex_question = r"Find all roots for the quadratic equation $(x-2)^2=3$."
    
    correct_answer_obj = {
        "rational_coefficient": 0, 
        "radical_coefficient": None if not root_positive.is_rational else float(root_positive - rational_part), # Re-check logic
        
        'canonical_latex': r"$$x = 2 \pm \sqrt{3}$$",

    }
    
    return {
            "question_text": latex_question, 
            "correct_answer": correct_answer_obj,
            "oracle_payload": oracle_payload
        }