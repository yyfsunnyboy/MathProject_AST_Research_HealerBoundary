from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    expression = "(5*x**2 - 2*x) - (4 - 3*x)"
    
    coeffs = PolynomialOps.coeffs_from_py_expression(expression, var='x')
    degree_map = PolynomialOps.to_degree_map(coeffs)
    
    # Ensure keys '2', '1', '0' are present and map to exact values
    coefficients_map = {deg: degree_map.get(deg, 0) for deg in ['2', '1', '0']}
    
    question_text = f"Simplify the following polynomial expression:\n\n{expression}"
    
    correct_answer = {
        "coefficients": coefficients_map
    }
    
    oracle_payload = {
        "expression": expression
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }