def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    if divisor_of % multiple_of != 0:
        count = 0
    else:
        n = divisor_of // multiple_of
        count = sum(1 for i in range(1, n + 1) if n % i == 0)
        
    question_text = f"How many positive integers are both a divisor of ${divisor_of}$ and a multiple of ${multiple_of}$?"
    
    return {
        "question_text": question_text,
        "correct_answer": {"count": count},
        "oracle_payload": {
            "divisor_of": divisor_of,
            "multiple_of": multiple_of
        }
    }