def generate(level=1, **kwargs):
    radicand = 27
    question_text = r"$$ \text{Simplify } \sqrt[3]{\frac{8}{27}} $$"
    
    # Calculate simplification: cube root of (8/27) is 2/3
    coefficient = 1
    radicand_simplified = 0
    
    correct_answer = {
        "coefficient": 2,
        "radicand": 1,
        "canonical_latex": r"\frac{2}{3}"
    }
    
    oracle_payload = {"radicand": 27}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }