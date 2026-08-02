from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    frozen = {
        "p1": [2, 6],
        "p2": [1, 5]
    }
    
    p1_frac = FractionOps.from_parts(frozen["p1"][0], frozen["p1"][1])
    p2_frac = FractionOps.from_parts(frozen["p2"][0], frozen["p2"][1])
    
    result = FractionOps.mul(p1_frac, p2_frac)
    
    return {
        "question_text": "第一組有 \(6\) 個等可能結果，其中 \(2\) 個符合條件；第二組有 \(5\) 個等可能結果，其中 \(1\) 個符合條件。若兩次選擇彼此獨立，求兩組皆符合條件的機率，並以最簡分數表示。",
        "correct_answer": {
            "numerator": result.numerator,
            "denominator": result.denominator,
            "canonical_latex": FractionOps.to_latex(result)
        },
        "oracle_payload": frozen
    }