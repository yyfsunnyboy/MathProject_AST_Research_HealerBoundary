import random
from typing import Dict, Any

def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    p1_val = frozen_params["p1"][0]
    p2_val = frozen_params["p2"][0]
    
    # Independent probability: P(A and B) = P(A) * P(B)
    numerator = p1_val * p2_val
    
    denominator = 6 * 5  # Since probabilities are given as n/d where d=6 for p1, d=5 for p2? 
                         # Wait, the format is [numerator, denominator]. 
                         # So P(A) = 2/6 and P(B) = 1/5.
    
    from core.prompts.domain_function_library import FractionOps
    
    frac_numerator = FractionOps.create(numerator)
    frac_denominator = FractionOps.create(denominator)
    
    product_frac = FractionOps.mul(frac_numerator, frac_denominator)
    
    # Simplify if necessary (though 2*1 / 6*5 = 2/30 which reduces to 1/15)
    simplified_num = product_frac.numerator
    simplified_den = product_frac.denominator
    
    canonical_latex = FractionOps.to_latex(product_frac, mixed=False)
    
    question_text = r"$P(A \cap B)$ given $P(A)=\frac{2}{6}$ and $P(B)=\frac{1}{5}$"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": simplified_num,
            "denominator": simplified_den,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }