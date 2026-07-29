# -*- coding: utf-8 -*-
import math
from fractions import Fraction

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    frozen_params = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }

    # Parse the equation to find roots of (x - 2)^2 = 3
    # This expands to x^2 - 4x + 1 = 0 or directly solve for x: x = 2 +/- sqrt(3)
    
    center_x = Fraction(2, 1)
    radicand_val = Fraction(3, 1)

    # Roots are a and b where a > b
    # Root formula: x = center + sign * sqrt(radicand)
    # Since we need exact representation with radicals:
    
    root_sign_positive = 1
    root_sign_negative = -1
    
    # Construct the radical term components for canonical LaTeX output
    # The result is of form (center +/- radicand^(1/2))
    # We will format this manually to ensure strict adherence to requirements without external libraries like RadicalOps if not imported.
    
    # However, based on "Compact Domain Scaffold" hint about importing RadicalOps:
    # Since no specific library 'RadicalOps' is standard in Python environment and the prompt implies native arithmetic for math16 tasks unless specified as API-only mixed task which usually refers to a custom context not available here. 
    # I will implement the canonical LaTeX generation natively using fractions and string formatting logic derived from mathematical rules.
    
    def format_radical_term(sign, center_val, radicand):
        """Formats a term like 'center +/- sqrt(radicand)' into canonical LaTeX."""
        if sign == 1:
            latex_sign = "+"
        else:
            latex_sign = "-"
        
        # Center value formatting
        c_str = str(int(center_val)) if center_val.denominator == 1 and abs(center_val) < 10 else f"{center_val}"
        
        return f"{{{c_str}}}{latex_sign}\\sqrt{{{{{radicand}}}}}}"

    root_a_latex = format_radical_term(root_sign_positive, center_x, radicand_val)
    root_b_latex = format_radical_term(root_sign_negative, center_x, radicand_val)
    
    # Ensure a > b. 
    # x1 = 2 + sqrt(3), x2 = 2 - sqrt(3). Clearly x1 > x2.
    latex_a = f"{{{center_x}}}+\\sqrt{{{{{radicand_val}}}}}}"
    latex_b = f"{{{center_x}}}-\\sqrt{{{{{radicand_val}}}}}}"

    # Compute target: 2a + b
    # a = center + sqrt(r)
    # b = center - sqrt(r)
    # 2a + b = 2(center + sqrt(r)) + (center - sqrt(r))
    #        = 2*center + 2*sqrt(r) + center - sqrt(r)
    #        = 3*center + sqrt(r)
    
    target_coefficient = Fraction(3, 1) * center_x
    
    # Construct the final answer string for correct_answer
    # Format: "rational_part" if integer else "fraction", radical part details.
    # Schema requires: rational (if applicable), radical_coefficient (+/-1 usually here but can be other integers?), radicand, canonical_latex.
    
    # Here result is 3*2 + sqrt(3) = 6 + sqrt(3).
    # Rational part: 6
    # Radical coefficient: 1 (implicit in standard form unless specified otherwise, prompt says may be +/-1 but math dictates the coeff here is 1)
    
    rational_part_num = int(target_coefficient.numerator / target_coefficient.denominator) if target_coefficient.denominator == 1 else None
    
    # Actually, let's stick to a robust structure for correct_answer dict:
    # { "rational": ..., "radical_coefficient": ..., "radicand": ..., "canonical_latex": ... }
    
    final_rational = Fraction(target_coefficient)
    radical_coef = 1
    
    canonical_ans_latex = f"{{{final_rational}}}+\\sqrt{{{{{radicand_val}}}}}"

    question_text = (f"Solve the equation {frozen_params['equation']}. "
                     f"If $x_1$ and $x_2$ are roots with $x_1 > x_2$, compute the value of 2$x_1$ + $x_2$. "
                     f"Express your answer in canonical form.")

    correct_answer = {
        "rational": final_rational,
        "radical_coefficient": radical_coef,
        "radicand": radicand_val,
        "canonical_latex": canonical_ans_latex
    }

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }