from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    divisor_of = 216
    multiple_of = 18
    
    divisors = IntegerOps.positive_divisors(divisor_of)
    valid_divisors = [d for d in divisors if IntegerOps.is_divisible(d, multiple_of)]
    count = len(valid_divisors)
    
    question_text = "有多少個正整數同時是 \\(18\\) 的倍數，也是 \\(216\\) 的因數？"
    
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