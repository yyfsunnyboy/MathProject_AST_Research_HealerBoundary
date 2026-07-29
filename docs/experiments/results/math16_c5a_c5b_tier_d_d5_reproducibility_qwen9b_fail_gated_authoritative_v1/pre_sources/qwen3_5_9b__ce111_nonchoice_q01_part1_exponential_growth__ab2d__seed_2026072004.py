from typing import Dict, Any
import math
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate number of generations based on days and hours per generation (assuming 24h day)
    total_hours = frozen_params["days"] * 24
    num_generations = int(total_hours / frozen_params["hours_per_generation"])
    
    initial_pop = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]
    
    # Exponential growth: P(t) = P0 * (r^t) where r is the split factor per generation
    final_count = IntegerOps.safe_eval(str(initial_pop * (split_factor ** num_generations)))
    
    question_text = f"A population starts with {IntegerOps.fmt_num(initial_pop)} individuals. Every {frozen_params['hours_per_generation']} hours, each individual splits into {split_factor} offspring. After {frozen_params['days']} days ({total_hours} hours), how many individuals are there? Assume the process runs for exactly that duration."
    
    correct_answer = {"k": final_count}
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }