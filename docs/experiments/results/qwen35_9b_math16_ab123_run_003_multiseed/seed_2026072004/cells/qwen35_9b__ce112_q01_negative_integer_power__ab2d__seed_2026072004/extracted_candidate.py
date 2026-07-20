from typing import Dict, Any
import math

def generate(level=1, **kwargs):
    frozen_params = {"base": -3, "exponent": 3}
    
    # Calculate power manually to handle negative base correctly without floating point issues if needed, 
    # but Python's ** operator handles integers natively and exactly.
    correct_answer = pow(frozen_params["base"], frozen_params["exponent"])

    question_text = (
        r"Calculate the value of $(-3)^{\text{" + str(frozen_params['exponent']) + "}}$."
    )

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }