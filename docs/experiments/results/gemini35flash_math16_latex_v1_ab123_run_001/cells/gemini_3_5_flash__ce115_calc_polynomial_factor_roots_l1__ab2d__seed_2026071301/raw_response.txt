from core.prompts.domain_function_library import PolynomialOps, FractionOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    quadratic_coefficients = [1, 4, -12]
    
    a, b, c = quadratic_coefficients
    
    # Use domain API to factor the quadratic
    roots, factorization_latex, roots_latex = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    # Ensure roots are sorted in ascending order
    roots = sorted(roots)
    
    # Format the polynomial for the question text
    question_text = "Factor the quadratic polynomial $x^2 + 4x - 12$ and find its roots."
    
    correct_answer = {
        "roots": roots,
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex
    }
    
    oracle_payload = {
        "quadratic_coefficients": quadratic_coefficients
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }