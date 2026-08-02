from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {
        "p1": [2, 6],
        "p2": [1, 5]
    }
    
    p1_num, p1_den = frozen_params["p1"]
    p2_num, p2_den = frozen_params["p2"]
    
    a = FractionOps.from_parts(p1_num, p1_den)
    b = FractionOps.from_parts(p2_num, p2_den)
    
    value = FractionOps.mul(a, b)
    
    correct_answer = {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "canonical_latex": FractionOps.to_latex(value)
    }
    
    question_text = "第一組有 \(6\) 個等可能結果，其中 \(2\) 個符合條件；第二組有 \(5\) 個等可能結果，其中 \(1\) 個符合條件。若兩次選擇彼此獨立，求兩組皆符合條件的機率，並以最簡分數表示。"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }