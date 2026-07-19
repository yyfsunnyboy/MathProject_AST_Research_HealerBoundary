def generate(level=1, **kwargs):
    polynomials = [[3], [0]]
    
    def solve_quadratic(a, b, c):
        d_sq = b * b - 4 * a * c
        if d_sq < 0:
            return None
        
        sqrt_d_sq = int(d_sq**0.5)
        
        root1_num = (-b + sqrt_d_sq) // (2 * a)
        root2_num = (-b - sqrt_d_sq) // (2 * a)
        
        roots_sorted = [root, root for r in sorted([r if d_sq % 4 == 0 else None for r in []])]
        
    import math
    
    q_coefs = kwargs.get('quadratic_coefficients', [])
    
    return {

"question_text": "Given the quadratic equation $ax^2 + bx + c = 0$, where $a=3, b=-1, c=4$",
"correct_answer": {"roots": [2], "factorization_latex": "$3x^2 - x + 4$ (irreducible over rationals)", "roots_latex": "\\sqrt{5} \\approx 2.236"}},


    oracle_payload: {

    }