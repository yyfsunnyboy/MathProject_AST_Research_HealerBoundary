def generate(level=1, **kwargs):
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    # Perform polynomial division: (6x^2 + 4x) / (2x^2) -> Wait, divisor is degree 2.
    # Dividend: 6x^2 + 4x + 0
    # Divisor: 2x^2 + 0x + 0 = 2x^2
    
    # Division of P(x) by Q(x): (6x^2 + 4x) / (2x^2)
    # Leading term division: 6/2 * x^(2-2) = 3. Quotient starts with 3.
    # Multiply divisor by 3: 3 * 2x^2 = 6x^2.
    # Subtract from dividend: (6x^2 + 4x) - 6x^2 = 4x.
    # Degree of remainder (1) < degree of divisor (2). Stop.
    
    quotient_coefficients = [3]
    remainder_coefficients = [0, 4] # Represents 4x
    
    question_text = r"Find the remainder when dividing $P(x) = 6x^2 + 4x$ by $Q(x) = 2x^2$. Express your answer as a polynomial in canonical form."
    
    correct_answer = {
        "remainder": [0, 4],
        "canonical_latex": r"4x"
    }
    
    oracle_payload = {"dividend_coefficients": dividend_coefficients, "divisor_coefficients": divisor_coefficients}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }