from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    divisor_of = 216
    multiple_of = 18
    
    count = 0
    for x in range(1, divisor_of + 1):
        if IntegerOps.is_divisible(divisor_of, x) and IntegerOps.is_divisible(x, multiple_of):
            count += 1
            
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