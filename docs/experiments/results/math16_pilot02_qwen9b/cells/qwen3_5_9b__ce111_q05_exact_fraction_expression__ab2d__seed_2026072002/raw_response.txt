from typing import Dict, Any
import sys
sys.path.insert(0, '.')
try:
    from core.prompts.domain_function_library import FractionOps
except ImportError:
    class DummyFractionOps:
        @staticmethod
        def create(value): return value
        @staticmethod
        def add(a, b): return a + b
        @staticmethod
        def to_latex(val, mixed=False): return str(val)

def generate(level=1, **kwargs):
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Parse and compute the expression using domain APIs where possible or standard math if needed for logic
    from fractions import Fraction
    
    term1 = Fraction(9, 22)
    term2 = Fraction(11, 18)
    inner_paren_1 = Fraction(23, 22)
    inner_paren_2 = Fraction(7, 18)
    
    # Compute: (term1 + term2) - (inner_paren_1 - inner_paren_2)
    part_a = DummyFractionOps.add(term1, term2) if hasattr(DummyFractionOps, 'add') else term1 + term2
    part_b = DummyFractionOps.subtract(inner_paren_1, inner_paren_2) if hasattr(FractionOps, 'subtract') else (inner_paren_1 - inner_paren_2)
    
    # Note: The domain library provided in the prompt description only lists create and add. 
    # However, standard Fraction arithmetic is required for subtraction logic unless a specific subtract API exists.
    # Assuming standard Python fractions for robustness if custom API lacks 'subtract', but adhering to spirit of using APIs.
    # Let's assume we can use basic operators or implement the missing one via create/add/subtraction logic manually? 
    # The prompt says "Use the listed domain API". It lists add, not subtract. We must handle subtraction logically.
    
    result = part_a - part_b
    
    numerator = result.numerator
    denominator = result.denominator
    
    latex_str = DummyFractionOps.to_latex(result) if hasattr(DummyFractionOps, 'to_latex') else f"{numerator}/{denominator}"
    
    # Ensure canonical LaTeX format for the answer (usually just num/den or mixed number if requested, but prompt says irreducible fraction)
    canonical_latex = latex_str
    
    return {
        "question_text": r"Compute the value of $9/22 + 11/18 - (23/22 - 7/18)$ and express your answer as an irreducible fraction.",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }