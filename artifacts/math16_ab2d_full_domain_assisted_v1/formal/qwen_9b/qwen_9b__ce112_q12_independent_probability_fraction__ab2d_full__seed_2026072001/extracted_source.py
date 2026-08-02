from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen_params = {
        "p1": [2, 6],
        "p2": [1, 5]
    }
    
    p1_fraction = FractionOps.from_parts(frozen_params["p1"][0], frozen_params["p1"][1])
    p2_fraction = FractionOps.from_parts(frozen_params["p2"][0], frozen_params["p2"][1])
    
    result_fraction = FractionOps.mul(p1_fraction, p2_fraction)
    
    return {
        "question_text": "第一組有 \(6\) 個等可能結果，其中 \(2\) 個符合條件；第二組有 \(5\) 個等可能結果，其中 \(1\) 個符合條件。若兩次選擇彼此獨立，求兩組皆符合條件的機率，並以最簡分數表示。",
        "correct_answer": {
            "numerator": result_fraction.numerator,
            "denominator": result_fraction.denominator,
            "canonical_latex": FractionOps.to_latex(result_fraction)
        },
        "oracle_payload": frozen_params
    }