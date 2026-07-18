from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    expression = "9/(4 - sqrt(7))"
    required_form = "a + b*sqrt(7)"
    target_expression = "a + b"
    
    # Calculations:
    # 9 / (4 - sqrt(7)) = 9 * (4 + sqrt(7)) / (16 - 7) = 9 * (4 + sqrt(7)) / 9 = 4 + 1 * sqrt(7)
    a_val = 4
    b_val = 1
    radicand_val = 7
    
    # Use FractionOps to compute value = a + b
    a_frac = FractionOps.create(a_val)
    b_frac = FractionOps.create(b_val)
    val_frac = FractionOps.add(a_frac, b_frac)
    
    try:
        value = int(val_frac)
    except Exception:
        try:
            value = val_frac.numerator // val_frac.denominator
        except Exception:
            value = a_val + b_val

    question_text = (
        f"Rationalize the denominator of the expression: {expression}.\n"
        f"Write the answer in the form {required_form}.\n"
        f"Find the value of {target_expression}."
    )
    
    correct_answer = {
        "a": a_val,
        "b": b_val,
        "radicand": radicand_val,
        "value": value
    }
    
    oracle_payload = {
        "expression": expression,
        "required_form": required_form,
        "target_expression": target_expression
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }