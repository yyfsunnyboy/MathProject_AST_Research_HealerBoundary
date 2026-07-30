from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    divisor_of = 216
    multiple_of = 18
    
    count = 0
    if divisor_of >= multiple_of:
        k = 1
        while True:
            x = k * multiple_of
            if x > divisor_of:
                break
            if IntegerOps.is_divisible(divisor_of, x):
                count += 1
            k += 1
            
    question_text = f"How many positive integers are both a divisor of ${divisor_of}$ and a multiple of ${multiple_of}$?"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "count": count
        },
        "oracle_payload": {
            "divisor_of": divisor_of,
            "multiple_of": multiple_of
        }
    }