from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    denominator_str = "4-sqrt(7)"
    numerator = 9
    radicand = 7
    
    # The expression is 9 / (4 - sqrt(7))
    # Rationalizing: 9 * (4 + sqrt(7)) / (16 - 7) = 9 * (4 + sqrt(7)) / 9 = 4 + sqrt(7)
    # Thus, a = 4, b = 7
    # We need to find a + b = 11
    
    a_val = FractionOps.create(4)
    b_val = FractionOps.create(7)
    ans_fraction = FractionOps.add(a_val, b_val)
    correct_answer = int(ans_fraction)
    
    question_text = (
        "Rationalize the denominator of the expression "
        "$\\frac{9}{4 - \\sqrt{7}}$. "
        "If the simplified expression is written in the form $a + \\sqrt{b}$, "
        "find the value of $a + b$."
    )
    
    oracle_payload = {
        "denominator": denominator_str,
        "numerator": numerator,
        "radicand": radicand
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }