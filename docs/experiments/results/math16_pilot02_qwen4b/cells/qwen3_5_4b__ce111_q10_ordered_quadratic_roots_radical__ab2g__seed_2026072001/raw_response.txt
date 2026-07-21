def generate(level=1, **kwargs):
    import re
    
    # Frozen sampled parameters as per task specification
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
    question_text = r"\text{Solve for } x \text{ in the quadratic equation: " + r"$(x-2)^2=3$".replace("$", "\\$")
    
    # Calculate roots manually to ensure precision and structure
    # Equation: x^2 - 4x + 1 = 0
    a_val, b_val, c_val = 1, -4, 1
    
    discriminant = b_val**2 - 4*a_val*c_val
    sqrt_discriminant = int(discriminant ** 0.5) # Should be exact for this case (sqrt(16-4)=sqrt(12))
    
    if sqrt_discriminant * sqrt_discriminant == discriminant:
        root_part_a = (-b_val + sqrt_discriminant) / (2*a_val)
        root_part_b = (-b_val - sqrt_discriminant) / (2*a_val)
        
        # Format the answer based on order "a>b" which implies listing larger first or specific format? 
        # Usually roots are listed as x1, x2. Let's assume standard form with rational part and radical coefficient.
        # Root 1: (-(-4) + sqrt(12)) / 2 = (4 + 2*sqrt(3))/2 = 2 + sqrt(3)
        # Root 2: (-(-4) - sqrt(12)) / 2 = (4 - 2*sqrt(3))/2 = 2 - sqrt(3)
        
        rational_part_1, radical_coefficient_1, radicand_1 = 2, 1, 3
        canonical_latex_1 = r"2 + \sqrt{3}"
        
        # The task asks for "correct_answer". Since there are two roots and order is specified as a>b (likely referring to coefficients or just listing), 
        # we will provide the set of solutions. However, looking at typical patterns for such tasks:
        # If it expects a single string representation covering both, often they list them separated by comma.
        # Let's construct the answer object containing details for verification.
        
        correct_answer = {
            "roots": [2 + sqrt_discriminant/(2*a_val), 2 - sqrt_discriminant/(2*a_val)], 
            "rational_part": rational_part_1, 
            "radical_coefficient": radical_coefficient_1, 
            "radicand": radicand_1,
            "canonical_latex": canonical_latex_1 + r", \quad 2 - \\sqrt{3}" # Combining both roots in LaTeX for completeness if needed, or just the first one?
        }
        
        # Re-evaluating based on typical 'ordered_quadratic_roots_radical' tasks: 
        # It usually expects a list of solutions formatted nicely.
        # Let's format the full answer string containing both roots properly.
        latex_str = r"2 + \\sqrt{3}, \quad 2 - \\sqrt{3}"
        
    else:
        correct_answer = "No real rational solution found."

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }