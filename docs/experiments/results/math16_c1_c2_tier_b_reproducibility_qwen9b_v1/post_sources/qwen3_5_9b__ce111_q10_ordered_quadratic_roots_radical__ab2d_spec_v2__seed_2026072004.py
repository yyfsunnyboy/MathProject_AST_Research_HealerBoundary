# -*- coding: utf-8 -*-
from math import sqrt, isclose

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    frozen_params = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }

    # Parse the specific equation provided in frozen_params
    # Equation: (x - 2)^2 = 3
    # Expand: x^2 - 4x + 4 = 3 => x^2 - 4x + 1 = 0
    
    a_coeff = 1.0
    b_coeff = -4.0
    c_const = 1.0

    discriminant = b_coeff**2 - 4*a_coeff*c_const
    sqrt_discriminant = sqrt(discriminant)

    # Roots: (-b +/- sqrt(D)) / (2a)
    root_a_raw = (-b_coeff + sqrt_discriminant) / (2 * a_coeff)
    root_b_raw = (-b_coeff - sqrt_discriminant) / (2 * a_coeff)

    # Order roots such that a > b
    if root_a_raw < root_b_raw:
        val_a, val_b = root_b_raw, root_a_raw
    else:
        val_a, val_b = root_a_raw, root_b_raw
        
    # Compute target: 2a + b (where 'b' in formula is the second variable name from task spec)
    # Task says "target": "2a+b", implying result = 2*val_a + val_b
    final_value = 2 * val_a + val_b

    # Construct canonical LaTeX for the radical part of the answer if it exists.
    # Since discriminant is not a perfect square (16 - 4 = 12), we have radicals.
    # sqrt(12) simplifies to 2*sqrt(3). However, standard form often keeps radicand simplified.
    # Let's simplify the radical term manually for canonical representation.
    
    disc_val = discriminant
    if disc_val > 0:
        sq_part = int(sqrt(disc_val))
        rem_part = disc_val % (sq_part**2)
        
        if rem_part == 0 and sqrt_discriminant != 1: # Simplify integer roots? No, usually keep as is unless perfect square.
            pass
            
    # Actually, for canonical_latex of the radical term in the answer context:
    # The problem asks for "radical_coefficient", "radicand". This implies a form like k * sqrt(n).
    # We need to express final_value or its components? 
    # Usually, these tasks expect the simplified radical form of the roots if they are irrational.
    # But here we compute 2a+b which might be rational or have radicals.
    
    # Let's re-evaluate: a = (4 + sqrt(12))/2 = 2 + sqrt(3)
    # b = (4 - sqrt(12))/2 = 2 - sqrt(3)
    # Order a > b -> a is the one with +sqrt, b is the one with -.
    # Target: 2a + b = 2*(2+sqrt(3)) + (2-sqrt(3)) = 4 + 2*sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3).
    
    # So final_value is rational part + radical part.
    # Rational part: 6
    # Radical coefficient: 1
    # Radicand: 3
    
    if disc_val > 0 and not (disc_val == int(disc_val)**2): 
        # It has a non-perfect square root component in the original roots, but they might cancel or combine.
        # In this specific case (6 + sqrt(3)), we have one radical term.
        
        # Extract simplified radical from final_value if it's not purely rational
        # We know mathematically: 2a+b = 6 + sqrt(3)
        # Let's verify programmatically to be safe against floating point issues or different inputs, 
        # though here input is fixed.
        
        # Check if result has a radical component by checking distance from integer/rational?
        # Better approach: Since we know the structure for this specific frozen param set:
        # We can hardcode the extraction logic based on the known math of (x-2)^2=3
        
        rational_part = 6.0
        radical_coefficient = 1.0
        radicand = 3
        
        canonical_latex = r"\\sqrt{3}"
    else:
        # Fallback for purely rational results if any other case existed (not here)
        radical_coefficient = None
        radicand = None
        canonical_latex = str(final_value).replace(".", "")

    question_text = f"Solve the equation {frozen_params['equation']} with roots ordered such that $a > b$. Calculate the value of ${frozen_params['target']}$."
    
    correct_answer_obj = {
        "rational": rational_part, # Or None if purely radical? The spec says "include result with rational...". 
                                   # If 6+sqrt(3), rational part is 6.
        "radical_coefficient": radical_coefficient,
        "radicand": radicand,
        "canonical_latex": canonical_latex
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_obj,
        "oracle_payload": frozen_params
    }