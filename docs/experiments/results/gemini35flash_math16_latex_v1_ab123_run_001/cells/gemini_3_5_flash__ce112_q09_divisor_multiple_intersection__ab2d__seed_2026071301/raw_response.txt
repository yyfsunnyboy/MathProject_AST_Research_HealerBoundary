from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    divisor_of = 216
    multiple_of = 18
    
    count = 0
    for i in range(1, divisor_of + 1):
        if IntegerOps.is_divisible(i, multiple_of) and IntegerOps.is_divisible(divisor_of, i):
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