import json
from fractions import Fraction as PyFraction
from typing import Dict, Any

def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    # Parse inputs as exact fractions
    val_1 = PyFraction("279") / PyFraction(100)
    val_2 = PyFraction("893") / PyFraction(10)
    
    term_a = val_1 * val_2
    
    val_3 = PyFraction("-21") / PyFraction(100)
    val_4 = PyFraction("893") / PyFraction(10)

    # Handle sign logic for second product: - (val3 * val4) is equivalent to adding negative result, 
    # but based on typical expression patterns "a*b + c*d" where signs are explicit in operands or operators.
    # The spec says "sign": 1 and "-1". Let's interpret as term_a = left*right, term_b = sign * (left2 * right2)
    val_5 = PyFraction("893") / PyFraction(10)

    if frozen_params["products"][1]["sign"] == -1:
        # Subtract the second product or add negative result. 
        # Given "sign": -1 usually implies subtraction in these templates, but let's calculate the value first.
        term_b = val_3 * val_5
        total = term_a + (-term_b)
    else:
        term_b = val_3 * val_5
        total = term_a + term_b

    # Ensure irreducible fraction representation
    p, q = total.numerator, total.denominator
    
    correct_answer_value = f"{p}/{q}"
    
    latex_val = r"\frac{" + str(p) + "}{"} + str(q) + r"}"
    
    question_text = (r"Let $x$ be the result of evaluating the expression: \n\n"
                     rf"$\left(\frac{279}{100} \times \frac{893}{10}\right)$ plus $\text{{sign}}_1 \cdot \left(-\frac{21}{100} \times \frac{893}{10}\right)$. "
                     r"Find the exact rational value of $x$ in irreducible form.")

    oracle_payload = json.dumps(frozen_params, separators=(',', ':'))

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_value + "|" + latex_val,
        "oracle_payload": oracle_payload
    }