# -*- coding: utf-8 -*-
import math
from fractions import Fraction

def generate(level=1, **kwargs):
    # Frozen sampled parameters are hardcoded as per specification to avoid reading from kwargs or external state for this specific task instance.
    frozen_params = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }

    # Parse the equation (x - 2)^2 = 3 to find roots of x^2 - 4x + 1 = 0.
    # Roots are given by (-b +/- sqrt(b^2 - 4ac)) / (2a) for ax^2+bx+c=0.
    # Here a_coeff=1, b_coeff=-4, c_coeff=1.
    
    a_coeff = 1
    b_coeff = -4
    c_coeff = 1
    
    discriminant_val = b_coeff**2 - 4*a_coeff*c_coeff
    sqrt_discriminant = math.sqrt(discriminant_val)
    
    root_a_numerator = -b_coeff + sqrt_discriminant
    root_b_numerator = -b_coeff - sqrt_discriminant
    denominator = 2 * a_coeff
    
    # Calculate roots as floats first to determine order, then refine for exact representation if needed.
    # However, the problem asks for radical form. 
    # Roots are (4 +/- sqrt(16-4))/2 = (4 +/- sqrt(12))/2 = (4 +/- 2*sqrt(3))/2 = 2 +/- sqrt(3).
    
    exact_root_a_val = Fraction(-b_coeff, denominator) + Fraction(sqrt_discriminant, denominator) # This is conceptual; let's use the simplified form directly.
    # Simplified: root1 = 2 + sqrt(3), root2 = 2 - sqrt(3).
    # Since sqrt(3) > 0, a = 2 + sqrt(3) and b = 2 - sqrt(3).
    
    integer_part = Fraction(-b_coeff // denominator if (-b_coeff % denominator == 0) else int(Fraction(-b_coeff)/denominator)) 
    # Actually, let's stick to the specific values derived from (x-2)^2=3 -> x = 2 +/- sqrt(3).
    
    integer_part_val = Fraction(2)
    radicand_val = Fraction(3)
    radical_sign = "+" if frozen_params["order"] == "a>b" else "-" # a > b implies we take the larger root as 'a'. 
    # Wait, order is specified in params. We must respect it.
    
    # Constructing the answer components:
    # Root A (larger): 2 + sqrt(3)
    # Root B (smaller): 2 - sqrt(3)
    # Target expression: 2a + b = 2*(2+sqrt(3)) + (2-sqrt(3)) = 4 + 2*sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3).
    
    # Let's generalize slightly to ensure correctness based on the frozen params provided.
    # Equation: (x-2)^2=3 => x^2 - 4x + 1 = 0.
    # Roots: r1, r2. 
    # If order is "a>b", then a = max(r1, r2), b = min(r1, r2).
    
    val_a_num = Fraction(-b_coeff) + sqrt_discriminant_val if False else None
    
    # Re-calculate specifically for (x-2)^2=3 to get exact rational/radical parts.
    shift = 2
    radicand_int = 3
    
    root_plus = shift + math.sqrt(radicand_int)
    root_minus = shift - math.sqrt(radicand_int)
    
    if frozen_params["order"] == "a>b":
        val_a = root_plus
        val_b = root_minus
    else: # order is b>a or unspecified but usually implies a<b in some contexts, here strictly follow param. 
         # The spec says "order": "a>b". We assume standard interpretation unless specified otherwise.
         # If the frozen param was different, we would swap. Here it is fixed to "a>b".
        val_a = root_plus
        val_b = root_minus
        
    # Compute target: 2*a + b
    result_val = 2 * val_a + val_b
    
    # Extract components for canonical_latex and correct_answer dict
    # Result form: Integer part + Radical part.
    # result_val = (4 + 2*sqrt(3)) + (2 - sqrt(3)) = 6 + sqrt(3).
    
    int_part_float = float(result_val)
    rad_coeff_float = math.sqrt(radicand_int) * 1 if True else 0.0
    
    # Exact calculation for components:
    # result_val = 6 + 1*sqrt(3)
    final_integer = Fraction(int(math.floor(float(result_val)))) 
    # Actually, let's do exact fraction arithmetic on the symbolic representation derived from roots.
    
    # Symbolic derivation:
    # a = S + R, b = S - R where S=2, R=sqrt(3).
    # 2a+b = 2(S+R) + (S-R) = 2S + 2R + S - R = 3S + R.
    # Here S=2, so Integer part = 6. Radical coeff = 1. Radicand = 3.
    
    final_integer_val = Fraction(3 * int(shift)) 
    radical_coefficient_sign = "+" if frozen_params["radical_sign"] == "positive" else "-" 
    # Since we derived it as +sqrt(3), sign is positive. If the problem had different equation, logic would adjust.
    # Given fixed params: radicand=3, coeff=1 (implicit in 6+sqrt(3)).
    
    radical_coefficient = Fraction(1) if frozen_params["order"] == "a>b" else Fraction(-1) 
    # Wait, the derivation 2(S+R)+(S-R) always yields +R regardless of order? No.
    # If a<b (i.e., a=S-R, b=S+R): 2(S-R) + (S+R) = 2S - 2R + S + R = 3S - R.
    # So sign depends on which root is 'a'.
    
    if frozen_params["order"] == "a>b":
        radical_coefficient_val = Fraction(1)
    else:
        radical_coefficient_val = Fraction(-1)
        
    final_integer_part = 3 * shift
    
    canonical_latex_str = f"{final_integer_part}{'+' if radical_coefficient_val > 0 else ''}{radical_coefficient_val}*\\sqrt{{{int(radicand_int)}}}"
    
    # Format correct_answer as a dict with rational, radical_coefficient, radicand, and canonical_latex.
    # Note: The prompt asks for "correct_answer" to include these fields. Usually this is the string representation or a structured object? 
    # Spec says: "correct_answer must include result with rational, radical_coefficient..., radicand, and canonical_latex."
    # It implies correct_answer might be a dict itself or contain them. Given JSON serializable requirement, likely a nested dict or specific structure.
    # Let's construct it as the expected output format for such math problems: 
    # {"rational": ..., "radical_coefficient": ..., "radicand": ..., "canonical_latex": ...}
    
    correct_answer_dict = {
        "rational": final_integer_part,
        "radical_coefficient": radical_coefficient_val if frozen_params["order"] == "a>b" else -Fraction(1), # Re-eval sign logic strictly.
        "radicand": radicand_int,
        "canonical_latex": canonical_latex_str.replace(" ", "") 
    }
    
    # Refine correct_answer to be the string representation if that's what is expected for 'correct_answer' field in a dict return?
    # Re-reading: "return a dict with exactly question_text, correct_answer, and oracle_payload."
    # And "correct_answer must include result with rational...". This suggests correct_answer IS the object containing those keys.
    
    if frozen_params["order"] == "a>b":
        sign_str = "+"
    else:
        sign_str = "-"
        
    final_canonical_latex = f"{final_integer_part}{sign_str}\\sqrt{{{radicand_int}}}"
    
    correct_answer_obj = {
        "rational": int(final_integer_part),
        "radical_coefficient": 1 if frozen_params["order"] == "a>b" else -1, 
        # Wait, logic check: If order is a<b (not the case here but for completeness): result was 3S - R. Coeff is -1.
        # Here order is a>b, so coeff is +1.
        "radicand": radicand_int,
        "canonical_latex": final_canonical_latex
    }

    question_text = f"Solve the equation {frozen_params['equation']}. Let $a$ and $b$ be the roots ordered by {frozen_params['order']}. Compute ${frozen_params['target']}."
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_obj,
        "oracle_payload": oracle_payload
    }