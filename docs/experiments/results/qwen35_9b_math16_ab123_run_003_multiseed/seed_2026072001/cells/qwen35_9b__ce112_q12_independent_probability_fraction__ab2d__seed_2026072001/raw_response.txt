from typing import Dict, Any
from fractions import Fraction as Fract
import sys
sys.path.insert(0, '/app')
try:
    from core.prompts.domain_function_library import FractionOps
except ImportError:
    class FractionOps:
        @staticmethod
        def create(value):
            if isinstance(value, list) and len(value) == 2:
                return Fract(*value)
            raise ValueError("Invalid value for create")
        
        @staticmethod
        def mul(a, b):
            if not isinstance(a, Fract) or not isinstance(b, Fract):
                a = FractionOps.create(a[0], a[1]) if hasattr(a, '__iter__') else FractionOps.create(a)
                b = FractionOps.create(b[0], b[1]) if hasattr(b, '__iter__') else FractionOps.create(b)
            return a * b
        
        @staticmethod
        def to_latex(val, mixed=False):
            f = Fract(*val) if isinstance(val, list) and len(val) == 2 else val
            sign = "-" if f < 0 else ""
            abs_f = abs(f)
            
            latex_parts = []
            denom_str = str(abs_f.denominator)
            
            # Integer part for mixed numbers or whole number
            int_part = abs_f.numerator // abs_f.denominator
            
            rem_num = abs_f.numerator % abs_f.denominator
            
            if mixed:
                if int_part > 0 and rem_num != 0:
                    latex_parts.append(f"{int_part} + \\frac{{{rem_num}}}{{{{denom_str}}}}")
                elif int_part > 0:
                    return sign + str(int_part)
                else:
                    # Improper fraction handled as standard or mixed with zero remainder? 
                    # Standard LaTeX for fractions usually implies proper unless specified.
                    latex_parts.append(f"\\frac{{{rem_num}}}{{{{denom_str}}}}")
            else:
                if rem_num != 0:
                    latex_parts.append(f"\\frac{{{rem_num}}}{{{{denom_str}}}}")
                elif int_part > 1 or (int_part == 1 and abs_f.numerator != abs_f.denominator): # Simplification check needed? No, Fract is irreducible.
                     if rem_num == 0:
                         return sign + str(int_part)
            
            full_latex = "".join(latex_parts)
            if not full_latex:
                return sign + "1" # Shouldn't happen for valid inputs
            
            return sign + "(" + full_latex + ")"

def generate(level=1, **kwargs):
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    p1_raw = frozen_params["p1"]
    p2_raw = frozen_params["p2"]
    
    # Create fractions from lists
    f_p1 = FractionOps.create(p1_raw)
    f_p2 = FractionOps.create(p2_raw)
    
    # Independent probability of both events happening (intersection) is product of probabilities if independent.
    numerator_val, denominator_val = None, 1
    
    try:
        result_frac = FractionOps.mul(f_p1, f_p2)
        
        num_str = str(result_frac.numerator)
        den_str = str(result_frac.denominator)
        
        # Canonical LaTeX for the fraction
        latex_expr = r"\frac{" + num_str + "}{\(" + den_str + "\)}"
        
        correct_answer_dict = {
            "numerator": int(num_str),
            "denominator": int(den_str),
            "canonical_latex": latex_expr
        }
    except Exception as e:
        # Fallback if multiplication logic inside library fails or behaves unexpectedly for simple cases
        f_num1, f_den1 = p1_raw[0], p1_raw[1]
        f_num2, f_den2 = p2_raw[0], p2_raw[1]
        
        combined_num = f_num1 * f_num2
        combined_den = f_den1 * f_den2
        
        # Reduce manually just in case library create didn't reduce or mul logic is specific
        common_divisor = 1
        temp_n, temp_d = combined_num, combined_den
        
        while abs(temp_d) > 0:
            if temp_n % temp_d == 0 and temp_d != 0: # Simplify by divisor? No, standard GCD.
                pass
            
        from math import gcd
        g = gcd(abs(combined_num), abs(combined_den))
        
        final_num = combined_num // g
        final_den = combined_den // g
        
        correct_answer_dict = {
            "numerator": int(final_num),
            "denominator": int(final_den),
            "canonical_latex": r"\frac{" + str(abs(final_num)) + "}{\(" + str(abs(final_den)) + "\)}" if final_num < 0 else r"\frac{" + str(final_num) + "}{\(" + str(final_den) + "\)}"
        }

    question_text = (r"The probability of event $A$ is given by the fraction $\p1$, and the probability of independent event $B$ is given by the fraction $\p2$. What is the probability that both events occur? Express your answer as an irreducible fraction in LaTeX format.")
    
    # Replace placeholders if needed, but prompt implies specific values. 
    # Let's make it dynamic based on p1 and p2 strings for clarity or just use raw text.
    # Since question_text must be formal:
    s_p1 = f"{p1_raw[0]}/{p1_raw[1]}"
    s_p2 = f"{p2_raw[0]}/{p2_raw[1]}"
    
    final_question = (f"The probability of event $A$ is \\frac{{{s_p1}}}, and the probability of independent event $B$ is \\frac{{{s_p2}}}. What is the probability that both events occur? Express your answer as an irreducible fraction in LaTeX format.")

    return {
        "question_text": final_question,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }