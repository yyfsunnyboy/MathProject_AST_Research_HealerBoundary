from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    question_text = "將一元二次方程式\n\\[\nx^2+4x-12=0\n\\]\n的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。"
    
    oracle_payload = {
        "quadratic_coefficients": [
            1,
            4,
            -12
        ]
    }
    
    # The quadratic is x^2 + 4x - 12 = (x + 6)(x - 2) = 0
    # The roots are -6 and 2, ordered ascending.
    roots = [-6, 2]
    factorization_latex = "(x+6)(x-2)"
    roots_latex = "-6, 2"
    
    correct_answer = {
        "roots": roots,
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }