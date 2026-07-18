def generate(level=1, **kwargs):
    expression = "(2*sqrt(3) + sqrt(6))*sqrt(2)"
    
    # Simplify the radical product: (2√3 + √6) * √2
    # Distribute √2: 2√3 * √2 + √6 * √2 = 2√6 + √12
    
    # Simplify terms where radicand has a perfect square factor
    # √12 simplifies to √(4*3) = 2√3
    
    # Combine like terms: 2√6 + 2√3
    # Sort by increasing radicand (3, then 6)
    
    term_list = [
        {"coefficient": 2.0, "radicand": 3},
        {"coefficient": 2.0, "radicand": 6}
    ]
    
    correct_answer = {
        "terms": term_list
    }
    
    oracle_payload = expression
    
    return {
        "question_text": f"Simplify the radical product: {expression}",
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }