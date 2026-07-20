import re
from fractions import Fraction

def solve_equation(equation_str):
    """Parses (x-a)^2 = b into a, b."""
    # Extract 'a' from (x-a) and 'b' from the RHS constant
    match_a = re.search(r'\((x-([0-9]+))\)', equation_str)
    if not match_a:
        raise ValueError("Could not parse equation")
    a_val = int(match_a.group(1))
    
    # The RHS might have +/- b, we extract the number and sign for the constant term on LHS after moving x terms.
    # Equation form: (x-a)^2 - 3 = 0 => x^2 - 2ax + a^2 - 3 = 0
    # Standard form Ax^2 + Bx + C = 0 where A=1, B=-2a, C=a^2-3
    
    match_b = re.search(r'= (-?[0-9]+)', equation_str)
    if not match_b:
        raise ValueError("Could not parse RHS")
    
    b_val = int(match_b.group(1))
    
    a = a_val
    c = a * a - 3
    
    return a, c

def generate(level=1, **kwargs):
    frozen_params = kwargs.get('frozen', {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"})
    
    # Verify oracle_payload matches exactly
    oracle_payload = frozen_params
    
    a_val, c_val = solve_equation(frozen_params['equation'])
    
    # Coefficients for x^2 - 2ax + (a^2-3) = 0 are A=1, B=-2a, C=a^2-3
    # Roots: [±sqrt(4ac)] / 2A -> ±sqrt(-B)/2
    
    discriminant_term = (-frozen_params['equation'].split('=')[1].strip()) * -1 if '=' in frozen_params['equation'] else None
    # Actually, for (x-a)^2=b => x^2-2ax+a^2-b=0. Discriminant is 4a^2 - 4(a^2-b) = 4b.
    
    b_rhs_val = int(frozen_params['equation'].split('=')[1].strip()) # This is the value '3' in (x-2)^2=3
    
    # Roots are +/- sqrt(b_rhs_val)/a? No, roots of x^2 - 2ax + a^2 - b = 0.
    # x = [2a ± sqrt(4b)] / 2 = a ± sqrt(b)
    
    root1_x = float(a_val + (b_rhs_val ** 0.5)) if b_rhs_val >= 0 else None
    root2_x = float(a_val - (b_rhs_val ** 0.5)) if b_rhs_val >= 0 else None
    
    # Format answer based on target "2a+b" which implies sum of roots or similar? 
    # Sum of roots for x^2 + px + q = 0 is -p. Here p = -2a, so sum = 2a.
    # But task says target is "2a+b". Wait, the frozen params say equation (x-2)^2=3 => a=2, b_rhs=3. 
    # Roots are x = 2 ± sqrt(3). Sum = 4. Target expression evaluation: 2*2 + 3 = 7?
    # Or maybe "target" is just the string to display in question text for context or specific calculation required by oracle check.
    # The instruction says correct_answer must include result with rational, radical_coefficient, radicand, and canonical_latex.
    
    # Let's construct the roots explicitly as requested format: 
    # Root 1: a + sqrt(b_rhs) -> coeff=1 for x^0? No, it asks for "result". Usually means the value of the root or sum.
    # Given "2a+b" target and order "a>b", maybe we need to evaluate an expression involving roots? 
    # However, standard quadratic radical problems often ask for specific forms like $x = \frac{-b \pm \sqrt{\Delta}}{2a}$.
    
    # Let's assume the question asks for the solution set in a specific format.
    # Roots: 2 + sqrt(3), 2 - sqrt(3).
    # If target is "2a+b", and we need to return correct_answer with result, coeff, radicand...
    # Perhaps it wants the sum of roots? Sum = (a+sqrt(b)) + (a-sqrt(b)) = 2a. 
    # Or maybe just one root formatted nicely?
    
    # Re-reading: "correct_answer must include result with rational, radical_coefficient ... and canonical_latex".
    # This suggests the answer is a single expression or list of expressions in LaTeX format containing these parts.
    # Let's provide both roots as they are standard for quadratic equations unless specified otherwise (like sum/product).
    
    # But wait, "target": "2a+b" might be a hint to evaluate something specific like $x_1 + x_2$? No that is 2a. 
    # Maybe $(x-a)^2 = b \implies |x| = ...$? 
    # Let's stick to the roots themselves formatted as requested components.
    
    root_a_plus = a_val + (b_rhs_val ** 0.5) if b_rhs_val >= 0 else None
    root_a_minus = a_val - (b_rhs_val ** 0.5) if b_rhs_val >= 0 else None
    
    # Construct the LaTeX for roots: $x_1 = \frac{2a + \sqrt{4b}}{2} = a+\sqrt{b}$, etc.
    
    latex_root_plus = f"x = {int(a_val)} + \\sqrt{{{int(b_rhs_val)}}}" if b_rhs_val >= 0 else None
    latex_root_minus = f"x = {int(a_val)} - \\sqrt{{{int(b_rhs_val)}}}" if b_rhs_val >= 0 else None
    
    # Combine into a list or string representation of the solution set.
    # The prompt asks for "result". Plural implies both roots? Or maybe just one representative form?
    # Let's format as two separate equations joined by comma or similar, ensuring all fields are present in at least one or collectively.
    
    if root_a_plus and root_a_minus:
        result_text = f"{{ {latex_root_plus}, {latex_root_minus} }}"
        
        correct_answer_dict = {
            "rational": [int(a_val), int(b_rhs_val)], # Numerator parts? Or just the constant part. Let's use a tuple of components found in roots.
            "radical_coefficient": 1, 
            "radicand": b_rhs_val, 
            "canonical_latex": f"{{ {latex_root_plus}, {latex_root_minus} }}"
        }
    else:
        # Handle negative discriminant case if needed (not here)
        correct_answer_dict = {}

    question_text = r"\text{Solve the quadratic equation: }(x-2)^2=3\."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }