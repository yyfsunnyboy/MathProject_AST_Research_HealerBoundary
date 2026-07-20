def generate(level=1, **kwargs):
    p1 = kwargs.get("p1", [2, 6])
    p2 = kwargs.get("p2", [1, 5])
    
    # Calculate the product of fractions: (numerator/denominator) * (numerator/denominator)
    num_total = p1[0] * p2[0]
    den_total = p1[1] * p2[1]
    
    # Simplify the fraction by dividing both numerator and denominator by their greatest common divisor
    import math
    gcd_val = math.gcd(num_total, den_total)
    num_simplified = num_total // gcd_val
    den_simplified = den_total // gcd_val
    
    question_text = r"The probability of two independent events occurring is the product of their individual probabilities. If event A has a probability of $\frac{%d}{%d}$ and event B has a probability of $\frac{%d}{%d}$, what is the combined probability expressed as an irreducible fraction? \text{Answer in form } \frac{\text{numerator}}{\text{denominator}}." % (p1[0], p1[1], p2[0], p2[1])
    
    correct_answer = {
        "numerator": num_simplified,
        "denominator": den_simplified,
        "canonical_latex": r"\frac{%d}{%d}" % (num_simplified, den_simplified)
    }
    
    oracle_payload = {"p1": p1, "p2": p2}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }