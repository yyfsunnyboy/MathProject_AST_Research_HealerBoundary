from core.prompts.domain_function_library import FractionOps, Fraction


def generate(level=1, **kwargs):
    oracle_payload = kwargs.get("oracle_payload", {"p1": [2, 6], "p2": [1, 5]})
    
    # Step 1: Create fractions from parts (numerator/denominator) for both groups
    p1_num, p1_den = oracle_payload["p1"]
    p2_num, p2_den = oracle_payload["p2"]
    
    a = FractionOps.from_parts(p1_num, p1_den)
    b = FractionOps.from_parts(p2_num, p2_den)
    
    # Step 2: Multiply the two probabilities (independent events)
    result_fraction = FractionOps.mul(a, b)
    
    # Step 3: Assemble correct_answer according to Task-specific answer contract
    canonical_latex = FractionOps.to_latex(result_fraction)
    
    return {
        "question_text": oracle_payload.get("question", 
            f"第一組有 \\({p1_den}\\) 個等可能結果，其中 \\({p1_num}\\) 個符合條件；第二組有 \\({p2_den}\\) 個等可能結果，其中 \\({p2_num}\\) 個符合條件。若兩次選擇彼此獨立，求兩組皆符合條件的機率，並以最簡分數表示。"),
        "correct_answer": {
            "numerator": result_fraction.numerator,
            "denominator": result_fraction.denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": oracle_payload
    }
