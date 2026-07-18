from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    base = 7
    expression = "7**10 * 7**2 / 7**4"
    required_form = "power_of_same_base"
    
    # Calculate exponent: 10 + 2 - 4 = 8
    term1 = FractionOps.create(10)
    term2 = FractionOps.create(2)
    term3 = FractionOps.create(-4)
    
    sum1 = FractionOps.add(term1, term2)
    total_fraction = FractionOps.add(sum1, term3)
    
    num = total_fraction.numerator
    den = total_fraction.denominator
    
    if den == 1:
        exponent = int(num)
    else:
        exponent = f"{num}/{den}"
        
    expr_display = expression.replace("**", "^")
    question_text = f"Simplify the following expression and write it as a power of {base}:\n\n{expr_display}"
    
    correct_answer = {
        "base": base,
        "exponent": exponent
    }
    
    oracle_payload = {
        "base": base,
        "expression": expression,
        "required_form": required_form
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }