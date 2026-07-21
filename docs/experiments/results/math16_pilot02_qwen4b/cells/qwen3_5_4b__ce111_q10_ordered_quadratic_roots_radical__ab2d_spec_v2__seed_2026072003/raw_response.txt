# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    FROZEN_PARAMS = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }

    from core.prompts.domain_function_library import RadicalOps
    
    # Parse the equation (x-2)^2 = 3 to find roots
    # Equation: x^2 - 4x + 4 = 3 => x^2 - 4x + 1 = 0
    # Roots using quadratic formula: (-b +/- sqrt(b^2 - 4ac)) / 2a
    # Here a=1, b=-4, c=1
    # Discriminant D = (-4)^2 - 4*1*1 = 16 - 4 = 12
    
    coeff_a = 1.0
    coeff_b = -4.0
    coeff_c = 1.0
    
    discriminant = (coeff_b ** 2) - (4 * coeff_a * coeff_c)
    
    # Calculate roots
    sqrt_discriminant = RadicalOps.sqrt(discriminant)
    root_numerator_plus = (-coeff_b + sqrt_discriminant) / (2 * coeff_a)
    root_numerator_minus = (-coeff_b - sqrt_discriminant) / (2 * coeff_a)
    
    # Order roots such that a > b as per "order": "a>b"
    if root_numerator_plus >= root_numerator_minus:
        val_a = root_numerator_plus
        val_b = root_numerator_minus
    else:
        val_a = root_numerator_minus
        val_b = root_numerator_plus
    
    # Compute target 2a + b
    result_val = (2 * val_a) + val_b
    
    # Format the answer with rational part and radical coefficient if applicable
    # Since discriminant is 12, sqrt(12) = 2*sqrt(3), so it's not a perfect square integer.
    # We need to represent result_val in terms of radicals or simplified form.
    
    # Let's express the roots exactly:
    # x = (4 +/- sqrt(12)) / 2 = 2 +/- sqrt(3)
    # So val_a = 2 + sqrt(3), val_b = 2 - sqrt(3) (since a > b and sqrt(3)>0)
    
    rational_part = 2.0
    
    # Construct the answer string components
    radical_coefficient = RadicalOps.simplify_term_sqrt(discriminant).coeff if hasattr(RadicalOps, 'simplify_term_sqrt') else None
    
    # Simplify sqrt(12) -> 2*sqrt(3)
    simplified_radicand = 3.0
    simplifier_factor = 2.0
    
    root_a_str = f"{rational_part} + {simplifier_factor}*{RadicalOps.sqrt(simplified_radicand)}" if False else "" # Placeholder logic for clarity in thought process, actual code below handles formatting directly

    # Re-calculate cleanly based on exact math:
    # x1 = 2 + sqrt(3)
    # x2 = 2 - sqrt(3)
    # a = 2 + sqrt(3), b = 2 - sqrt(3) (since 2+sqrt(3) > 2-sqrt(3))
    
    # Target: 2a + b = 2*(2 + sqrt(3)) + (2 - sqrt(3)) 
    #          = 4 + 2*sqrt(3) + 2 - sqrt(3)
    #          = 6 + sqrt(3)
    
    final_rational_part = 6.0
    final_radical_coefficient = 1.0
    final_radicand = 3.0
    
    question_text = r"\text{Solve the quadratic equation } (x-2)^2=3 \text{ for real roots } x_1, x_2 \text{ such that } x_1 > x_2. \text{ Compute } 2x_1 + x_2."
    
    correct_answer = {
        "rational": final_rational_part,
        "radical_coefficient": int(final_radical_coefficient),
        "radicand": int(final_radicand),
        "canonical_latex": r"6 + \sqrt{3}"
    }

    oracle_payload = FROZEN_PARAMS.copy()

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }