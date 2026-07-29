from fractions import Fraction as PyFraction

def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    # Parse inputs as Fractions
    p1 = PyFraction("279") / PyFraction(100)
    q1 = PyFraction("893") / PyFraction(10)
    
    p2 = PyFraction("-21") / PyFraction(100)
    q2 = PyFraction("893") / PyFraction(10)

    # Perform arithmetic using domain-style logic (simulated via standard Fraction for exactness as per API constraints in this isolated context, ensuring irreducible form)
    term1 = p1 * q1
    term2 = p2 * q2
    
    result = term1 + term2

    # Format answer
    num_str = str(result.numerator)
    den_str = str(result.denominator) if result.denominator != 1 else "1"
    
    question_text = r"\text{Calculate the exact value of: } \left( \frac{2.79}{89.3} + (-0.21) \times \frac{89.3}{10} \right)"

    correct_answer_value = f"{num_str}/{den_str}"
    
    # Canonical LaTeX representation for the fraction
    if den_str == "1":
        canonical_latex = r"\text{" + num_str + r"}"
    else:
        canonical_latex = rf"\frac{{{num_str}}}{{ {den_str} }}"

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_value,
        "oracle_payload": frozen_params
    }