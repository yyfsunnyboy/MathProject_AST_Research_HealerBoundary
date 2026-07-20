from typing import Dict, Any
import math
from fractions import Fraction as _Fraction
# Mocking the required domain library structure since actual imports are not available in this context
class CorePromptsDomainFunctionLibrary:
    class FractionOps:
        @staticmethod
        def create(value):
            return value
        
        @staticmethod
        def add(a, b):
            if isinstance(a, _Fraction) and isinstance(b, _Fraction):
                return a + b
            
        @staticmethod
        def to_latex(val, mixed=False):
            f = val
            numerator = str(f.numerator)
            denominator = str(f.denominator)
            
            # Construct LaTeX for irreducible fraction: \frac{numerator}{denominator}
            latex_str = r'\frac{' + numerator + r'}{' + denominator + r'}'
            return latex_str

# Inject the mocked library into global scope if needed, or use directly here.
FractionOps = CorePromptsDomainFunctionLibrary.FractionOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters from task specification
    frozen_params: Dict[str, Any] = {
        "expression": "9/22 + 11/18 - (23/22 - 7/18)"
    }

    # Parse and evaluate the expression using domain APIs where applicable or standard arithmetic logic
    # The task requires rational arithmetic. We will compute the exact fraction manually to ensure correctness 
    # before formatting with domain tools if necessary, but since FractionOps.create/add are provided:
    
    term1 = _Fraction(9, 22)
    term2 = _Fraction(11, 18)
    inner_subtrahend_1 = _Fraction(23, 22)
    inner_subtrahend_2 = _Fraction(7, 18)
    
    # Calculate (23/22 - 7/18) first as per parentheses in expression string logic? 
    # Actually the input is "9/22 + 11/18 - (23/22 - 7/18)"
    inner_paren = _Fraction(0, 1) # Placeholder for calculation
    
    term_a = FractionOps.create(_Fraction(23, 22))
    term_b = FractionOps.create(_Fraction(7, 18))
    
    try:
        diff_inner = FractionOps.add(term_a, -term_b) if hasattr(FractionOps, 'add') else (term_a + (-term_b))
    except TypeError:
        # Fallback for the specific add signature if strictly enforced or mocked behavior differs
        diff_inner = term_a + (_Fraction(-1, 1) * term_b)

    final_result = FractionOps.add(term1, _Fraction(0, 1))
    try:
         partial_sum = FractionOps.add(final_result, term2)
    except TypeError:
        partial_sum = term1 + term2
        
    # Subtract the inner result from the sum of first two terms
    final_fraction = partial_sum - diff_inner
    
    # Ensure irreducible (Fraction class guarantees this automatically upon construction/operation)
    
    # Generate correct_answer components using domain API if possible, otherwise format manually ensuring compliance
    canonical_latex_str = FractionOps.to_latex(final_fraction, mixed=False)
    
    numerator_val = final_fraction.numerator
    denominator_val = final_fraction.denominator
    
    answer_dict: Dict[str, Any] = {
        "question_text": r"Compute the exact value of $9/22 + 11/18 - (23/22 - 7/18)$ as an irreducible fraction.",
        "correct_answer": {
            "numerator": numerator_val,
            "denominator": denominator_val,
            "canonical_latex": canonical_latex_str
        },
        "oracle_payload": frozen_params
    }

    return answer_dict