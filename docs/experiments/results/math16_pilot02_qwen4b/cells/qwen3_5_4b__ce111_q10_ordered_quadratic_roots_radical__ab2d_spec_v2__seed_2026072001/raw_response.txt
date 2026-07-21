# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters for this task instance
    FROZEN_PARAMS = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }

    import math
    
    # Parse the equation (x-a)^2 = b to find roots x = a ± sqrt(b)
    # From frozen params: (x-2)^2=3 => a_coefficient = 2, constant_term = 3
    shift_val = 2.0
    radicand_base = 3.0
    
    # Calculate the two potential roots before ordering
    root_plus = shift_val + math.sqrt(radicand_base)
    root_minus = shift_val - math.sqrt(radicand_base)
    
    # Determine order based on 'order' parameter (a > b means larger first)
    if FROZEN_PARAMS["order"] == "a>b":
        a = max(root_plus, root_minus)
        b = min(root_plus, root_minus)
    else:  # Assume default or other orders handled similarly but spec says a>b
        a = root_plus
        b = root_minus
    
    # Compute target expression: 2*a + b
    result_value = (2 * a) + b
    
    # Extract components for the answer structure
    rational_part = int(round(result_value)) if abs(result_value - round(result_value)) < 1e-9 else None
    radical_coefficient = 0.0
    radicand_final = float(radicand_base)
    
    # If result is purely irrational, format as coefficient * sqrt(radicand)
    # Since a and b are of form k ± sqrt(m), 
    # 2*(k + sqrt(m)) + (k - sqrt(m)) = 3*k + sqrt(m) OR similar linear combination.
    # Let's verify the algebra:
    # Case 1: a = shift + sqrt(b), b = shift - sqrt(b) -> order doesn't matter for sum/diff structure but matters for assignment
    # If we pick larger as 'a': 
    #   a = 2 + sqrt(3), b = 2 - sqrt(3)
    #   Target: 2*(2+sqrt(3)) + (2-sqrt(3)) = 4 + 2*sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3)
    
    final_rational = rational_part if rational_part is not None else result_value
    
    # Construct the canonical LaTeX for the radical part if it exists and isn't integer
    latex_radical = f"\\sqrt{{{radicand_final}}}"
    
    correct_answer_str = ""
    if isinstance(final_rational, int) or (isinstance(final_rational, float) and final_rational.is_integer()):
        # Handle pure rational case explicitly if applicable, though here we have a radical term
        pass
    
    # Format the answer: Rational + Coefficient * Radical
    # In this specific math problem context derived from roots of quadratics with radicals:
    # Result is 6 + sqrt(3)
    
    latex_full = f"{final_rational}+{radical_coefficient}\\sqrt{{{radicand_final}}}" if radical_coefficient != 0 else str(final_rational).replace('.', '')
    
    question_text = r"\text{Solve the quadratic equation } (x-2)^2=3 \text{ for real roots. Let the ordered roots be } a > b. \text{ Compute the value of } 2a+b."

    return {
        "question_text": question_text,
        "correct_answer": latex_full,
        "oracle_payload": FROZEN_PARAMS.copy()
    }