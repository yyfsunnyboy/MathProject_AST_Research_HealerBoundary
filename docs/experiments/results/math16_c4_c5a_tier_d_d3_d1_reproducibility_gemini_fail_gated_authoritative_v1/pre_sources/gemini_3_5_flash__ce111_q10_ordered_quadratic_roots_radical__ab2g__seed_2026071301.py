def generate(level=1, **kwargs):
    oracle_payload = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }
    
    question_text = (
        "Solve the equation $(x-2)^2=3$. Let its roots be $a$ and $b$ "
        "such that $a > b$. Find the value of $2a+b$."
    )
    
    result = {
        "rational": 6,
        "radical_coefficient": 1,
        "radicand": 3,
        "canonical_latex": "6+\\sqrt{3}"
    }
    
    correct_answer = {
        "rational": 6,
        "radical_coefficient": 1,
        "radicand": 3,
        "canonical_latex": "6+\\sqrt{3}",
        "result": result
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }