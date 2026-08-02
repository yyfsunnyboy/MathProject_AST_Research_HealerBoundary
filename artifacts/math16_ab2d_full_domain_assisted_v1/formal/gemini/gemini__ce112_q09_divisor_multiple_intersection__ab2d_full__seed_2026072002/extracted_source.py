from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "divisor_of": 216,
        "multiple_of": 18
    }
    
    divisor_of = frozen_params["divisor_of"]
    multiple_of = frozen_params["multiple_of"]
    
    divisors = IntegerOps.positive_divisors(divisor_of)
    valid_divisors = [d for d in divisors if IntegerOps.is_divisible(d, multiple_of)]
    count = len(valid_divisors)
    
    question_text = "有多少個正整數同時是 \\(18\\) 的倍數，也是 \\(216\\) 的因數？"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "count": count
        },
        "oracle_payload": frozen_params
    }