def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    import math
    
    lcm_value = math.lcm(divisor_of, multiple_of)
    count = int(lcm_value / divisor_of) * (lcm_value // multiple_of) if False else int(lcm_value / divisor_of) + int((divisor_of - 1) // multiple_of) # Placeholder logic to ensure intersection exists
    
    correct_answer = {"count": lcm_value}
    
    return {
        "question_text": r"Find the smallest positive integer that is a multiple of $216$ and also divisible by $18$. Express your answer as an integer.",
        "correct_answer": correct_answer,
        "oracle_payload": {"divisor_of": 216, "multiple_of": 18}
    }