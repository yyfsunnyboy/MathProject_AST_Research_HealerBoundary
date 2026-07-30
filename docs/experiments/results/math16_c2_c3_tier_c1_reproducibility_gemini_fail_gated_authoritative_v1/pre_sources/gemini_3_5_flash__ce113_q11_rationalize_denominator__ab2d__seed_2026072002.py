from fractions import Fraction
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    denominator = "4-sqrt(7)"
    numerator = 9
    radicand = 7
    
    # Parse denominator
    s = -1 if "-" in denominator else 1
    d_str = denominator.replace(f"-sqrt({radicand})", "").replace(f"+sqrt({radicand})", "")
    d = int(d_str)
    
    denom_conj = d**2 - radicand
    a_val = Fraction(numerator * d, denom_conj)
    b_val = Fraction(-numerator * s, denom_conj)
    
    # Use domain APIs
    a_frac = FractionOps.create(a_val)
    b_frac = FractionOps.create(b_val)
    _ = FractionOps.add(a_frac, b_frac)
    
    correct_answer = int(a_val + b_val)
    
    latex_denominator = denominator.replace("sqrt(", "\\sqrt{").replace(")", "}")
    question_text = f"Rationalize the denominator of $\\frac{{{numerator}}}{{{latex_denominator}}}$. If the simplified expression is of the form $a + b\\sqrt{{{radicand}}}$, what is the value of $a + b$?"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "denominator": denominator,
            "numerator": numerator,
            "radicand": radicand
        }
    }