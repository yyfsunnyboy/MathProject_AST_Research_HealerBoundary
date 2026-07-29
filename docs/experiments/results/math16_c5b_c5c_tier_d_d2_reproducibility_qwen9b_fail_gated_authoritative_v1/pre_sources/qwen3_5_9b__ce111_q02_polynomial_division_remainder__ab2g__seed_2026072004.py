def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    # Polynomial: P(x) = 6x^2 + 4x (from coefficients [6, 4, 0])
    # Divisor: D(x) = 2x^2 (from coefficients [2, 0, 0])
    # Division: (6x^2 + 4x) / (2x^2) -> Quotient is not scored. Remainder calculation logic below.
    
    # Since divisor degree equals dividend degree here:
    # Leading term division: 6/2 = 3, so quotient starts with x^0? 
    # Actually, standard polynomial long division for P(x)/D(x):
    # (6x^2 + 4x) / (2x^2) = 3 + (4x)/(2x^2) = 3 + 2/x. Since we are in polynomials over a field usually implying integer/rational coeffs, 
    # strictly speaking if divisor degree >= dividend degree and leading coeff doesn't divide perfectly to eliminate lower terms without fractions or negative powers:
    # However, the task implies finding remainder R(x) such that P = Q*D + R where deg(R) < deg(D).
    
    # Let's compute manually for correctness verification before generating text.
    # Dividend: 6x^2 + 4x (deg 2)
    # Divisor: 2x^2 (deg 2)
    # Step 1: Divide leading terms: 6x^2 / 2x^2 = 3. 
    # Multiply divisor by 3: 3 * (2x^2) = 6x^2.
    # Subtract from dividend: (6x^2 + 4x) - 6x^2 = 4x.
    # New remainder candidate is 4x. Degree of 4x is 1, which is < degree of divisor (2).
    # So Quotient Q(x) = 3, Remainder R(x) = 4x.
    
    quotient_val = "3"
    remainder_coefficients = [0, 4] # Represents 4x
    
    question_text = r"""Find the remainder when $P(x) = 6x^2 + 4x$ is divided by $D(x) = 2x^2$. Express your answer as a polynomial in standard form."""
    
    correct_answer_latex = "4x"
    canonical_latex = f"${correct_answer_latex}$"

    return {
        "question_text": question_text,
        "correct_answer": canonical_latex,
        "oracle_payload": frozen_params
    }