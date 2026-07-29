def generate(level=1, **kwargs):
    expression = kwargs.get("expression", "3/7 - (-1/4)")
    
    # Parse components from expression string: 3/7 - (-1/4) -> (num1, den1), sign2, (num2, den2)
    import re
    
    match = re.match(r"(-?\d+)/(\d+)\s*([+-])\s*(-?\d+)/(\d+)", expression)
    
    if not match:
        raise ValueError("Invalid expression format")
        
    num1, den1, op_sign_str, num2, den2 = map(int, [match.group(1), match.group(2), match.group(3), match.group(4), match.group(5)])
    
    # Determine the operator based on sign before second fraction and minus in expression logic
    # Expression is A - B. If B has a negative numerator like (-1/4), it becomes + 1/4 effectively if we treat subtraction of negative as addition.
    # However, standard parsing: "3/7 - (-1/4)" means num2=-1, den2=4, op_sign_str='-' (the minus between fractions).
    
    # Logic for result numerator and denominator based on A +/- B where sign depends on the operator in string or explicit negative handling.
    # Here: 3/7 - (-1/4) -> 3/7 + 1/4
    
    if op_sign_str == '-':
        is_subtraction = True
    else:
        is_subtraction = False
        
    # Special case for subtraction of a negative fraction (effectively addition) or handling the sign in num2 directly?
    # The prompt says "3/7 - (-1/4)". 
    # If we parse strictly as A op B where op is '-', and B has numerator -1:
    # Result = 3/7 + 1/4.
    
    if is_subtraction:
        effective_num2 = num2 * -1
        sign_to_add = True # Effectively adding because subtracting a negative
    else:
        effective_num2 = num2
        sign_to_add = False
        
    # Actually, simpler approach for "A - B": result numerator = A*numB_den + (if sub then -numB*denA) ... wait.
    # Standard subtraction of fractions: n1/d1 - n2/d2 = (n1*d2 - n2*d1) / (d1*d2)
    # If the expression is "3/7 - (-1/4)", mathematically it is 3/7 + 1/4.
    # Let's stick to standard arithmetic rules on parsed integers: 
    # Term 1: 3/7, Term 2: -1/4 (parsed from string). Operator between them in text is '-'.
    # So calculation is: (3 * 4) - (-1 * 7) = 12 + 7 = 19. Denom = 28.
    
    numerator = num1 * den2 - num2 * den1
    denominator = den1 * den2
    
    if sign_to_add and is_subtraction: # This logic was getting confused, let's re-evaluate based on standard math parsing of the string "3/7 - (-1/4)"
        pass
        
    # Re-calculation strictly following algebraic expansion of the parsed integers from regex match groups 1-5.
    # Group 1: num1 (e.g., 3)
    # Group 2: den1 (e.g., 7)
    # Group 3: op_char between fractions ('-' or '+')
    # Group 4: num2 (e.g., -1)
    # Group 5: den2 (e.g., 4)
    
    if op_sign_str == '-':
        numerator = num1 * den2 - num2 * den1
    else:
        numerator = num1 * den2 + num2 * den1
        
    denominator = den1 * den2
    
    # Simplify fraction
    import math
    gcd_val = abs(math.gcd(numerator, denominator))
    
    if gcd_val != 0 and gcd_val > 1:
        simplified_num = numerator // gcd_val
        simplified_den = denominator // gcd_val
        
        # Ensure canonical form (denominator positive)
        if simplified_den < 0:
            simplified_num *= -1
            simplified_den *= -1
            
    else:
        simplified_num = numerator
        simplified_den = denominator

    correct_answer_str = f"{simplified_num}/{simplified_den}"
    
    # Construct LaTeX for the answer part (irreducible fraction)
    canonical_latex = r"\frac{" + str(simplified_num) + r"}{" + str(simplified_den) + "}"
    
    return {
        "question_text": f"Compute: $\\{expression}\\}$",
        "correct_answer": correct_answer_str,
        "canonical_latex": canonical_latex,
        "oracle_payload": {"expression": expression}
    }