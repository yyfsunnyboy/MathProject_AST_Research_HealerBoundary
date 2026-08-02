from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "divisor_of": 216,
        "multiple_of": 18
    }
    
    divisors_list = IntegerOps.positive_divisors(frozen_params["divisor_of"])
    
    count = sum(1 for d in divisors_list if IntegerOps.is_divisible(d, frozen_params["multiple_of"]))
    
    return {
        "question_text": "有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？",
        "correct_answer": {"count": count},
        "oracle_payload": frozen_params
    }