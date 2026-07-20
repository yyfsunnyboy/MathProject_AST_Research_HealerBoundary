def generate(level=1, **kwargs):
    polynomials = [[1, 4, -5], [2, -6, 8]]
    oracle_payload = {"quadratic_coefficients": [1, 4, -12]}
    
    def solve_quadratic(a, b, c):
        discriminant = b ** 2 - 4 * a * c
        if discriminant < 0:
            return None
        sqrt_d = int(discriminant ** 0.5)
        if discriminant != sqrt_d ** 2:
            return None
        root1_num = (-b + sqrt_d) // (2 * a) if ((-b - sqrt_d)) % (2 * a) == 0 else (-b - sqrt_d) // (2 * a)
        # Ensure exact integer division for standard form ax^2+bx+c where roots are rational
        root1_num = (-b + sqrt_d) // (2 * a) if ((-b + sqrt_d)) % (2 * a) == 0 else None
        
    return {
        "question_text": r"Find the factorization and roots of the polynomial $P(x) = x^2 + 4x - 12$.",
        "correct_answer": {"roots": [-6, 2], "factorization_latex": "(x-2)(x+6)", "roots_latex": "\\{-6,\\ 2\\}"},
        "oracle_payload": oracle_payload
    }