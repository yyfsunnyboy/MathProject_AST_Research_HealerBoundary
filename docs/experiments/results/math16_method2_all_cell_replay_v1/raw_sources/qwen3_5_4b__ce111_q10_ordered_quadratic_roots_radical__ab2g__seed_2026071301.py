def generate(level=1, **kwargs):
    import re
    
    # Frozen sampled parameters must be preserved exactly in oracle_payload
    frozen_params = {
        "equation": "(x-2)^2=3", 
        "order": "a>b", 
        "target": "2a+b"
    }
    
    # Parse the equation to extract coefficients for a quadratic form ax^2 + bx + c = 0
    # Equation: (x-2)^2 = 3 => x^2 - 4x + 4 = 3 => x^2 - 4x + 1 = 0
    # Here, a=1, b=-4, c=1
    
    equation_str = frozen_params["equation"]
    
    # Construct the question text using formal LaTeX delimiters
    question_text = r"\text{Solve for } x \text{ in the quadratic equation: } " + r"$(x-2)^2=3$."
    
    # Calculate roots manually to ensure correctness and structure
    # Equation form after expansion: 1*x^2 - 4*x + (4-3) = 0 => x^2 - 4x + 1 = 0
    a_val = 1
    b_val = -4
    
    discriminant = b_val**2 - 4*a_val*1 # c is implicitly 1 from expansion logic above, but let's re-verify: (x-2)^2=3 -> x^2-4x+4=3 -> x^2-4x+1=0. Yes, c=1.
    # Wait, the prompt asks for radical form specifically. 
    # Roots are (-b ± sqrt(discriminant)) / 2a
    
    discriminant = b_val**2 - 4*a_val*1 
    
    if discriminant < 0:
        raise ValueError("No real roots found.")
    
    root_part_a = -b_val / (2 * a_val) # This is the rational part of the linear term adjustment, but for standard form (-B)/2A. 
    # Actually, let's stick to the formula directly from x^2 - 4x + 1 = 0
    # Roots: [4 ± sqrt(16 - 4)] / 2 = [4 ± sqrt(12)] / 2 = [4 ± 2*sqrt(3)] / 2 = 2 ± sqrt(3)
    
    # Let's re-calculate based on the specific equation (x-2)^2=3 to be absolutely sure.
    # x^2 - 4x + 4 = 3
    # x^2 - 4x + 1 = 0
    
    a_coeff = 1
    b_coeff = -4
    c_coeff = 1
    
    delta = b_coeff**2 - 4*a_coeff*c_coeff # (-4)^2 - 4*1*1 = 16 - 4 = 12
    
    sqrt_delta_val = int(delta ** 0.5) if delta.is_integer() else float('inf')
    
    # Since discriminant is 12, which is not a perfect square in integers but the problem asks for radical form.
    # The roots are (4 ± √12)/2 = 2 ± √3
    
    # We need to format this as: rational_part + coefficient * sqrt(radicand)
    # Rational part of root 1: 2, Radical coeff: 1, Radicand: 3
    # Or we can keep it unsimplified if the prompt implies a specific structure. 
    # "correct_answer must include result with rational, radical_coefficient (may be +1 or -1), radicand"
    
    # Let's simplify sqrt(12) to 2*sqrt(3).
    # Root = 2 ± √3
    
    rational_part = delta_val := int(delta ** 0.5) if isinstance(int(delta**0.5), float) else None 
    # Re-evaluating: delta=12, sqrt(12)=2*sqrt(3).
    
    simplified_radicand = 3
    radical_coefficient = 1
    
    # The roots are 2 + √3 and 2 - √3.
    # We will present the set of solutions or a specific format? 
    # Usually "ordered quadratic roots" implies listing them in order (ascending).
    root_1 = rational_part_base := int(delta**0.5) if isinstance(int(delta**0.5), float) else None 
    
    # Let's do this cleanly:
    # Roots are (-(-4) ± sqrt(12)) / 2 
    # = (4 ± 2*sqrt(3)) / 2 
    # = 2 ± sqrt(3)
    
    rational_part_val = 2.0
    
    # Construct the answer string components
    canonical_latex_root_1 = r"2 + \sqrt{3}"
    canonical_latex_root_2 = r"2 - \sqrt{3}"
    
    correct_answer_str = f"{rational_part_val} \\pm \\sqrt{{{simplified_radicand}}}"
    
    # Construct the full answer object as a dict for structured comparison if needed, 
    # but the spec says "correct_answer must include result with...". 
    # I will return a string representation that contains these elements clearly.
    
    correct_answer = f"{rational_part_val} \\pm \\sqrt{{{simplified_radicand}}}"
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }