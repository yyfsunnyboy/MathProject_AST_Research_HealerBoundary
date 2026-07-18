from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    expression = "5*x*(5*x - 2) - 4*(5*x - 2)**2"
    required_form = "fully_factored"
    
    # Using FractionOps to construct the coefficients
    f1_x = FractionOps.create(5)
    f1_c = FractionOps.create(-2)
    f2_x = FractionOps.create(-15)
    f2_c = FractionOps.create(8)
    
    # Convert to int for JSON compatibility
    factors = [
        {"x_coefficient": int(f1_x), "constant": int(f1_c)},
        {"x_coefficient": int(f2_x), "constant": int(f2_c)}
    ]
    
    question_text = "Factorize the expression: $5x(5x - 2) - 4(5x - 2)^2$"
    
    correct_answer = {
        "factors": factors
    }
    
    oracle_payload = {
        "expression": expression,
        "required_form": required_form
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }