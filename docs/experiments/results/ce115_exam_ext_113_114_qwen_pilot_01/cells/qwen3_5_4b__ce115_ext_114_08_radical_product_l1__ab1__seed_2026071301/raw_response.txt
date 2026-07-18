def generate(level=1, **kwargs):
    expression = "(2*sqrt(3) + sqrt(6))*sqrt(2)"
    
    # Simplify the radical product: (2√3 + √6) * √2
    # Distribute √2: 2√3 * √2 + √6 * √2 = 2√6 + √12
    
    # Further simplify terms where radicand has a perfect square factor
    # √12 simplifies to √(4*3) = 2√3, so the term becomes 2√3 (coefficient part of original sqrt was implicit in value but here we track coefficient and radicand separately from input structure logic usually expected: 
    # Let's re-evaluate based on standard algebraic simplification rules for such problems.
    # Term 1: 2 * √(3) * √(2) = 2 * √6 -> {coefficient: 2, radicand: 6}
    # Term 2: 1 * √(6) * √(2) = 1 * √(12). 
    # Simplify √12: √(4*3) = 2√3. So this term becomes {coefficient: 2, radicand: 3}.
    
    terms = [
        {"coefficient": 2, "radicand": 6},
        {"coefficient": 2, "radicand": 3}
    ]
    
    # Sort by increasing radicand as per spec (though order might vary if not strictly enforced in sort key, let's ensure ascending)
    terms.sort(key=lambda x: x["radicand"])
    
    correct_answer = {"terms": terms}
    oracle_payload = expression
    
    return {
        "question_text": f"Simplify the radical product given by the expression:\n{expression}",
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }