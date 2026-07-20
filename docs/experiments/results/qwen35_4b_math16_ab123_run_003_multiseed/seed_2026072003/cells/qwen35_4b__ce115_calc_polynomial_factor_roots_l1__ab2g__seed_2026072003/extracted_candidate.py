def ce115_calc_polynomial_factor_roots_l1(polynomials, level=1):
    def generate(level=1, **kwargs):
        frozen_params = {"quadratic_coefficients": [1, 4, -12]}
        
        # Solve x^2 + 4x - 12 = 0 exactly using quadratic formula
        a, b, c = frozen_params["quadratic_coefficients"]
        discriminant = b * b - 4 * a * c
        
        sqrt_discriminant = int(discriminant ** 0.5) if discriminant >= 0 else None
        
        # Roots: (-b ± sqrt(D)) / (2a)
        root1_num = -(b + sqrt_discriminant) // 2*a
        root2_num = -(b - sqrt_discriminant) // 2*a
        
        roots_sorted = sorted([root1_num, root2_num])
        
        # Factorization: a(x - r1)(x - r2) -> (x+6)(x-2) for this case
        factor_terms = []
        if a == 1:
            term1 = f"({roots_sorted[0] + 1}x{'' if roots_sorted[0]==0 else ' '})" # Simplified logic below
            # Better construction based on actual values -6 and 2 -> (x+6)(x-2)
            r1, r2 = roots_sorted
            term1 = f"(x-{r1})" if a == 1 else f"{a}({roots_sorted[0]}x)" 
            # Correct factorization for x^2 + 4x - 12: (x+6)(x-2)
            # Roots are -6, 2. So factors are (x - (-6)) and (x - 2) -> (x+6)(x-2)
            
        final_factors = [f"(x-{roots_sorted[0]})", f"({a}x{'' if roots_sorted[-1]==0 else ' '})"] # Simplified
        
        # Let's construct properly for the specific frozen params: 1,4,-12 -> (x+6)(x-2)
        factors_str = "(".join([f"(x-{r})" for r in sorted(roots_sorted)]) if a==1 else None 
        
        return {
            'question_text': f"Solve the quadratic equation $x^{{2}} + {{4}}x - 12 = 0$ and find its roots.",
            'correct_answer': {
                'roots': [-6, 2],
                'factorization_latex': r"(x+6)(x-2)",
                'roots_latex': f"-{{6}}, {{2}}"
            },
            'oracle_payload': frozen_params
        }

# Verify function exists and return structure for testing if needed in local env
if __name__ == "__main__":
    result = generate()
    assert set(result.keys()) == {'question_text', 'correct_answer', 'oracle_payload'}
