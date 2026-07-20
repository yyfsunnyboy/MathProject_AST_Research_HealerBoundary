from functools import partial
import sys

# Mocking required imports from `core.prompts.domain_function_library` as they are not available in standard env
class FractionOps:
    @staticmethod
    def create(value):
        # Simulate creating a fraction object, but for this logic we just return the value or tuple if list
        if isinstance(value, (int, float)):
            from fractions import Fraction
            return Fraction(value)
        elif isinstance(value, list) and len(value) == 2:
            num, den = int(float(value[0])), int(float(value[1]))
            # Handle negative denominator normalization manually to match standard fraction logic if needed
            if den < 0:
                num *= -1
                den *= -1
            return (num, den) 
        else:
            raise ValueError("Unsupported value for create")

    @staticmethod
    def mul(a, b):
        # a and b are expected to be tuples or Fraction-like objects from our mock context
        if isinstance(a, tuple) and isinstance(b, tuple):
            num_a, den_a = a
            num_b, den_b = b
            new_num = num_a * num_b
            new_den = den_a * den_b
            # Simplify (irreducible fraction logic)
            import math
            gcd_val = math.gcd(abs(new_num), abs(new_den))
            if gcd_val > 1:
                new_num //= gcd_val
                new_den //= gcd_val
            return (new_num, new_den)
        elif isinstance(a, tuple):
            num_a, den_a = a
            # Assuming b is already simplified or handled similarly
            from fractions import Fraction as Frac
            frac_b = Frac(b[0], b[1]) if isinstance(b, list) else Frac(float(b))
            res = (num_a * frac_b.numerator, den_a * frac_b.denominator)
            gcd_val = math.gcd(abs(res[0]), abs(res[1]))
            return tuple(x // gcd_val for x in res)
        elif isinstance(a, list): # b is float/int from kwargs maybe? No, spec says mul takes a,b. Assuming both tuples/lists here or mixed logic not needed based on frozen params being lists initially converted to Fractions internally if needed. 
             pass
        
    @staticmethod
    def to_latex(val, mixed=False):
        num, den = val[0], val[1] # assuming val is tuple from create/mul chain
        import math
        gcd_val = math.gcd(abs(num), abs(den))
        
        latex_num = str(num) if not (num == 0 and den != 0) else "0"
        latex_den = str(den)
        
        # Handle signs in LaTeX properly: \frac{...}{...} 
        sign_str = "-" if num < 0 or den < 0 else ""
        abs_num, abs_den = abs(num), abs(den)
        
        return f"\\dfrac{{{sign_str}{abs_num}}}{{{{abs({den})}}}}"

# Re-implementing the logic cleanly to satisfy requirements without external mocks failing at runtime in a strict way.
from fractions import Fraction as Frac
import math

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    p1_val = Frac(frozen_params["p1"][0], frozen_params["p1"][1])
    p2_val = Frac(frozen_params["p2"][0], frozen_params["p2"][1])
    
    # Independent probability: P(A and B) = P(A) * P(B)
    result_frac = p1_val * p2_val
    
    # Ensure irreducible (Fracton does this automatically upon creation/multiplication usually, but let's be safe)
    num = result_frac.numerator
    den = result_frac.denominator
    
    # Construct canonical LaTeX for the fraction: \frac{numerator}{denominator}
    latex_str = f"\\dfrac{{{num}}}{{{{den}}}}"
    
    correct_answer_dict = {
        "numerator": num,
        "denominator": den,
        "canonical_latex": latex_str
    }
    
    question_text = (
        r"What is the probability of two independent events occurring together? "
        r"If event A has a probability of \(\frac{" + str(frozen_params["p1"][0]) + r"}{(" + str(frozen_params["p1"][1]) + r"})\) and "
        r"event B has a probability of \(\frac{" + str(frozen_params["p2"][0]) + r"}{(" + str(frozen_params["p2"][1]) + r"})\), "
        r"calculate the combined probability."
    )

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }