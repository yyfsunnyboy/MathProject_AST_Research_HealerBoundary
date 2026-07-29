from typing import Dict, Any
import json
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate number of generations: total hours / hours per generation
    days = frozen_params["days"]
    hours_per_gen = frozen_params["hours_per_generation"]
    initial_pop = frozen_params["initial"]
    split_factor = frozen_params["split_factor"]
    
    total_hours = days * 24
    num_generations = int(total_hours / hours_per_gen)
    
    # Calculate final population: P = P0 * (r ^ n)
    if initial_pop == 1 and split_factor > 1:
        correct_k = pow(split_factor, num_generations)
    else:
        correct_k = initial_pow * pow(split_factor, num_generations)

    question_text = f"A population starts with {IntegerOps.fmt_num(initial_pop)} individuals. Every {hours_per_gen} hours, the population splits by a factor of {split_factor}. Over {days} days ({total_hours} hours), how many generations occur and what is the final population count?\n\nMathematical expression: $P = P_0 \\times r^n$ where $r={split_factor}$."
    
    correct_answer = {"k": correct_k}
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }