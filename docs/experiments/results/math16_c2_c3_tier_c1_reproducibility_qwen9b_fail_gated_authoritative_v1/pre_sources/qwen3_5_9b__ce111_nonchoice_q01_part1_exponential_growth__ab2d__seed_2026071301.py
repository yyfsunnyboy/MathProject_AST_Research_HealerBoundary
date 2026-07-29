from typing import Dict, Any
import math
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate number of generations based on days and hours per generation (assuming 24h day)
    total_hours = frozen_params["days"] * 24
    num_generations = int(total_hours / frozen_params["hours_per_generation"])
    
    # Exponential growth calculation: final_amount = initial * split_factor ^ num_generations
    base_growth = IntegerOps.safe_eval(f"{frozen_params['initial']} * {frozen_params['split_factor'] ** num_generations}")
    
    question_text = (
        r"A population starts with an \text{{" + str(IntegerOps.fmt_num(1)) + r"}} individual and doubles every generation. "
        r"If the split factor is $4$ per generation, how many individuals are there after $\text{" + 
        str(frozen_params['days']) + r"}$ days given that each generation takes $\text{" + 
        str(frozen_params['hours_per_generation']) + r"}}$ hours? "
    )

    correct_answer = {"k": base_growth}
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }