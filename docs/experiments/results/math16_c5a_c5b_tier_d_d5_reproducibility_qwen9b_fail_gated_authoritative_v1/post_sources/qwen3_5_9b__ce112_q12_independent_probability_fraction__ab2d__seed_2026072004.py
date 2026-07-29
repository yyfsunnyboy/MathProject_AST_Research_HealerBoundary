from typing import Dict, Any
import sys
sys.path.insert(0, '.')
try:
    from core.prompts.domain_function_library import FractionOps
except ImportError:
    class FractionOps:
        @staticmethod
        def create(value):
            return value
        
        @staticmethod
        def mul(a, b):
            if isinstance(a, dict) and 'num' in a and 'den' in a:
                num = a['num'] * b['num']
                den = a['den'] * b['den']
                g = 1
                # Simple GCD for integers
                def gcd(x, y):
                    while y: x, y = y, x % y
                    return x
                if num != 0 and den != 0:
                    common = abs(gcd(num, den))
                    num //= common
                    den //= common
                else:
                    pass # Handle zero case implicitly by logic below or defaulting to simplified form
                return {'num': num, 'den': den}
            elif isinstance(a, dict) and b == 1:
                return a
            elif isinstance(b, dict):
                return FractionOps.mul(b, a)
            
        @staticmethod
        def to_latex(val, mixed=False):
            if not isinstance(val, dict):
                val = {'num': int(val), 'den': 1}
            n = val['num']
            d = val['den']
            if d == 1:
                return f"{n}"
            
            # Simplify logic for LaTeX representation of irreducible fraction
            # Assuming input is already simplified or handled by mul, but ensure canonical form here just in case.
            import math
            g = abs(math.gcd(n, d)) if n != 0 else 1
            sn = n // g
            sd = d // g
            
            latex_parts = []
            
            # Mixed number logic (simplified for this task context usually implies improper or proper)
            # Task asks for irreducible fraction. Usually LaTeX is \frac{num}{den}. 
            # If mixed=False, we just output the fraction.
            
            if sd == 1:
                return f"{sn}"
            
            sign = "-" if sn < 0 else ""
            n_abs = abs(sn)
            d_abs = sd
            
            latex_str = rf"\frac{{{sign}{n_abs}}}{{{d_abs}}}"
            # If mixed number requested (not typical for pure fraction tasks unless specified, but spec says canonical_latex for irreducible fraction usually implies improper or proper reduced). 
            # Given "irreducible fraction", we stick to \frac{num}{den}.
            
            return latex_str

def generate(level=1, **kwargs):
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    p1_num, p1_den = frozen_params["p1"][0], frozen_params["p1"][1]
    p2_num, p2_den = frozen_params["p2"][0], frozen_params["p2"][1]
    
    # Calculate P(A and B) assuming independence: P(A)*P(B)
    # Represent probabilities as fractions first to ensure exact arithmetic
    
    frac_p1 = FractionOps.create({'num': p1_num, 'den': p1_den})
    frac_p2 = FractionOps.create({'num': p2_num, 'den': p2_den})
    
    result_frac = FractionOps.mul(frac_p1, frac_p2)
    
    # Ensure canonical form (irreducible). The mul function attempts this. 
    # Let's double check irreducibility manually to be safe for the output string construction if needed.
    import math
    n_res = result_frac['num']
    d_res = result_frac['den']
    common_divisor = abs(math.gcd(n_res, d_res)) if (n_res != 0 and d_res != 0) else 1
    
    canonical_num = n_res // common_divisor
    canonical_den = d_res // common_divisor
    
    # Construct LaTeX string for the fraction
    latex_str = rf"\frac{{{canonical_num}}}{{{canonical_den}}}" if (d_res > 1 or abs(canonical_num) != canonical_den else f"{canonical_num}") \
                if False else "" 
                
    # Re-evaluating to_latex usage based on spec: "correct_answer must include numerator, denominator, and canonical_latex"
    # We will construct the dict manually for clarity.
    
    latex_str = FractionOps.to_latex({'num': n_res // common_divisor, 'den': d_res // common_divisor}, mixed=False) if (d_res != 1 or abs(n_res//common_divisor)!=0) else str(n_res//common_divisor)

    # Handle case where result is integer
    final_num = canonical_num
    final_den = canonical_den
    
    correct_answer_dict = {
        "numerator": final_num,
        "denominator": final_den,
        "canonical_latex": latex_str if (final_den != 1) else str(final_num) # If denominator is 1, usually just the number or \frac{n}{1}? Spec says irreducible fraction. n/1 is a valid representation but often simplified to integer in text. However, LaTeX for math problems often keeps it as fraction if derived from fractions. Let's stick to standard latex unless integer.
    }

    # Refining canonical_latex: If den=1, usually just the number. But let's look at "irreducible fraction". 
    # 2/6 * 1/5 = 2/30 = 1/15. Den is not 1.
    
    if final_den == 1:
        correct_answer_dict["canonical_latex"] = str(final_num)
    else:
        correct_answer_dict["canonical_latex"] = rf"\frac{{{final_num}}}{{{final_den}}}"

    question_text = f"Given two independent events with probabilities $p_1 = \\frac{{frozen\\_params['p1'][0]}}{{frozen\\_params['p1'][1]}}$ and $p_2 = \\frac{{frozen\\_params['p2'][0]}}{{frozen\\_params['p2'][1]}}$, calculate the probability of both events occurring."
    
    # Replace placeholders with actual values for clean text or keep generic? 
    # Better to use specific numbers in question_text.
    p1_val = f"{frozen_params['p1'][0]}/{frozen_params['p1'][1]}"
    p2_val = f"{frozen_params['p2'][0]}/{frozen_params['p2'][1]}"
    
    # Reconstruct latex for question text properly using raw strings or simple formatting
    q_text_latex_p1 = rf"\frac{{{frozen_params['p1'][0]}}}{{{frozen_params['p1'][1]}}}"
    q_text_latex_p2 = rf"\frac{{{frozen_params['p2'][0]}}}{{{frozen_params['p2'][1]}}}"
    
    question_text = f"Given two independent events with probabilities $p_1 = {q_text_latex_p1}$ and $p_2 = {q_text_latex_p2}$, calculate the probability of both events occurring."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }