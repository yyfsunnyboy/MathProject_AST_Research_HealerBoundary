import json
from fractions import Fraction as PyFraction

def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    # Parse inputs as Fractions
    val_1 = PyFraction("279") / PyFraction(100)
    val_2 = PyFraction("893") / PyFraction(10)
    
    term_a = val_1 * val_2
    
    val_3 = PyFraction("-21") / PyFraction(100)
    term_b = val_3 * val_2

    # Perform exact arithmetic using FractionOps if available, otherwise standard Python Fractions
    try:
        from core.prompts.domain_function_library import FractionOps
        
        result_a = FractionOps.mul(term_a.numerator // 100, term_a.denominator) / (FractionOps.create(893)) * (FractionOps.create(10)) # Simplified logic to match standard fraction math for clarity in this context
    except ImportError:
        pass

    # Re-calculate using pure Python Fractions to ensure correctness without external dependencies failing
    term_a_exact = PyFraction("279") / 100 * (PyFraction("893") / 10)
    term_b_exact = (-PyFraction("21")) / 100 * (PyFraction("893") / 10)

    total_sum = term_a_exact + term_b_exact
    
    # Format answer as p/q string and LaTeX
    numerator_str, denominator_str = str(total_sum.numerator), str(total_sum.denominator)
    
    question_text = r"\text{Calculate the exact value of: } \left( 2.79 \times 89.3 + (-0.21) \times 89.3 \right)"
    
    correct_answer_value = f"{numerator_str}/{denominator_str}"
    canonical_latex = r"\frac{" + numerator_str + "}{"} + denominator_str + r"}"

    return {
        "question_text": question_text,
        "correct_answer": {"value": correct_answer_value, "canonical_latex": canonical_latex},
        "oracle_payload": frozen_params
    }
