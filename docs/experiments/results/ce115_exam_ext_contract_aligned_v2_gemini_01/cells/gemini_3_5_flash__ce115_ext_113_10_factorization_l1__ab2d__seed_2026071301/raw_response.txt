from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    expression = "5*x*(5*x - 2) - 4*(5*x - 2)**2"
    required_form = "fully_factored"
    
    # Extract coefficients from the expression
    coeffs = PolynomialOps.coeffs_from_py_expression(expression, var='x')
    a, b, c = coeffs[0], coeffs[1], coeffs[2]
    
    # Factor the quadratic expression
    factors = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    # Format the question text
    question_text = "Factor the expression completely:\n\n5x(5x - 2) - 4(5x - 2)^2"
    
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